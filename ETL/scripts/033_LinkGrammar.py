import os, re


from file_paths import etl_source, etl_dest
from Section import Section


class LinkGrammar:

	def __init__(self, in_path = etl_source + '/LinkGrammar/words', out_path = etl_dest):
		self.in_path = in_path
		self.words	 = Section('LinkGrammar', 'word', out_path + '/LinkGrammar', num_rows = 10000)


	def build(self):
		rex_fn	  = re.compile('^words.*$')
		rex_split = re.compile('^([A-Za-z]+)\\.[A-Za-z]+$')
		rex_word  = re.compile('^[A-Za-z]+$')
		words	  = set()
		names	  = os.listdir(self.in_path)
		names.sort()

		for fn in names:
			if rex_fn.match(fn):
				print(fn, ',', end = ' ', flush = True)
				f_in = open('%s/%s' % (self.in_path, fn), 'r', encoding = 'ISO-8859-1')
				line = f_in.readline()

				while line != '':
					line = line.strip()
					if line != '':
						ww = line.split(' ')
						for w in ww:
							if rex_split.match(w):
								w = rex_split.sub('\\1', w)
							if rex_word.match(w):
								words.add(w)

					line = f_in.readline()

				f_in.close()

		wl = list(words)
		wl.sort()
		for w in wl:
			self.words.write_line(w)

		self.words.close()


c = LinkGrammar()
c.build()
print('\n\nDone.')
