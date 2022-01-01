# The Tangle: An entangled collection of English text for Jazz

# 	Jazz (c) 2021-2021 kaalam.ai (The Authors of Jazz)

# 		Code is licensed under the Apache License, Version 2.0 http://www.apache.org/licenses/LICENSE-2.0
#		Data is open source (see LICENSE_* files in kaalam/tng-data-* repositories for details.)


import re

from file_paths import etl_source, etl_dest
from Section import Section


class OpenSubtitles:

	def __init__(self, source_fn = etl_source + '/open_sub/monolingual.raw.en', out_path = etl_dest):
		self.source_fn = source_fn
		self.text	   =  Section('OpenSubtitles', 'text', out_path + '/OpenSubtitles', num_rows = 10000)


	def build(self):
		f_in = open(self.source_fn, 'r')

		rex_cl = re.compile('(:|\\(|]|^[^a-zA-Z]|^Presented|^Produced|^In association)')
		rex_md = re.compile('.*[aeiou].*')

		lines = set()

		t_zz = t_rl = 0

		line = f_in.readline()
		while line is not None:
			t_rl += 1
			if t_rl % 1000000 == 0:
				print('%0.1f/%0.1fM,' % (len(lines)/1000000, t_rl/1000000), end = ' ', flush = True)

			if len(line) == 0:
				t_zz += 1
				if t_zz == 1000:
					break
			else:
				t_zz = 0

				if (not rex_cl.match(line)) and (rex_md.match(line)):
					line = line.strip()
					lines.add(line)

			line = f_in.readline()

		print('\nSorting ...', end = ' ', flush = True)
		wl = list(lines)
		wl.sort()
		print('Ok.\nWriting ...', end = ' ', flush = True)
		for w in wl:
			self.text.write_line(w)
		print('Ok.')

		f_in.close()
		self.text.close()


c = OpenSubtitles()
c.build()
print('\n\nDone.')
