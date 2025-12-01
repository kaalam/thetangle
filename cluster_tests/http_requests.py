import re

import requests as http

SERVER_URL = 'http://192.168.1.50:8899'
REMOTE_URL = 'http://192.168.1.19:8899'


def get(qq, remote = False):
	if remote:
		return http.get(REMOTE_URL + qq)

	return http.get(SERVER_URL + qq)


def put(qq, string, remote = False):
	if remote:
		return http.put(REMOTE_URL + qq, string)

	return http.put(SERVER_URL + qq, string)


def delete(qq, remote = False):
	if remote:
		return http.delete(REMOTE_URL + qq)

	return http.delete(SERVER_URL + qq)


def options(qq):
	return http.options(SERVER_URL + qq)


def head(qq):
	return http.head(SERVER_URL + qq)


def post(qq, tt):
	return http.post(SERVER_URL + qq, data = tt)


def patch_broken_requests():
	import requests.adapters
	fn = requests.adapters.__file__

	with open(fn, 'r') as f:
		txt = f.read().splitlines()

	rex_st = re.compile('^[ ]+url = request.path_url$')
	rex_end = re.compile('^[ ]+return url$')

	found	 = 0
	lines	 = 0
	patch	 = False
	modified = False
	for i, s in enumerate(txt):
		if rex_st.match(s):
			assert found == 0
			found += 1
			patch = True
			continue

		if patch:
			assert lines < 7
			lines += 1

			if rex_end.match(s):
				patch = False
				continue

			if not s.startswith('#'):
				txt[i] = '# %s' % s
				modified = True

	assert found == 1

	if modified:
		with open(fn, 'w') as f:
			f.write('\n'.join(txt))


patch_broken_requests()
