from http_requests import get, put, delete

import requests								# Must be imported after possibly patching it by http_requests.


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
	q = get('//deque/stack.new')
	assert q.status_code == 200

	q = get('//index/index01.new')
	assert q.status_code == 200

	a = put('//index/index01/planet', 'A celestial body distinguished from the fixed stars by having an apparent motion of its own.')
	assert a.status_code == 201

	a = put('//index/index01/country', 'A nation with its own government, occupying a particular territory.')
	assert a.status_code == 201

	a = put('//index/index01/dog', 'A domesticated carnivorous mammal that typically has a long snout, an acute sense ...')
	assert a.status_code == 201

	a = get('//index/index01/country')
	assert a.status_code == 200 and a.text == 'A nation with its own government, occupying a particular territory.'

	a = get('//deque/stack/~last=//index/index01/~get')
	assert a.status_code == 200

	a = get('//deque/stack/~plast.text')
	assert a.status_code == 200 and a.text[:11] == '("key" : ["' and a.text[-3:] == '"])'

	a = put('//deque/stack/tupl.raw', a.text)
	assert a.status_code == 201

	q = get('//index/index02.new')
	assert q.status_code == 200

	q = get('//index/index02/~put=//deque/stack/tupl')
	assert q.status_code == 200

	a = get('//index/index02/dog')
	assert a.status_code == 200 and a.text == 'A domesticated carnivorous mammal that typically has a long snout, an acute sense ...'

	a = get('//index/index02/planet')
	assert a.status_code == 200 and a.text == 'A celestial body distinguished from the fixed stars by having an apparent motion of its own.'

	q = delete('//index/index01')
	assert q.status_code == 200

	q = delete('//index/index02')
	assert q.status_code == 200

	q = delete('//deque/stack')
	assert q.status_code == 200


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
	q = get('//tree/game.new')
	assert q.status_code == 200

	a = put('//tree/game/root', '{}')
	assert a.status_code == 201

	a = put('//tree/game/l1_3~root', '{3}')
	assert a.status_code == 201

	a = put('//tree/game/l1_2~root', '{2}')
	assert a.status_code == 201

	a = put('//tree/game/l1_1~root', '{1}')
	assert a.status_code == 201

	a = put('//tree/game/l2_3b~l1_3', '{3,b}')
	assert a.status_code == 201

	a = put('//tree/game/l2_3a~l1_3', '{3,a}')
	assert a.status_code == 201

	a = put('//tree/game/l2_1a~l1_1', '{1,a}')
	assert a.status_code == 201

	a = put('//tree/game/final~l2_3b', '{...}')
	assert a.status_code == 201

	a = get('//tree/game/~first')
	assert a.status_code == 200 and a.text == '{}'

	a = get('//tree/game/l2_3a~next')
	assert a.status_code == 200 and a.text == '{3,b}'

	a = get('//tree/game/l2_3b~next')
	assert a.status_code == 404

	a = get('//tree/game/l2_3b~child')
	assert a.status_code == 200 and a.text == '{...}'

	a = get('//tree/game/l2_1a~parent')
	assert a.status_code == 200 and a.text == '{1}'

	q = delete('//tree/game')
	assert q.status_code == 200


# if __name__ == '__main__':
# 	test_VolatileDeque()
# 	test_VolatileIndex()
# 	test_VolatileQueue()
# 	test_VolatileTree()

# 	print('\n\nDone.')
