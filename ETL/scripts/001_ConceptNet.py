import re


class ConceptNet:

	def __init__(self, source_fn = '/home/jadmin/kaalam.etc/nlp/corpora/ConceptNet55/conceptnet-assertions-5.7.0.csv', out_path  = './'):
		self.source_fn = source_fn
		self.out_relations = out_path + 'conceptnet/blocks.txt'
		self.out_concepts  = out_path + 'indices/words.conceptnet'


	def inputs(self):
		return [self.source_fn]


	def outputs(self):
		return [self.out_relations, self.out_concepts]


	def build(self):
		f_in = open(self.source_fn, 'r')
		f_ix = open(self.out_concepts, 'w')
		f_rl = open(self.out_relations, 'w')

		rex_ix = re.compile('^/c/en/([a-z_]+)(/.*)?$')
		rex_rl = re.compile('^.*"surfaceText": "([^"]+)".*$')
		rex_cl = re.compile('[^a-z ]')

		words = set()

		t_zz = t_ll = t_en = t_m1 = t_m2 = t_rl = 0

		line = f_in.readline()
		while line is not None:
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
					full, rel, arg1, arg2, extra = line.split('\t')

					if (arg1.startswith('/c/en/') and arg2.startswith('/c/en/')):
						t_en += 1

						if rex_ix.match(arg1):
							t_m1 += 1
							words.add(rex_ix.sub('\\1', arg1).replace('_', ' '))

						if rex_ix.match(arg2):
							t_m2 += 1
							words.add(rex_ix.sub('\\1', arg2).replace('_', ' '))

						if rex_rl.match(extra):
							t_rl += 1
							f_rl.write(rex_cl.sub('', rex_rl.sub('\\1', extra).lower().strip()) + '\n')

				except ValueError:
					pass

			line = f_in.readline()

		wl = list(words)
		wl.sort()
		f_ix.write('\n'.join(wl))

		f_in.close()
		f_ix.close()
		f_rl.close()


c = ConceptNet()
c.build()
print('\n\nDone.')