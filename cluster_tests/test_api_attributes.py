import pytest, requests

from http_requests import get, put, delete


def test_PutStaticAttributes():
#define BLOCK_ATTRIB_MIMETYPE	4			///< The mime type (can also be some proprietary file spec. E.g., "Adobe PhotoShop Image")
#define BLOCK_ATTRIB_URL		5			///< A url for the server to expose the file by.
#define BLOCK_ATTRIB_LANGUAGE	6			///< An http language identifier that will be returned in an API GET call.

	p = get('/hello/index.html')
	assert p.status_code == 404 or p.status_code == 502

	n = get('//lmdb/www/blk_blk123=&<html>\n<body>\n<h3>\nHello World!\n</h3>\n</body>\n</html>\n;')
	assert n.status_code == 200

	a = get('//lmdb/www/blk_blk123')
	assert a.status_code == 200 and a.text == '<html>\n<body>\n<h3>\nHello World!\n</h3>\n</body>\n</html>\n'

	a = get('//lmdb/www/blk_blk123.attribute(4)')
	assert a.status_code == 404

	a = get('//lmdb/www/blk_blk123.attribute(4)=&text/html;')
	assert a.status_code == 200

	a = get('//lmdb/www/blk_blk123.attribute(4)')
	assert a.status_code == 200 and a.text == 'text/html'

	a = get('//lmdb/www/blk_blk123.attribute(6)=&en-us;')
	assert a.status_code == 200

	a = get('//lmdb/www/blk_blk123.attribute(6)')
	assert a.status_code == 200 and a.text == 'en-us'

	a = get('//lmdb/www/blk_blk123.attribute(5)=&/hello/index.html;')
	assert a.status_code == 200

	a = get('//lmdb/www/blk_blk123.attribute(5)')
	assert a.status_code == 200 and a.text == '/hello/index.html'

	p = get('/hello/index.html')
	assert p.status_code == 200 and p.text == '<html>\n<body>\n<h3>\nHello World!\n</h3>\n</body>\n</html>\n'

	a = delete('//lmdb/www/blk_blk123')
	assert a.status_code == 200

	p = get('/hello/index.html')
	assert p.status_code == 502


def test_PutGetRemoteAttributes():
	p = get('/hello/index.html', remote = True)
	assert p.status_code == 404 or p.status_code == 502

	n = get('///424x4//lmdb/www/blk_blk123=&<html>\n<body>\n<h3>\nHello World!\n</h3>\n</body>\n</html>\n;')
	assert n.status_code == 200

	a = get('///424x4//lmdb/www/blk_blk123')
	assert a.status_code == 200 and a.text[0:6] == '<html>'

	a = get('///424x4//lmdb/www/blk_blk123.attribute(4)')
	assert a.status_code == 404

	a = get('///424x4//lmdb/www/blk_blk123.attribute(4)=&text/html;')
	assert a.status_code == 200

	a = get('///424x4//lmdb/www/blk_blk123.attribute(4)')
	assert a.status_code == 200 and a.text == 'text/html'

	a = get('///424x4//lmdb/www/blk_blk123.attribute(6)=&en-us;')
	assert a.status_code == 200

	a = get('///424x4//lmdb/www/blk_blk123.attribute(6)')
	assert a.status_code == 200 and a.text == 'en-us'

	a = get('///424x4//lmdb/www/blk_blk123.attribute(5)=&/hello/index.html;')
	assert a.status_code == 200

	a = get('///424x4//lmdb/www/blk_blk123.attribute(5)')
	assert a.status_code == 200 and a.text == '/hello/index.html'

	p = get('/hello/index.html', remote = True)
	assert p.status_code == 200 and p.text[0:6] == '<html>'

	a = delete('///424x4//lmdb/www/blk_blk123')
	assert a.status_code == 200

	p = get('/hello/index.html', remote = True)
	assert p.status_code == 502


# if __name__ == '__main__':
# 	test_PutStaticAttributes()
# 	test_PutGetRemoteAttributes()

# 	print('\n\nDone.')
