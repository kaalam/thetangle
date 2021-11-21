import re

from lxml import etree


def clean(s):
	while s.find('  ') >=0: s = s.replace('  ', ' ')
	while s.find(' ,') >=0: s = s.replace(' ,', ',')
	while s.find(' .') >=0: s = s.replace(' .', '.')
	return s.strip()


class EchoTarget:

	def __init__(self, fn_title, fn_text):
		self.level	= 0
		self.state	= 0
		self.rex_tg	= re.compile("^\\{http://www.mediawiki.org/xml/export-0.10/\\}([a-z0-9]+)$")
		self.rex_cl	= re.compile('[^a-z0-9\'\\-,\\.\\? ]')
		self.rex_st	= re.compile('^(\\{\\{|#|name|file|image).*$')
		self.title	= None
		self.text	= ''
		self.f_titl	= open(fn_title, 'w')
		self.f_text	= open(fn_text, 'w')
		self.t_ll	= 0


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

			self.t_ll += 1
			if self.t_ll % 10000 == 0:
				print('%0.2fM,' % (self.t_ll/1000000), end = ' ', flush = True)

			txt = self.text.split('\n')
			par = ''
			for line in txt:
				if not self.rex_st.match(line):
					line = clean(self.rex_cl.sub(' ', line.lower()))
					par  = clean(par + ' ' + line)

					if len(par) > 4096:
						break

			if (len(par) > 20):
				self.f_titl.write(self.title + '\n')
				self.f_text.write(par + '\n')

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
		self.f_titl.close()
		self.f_text.close()

		return "closed!"


class Wikipedia:

	def __init__(self,
				 source_fn = '/home/jadmin/kaalam.etc/nlp/corpora/en_wiki_20211001/enwiki-20211001-pages-articles-multistream.xml',
				 out_path  = './'):

		self.source_fn	 = source_fn
		self.out_title	 = out_path + 'wikipedia/titles.txt'
		self.out_content = out_path + 'wikipedia/content.txt'


	def inputs(self):
		return [self.source_fn]


	def outputs(self):
		return [self.out_title, self.out_content]


	def build(self):
		parser = etree.XMLParser(target = EchoTarget(self.out_title, self.out_content))

		etree.parse(self.source_fn, parser)


c = Wikipedia()
c.build()
print('\n\nDone.')
