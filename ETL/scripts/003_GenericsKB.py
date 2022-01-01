# The Tangle: An entangled collection of English text for Jazz

# 	Jazz (c) 2021-2021 kaalam.ai (The Authors of Jazz)

# 		Code is licensed under the Apache License, Version 2.0 http://www.apache.org/licenses/LICENSE-2.0
#		Data is open source (see LICENSE_* files in kaalam/tng-data-* repositories for details.)


import re

from file_paths import etl_source, etl_dest
from Section import Section


class GenericsKB:

	def __init__(self, source_fn = etl_source + '/GenericsKB/GenericsKB.tsv', out_path = etl_dest):
		self.source_fn = source_fn
		self.relations = Section('GenericsKB', 'relations', out_path + '/GenericsKB')
		self.concepts  = Section('GenericsKB', 'concepts', out_path + '/GenericsKB', num_rows = 10000)


	def build(self):
		f_in = open(self.source_fn, 'r')

		rex_fi = re.compile('^[a-zA-Z ]+$')

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

					if rex_fi.match(term):
						words.add(term)

						self.relations.write_line(sentence)

				except ValueError:
					pass

		wl = list(words)
		wl.sort()
		for w in wl:
			self.concepts.write_line(w)

		f_in.close()
		self.relations.close()
		self.concepts.close()


c = GenericsKB()
c.build()
print('\n\nDone.')
