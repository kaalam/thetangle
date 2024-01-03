# The Tangle: An entangled collection of English text for Jazz

# 	Jazz (c) 2021-2024 kaalam.ai (The Authors of Jazz)

# 		Code is licensed under the Apache License, Version 2.0 http://www.apache.org/licenses/LICENSE-2.0
#		Data is open source (see LICENSE_* files in kaalam/tng-data-* repositories for details.)


import os


from file_paths import etl_source, etl_dest
from Section import Section


class Gutenberg:

	def __init__(self,
				 in_tit	  = etl_source + '/gutenberg/index-titles.txt',
				 in_idx	  = etl_source + '/gutenberg/index-blocks.txt',
				 in_pat	  = etl_source + '/gutenberg/books/',
				 out_path = etl_dest):

		self.in_tit = in_tit
		self.in_idx = in_idx
		self.in_pat = in_pat
		self.title	= Section('gutenberg', 'title', out_path + '/gutenberg')
		self.book	= Section('gutenberg', 'book', out_path + '/gutenberg', num_rows = 10)


	def build(self):
		f_tit = open(self.in_tit, 'r')
		f_idx = open(self.in_idx, 'r')

		tt = f_tit.readline()
		xx = f_idx.readline()

		assert ((tt == '') == (xx == ''))

		t_ll = 0

		while tt != '':
			t_ll += 1
			if t_ll % 100 == 0:
				print('%2.1fK-books,' % (t_ll/1000), end = ' ', flush = True)

			tt = tt.strip()
			xx = xx.strip()

			self.title.write_line(tt)

			fn_in  = "%s%s.RData" % (self.in_pat, xx)
			fn_out = "./book_text.txt"

			cmd = "%s/gutenberg/cat.R %s > %s" % (etl_source, fn_in, fn_out)

			os.system(cmd)

			with open(fn_out, 'r', encoding = 'ISO-8859-1') as f:
				book = f.read()
				self.book.write_line(book)

			os.remove(fn_out)

			tt = f_tit.readline()
			xx = f_idx.readline()

			assert ((tt == '') == (xx == ''))

		f_tit.close()
		f_idx.close()
		self.title.close()
		self.book.close()


c = Gutenberg()
c.build()
print('\n\nDone.')
