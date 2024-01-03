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
		self.pos		= Section('gCide', 'pos', out_path + '/gCide', num_rows = 10000)
		self.definition	= Section('gCide', 'definition', out_path + '/gCide', num_rows = 10000)


	def build(self):
		rex_fn		 = re.compile('^CIDE\\..$')
		rex_ent_any	 = re.compile('^<p><ent>(.*)</ent>.*$')
		rex_ent_neat = re.compile('^<p><ent>([A-Za-z0-9\\-\' ]+)</ent>.*$')
		rex_pos_any	 = re.compile('^.*<pos>(.*)</pos>.*$')
		rex_pos_neat = re.compile('^.*<pos>([A-Za-z0-9,\\.& ]+)</pos>.*$')
		rex_def		 = re.compile('^.*<def>(.*)</def>.*$')
		rex_tag		 = re.compile('^(.*)</?[A-Za-z]+>(.*)$')
		names		 = os.listdir(self.in_path)
		names.sort()

		pos_set = set()

		for fn in names:
			if rex_fn.match(fn):
				print(fn, ',', end = ' ', flush = True)
				f_in = open('%s/%s' % (self.in_path, fn), 'r', encoding = 'ISO-8859-1')
				line = f_in.readline()

				ent = None
				pos = '?'
				while line != '':
					line = line.strip()

					if rex_ent_any.match(line):
						ent = None
						if rex_ent_neat.match(line):
							ent = rex_ent_neat.sub('\\1', line)

					if rex_pos_any.match(line):
						pos = '?'
						if rex_pos_neat.match(line):
							pos = rex_pos_neat.sub('\\1', line)
							pos_set.add(pos)

					if rex_def.match(line):
						dfn = rex_def.sub('\\1', line)
						if ent is not None:
							while rex_tag.match(dfn):
								dfn = rex_tag.sub('\\1\\2', dfn)

							self.entity.write_line(ent)
							self.pos.write_line(pos)
							self.definition.write_line(dfn)

					line = f_in.readline()

				f_in.close()

		self.entity.close()
		self.pos.close()
		self.definition.close()


c = gCide()
c.build()
print('\n\nDone.')
