import json, re

from file_paths import etl_source, etl_dest
from Section import Section


class SQUAD20:

	def __init__(self, source_fn = etl_source + '/SQuAD/train-v2.0.json', out_path = etl_dest):
		self.source_fn = source_fn
		self.context   = Section('squad20', 'context', out_path + '/squad20')
		self.qa_index  = Section('squad20', 'qa-index', out_path + '/squad20')
		self.question  = Section('squad20', 'question', out_path + '/squad20')
		self.answer	   = Section('squad20', 'answer', out_path + '/squad20')


	def inputs(self):
		return [self.source_fn]


	def outputs(self):
		return [self.out_contexts, self.out_qa_index, self.out_questions, self.out_answers]


	def build(self):
		f_in = open(self.source_fn, 'r')

		obj = json.load(f_in)

		ctx_row = 1
		for item in obj['data']:
			for row in item['paragraphs']:
				self.context.write_line(row['context'])

				for qa in row['qas']:
					self.question.write_line(qa['question'])
					self.qa_index.write_line(str(ctx_row))

					if qa['is_impossible']:
						self.answer.write_line('(IMPOSSIBLE)')
					else:
						self.answer.write_line(qa['answers'][0]['text'])

				ctx_row += 1

		f_in.close()
		self.context.close()
		self.qa_index.close()
		self.question.close()
		self.answer.close()


c = SQUAD20()
c.build()
print('\n\nDone.')
