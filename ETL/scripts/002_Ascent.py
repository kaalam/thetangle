import json
import re


class Ascent:

	def __init__(self, source_fn = '/home/jadmin/kaalam.etc/nlp/corpora/ascent/ascent-v1.0.0.json', out_path  = './'):
		self.source_fn = source_fn
		self.out_relations = out_path + 'ascent/blocks.txt'
		self.out_concepts  = out_path + 'indices/words.ascent'


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
					obj = json.loads(line)

					arg1 = obj['arg1'].lower()
					if rex_fi.match(arg1):
						words.add(arg1)

					arg2 = obj['arg2'].lower()
					if rex_fi.match(arg2):
						words.add(arg2)

					if "source_sentences" in obj:
						ll = obj["source_sentences"]
						for s in ll:
							f_rl.write(rex_cl.sub('', s['text'].lower()).replace('  ', ' ') + '\n')

				except ValueError:
					pass

			line = f_in.readline()

		wl = list(words)
		wl.sort()
		f_ix.write('\n'.join(wl))

		f_in.close()
		f_ix.close()
		f_rl.close()


c = Ascent()
c.build()
print('\n\nDone.')