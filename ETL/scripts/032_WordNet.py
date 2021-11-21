import os, re


class WordNet:

	def __init__(self, in_path = '/home/jadmin/kaalam.etc/nlp/corpora/princeton-wordnet/dict/dbfiles/', out_path  = './'):
		self.in_path = in_path
		self.rel_types = out_path + 'wordnet/rel_type.txt'
		self.relations = out_path + 'wordnet/relation.txt'


	def inputs(self):
		return [self.in_path + '*']


	def outputs(self):
		return [self.rel_types, self.relations]


	def build(self):
		f_rt = open(self.rel_types, 'w')
		f_rl = open(self.relations, 'w')

		rex = re.compile('^[a-z]+\\.[a-z]+$')

		for fn in os.listdir(self.in_path):
			if rex.match(fn):
				print(fn)
				with open(self.in_path + fn, 'r') as fh:
					line = fh.readline()
					while line != '':
						line = line.strip()
						if line.startswith('{') and line.endswith('}'):
							f_rt.write(fn + '\n')
							f_rl.write(line + '\n')

						line = fh.readline()

		f_rt.close()
		f_rl.close()


c = WordNet()
c.build()
print('\n\nDone.')