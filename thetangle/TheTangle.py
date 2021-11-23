# MIT License

# Copyright (c) 2021 kaalam.ai The Authors of Jazz

# Hosted at https://github.com/kaalam/thetangle

import re
import requests as http


LOCAL_SERVER_URL = 'http://127.0.0.1:8899'


def get(qq):
	""" Do an http GET call from a local Jazz server. See https://kaalam.github.io/jazz_reference/api_ref_intro.html """
	return http.get(LOCAL_SERVER_URL + qq)


def put(qq, string):
	""" Do an http PUT call to a local Jazz server. See https://kaalam.github.io/jazz_reference/api_ref_intro.html """
	return http.put(LOCAL_SERVER_URL + qq, string)


def delete(qq):
	""" Do an http DELETE call to a local Jazz server. See https://kaalam.github.io/jazz_reference/api_ref_intro.html """
	return http.delete(LOCAL_SERVER_URL + qq)


class TangleExplorer():
	"""
	A simple example to understand the structure of The Tangle dataset in a Jazz (TNG series) server.

	NOTE: The Tangle is not supposed to be accessed via http, but to serve for language research coded inside the Jazz server.
	"""

	def __init__(self, root = '//lmdb/the_tangle/datasets'):
		self.root = root

		self.rex_dataset = re.compile('^//lmdb/the_tangle/([^_]+)_sections$')
		self.rex_section = re.compile('^//lmdb/the_tangle/([^_]+)_([^_]+)_blocks$')
		self.rex_block	 = re.compile('^//lmdb/the_tangle/([^_]+)_([^_]+)_([0-9]+)_([0-9]+)$')


	def datasets(self, urls_as_names = False):
		"""
		Returns a list with the dataset names stored in The Tangle.

	    Arguments:
		urls_as_names -- If true, the returns the urls of the sections list rather than just the dataset names.
		"""

		a = get(self.root)
		assert a.status_code == 200

		ds = a.text.split(',')
		if urls_as_names:
			return ds

		return [self.rex_dataset.sub('\\1', d) for d in ds]


	def sections(self, dataset, urls_as_names = False):
		"""
		Returns a list with the section names for a given dataset.

	    Arguments:
		dataset		  -- The name of the dataset. (The url to its sections list is also accepted.)
		urls_as_names -- If true, the returns the urls of the blocks list rather than just the section names.
		"""

		if not self.rex_dataset.match(dataset):
			dataset = '//lmdb/the_tangle/%s_sections' % dataset

		a = get(dataset)
		assert a.status_code == 200

		ss = a.text.split(',')
		if urls_as_names:
			return ss

		return [self.rex_section.sub('\\2', s) for s in ss]


	def blocks(self, dataset, section):
		"""
		Returns a list with the block names (as urls) for a given section of a dataset.

	    Arguments:
		dataset		  -- The name of the dataset. (The url to its sections list is also accepted.)
		section		  -- The name of the section. (The url to its blocks list is also accepted.)
		"""

		if self.rex_dataset.match(dataset):
			dataset = self.rex_dataset.sub('\\1', dataset)

		if self.rex_section.match(section):
			section = self.rex_section.sub('\\2', section)

		url = '//lmdb/the_tangle/%s_%s_blocks' % (dataset, section)

		a = get(url)
		assert a.status_code == 200

		return a.text.split(',')


class CompileTheTangle():
	"""
	This class compiles the sources of The Tangle (downloaded from github) into the Jazz server LMDB persistence.

	To do that, you have to run its .compile() method.

	This must only be done once.

	See https://kaalam.github.io/jazz_reference/reference_docker_tangle_server.html
	"""

	def __init__(self):
		self.repos_path = '/home/jazz/jazz_dbg_mdb/github_repos'
		self.rex = re.compile('^([^_]+)_([^_]+)_([0-9]+)_([0-9]+)$')
		self.datasets = set()
		self.sections = dict()
		self.blocks	  = dict()


	def ls(self, path):
		a = get('//deque/etl_stack/~last=//file&%s;' % path)
		assert a.status_code == 200

		a = get('//deque/etl_stack/~plast.text')
		assert a.status_code == 200

		return eval('{%s}' % a.text[1:-1])


	def push_block(self, repo, s_dataset, s_section, fn):
		u_dataset = '//lmdb/the_tangle/%s_sections' % s_dataset
		u_section = '//lmdb/the_tangle/%s_%s_blocks' % (s_dataset, s_section)
		u_block	  = '//lmdb/the_tangle/%s' % fn

		self.datasets.add(u_dataset)

		if u_dataset not in self.sections:
			self.sections[u_dataset] = set()

		self.sections[u_dataset].add(u_section)

		if u_dataset not in self.blocks:
			self.blocks[u_dataset] = dict()

		if u_section not in self.blocks[u_dataset]:
			self.blocks[u_dataset][u_section] = []

		self.blocks[u_dataset][u_section].append(u_block)

		a = get('//deque/etl_stack/~last=//file&%s/%s/data/%s/%s;' % (self.repos_path, repo, s_dataset, fn))
		assert a.status_code == 200

		a = get('%s=//deque/etl_stack/~plast.raw' % u_block)
		assert a.status_code == 200


	def compile_dataset(self, repo, dataset):
		print('Compiling %s:' % dataset, end = ' ', flush = True)
		ll = self.ls('%s/%s/data/%s' % (self.repos_path, repo, dataset))
		ln = 0
		for fn, typ in zip(ll['key'], ll['value']):
			if typ == 'file':
				assert self.rex.match(fn)
				assert self.rex.sub('\\1', fn) == dataset
				section = self.rex.sub('\\2', fn)
				if ln % 10 == 0:
					print(end = '.', flush = True)
				ln += 1
				self.push_block(repo, dataset, section, fn)
		print()


	def compile_repo(self, repo):
		ll = self.ls('%s/%s/data' % (self.repos_path, repo))
		for dataset, typ in zip(ll['key'], ll['value']):
			if typ == 'folder':
				self.compile_dataset(repo, dataset)


	def write_block(self, w_url, w_list):
		print('Writing %s' % w_url)
		a = put(w_url, ','.join(w_list))
		assert a.status_code == 201


	def compile(self, keep_repositories = False):
		"""
		This is the compiler. See https://kaalam.github.io/jazz_reference/reference_docker_tangle_server.html
		"""

		get('//deque/etl_stack.new')
		if 'github_repos' not in self.ls('/home/jazz/jazz_dbg_mdb/')['key']:
			print('The "github_repos" folder does not exist in the docker image!')
			print('\nPossible reasons are:\n')
			print('  1. You are trying to use this on a Jazz server that is not The Tangle.')
			print('  2. You have not yet run "./download_and_store.sh" in the container.')
			print('  3. You already completed CompileTheTangle (must only be done once).\n')
			print('See https://kaalam.github.io/jazz_reference/reference_docker_tangle_server.html for details')
			delete('//deque/etl_stack')

			return

		delete('//lmdb/the_tangle')
		a = get('//lmdb/the_tangle.new')
		assert a.status_code == 200

		for repo in self.ls(self.repos_path)['key']:
			self.compile_repo(repo)

		for dataset in self.datasets:
			for section in self.sections[dataset]:
				self.write_block(section, self.blocks[dataset][section])

			self.write_block(dataset, list(self.sections[dataset]))

		self.write_block('//lmdb/the_tangle/datasets', list(self.datasets))

		if not keep_repositories:
			print('Removing the source tree ...', end = ' ', flush = True)
			delete('//file&%s;' % self.repos_path)
			print('Ok.')

		print('\nDone.')
		delete('//deque/etl_stack')
