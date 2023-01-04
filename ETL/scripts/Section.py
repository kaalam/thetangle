# The Tangle: An entangled collection of English text for Jazz

# 	Jazz (c) 2021-2023 kaalam.ai (The Authors of Jazz)

# 		Code is licensed under the Apache License, Version 2.0 http://www.apache.org/licenses/LICENSE-2.0
#		Data is open source (see LICENSE_* files in kaalam/tng-data-* repositories for details.)


import os, re


class Section():

	def __init__(self, dataset_name, section_name, path_blocks, num_rows = 1000):
		self.num_rows = num_rows

		if num_rows <= 1000:
			self.format = '%s/%s_%s_%05i_%03i'
		elif num_rows <= 10000:
			self.format = '%s/%s_%s_%05i_%04i'
		else:
			raise(SyntaxError)

		self.dataset_name = dataset_name
		self.section_name = section_name
		self.path_blocks  = path_blocks

		self.block_num = 1
		self.block_idx = 0
		self.f_out	   = None

		self.rex = re.compile('[^A-Za-z0-9;:,_+*= !@&/()\'\\.\\-\\?]')


	def block_name(self, last_idx):
		return self.format % (self.path_blocks, self.dataset_name, self.section_name, self.block_num, last_idx)


	def close_block(self):
		last_idx = self.block_idx - 1

		self.f_out.write(']\n')
		self.f_out.close()

		if last_idx != 0:
			os.rename(self.block_name(0), self.block_name(last_idx))

		self.block_num += 1
		self.block_idx  = 0


	def write_line(self, ln):
		if self.block_idx == self.num_rows:
			self.close_block()

		if self.block_idx == 0:
			self.f_out = open(self.block_name(0), 'w')
			self.f_out.write('[')
		else:
			self.f_out.write(',')

		self.f_out.write('"%s"' % ' '.join(self.rex.sub('', ln.replace('\n', ' ').replace('"', "'")).strip().split()))
		self.block_idx += 1


	def close(self):
		if self.block_idx != 0:
			self.close_block()
