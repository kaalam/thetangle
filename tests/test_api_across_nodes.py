import pytest, requests

from http_requests import get, put, delete


def test_AcrossNodes():
	d = get('///424x4//lmdb/test_dbi.new')
	assert d.status_code == 200

	n = put('///424x4//lmdb/test_dbi/twenty', 'What is 5*4?')
	assert n.status_code == 201

	n = put('///424x4//lmdb/test_dbi/five', 'What is 7 - 2?')
	assert n.status_code == 201

	a = get('///424x4//lmdb/test_dbi/twenty')
	assert a.status_code == 200 and a.text == 'What is 5*4?'

	a = get('//lmdb/test_dbi/twenty', remote = True)
	assert a.status_code == 200

	a = get('//lmdb/test_dbi/five', remote = True)
	assert a.status_code == 200

	a = get('///424x4//lmdb/test_dbi/five')
	assert a.status_code == 200 and a.text == 'What is 7 - 2?'

	d = delete('///424x4//lmdb/test_dbi/twenty')
	assert d.status_code == 200

	d = delete('///424x4//lmdb/test_dbi/zx81')
	assert d.status_code == 404

	d = delete('//zz/test_dbi/zx81')
	assert d.status_code == 503

	d = delete('//file&/tmp/aa/bb/cc;')
	assert d.status_code == 404

	a = get('//lmdb/test_dbi/twenty')
	assert a.status_code == 404

	a = get('//lmdb/test_dbi/twenty', remote = True)
	assert a.status_code == 404

	a = get('///424x4//lmdb/test_dbi/twenty')
	assert a.status_code == 404

	a = get('///424x4//lmdb/test_dbi/five')
	assert a.status_code == 200 and a.text == 'What is 7 - 2?'

	d = delete('///424x4//lmdb/test_dbi')
	assert d.status_code == 200

	a = get('///424x4//lmdb/test_dbi/twenty')
	assert a.status_code == 404

	a = get('///424x4//lmdb/test_dbi/five')
	assert a.status_code == 404


if __name__ == '__main__':
	test_AcrossNodes()

	print('\n\nDone.')
