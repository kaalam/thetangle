# The Tangle: An entangled collection of English text for Jazz

# 	Jazz (c) 2021-2025 kaalam.ai (The Authors of Jazz)

# 		Code is licensed under the Apache License, Version 2.0 http://www.apache.org/licenses/LICENSE-2.0
#		Data is open source (see LICENSE_* files in kaalam/tng-data-* repositories for details.)


import os, re


from lxml import etree


from file_paths import etl_source, etl_dest
from Section import Section


class EchoTarget:

	def __init__(self, out_path = etl_dest):
		self.level	= 0
		self.ent_id	= None
		self.form	= None
		self.pos	= None
		self.ss_id	= None
		self.synset	= None
		self.tx_pos	= Section('WordNet', 'tx-pos', out_path + '/WordNet', num_rows = 10000)
		self.tx_syn	= Section('WordNet', 'tx-syn', out_path + '/WordNet', num_rows = 10000)
		self.tx_rel	= Section('WordNet', 'tx-rel', out_path + '/WordNet', num_rows = 10000)
		self.t_ll	= 0


	def start(self, tag, attrib):
		# print ('  '*self.level + ':>' + tag)
		self.level += 1

		if tag == 'LexicalEntry':
			assert self.level == 3 and self.ent_id is None
			self.ent_id = attrib['id']

			return

		if tag == 'Lemma':
			assert self.level == 4 and self.ent_id is not None and self.form is None and self.pos is None

			self.form = attrib['writtenForm']
			self.pos  = attrib['partOfSpeech']

			self.t_ll += 1
			if self.t_ll % 10000 == 0:
				print('%0.2fM,' % (self.t_ll/1000000), end = ' ', flush = True)

			self.tx_pos.write_line('%s, %s, %s' % (self.form, self.pos, self.ent_id))

			return

		if tag == 'Sense':
			assert self.level == 4 and self.ent_id is not None and self.form is None and self.pos is None

			self.ss_id	= attrib['id']
			self.synset	= attrib['synset']

			self.tx_syn.write_line('%s, %s, %s' % (self.ent_id, self.ss_id, self.synset))

			return

		if tag == 'SenseRelation':
			assert (self.level == 5 and self.ent_id is not None and self.form is None and self.pos is None
					and self.ss_id is not None and self.synset is not None)

			self.relation = attrib['relType']
			self.target	  = attrib['target']

			self.tx_rel.write_line('%s, %s, %s, %s' % (self.ent_id, self.ss_id, self.relation, self.target))

			return


	def end(self, tag):
		self.level -= 1

		if tag == 'LexicalEntry':
			self.ent_id = None
			return

		if tag == 'Lemma':
			self.form = None
			self.pos  = None
			return

		if tag == 'Sense':
			self.ss_id	= None
			self.synset	= None


	def data(self, data):
		pass


	def close(self):
		self.tx_pos.close()
		self.tx_syn.close()
		self.tx_rel.close()

		return "closed!"


class WordNet:

	def __init__(self,
				 source_fn = etl_source + '/english-wordnet/wn.xml',
				 out_path  = etl_dest):

		self.source_fn = source_fn
		self.out_path  = out_path


	def build(self):
		parser = etree.XMLParser(target = EchoTarget(self.out_path))

		etree.parse(self.source_fn, parser)


c = WordNet()
c.build()
print('\n\nDone.')
