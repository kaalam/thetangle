import pytest, requests

from http_requests import get, put, delete, options, head, post


def test_OtherHttp():
	a = options('///')
	assert isinstance(a, requests.models.Response)
	assert a.status_code == 204 and a.headers['Allow'] == 'HEAD,GET,OPTIONS'

	a = options('//base_s/entity2/key[&[2,4,6]]')
	assert a.status_code == 204 and a.headers['Allow'] == 'HEAD,GET,OPTIONS'

	a = options('//base/entity/key')
	assert a.status_code == 204 and a.headers['Allow'] == 'HEAD,GET,PUT,DELETE,OPTIONS'

	a = options('//base/entity')
	assert a.status_code == 204 and a.headers['Allow'] == 'DELETE,OPTIONS'

	a = options('///nX//base/entity/key.text')
	assert a.status_code == 204 and a.headers['Allow'] == 'HEAD,GET,PUT,OPTIONS'

	a = options('/__AUTOLOAD__.md')
	assert a.status_code == 204 and a.headers['Allow'] == 'HEAD,GET,OPTIONS'

	a = options('/qwuhckies.html')
	assert a.status_code == 204 and a.headers['Allow'] == 'OPTIONS'

	a = head('///')
	assert isinstance(a, requests.models.Response)
	assert a.status_code == 200 and a.text == ''

	with pytest.raises(requests.exceptions.ConnectionError):
		post('//aa/bb/cc', {'aaa' : 'xxx'})

	with pytest.raises(requests.exceptions.ConnectionError):
		put('/__AUTOLOAD__.md', '123')

	a = put('//ba se/ent/ky', '123')
	assert a.status_code == 400

	a = get('//ba se/ent/ky')
	assert a.status_code == 400

	a = delete('//ba se/ent/ky')
	assert a.status_code == 400

	ss = str([x for x in range(1000000)])

	a = put('//lmdb/www/tmp~ky-7521', ss)
	assert a.status_code == 201

	a = get('//lmdb/www/tmp~ky-7521')
	assert a.status_code == 200 and a.text == ss

	a = delete('//lmdb/www/tmp~ky-7521')
	assert a.status_code == 200

	with pytest.raises(requests.exceptions.ConnectionError):
		put('//lmdb/tmp~ent-7521/kk', '123')

	with pytest.raises(requests.exceptions.ConnectionError):
		put('//zz/ent/kk', '123')

	with pytest.raises(requests.exceptions.ConnectionError):
		put('///as23-94ph//zz/ent/kk', '123')


# if __name__ == '__main__':
# 	test_OtherHttp()

# 	print('\n\nDone.')
