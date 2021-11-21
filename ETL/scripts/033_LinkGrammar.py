import re


class LinkGrammar:

	def __init__(self, in_path = '/home/jadmin/kaalam.github/neat-lg/neatlg/data/', out_path  = './'):
		self.in_path = in_path
		self.out_word_lnk = out_path + 'linkgrammar/links.txt'
		self.out_word_pos = out_path + 'linkgrammar/pos.txt'
		self.out_words = out_path + 'indices/words.linkgram'
		self.out_links = out_path + 'indices/links.linkgram'


	def inputs(self):
		return [self.in_path + '*']


	def outputs(self):
		return [self.out_word_lnk, self.out_word_pos, self.out_words, self.out_links]


	def build(self):
		pass


c = LinkGrammar()
c.build()
print('\n\nDone.')