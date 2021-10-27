import pytest, requests

from http_requests import get, put, delete


def test_VolatileDeque():
	q = get('//deque/stack_01.new')
	assert q.status_code == 200

	q = get('//deque/stack_02.new')
	assert q.status_code == 200

	a = put('//deque/stack_02/tensor.raw', '[[1,1], [2,2], [3,3]]')
	assert a.status_code == 201

	a = put('//deque/stack_02/filter.raw', '[0,1]')
	assert a.status_code == 201

	a = get('//deque/stack_01/tensor-src=//deque/stack_02/tensor.text')
	assert a.status_code == 200

	a = get('//deque/stack_01/slice-1=//deque/stack_02/tensor[//deque/stack_02/filter]')
	assert a.status_code == 200

	a = get('//deque/stack_01/slice-2=//deque/stack_02/tensor[&[0]]')
	assert a.status_code == 200

	a = get('//deque/stack_02/result=//bash/exec/(&echo "2 + 2 = $(expr 2 + 2)")')
	assert a.status_code == 200

	a = get('//deque/stack_02/result.text')
	assert a.status_code == 200
	ii = eval(a.text)
	s = ''.join([chr(i) for i in ii])
	assert s[0:9] == '2 + 2 = 4'

	a = get('//deque/stack_01/slice-1.text')
	assert a.status_code == 200 and a.text == '[[1, 1], [2, 2]]'

	a = get('//deque/stack_01/slice-2.text')
	assert a.status_code == 200 and a.text == '[[1, 1]]'

	a = get('//deque/stack_01/tensor-src')
	assert a.status_code == 200 and a.text == '[[1, 1], [2, 2], [3, 3]]'

	tp = get('//bash/exec/(&echo "2 + 2 = $(expr 2 + 2)")')
	assert tp.status_code == 200

	a = put('//deque/stack_02/~first', tp.content)
	assert a.status_code == 201

	a = get('//deque/stack_02/~pfirst.text')
	assert a.status_code == 200
	ii = eval(a.text)
	s = ''.join([chr(i) for i in ii])
	assert s[0:9] == '2 + 2 = 4'

	tp = get('//deque/stack_02/tensor[//deque/stack_02/filter]')
	assert tp.status_code == 200

	a = put('//deque/stack_02/~first', tp.content)
	assert a.status_code == 201

	a = get('//deque/stack_02/~pfirst.text')
	assert a.status_code == 200 and a.text == '[[1, 1], [2, 2]]'

	tp = get('//deque/stack_02/tensor[&[1,2]]')
	assert tp.status_code == 200

	a = put('//deque/stack_02/~first', tp.content)
	assert a.status_code == 201

	a = get('//deque/stack_02/~pfirst.text')
	assert a.status_code == 200 and a.text == '[[2, 2], [3, 3]]'

	a = put('//deque/stack_02/mat_2x2', '[[2, 2], [3, 3]]')
	assert a.status_code == 201

	tp = get('//deque/stack_02/mat_2x2.raw')
	assert tp.status_code == 200

	a = put('//deque/stack_02/~first', tp.content)
	assert a.status_code == 201

	a = get('//deque/stack_02/~pfirst.text')
	assert a.status_code == 200 and a.text == '[[2, 2], [3, 3]]'

	q = delete('//deque/stack_01')
	assert q.status_code == 200

	q = delete('//deque/stack_02')
	assert q.status_code == 200



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
