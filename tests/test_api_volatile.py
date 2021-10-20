import pytest, requests

from http_requests import get, put, delete


def test_VolatileDeque():
	a = 1

	assert isinstance(a, int)

	with pytest.raises(ZeroDivisionError):
		b = a/0

	assert 3*a == 3


def test_VolatileIndex():
	a = 1

	assert isinstance(a, int)

	with pytest.raises(ZeroDivisionError):
		b = a/0

	assert 3*a == 3


def test_VolatileQueue():
	a = get('//queue/test_q/hello')
	assert isinstance(a, requests.models.Response)
	assert a.status_code == 404

	d = get('//queue/test_q/~10.new')
	assert d.status_code == 200

	n = put('//queue/test_q/twenty~.20', 'What is 5*4?')
	assert n.status_code == 201

	n = put('//queue/test_q/five~.05', 'What is 7 - 2?')
	assert n.status_code == 201

	n = put('//queue/test_q/twelve~0.12', 'What comes after 11?')
	assert n.status_code == 201

	a = get('//queue/test_q/twenty')
	assert a.status_code == 200 and a.text == 'What is 5*4?'

	a = get('//queue/test_q/~lowest')
	assert a.status_code == 200 and a.text == 'What is 7 - 2?'

	a = get('//queue/test_q/~xhigh')
	assert a.status_code == 200 and a.text == 'What is 5*4?'

	a = get('//queue/test_q/~xhigh')
	assert a.status_code == 200 and a.text == 'What comes after 11?'

	a = get('//queue/test_q/~xhigh')
	assert a.status_code == 200 and a.text == 'What is 7 - 2?'

	a = get('//queue/test_q/~xhigh')
	assert a.status_code == 404

	d = delete('//queue/test_q')
	assert d.status_code == 200

	a = get('//queue/test_q/five')
	assert a.status_code == 404


def test_VolatileTree():
	a = 1

	assert isinstance(a, int)

	with pytest.raises(ZeroDivisionError):
		b = a/0

	assert 3*a == 3


if __name__ == '__main__':
	test_VolatileDeque()
	test_VolatileIndex()
	test_VolatileQueue()
	test_VolatileTree()

	print('\n\nDone.')
