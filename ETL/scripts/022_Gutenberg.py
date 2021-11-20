import os


class Gutenberg:

	def __init__(self,
				 in_tit = '/home/jadmin/kaalam.etc/nlp/corpora/gutenberg/index-titles.txt',
				 in_idx = '/home/jadmin/kaalam.etc/nlp/corpora/gutenberg/index-blocks.txt',
				 in_pat = '/home/jadmin/kaalam.etc/nlp/corpora/gutenberg/books/',
				 oo_pat = 'gutenberg/'):

		self.in_tit = in_tit
		self.in_idx = in_idx
		self.in_pat = in_pat
		self.oo_pat = oo_pat


	def inputs(self):
		return [self.in_tit, self.in_idx, self.in_pat + '*']


	def outputs(self):
		return [self.oo_pat + '*']


	def build(self):
		f_tit = open(self.in_tit, 'r')
		f_idx = open(self.in_idx, 'r')
		fo_tt = open(self.oo_pat + 'index-titles.txt', 'w')
		fo_ix = open(self.oo_pat + 'index-blocks.txt', 'w')

		tt = f_tit.readline()
		xx = f_idx.readline()

		assert ((tt == '') == (xx == ''))

		blocks = set()

		t_ll = 0

		while tt != '':
			t_ll += 1
			if t_ll % 100 == 0:
				print('%2.1fK-books,' % (t_ll/1000), end = ' ', flush = True)

			tt = tt.strip()
			xx = xx.strip()

			fn_in = "%s%s.RData" % (self.in_pat, xx)

			if len(xx) < 30:
				blocks.add(xx)
			else:
				xx = xx[0:28]
				for i in range(101):
					if i == 100:
						raise AssertionError

					if xx + str(i) not in blocks:
						xx = xx + str(i)
						blocks.add(xx)
						break

			fn_out = "%s%s.txt" % (self.oo_pat, xx)

			cmd = "/home/jadmin/kaalam.etc/nlp/corpora/gutenberg/cat.R %s > %s" % (fn_in, fn_out)

			os.system(cmd)

			fo_tt.write(tt + '\n')
			fo_ix.write(xx + '\n')

			tt = f_tit.readline()
			xx = f_idx.readline()

			assert ((tt == '') == (xx == ''))

		f_tit.close()
		f_idx.close()
		fo_tt.close()
		fo_ix.close()


c = Gutenberg()
c.build()
print('\n\nDone.')
