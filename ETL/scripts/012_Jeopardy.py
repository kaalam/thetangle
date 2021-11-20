import re


def clean(s):
	while s.find('  ') >=0: s = s.replace('  ', ' ')
	while s.find(' ,') >=0: s = s.replace(' ,', ',')
	while s.find(' .') >=0: s = s.replace(' .', '.')
	return s.strip()


class Jeopardy:

	def __init__(self, in_path = '/home/jadmin/kaalam.etc/nlp/corpora/jeopardy/', out_path  = './'):
		self.in_category  = in_path	 + 'category.txt'
		self.in_question  = in_path	 + 'question.txt'
		self.in_answer	  = in_path	 + 'answer.txt'
		self.out_category = out_path + 'jeopardy/category.txt'
		self.out_question = out_path + 'jeopardy/question.txt'
		self.out_answer	  = out_path + 'jeopardy/answer.txt'


	def inputs(self):
		return [self.in_category, self.in_question, self.in_answer]


	def outputs(self):
		return [self.out_category, self.out_question, self.out_answer]


	def build(self):
		f_ic = open(self.in_category, 'r')
		f_iq = open(self.in_question, 'r')
		f_ia = open(self.in_answer, 'r')
		f_oc = open(self.out_category, 'w')
		f_oq = open(self.out_question, 'w')
		f_oa = open(self.out_answer, 'w')

		rex_cl = re.compile('[^a-z0-9\'\\-,\\.\\? ]')

		t_ll = 0

		ct = f_ic.readline()
		qq = f_iq.readline()
		aa = f_ia.readline()

		assert ((ct == '') == (qq == '') and (ct == '') == (aa == ''))

		while ct != '':
			t_ll += 1
			if t_ll % 10000 == 0:
				print('%0.2fM,' % (t_ll/1000000), end = ' ', flush = True)

			f_oc.write(clean(rex_cl.sub(' ', ct.lower())) + '\n')
			f_oq.write(clean(rex_cl.sub(' ', qq.lower())) + '\n')
			f_oa.write(clean(rex_cl.sub(' ', aa.lower())) + '\n')

			ct = f_ic.readline()
			qq = f_iq.readline()
			aa = f_ia.readline()

			assert ((ct == '') == (qq == '') and (ct == '') == (aa == ''))

		f_ic.close()
		f_iq.close()
		f_ia.close()
		f_oc.close()
		f_oq.close()
		f_oa.close()


c = Jeopardy()
c.build()
print('\n\nDone.')