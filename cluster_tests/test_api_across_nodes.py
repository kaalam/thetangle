from http_requests import get, put, delete


def test_AcrossNodesBasic():
	d = get('///Troppo//lmdb/test_dbi.new')
	assert d.status_code == 200

	n = put('///Troppo//lmdb/test_dbi/twenty', 'What is 5*4?')
	assert n.status_code == 201

	n = put('///Troppo//lmdb/test_dbi/five', 'What is 7 - 2?')
	assert n.status_code == 201

	a = get('///Troppo//lmdb/test_dbi/twenty')
	assert a.status_code == 200 and a.text == 'What is 5*4?'

	a = get('//lmdb/test_dbi/twenty', remote = True)
	assert a.status_code == 200 and a.text == 'What is 5*4?'

	a = get('//lmdb/test_dbi/five', remote = True)
	assert a.status_code == 200 and a.text == 'What is 7 - 2?'

	a = get('///Troppo//lmdb/test_dbi/five')
	assert a.status_code == 200 and a.text == 'What is 7 - 2?'

	d = delete('///Troppo//lmdb/test_dbi/twenty')
	assert d.status_code == 200

	d = delete('///Troppo//lmdb/test_dbi/zx81')
	assert d.status_code == 404

	d = delete('//zz/test_dbi/zx81')
	assert d.status_code == 503

	d = delete('//file&/tmp/aa/bb/cc;')
	assert d.status_code == 404

	a = get('//lmdb/test_dbi/twenty')
	assert a.status_code == 404

	a = get('//lmdb/test_dbi/twenty', remote = True)
	assert a.status_code == 404

	a = get('///Troppo//lmdb/test_dbi/twenty')
	assert a.status_code == 404

	a = get('///Troppo//lmdb/test_dbi/five')
	assert a.status_code == 200 and a.text == 'What is 7 - 2?'

	d = delete('///Troppo//lmdb/test_dbi')
	assert d.status_code == 200

	a = get('///Troppo//lmdb/test_dbi/twenty')
	assert a.status_code == 404

	a = get('///Troppo//lmdb/test_dbi/five')
	assert a.status_code == 404


def test_AcrossNodesAllRemoteRight():
	q = get('//deque/my_stack.new')
	assert q.status_code == 200

	q = get('///Troppo//deque/my_stack.new')
	assert q.status_code == 200

	tupl = '("weights" : [[17, 170], [112, 54], [207, 149]], "author" : ["Billy"], "score" : [0.95])'

	a = put('//lmdb/www/a_tupl.raw', tupl)
	assert a.status_code == 201

	a = get('//deque/my_stack/~last=//lmdb/www/a_tupl:weights')
	assert a.status_code == 200

	a = get('//deque/my_stack/~plast.text')
	assert a.status_code == 200 and a.text == '[[17, 170], [112, 54], [207, 149]]'

	a = get('//lmdb/www/a_tupl:author')
	assert a.status_code == 200 and a.text == 'Billy'

	a = get('//deque/my_stack/~last=//lmdb/www/a_tupl:score')
	assert a.status_code == 200

	a = get('//deque/my_stack/~plast.text')
	assert a.status_code == 200 and a.text == '[9.499999999999999556e-01]'

	a = get('///Troppo//lmdb/www/a_tupl=//lmdb/www/a_tupl')
	assert a.status_code == 200

	b = get('//lmdb/www/a_tupl')
	assert b.status_code == 200

	r = get('//lmdb/www/a_tupl', remote = True)
	assert r.status_code == 200 and b.text == r.text

	t = get('///Troppo//lmdb/www/a_tupl')
	assert t.status_code == 200 and b.text == t.text

	b = get('//lmdb/www/a_tupl:weights')
	assert b.status_code == 200

	r = get('//lmdb/www/a_tupl:weights', remote = True)
	assert r.status_code == 200 and b.text[0:7] == r.text[0:7] and len(b.content) == len(r.content)		# Bytes before .created

	r = get('///Troppo//lmdb/www/a_tupl:weights')
	assert r.status_code == 200 and b.text[0:7] == r.text[0:7] and len(b.content) == len(r.content)		# Bytes before .created

	a = get('//deque/my_stack/~last=//lmdb/www/a_tupl:weights', remote = True)
	assert a.status_code == 200

	a = get('//deque/my_stack/~plast.text', remote = True)
	assert a.status_code == 200 and a.text == '[[17, 170], [112, 54], [207, 149]]'

	a = get('//lmdb/www/a_tupl:author', remote = True)
	assert a.status_code == 200 and a.text == 'Billy'

	a = get('//deque/my_stack/~last=//lmdb/www/a_tupl:score', remote = True)
	assert a.status_code == 200

	a = get('//deque/my_stack/~plast.text', remote = True)
	assert a.status_code == 200 and a.text == '[9.499999999999999556e-01]'

	a = get('//deque/my_stack/~last=///Troppo//lmdb/www/a_tupl:weights')
	assert a.status_code == 200

	a = get('//deque/my_stack/~plast.text')
	assert a.status_code == 200 and a.text == '[[17, 170], [112, 54], [207, 149]]'

	a = get('///Troppo//lmdb/www/a_tupl:author')
	assert a.status_code == 200 and a.text == 'Billy'

	a = put('///Troppo//lmdb/www/a_tupl.raw', tupl)
	assert a.status_code == 201

	b = get('//lmdb/www/a_tupl')
	assert b.status_code == 200

	r = get('//lmdb/www/a_tupl', remote = True)
	assert r.status_code == 200 and b.text[0:7] == r.text[0:7] and len(b.content) == len(r.content)		# Bytes before .created

	t = get('///Troppo//lmdb/www/a_tupl')
	assert t.status_code == 200 and b.text[0:7] == t.text[0:7] and len(b.content) == len(t.content)		# Bytes before .created

	b = get('//lmdb/www/a_tupl:weights')
	assert b.status_code == 200

	r = get('//lmdb/www/a_tupl:weights', remote = True)
	assert r.status_code == 200 and b.text[0:7] == r.text[0:7] and len(b.content) == len(r.content)		# Bytes before .created

	r = get('///Troppo//lmdb/www/a_tupl:weights')
	assert r.status_code == 200 and b.text[0:7] == r.text[0:7] and len(b.content) == len(r.content)		# Bytes before .created

	a = get('//deque/my_stack/~last=//lmdb/www/a_tupl:weights', remote = True)
	assert a.status_code == 200

	a = get('//deque/my_stack/~plast.text', remote = True)
	assert a.status_code == 200 and a.text == '[[17, 170], [112, 54], [207, 149]]'

	a = get('//lmdb/www/a_tupl:author', remote = True)
	assert a.status_code == 200 and a.text == 'Billy'

	a = get('//deque/my_stack/~last=//lmdb/www/a_tupl:score', remote = True)
	assert a.status_code == 200

	a = get('//deque/my_stack/~plast.text', remote = True)
	assert a.status_code == 200 and a.text == '[9.499999999999999556e-01]'

	a = get('//deque/my_stack/~last=///Troppo//lmdb/www/a_tupl:weights')
	assert a.status_code == 200

	a = get('//deque/my_stack/~plast.text')
	assert a.status_code == 200 and a.text == '[[17, 170], [112, 54], [207, 149]]'

	a = get('///Troppo//lmdb/www/a_tupl:author')
	assert a.status_code == 200 and a.text == 'Billy'

	q = delete('//deque/my_stack')
	assert q.status_code == 200

	q = delete('///Troppo//deque/my_stack')
	assert q.status_code == 200


def test_AcrossNodesAllRemoteBoth():
	q = get('//deque/stack_01.new')
	assert q.status_code == 200

	q = get('///Troppo//deque/stack_02.new')
	assert q.status_code == 200

	a = put('///Troppo//deque/stack_02/tensor.raw', '[[1,1], [2,2], [3,3]]')
	assert a.status_code == 201

	a = put('//deque/stack_01/tt.raw', '[[1,4], [2,5], [3,6]]')
	assert a.status_code == 201

	a = put('//deque/stack_02/filter.raw', '[0,1]', remote = True)
	assert a.status_code == 201

	a = put('///Troppo//deque/stack_02/filter.raw', '[0,1]')
	assert a.status_code == 201

	a = put('//deque/stack_01/fi_fi.raw', '[1]')
	assert a.status_code == 201

	a = get('//deque/stack_01/tensor-src=///Troppo//deque/stack_02/tensor.text')
	assert a.status_code == 200

	a = get('//deque/stack_01/slice-1=///Troppo//deque/stack_02/tensor[//deque/stack_02/filter]')
	assert a.status_code == 200

	a = get('//deque/stack_01/slice-2=///Troppo//deque/stack_02/tensor[&[0]]')
	assert a.status_code == 200

	a = get('//deque/stack_01/slice-3=//deque/stack_01/tt[///Troppo//deque/stack_02/filter]')
	assert a.status_code == 400

	a = get('///Troppo//deque/stack_02/tensor[//deque/stack_01/fi_fi]')
	assert a.status_code == 404

	a = get('//deque/stack_02/tensor[//deque/stack_01/fi_fi]', remote = True)
	assert a.status_code == 404

	a = get('//deque/stack_01/slice-4=///Troppo//deque/stack_02/tensor[//deque/stack_01/fi_fi]')
	assert a.status_code == 400

	tp = get('///Troppo//bash/exec/(&echo "2 + 2 = $(expr 2 + 2)")')
	assert tp.status_code == 200

	a = put('//deque/stack_01/~last', tp.content)
	assert a.status_code == 201

	a = get('//deque/stack_01/~plast.text')
	assert a.status_code == 200

	a = get('///Troppo//deque/stack_02/result=//bash/exec/(&echo "2 + 2 = $(expr 2 + 2)")')
	assert a.status_code == 200

	a = get('///Troppo//deque/stack_02/result.text')
	assert a.status_code == 200 and a.text == '["2 + 2 = 4\\n"]'

	a = get('//deque/stack_01/result=///Troppo//bash/exec/(&echo "2 + 2 = $(expr 2 + 2)")')
	assert a.status_code == 200

	a = get('//deque/stack_01/result.text')
	assert a.status_code == 200

	a = get('///Troppo//deque/stack_02/result=///Troppo//bash/exec/(&echo "2 + 2 = $(expr 2 + 2)")')
	assert a.status_code == 200

	a = get('///Troppo//deque/stack_02/result.text')
	assert a.status_code == 200 and a.text == '["2 + 2 = 4\\n"]'

	a = get('//deque/stack_01/slice-1.text')
	assert a.status_code == 200 and a.text == '[[1, 1], [2, 2]]'

	a = get('//deque/stack_01/slice-2.text')
	assert a.status_code == 200 and a.text == '[[1, 1]]'

	a = get('//deque/stack_01/tensor-src')
	assert a.status_code == 200 and a.text == '[[1, 1], [2, 2], [3, 3]]'

	tp = get('//bash/exec/(&echo "2 + 2 = $(expr 2 + 2)")')
	assert tp.status_code == 200

	a = put('///Troppo//deque/stack_02/~first', tp.content)
	assert a.status_code == 201

	a = get('///Troppo//deque/stack_02/~pfirst.text')
	assert a.status_code == 200 and a.text == '["2 + 2 = 4\\n"]'

	tp = get('///Troppo//deque/stack_02/tensor[//deque/stack_02/filter]')
	assert tp.status_code == 200

	a = put('///Troppo//deque/stack_02/~first', tp.content)
	assert a.status_code == 201

	a = get('///Troppo//deque/stack_02/~pfirst.text')
	assert a.status_code == 200 and a.text == '[[1, 1], [2, 2]]'

	tp = get('///Troppo//deque/stack_02/tensor[&[1,2]]')
	assert tp.status_code == 200

	a = put('///Troppo//deque/stack_02/~first', tp.content)
	assert a.status_code == 201

	a = get('///Troppo//deque/stack_02/~pfirst.text')
	assert a.status_code == 200 and a.text == '[[2, 2], [3, 3]]'

	a = put('///Troppo//deque/stack_02/mat_2x2', '[[2, 2], [3, 3]]')
	assert a.status_code == 201

	tp = get('///Troppo//deque/stack_02/mat_2x2.raw')
	assert tp.status_code == 200

	a = put('///Troppo//deque/stack_02/~first', tp.content)
	assert a.status_code == 201

	a = get('///Troppo//deque/stack_02/~pfirst.text')
	assert a.status_code == 200 and a.text == '[[2, 2], [3, 3]]'

	a = get('//deque/stack_01/~last=///Troppo//deque/stack_02/mat_2x2.raw')
	assert tp.status_code == 200

	a = get('//deque/stack_01/~plast.text')
	assert a.status_code == 200 and a.text == '[[2, 2], [3, 3]]'

	a = get('//deque/stack_01/~last=///Troppo//deque/stack_02/mat_2x2(//bb/ee/kk)')
	assert a.status_code == 400

	a = get('///Troppo//deque/stack_02/mat_2x2(//bb/ee/kk)')
	assert a.status_code == 404

	a = get('//deque/stack_02/mat_2x2(//bb/ee/kk)', remote = True)
	assert a.status_code == 404

	a = get('//deque/stack_01/~last=///Troppo//deque/stack_02/tensor')
	assert tp.status_code == 200

	a = get('//deque/stack_01/~plast.text')
	assert a.status_code == 200 and a.text == '[[1, 1], [2, 2], [3, 3]]'

	a = get('//deque/stack_01/~last=///Troppo//http&http://127.0.0.1:5000/test/capital/Spain;')
	assert tp.status_code == 200

	a = get('//deque/stack_01/~plast.text')
	assert a.status_code == 200

	a = get('//deque/stack_01/tt-src=//deque/stack_01/tt.text')
	assert a.status_code == 200

	a = get('//deque/stack_01/tt-src')
	assert a.status_code == 200 and a.text == '[[1, 4], [2, 5], [3, 6]]'

	a = get('//deque/stack_01/tt-raw=//deque/stack_01/tt-src.raw')
	assert a.status_code == 200

	a = get('//deque/stack_01/tt-raw.text')
	assert a.status_code == 200 and a.text == '[[1, 4], [2, 5], [3, 6]]'

	q = delete('//deque/stack_01')
	assert q.status_code == 200

	q = delete('//deque/stack_02', remote = True)
	assert q.status_code == 200


# if __name__ == '__main__':
# 	test_AcrossNodesBasic()
# 	test_AcrossNodesAllRemoteRight()
# 	test_AcrossNodesAllRemoteBoth()

# 	print('\n\nDone.')
