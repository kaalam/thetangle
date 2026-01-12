# The Tangle: An entangled collection of English text for Jazz

# 	Jazz (c) 2021-2026 kaalam.ai (The Authors of Jazz)

# 		Code is licensed under the Apache License, Version 2.0 http://www.apache.org/licenses/LICENSE-2.0
#		Data is open source (see LICENSE_* files in kaalam/tng-data-* repositories for details.)


import re

from lxml import etree


from file_paths import etl_source, etl_dest
from Section import Section


class EchoTarget:

	def __init__(self, out_path = etl_dest):
		self.level		= 0
		self.state		= 0
		self.rex_tg		= re.compile("^\\{http://www.mediawiki.org/xml/export-0.10/\\}([a-z0-9]+)$")
		self.rex_head	= re.compile('^{{[Ss]hort description\\|(.*)}}$')
		self.rex_text	= re.compile("^(==.*==|[A-Z].*|'''.*)$")
		self.title		= None
		self.text		= ''
		self.titles		= Section('wikipedia', 'title', out_path + '/wikipedia', num_rows = 5000)
		self.in_short	= Section('wikipedia', 'in-short', out_path + '/wikipedia', num_rows = 5000)
		self.texts		= Section('wikipedia', 'text', out_path + '/wikipedia', num_rows = 5000)
		self.t_ll		= 0

		self.titles.write_line('__en_wiki_date__')
		self.in_short.write_line('20241220')
		self.texts.write_line('enwiki-20241220-pages-articles-multistream.xml downloaded from https://dumps.wikimedia.org/enwiki/')


	def start(self, tag, attrib):
		tag = self.rex_tg.sub('\\1', tag)

		self.level += 1

		if tag == 'page':
			assert self.state == 0 and self.level == 2
			self.state = 1
			return

		if tag == 'title':
			assert self.state == 1 and self.level == 3
			self.state = 2
			return

		if tag == 'text':
			assert self.state == 3 and self.level == 4
			self.state = 4
			return

		if self.state > 3:
			assert self.state == 5

			txt = self.text.split('\n')

			if len(txt) > 3 and self.rex_head.match(txt[0]):
				short = self.rex_head.sub('\\1', txt[0])
				parag = ''
				for line in txt:
					if self.rex_text.match(line):
						parag += line
						if len(parag) > 4096:
							break

				if (len(parag) > 20):
					self.t_ll += 1
					if self.t_ll % 10000 == 0:
						print('%0.2fM,' % (self.t_ll/1000000), end = ' ', flush = True)

					self.titles.write_line(self.title)
					self.in_short.write_line(short)
					self.texts.write_line(parag)

			self.state = 0
			self.title = None
			self.text  = ''


	def end(self, tag):
		self.level -= 1


	def data(self, data):
		if self.state < 2:
			return

		if self.state < 4:
			if self.state == 2:
				self.title = data
				self.state = 3

			return

		self.text += data
		self.state = 5


	def close(self):
		self.titles.close()
		self.in_short.close()
		self.texts.close()

		return "closed!"


class Wikipedia:

	def __init__(self,
				 source_fn = etl_source + '/en_wiki_20241220/enwiki-20241220-pages-articles-multistream.xml',
				 out_path  = etl_dest):

		self.source_fn = source_fn
		self.out_path  = out_path


	def build(self):
		parser = etree.XMLParser(target = EchoTarget(self.out_path))

		etree.parse(self.source_fn, parser)


c = Wikipedia()
c.build()
print('\n\nDone.')
