import re


class gCide:

	def __init__(self, in_path = '/home/jadmin/kaalam.etc/nlp/corpora/gcide/gcide-0.53/', out_path = './'):
		self.in_path = in_path
		self.out_definitions = out_path + 'gcide/definitions.txt'
		self.out_synonyms = out_path + 'gcide/synonyms.txt'
		self.out_words = out_path + 'indices/words.gcide'


	def inputs(self):
		return [self.in_path + '*']


	def outputs(self):
		return [self.out_definitions, self.out_synonyms, self.out_words]


	def build(self):
		pass


c = gCide()
c.build()
print('\n\nDone.')