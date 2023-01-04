# The Tangle: An entangled collection of English text for Jazz

# 	Jazz (c) 2021-2023 kaalam.ai (The Authors of Jazz)

# 		Code is licensed under the Apache License, Version 2.0 http://www.apache.org/licenses/LICENSE-2.0
#		Data is open source (see LICENSE_* files in kaalam/tng-data-* repositories for details.)


from file_paths import etl_source, etl_dest
from Section import Section


class Jeopardy:

	def __init__(self, in_path = etl_source + '/jeopardy', out_path = etl_dest):
		self.in_category  = in_path	 + '/category.txt'
		self.in_question  = in_path	 + '/question.txt'
		self.in_answer	  = in_path	 + '/answer.txt'

		self.category = Section('jeopardy', 'category', out_path + '/jeopardy')
		self.question = Section('jeopardy', 'question', out_path + '/jeopardy')
		self.answer	  = Section('jeopardy', 'answer',	out_path + '/jeopardy')


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
