# The Tangle: An entangled collection of English text for Jazz

# 	Jazz (c) 2021-2022 kaalam.ai (The Authors of Jazz)

# 		Code is licensed under the Apache License, Version 2.0 http://www.apache.org/licenses/LICENSE-2.0
#		Data is open source (see LICENSE_* files in kaalam/tng-data-* repositories for details.)


import json, re

from file_paths import etl_source, etl_dest
from Section import Section


class Raiders:

	def __init__(self, source_fn = etl_source + '/RaidersOfTheLostKek/pol_062016-112019_labeled.json', out_path = etl_dest):
		self.source_fn = source_fn
		self.text	   = Section('Raiders', 'text', out_path + '/Raiders', num_rows = 5000)


	def build(self):
		rx_l = re.compile("^([A-Za-z0-9 ,!?'\\.]+)(<.*)?$")
		rx_r = re.compile("^(.*>)([A-Za-z0-9 ,!?'\\.]+)$")

		f_in = open(self.source_fn, 'r')
		t_ll = 0
		line = f_in.readline()
		while line is not None:
			if t_ll % 10000 == 0:
				print('%0.2fM,' % (t_ll/1000000), end = ' ', flush = True)

			try:
				blk = json.loads(line)

			except json.decoder.JSONDecodeError:
				break

			for post in blk['posts']:
				if 'com' in post:
					txt = post['com'].replace('&#039;', "'")

					if rx_l.match(txt):
						# print(rx_l.sub('\\1', txt))
						self.text.write_line(rx_l.sub('\\1', txt))

					if rx_r.match(txt):
						# print(rx_r.sub('\\2', txt))
						self.text.write_line(rx_r.sub('\\2', txt))

			t_ll += 1
			line  = f_in.readline()

		f_in.close()
		self.text.close()


c = Raiders()
c.build()
print('\n\nDone.')
