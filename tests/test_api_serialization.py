import pytest, requests

from http_requests import get, put, delete


def test_Serialization():

	a = get('//lmdb/test_serial/hello')
	assert isinstance(a, requests.models.Response)
	assert a.status_code == 404

	d = get('//lmdb/test_serial.new')
	assert d.status_code == 200

	src_kind = '{"palette":BYTE[10,height],"time":TIME[3],"author":STRING[40],"filter":SINGLE[height,height,3]}'
	src_tupl = '("weights":[[17,170],[112,54],[207,149]],"author":["Billy"],"score":[0.95])'
	src_tens = '[[10,170,99],[11,54,999],[12,149,9999],[13,36,9999],[14,149,999],[15,44,99]]'

	a = get('//lmdb/test_serial/kind=&%s;' % src_kind)
	assert a.status_code == 200

	a = get('//lmdb/test_serial/kind')
	assert a.status_code == 200 and len(a.content) > 64

	a = get('//lmdb/test_serial/tupl=&%s;' % src_tupl)
	assert a.status_code == 200

	a = get('//lmdb/test_serial/tupl')
	assert a.status_code == 200 and len(a.content) > 64

	a = get('//lmdb/test_serial/tens=&%s;' % src_tens)
	assert a.status_code == 200

	a = get('//lmdb/test_serial/tens')
	assert a.status_code == 200 and len(a.content) > 64

	a = get('//lmdb/test_serial/s_kind=//lmdb/test_serial/kind.text')
	assert a.status_code == 200

	a = get('//lmdb/test_serial/s_tupl=//lmdb/test_serial/tupl.text')
	assert a.status_code == 200

	a = get('//lmdb/test_serial/s_tens=//lmdb/test_serial/tens.text')
	assert a.status_code == 200

	ret_kind = '{"palette" : BYTE[10, height], "time" : TIME[3], "author" : STRING[40], "filter" : SINGLE[height, height, 3]}'
	ret_tupl = '("weights" : [[17, 170], [112, 54], [207, 149]], "author" : ["Billy"], "score" : [9.499999999999999556e-01])'
	ret_tens = '[[10, 170, 99], [11, 54, 999], [12, 149, 9999], [13, 36, 9999], [14, 149, 999], [15, 44, 99]]'
	ret_sli1 = '[[13, 36, 9999], [15, 44, 99]]'
	ret_sli2 = '[[11, 54, 999], [12, 149, 9999], [15, 44, 99]]'

	a = get('//lmdb/test_serial/kind.text')
	assert a.status_code == 200 and a.text[:-1] == ret_kind

	a = get('//lmdb/test_serial/s_kind')
	assert a.status_code == 200 and a.text[:-1] == ret_kind

	a = get('//lmdb/test_serial/tupl.text')
	assert a.status_code == 200 and a.text[:-1] == ret_tupl

	a = get('//lmdb/test_serial/s_tupl')
	assert a.status_code == 200 and a.text[:-1] == ret_tupl

	a = get('//lmdb/test_serial/tens.text')
	assert a.status_code == 200 and a.text[:-1] == ret_tens

	a = get('//lmdb/test_serial/s_tens')
	assert a.status_code == 200 and a.text[:-1] == ret_tens

	p = put('//lmdb/test_serial/slice.raw', ret_sli2)
	assert p.status_code == 201

	a = get('//lmdb/test_serial/slice.text')
	assert a.status_code == 200 and a.text[:-1] == ret_sli2

	a = get('//lmdb/test_serial/tupl')
	assert a.status_code == 200 and len(a.content) > 64

	p = put('//lmdb/test_serial/tup_src.text', a.content)
	assert p.status_code == 201

	a = get('//lmdb/test_serial/tup_src')
	assert a.status_code == 200 and a.text[0] == '[' and a.text[-2] == ']'

	q = get('//deque/my_stack.new')
	assert q.status_code == 200

	a = get('//deque/my_stack/~last=//lmdb/test_serial/tens[&[3,5]]')
	assert a.status_code == 200

	a = get('//deque/my_stack/~plast.text')
	assert a.status_code == 200 and a.text[:-1] == ret_sli1

	q = delete('//deque/my_stack')
	assert q.status_code == 200

	a = get('//lmdb/test_serial/slic=//lmdb/test_serial/tens[&[1,2,5]]')
	assert a.status_code == 200

	a = get('//lmdb/test_serial/slic.text')
	assert a.status_code == 200 and a.text[:-1] == ret_sli2

	d = delete('//lmdb/test_serial')
	assert d.status_code == 200

	a = get('//lmdb/test_serial/twenty')
	assert a.status_code == 404


if __name__ == '__main__':
	test_Serialization()

	print('\n\nDone.')
