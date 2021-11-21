import re


class OpenSubtitles:

	def __init__(self, source_fn = '/home/jadmin/kaalam.etc/nlp/corpora/open_sub/monolingual.raw.en', out_path  = './'):
		self.source_fn = source_fn
		self.text	   = out_path + 'open_subtitles/blocks.txt'


	def inputs(self):
		return [self.source_fn]


	def outputs(self):
		return [self.text]


	def build(self):
		f_in = open(self.source_fn, 'r')
		f_oo = open(self.text, 'w')

		rex_cl = re.compile('(:|\\(|]|^[^a-zA-Z]|^Presented|^Produced|^In association)')
		rex_md = re.compile('.*[aeiou].*')

		lines = set()

		t_zz = t_rl = 0

		line = f_in.readline()
		while line is not None:
			t_rl += 1
			if t_rl % 100000 == 0:
				print('%0.1f/%0.1fM,' % (len(lines)/1000000, t_rl/1000000), end = ' ', flush = True)

			if len(line) == 0:
				t_zz += 1
				if t_zz == 1000:
					break
			else:
				t_zz = 0

				if (not rex_cl.match(line)) and (rex_md.match(line)):
					line = line.strip()
					lines.add(line)

			line = f_in.readline()

		wl = list(lines)
		wl.sort()
		f_oo.write('\n'.join(wl))

		f_in.close()
		f_oo.close()


c = OpenSubtitles()
c.build()
print('\n\nDone.')