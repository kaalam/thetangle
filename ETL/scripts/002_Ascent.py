# The Tangle: An entangled collection of English text for Jazz

# 	Jazz (c) 2021-2025 kaalam.ai (The Authors of Jazz)

# 		Code is licensed under the Apache License, Version 2.0 http://www.apache.org/licenses/LICENSE-2.0
#		Data is open source (see LICENSE_* files in kaalam/tng-data-* repositories for details.)


import json, re

from file_paths import etl_source, etl_dest
from Section import Section


class Ascent:

	def __init__(self, source_fn = etl_source + '/ascent/ascent-v1.0.0.json', out_path = etl_dest):
		self.source_fn = source_fn
		self.relations = Section('ascent', 'relations', out_path + '/ascent')
		self.concepts  = Section('ascent', 'concepts', out_path + '/ascent', num_rows = 10000)


	def build(self):
		f_in = open(self.source_fn, 'r')

		rex_fi = re.compile('^[a-zA-Z ]+$')

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

					arg1 = obj['arg1']
					if rex_fi.match(arg1):
						words.add(arg1)

					arg2 = obj['arg2']
					if rex_fi.match(arg2):
						words.add(arg2)

					if "source_sentences" in obj:
						ll = obj["source_sentences"]
						for s in ll:
							self.relations.write_line(s['text'])

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


c = Ascent()
c.build()
print('\n\nDone.')
