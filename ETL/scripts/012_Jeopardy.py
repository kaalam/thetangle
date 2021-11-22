import re

from file_paths import etl_source, etl_dest
from Section import Section


def clean(s):
	while s.find('  ') >=0: s = s.replace('  ', ' ')
	while s.find(' ,') >=0: s = s.replace(' ,', ',')
	while s.find(' .') >=0: s = s.replace(' .', '.')
	return s.strip()


class Jeopardy:

	def __init__(self, in_path = etl_source + '/jeopardy', out_path = etl_dest):
		self.in_category  = in_path	 + '/category.txt'
		self.in_question  = in_path	 + '/question.txt'
		self.in_answer	  = in_path	 + '/answer.txt'

		self.category = Section('jeopardy', 'category', out_path + '/jeopardy')
		self.question = Section('jeopardy', 'question', out_path + '/jeopardy')
		self.answer	  = Section('jeopardy', 'answer',	out_path + '/jeopardy')


	def inputs(self):
		return [self.in_category, self.in_question, self.in_answer]


	def outputs(self):
		return [self.out_category, self.out_question, self.out_answer]


	def build(self):
		f_ic = open(self.in_category, 'r')
		f_iq = open(self.in_question, 'r')
		f_ia = open(self.in_answer, 'r')

		t_ll = 0

		ct = f_ic.readline()
		qq = f_iq.readline()
		aa = f_ia.readline()

		assert ((ct == '') == (qq == '') and (ct == '') == (aa == ''))

		while ct != '':
			t_ll += 1
			if t_ll % 10000 == 0:
				print('%0.2fM,' % (t_ll/1000000), end = ' ', flush = True)

			self.category.write_line(ct)
			self.question.write_line(qq)
			self.answer.write_line(aa)

			ct = f_ic.readline()
			qq = f_iq.readline()
			aa = f_ia.readline()

			assert ((ct == '') == (qq == '') and (ct == '') == (aa == ''))

		f_ic.close()
		f_iq.close()
		f_ia.close()

		self.category.close()
		self.question.close()
		self.answer.close()


c = Jeopardy()
c.build()
print('\n\nDone.')
