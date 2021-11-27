import os, re


from lxml import etree


from file_paths import etl_source, etl_dest
from Section import Section


class EchoTarget:

	def __init__(self, out_path = etl_dest):
		self.level	= 0
		self.ent_id	= None
		self.t_ll	= 0
		self.form	= Section('WordNet', 'written-form', out_path + '/WordNet', num_rows = 10000)
		self.pos	= Section('WordNet', 'part-of-speech', out_path + '/WordNet', num_rows = 10000)


	def start(self, tag, attrib):
		# print ('  '*self.level + ':>' + tag)
		self.level += 1

		if tag == 'LexicalEntry':
			assert self.level == 3
			self.ent_id = attrib['id']

			return

		if tag == 'Lemma':
			assert self.level == 4
			if 'writtenForm' in attrib and 'partOfSpeech' in attrib:
				self.t_ll += 1
				if self.t_ll % 10000 == 0:
					print('%0.2fM,' % (self.t_ll/1000000), end = ' ', flush = True)

				self.form.write_line(attrib['writtenForm'])
				self.pos.write_line(attrib['partOfSpeech'])
			else:
				assert False

			return

		if tag == 'Sense':
			assert self.level == 4
			if 'id' in attrib and 'synset' in attrib:
				""" This is a previous clarification that applies to the following edge. """
			else:
				assert False

			return

		if tag == 'SenseRelation':
			assert self.level == 5
			if 'relType' in attrib and 'target' in attrib:
				""" This is an edge in the graph!!! """
			else:
				assert False

			return


	def end(self, tag):
		self.level -= 1
		if self.level < 3:
			self.ent_id = None


	def data(self, data):
		pass


	def close(self):
		self.form.close()
		self.pos.close()

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