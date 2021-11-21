import re


class GenericsKB:

	def __init__(self, source_fn = '/home/jadmin/kaalam.etc/nlp/corpora/GenericsKB/GenericsKB.tsv', out_path  = './'):
		self.source_fn = source_fn
		self.out_relations = out_path + 'generics_kb/blocks.txt'
		self.out_concepts  = out_path + 'indices/words.generics_kb'


	def inputs(self):
		return [self.source_fn]


	def outputs(self):
		return [self.out_relations, self.out_concepts]


	def build(self):
		f_in = open(self.source_fn, 'r')
		f_ix = open(self.out_concepts, 'w')
		f_rl = open(self.out_relations, 'w')

		rex_cl = re.compile('[^a-z ]')
		rex_fi = re.compile('^[a-z ]+$')

		words = set()

		t_zz = t_ll = 0

		line = f_in.readline()
		while line is not None:
			line = f_in.readline()

			if len(line) == 0:
				t_zz += 1
				if t_zz == 1000:
					break
			else:
				t_zz = 0

				t_ll += 1
				if t_ll % 100000 == 0:
					print('%0.1fM,' % (t_ll/1000000), end = ' ', flush = True)
				try:
					source, term, quantifier, sentence, score = line.split('\t')

					if rex_fi.match(term.lower()):
						words.add(term.lower())

						f_rl.write(rex_cl.sub('', sentence.lower()) + '\n')

				except ValueError:
					pass

		wl = list(words)
		wl.sort()
		f_ix.write('\n'.join(wl))

		f_in.close()
		f_ix.close()
		f_rl.close()


c = GenericsKB()
c.build()
print('\n\nDone.')