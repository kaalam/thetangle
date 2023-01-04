# The Tangle: An entangled collection of English text for Jazz

# 	Jazz (c) 2021-2023 kaalam.ai (The Authors of Jazz)

# 		Code is licensed under the Apache License, Version 2.0 http://www.apache.org/licenses/LICENSE-2.0
#		Data is open source (see LICENSE_* files in kaalam/tng-data-* repositories for details.)


import re

from file_paths import etl_source, etl_dest
from Section import Section


class ConceptNet:

	def __init__(self, source_fn = etl_source + '/ConceptNet55/conceptnet-assertions-5.7.0.csv', out_path = etl_dest):
		self.source_fn = source_fn
		self.relations = Section('ConceptNet', 'relations', out_path + '/ConceptNet')
		self.concepts  = Section('ConceptNet', 'concepts', out_path + '/ConceptNet', num_rows = 10000)


	def build(self):
		f_in = open(self.source_fn, 'r')

		rex_ix = re.compile('^/c/en/([a-z_]+)(/.*)?$')
		rex_rl = re.compile('^.*"surfaceText": "([^"]+)".*$')

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
							self.relations.write_line(rex_rl.sub('\\1', extra))

				except ValueError:
					pass

			line = f_in.readline()

		wl = list(words)
		wl.sort()
		for w in wl:
			self.concepts.write_line(w)

		f_in.close()
		self.relations.close()
		self.concepts.close()


c = ConceptNet()
c.build()
print('\n\nDone.')
