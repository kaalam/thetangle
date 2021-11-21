import pytest, requests

from http_requests import get, put, delete


def test_PersistedLmdb():

	a = get('//lmdb/test_dbi/hello')
	assert isinstance(a, requests.models.Response)
	assert a.status_code == 404

	d = get('//lmdb/test_dbi.new')
	assert d.status_code == 200

	n = put('//lmdb/test_dbi/twenty', 'What is 5*4?')
	assert n.status_code == 201

	n = put('//lmdb/test_dbi/five', 'What is 7 - 2?')
	assert n.status_code == 201

	a = get('//lmdb/test_dbi/twenty')
	assert a.status_code == 200 and a.text == 'What is 5*4?'

	a = get('//lmdb/test_dbi/five')
	assert a.status_code == 200 and a.text == 'What is 7 - 2?'

	d = delete('//lmdb/test_dbi/twenty')
	assert d.status_code == 200

	a = get('//lmdb/test_dbi/twenty')
	assert a.status_code == 404

	a = get('//lmdb/test_dbi/five')
	assert a.status_code == 200 and a.text == 'What is 7 - 2?'

	d = delete('//lmdb/test_dbi')
	assert d.status_code == 200

	a = get('//lmdb/test_dbi/twenty')
	assert a.status_code == 404

	a = get('//lmdb/test_dbi/five')
	assert a.status_code == 404


# if __name__ == '__main__':
# 	test_PersistedLmdb()

# 	print('\n\nDone.')
