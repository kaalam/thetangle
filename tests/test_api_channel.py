import pytest, requests

from http_requests import get, put, delete


def test_ChannelZmq():
	q = get('//deque/my_stack.new')
	assert q.status_code == 200

	a = put('//0-mq&pipeline/alpha;', 'tcp://localhost:5555')
	assert a.status_code == 201

	a = get('//0-mq&pipeline/alpha;')
	assert a.status_code == 200 and a.text == 'tcp://localhost:5555'

	a = get('//deque/my_stack/~last=//0-mq/alpha/(&a b c & Z P T - 456 = .)')
	assert a.status_code == 200

	a = get('//deque/my_stack/~plast.text')
	assert a.status_code == 200
	ii = eval(a.text)
	s = ''.join([chr(i) for i in ii])
	assert s[0:9] == 'abcZPT456'

	a = delete('//0-mq&pipeline/alpha;')
	assert a.status_code == 200

	q = delete('//deque/my_stack')
	assert q.status_code == 200


def test_ChannelBash():
	a = get('//bash/exec/(&echo "2 + 2 = $(expr 2 + 2)")')
	assert isinstance(a, requests.models.Response)
	assert a.status_code == 200

	q = get('//deque/my_stack.new')
	assert q.status_code == 200

	a = get('//deque/my_stack/~last=//bash/exec/(&echo "2 + 2 = $(expr 2 + 2)")')
	assert a.status_code == 200

	a = get('//deque/my_stack/~plast.text')
	assert a.status_code == 200
	ii = eval(a.text)
	s = ''.join([chr(i) for i in ii])
	assert s[0:9] == '2 + 2 = 4'

	q = delete('//deque/my_stack')
	assert q.status_code == 200


def test_ChannelFile():
	a = get('//file&/tmp/new_folder;.new')
	assert isinstance(a, requests.models.Response)
	assert a.status_code == 200

	n = put('//file&/tmp/new_folder/file.txt;', 'This is\nmultiline.')
	assert n.status_code == 201

	a = delete('//file&/tmp/new_folder/file.txt;')
	assert isinstance(a, requests.models.Response)
	assert a.status_code == 200

	a = delete('//file&/tmp/new_folder;')
	assert isinstance(a, requests.models.Response)
	assert a.status_code == 200


def test_ChannelHttp():
	a = 1

	assert isinstance(a, int)

	with pytest.raises(ZeroDivisionError):
		b = a/0

	assert 3*a == 3


if __name__ == '__main__':
	test_ChannelBash()
	test_ChannelZmq()
	test_ChannelFile()
	test_ChannelHttp()

	print('\n\nDone.')
