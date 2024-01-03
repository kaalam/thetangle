# The Tangle: An entangled collection of English text for Jazz

# 	Jazz (c) 2021-2024 kaalam.ai (The Authors of Jazz)

# 		Code is licensed under the Apache License, Version 2.0 http://www.apache.org/licenses/LICENSE-2.0
#		Data is open source (see LICENSE_* files in kaalam/tng-data-* repositories for details.)


import os, re


from file_paths import etl_source, etl_dest
from Section import Section


class gCide:

	def __init__(self, in_path = etl_source + '/gcide/gcide-0.53', out_path = etl_dest):
		self.in_path	= in_path
		self.entity		= Section('gCide', 'entity', out_path + '/gCide', num_rows = 10000)
		self.definition	= Section('gCide', 'definition', out_path + '/gCide', num_rows = 10000)


	def build(self):
		rex_fn	= re.compile('^CIDE\\..$')
		rex_ent	= re.compile('^.*<ent>(.*)</ent>.*$')
		rex_def	= re.compile('^.*<def>(.*)</def>.*$')
		names	= os.listdir(self.in_path)
		names.sort()

		for fn in names:
			if rex_fn.match(fn):
				print(fn, ',', end = ' ', flush = True)
				f_in = open('%s/%s' % (self.in_path, fn), 'r', encoding = 'ISO-8859-1')
				line = f_in.readline()

				ent = ''
				dfn = ''
				while line != '':
					line = line.strip()
					if line == '':
						ent = ''
						dfn = ''
					else:
						if rex_ent.match(line):
							ent = rex_ent.sub('\\1', line)
						if rex_def.match(line):
							dfn = rex_def.sub('\\1', line)
							if len(ent) > 0:
								self.entity.write_line(ent)
								self.definition.write_line(dfn)

					line = f_in.readline()

				f_in.close()

		self.entity.close()
		self.definition.close()


c = gCide()
c.build()
print('\n\nDone.')
