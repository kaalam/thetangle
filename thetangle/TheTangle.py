# MIT License

# Copyright (c) 2021 kaalam.ai The Authors of Jazz

# Hosted at https://github.com/kaalam/thetangle

import re
import requests as http


LOCAL_SERVER_URL = 'http://127.0.0.1:8899'


def get(qq):
	return http.get(LOCAL_SERVER_URL + qq)

def put(qq, string):
	return http.put(LOCAL_SERVER_URL + qq, string)

def delete(qq):
	return http.delete(LOCAL_SERVER_URL + qq)


class TangleExplorer():

	def __init__(self):
		pass


class CompileTheTangle():

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
		print('  ', repo, ', ', dataset)
		ll = self.ls('%s/%s/data/%s' % (self.repos_path, repo, dataset))
		for fn, typ in zip(ll['key'], ll['value']):
			if typ == 'file':
				assert self.rex.match(fn)
				assert self.rex.sub('\\1', fn) == dataset
				section = self.rex.sub('\\2', fn)
				self.push_block(repo, dataset, section, fn)


	def compile_repo(self, repo):
		print(repo)
		ll = self.ls('%s/%s/data' % (self.repos_path, repo))
		for dataset, typ in zip(ll['key'], ll['value']):
			if typ == 'folder':
				self.compile_dataset(repo, dataset)


		delete('//lmdb/the_tangle')
		a = get('//lmdb/the_tangle.new')
		assert a.status_code == 200

		for repo in self.ls(self.repos_path)['key']:
			self.compile_repo(repo)


	def __del__(self):
		delete('//deque/etl_stack')


ct = CompileTheTangle()

ct.main()

a = ct.ls('/')

print(a)
