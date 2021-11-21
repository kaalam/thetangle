import json
from os import replace
import re


def clean(s):
	while s.find('  ') >=0: s = s.replace('  ', ' ')
	while s.find(' ,') >=0: s = s.replace(' ,', ',')
	while s.find(' .') >=0: s = s.replace(' .', '.')
	return s.strip()


class SQUAD20:

	def __init__(self, source_fn = '/home/jadmin/kaalam.etc/nlp/corpora/SQuAD/train-v2.0.json', out_path  = './'):
		self.source_fn = source_fn
		self.out_contexts  = out_path + 'squad20/context.txt'
		self.out_qa_index  = out_path + 'squad20/qa_index.txt'
		self.out_questions = out_path + 'squad20/question.txt'
		self.out_answers   = out_path + 'squad20/answer.txt'


	def inputs(self):
		return [self.source_fn]


	def outputs(self):
		return [self.out_contexts, self.out_qa_index, self.out_questions, self.out_answers]


	def build(self):
		f_in = open(self.source_fn, 'r')
		f_ct = open(self.out_contexts, 'w')
		f_ii = open(self.out_qa_index, 'w')
		f_qq = open(self.out_questions, 'w')
		f_aa = open(self.out_answers, 'w')

		rex_cl = re.compile('[^a-z0-9\'\\-,\\.\\? ]')

		obj = json.load(f_in)

		ctx_row = 1
		for item in obj['data']:
			for row in item['paragraphs']:
				ctx = clean(rex_cl.sub(' ', row['context'].lower()))
				f_ct.write(ctx + '\n')

				for qa in row['qas']:
					qq = clean(rex_cl.sub(' ', qa['question'].lower()))
					f_qq.write(qq + '\n')
					f_ii.write(str(ctx_row) + '\n')
					if qa['is_impossible']:
						f_aa.write('\n')
					else:
						aa = clean(rex_cl.sub(' ', qa['answers'][0]['text'].lower()))
						f_aa.write(aa + '\n')

				ctx_row += 1

		f_in.close()
		f_ct.close()
		f_ii.close()
		f_qq.close()
		f_aa.close()


c = SQUAD20()
c.build()
print('\n\nDone.')