import pytest, requests

from http_requests import get, put, delete


def test_ChannelZmq():
	a = 1

	assert isinstance(a, int)

	with pytest.raises(ZeroDivisionError):
		b = a/0

	assert 3*a == 3


def test_ChannelBash():
	a = get('//bash/exec/(&ls -la)')
	assert isinstance(a, requests.models.Response)
	assert a.status_code == 200


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


# test_ChannelBash()
# test_ChannelZmq()
# test_ChannelFile()
# test_ChannelHttp()
