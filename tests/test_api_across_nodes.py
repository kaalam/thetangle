import pytest, requests

from http_requests import get, put, delete


def test_AcrossNodesBasic():
	d = get('///424x4//lmdb/test_dbi.new')
	assert d.status_code == 200

	n = put('///424x4//lmdb/test_dbi/twenty', 'What is 5*4?')
	assert n.status_code == 201

	n = put('///424x4//lmdb/test_dbi/five', 'What is 7 - 2?')
	assert n.status_code == 201

	a = get('///424x4//lmdb/test_dbi/twenty')
	assert a.status_code == 200 and a.text == 'What is 5*4?'

	a = get('//lmdb/test_dbi/twenty', remote = True)
	assert a.status_code == 200 and a.text == 'What is 5*4?'

	a = get('//lmdb/test_dbi/five', remote = True)
	assert a.status_code == 200 and a.text == 'What is 7 - 2?'

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


def test_AcrossNodesAllRemoteRight():

	q = get('//deque/my_stack.new')
	assert q.status_code == 200

	q = get('///424x4//deque/my_stack.new')
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

	a = get('///424x4//lmdb/www/a_tupl=//lmdb/www/a_tupl')
	assert a.status_code == 200

	b = get('//lmdb/www/a_tupl')
	assert b.status_code == 200

	r = get('//lmdb/www/a_tupl', remote = True)
	assert r.status_code == 200 and b.text == r.text

	t = get('///424x4//lmdb/www/a_tupl')
	assert t.status_code == 200 and b.text == t.text

	b = get('//lmdb/www/a_tupl:weights')
	assert b.status_code == 200

	r = get('//lmdb/www/a_tupl:weights', remote = True)
	assert r.status_code == 200 and b.text[0:7] == r.text[0:7] and len(b.content) == len(r.content)		# Bytes before .created

	r = get('///424x4//lmdb/www/a_tupl:weights')
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

	a = get('//deque/my_stack/~last=///424x4//lmdb/www/a_tupl:weights')
	assert a.status_code == 200

	a = get('//deque/my_stack/~plast.text')
	assert a.status_code == 200 and a.text == '[[17, 170], [112, 54], [207, 149]]'

	a = get('///424x4//lmdb/www/a_tupl:author')
	assert a.status_code == 200 and a.text == 'Billy'

	a = put('///424x4//lmdb/www/a_tupl.raw', tupl)
	assert a.status_code == 201

	b = get('//lmdb/www/a_tupl')
	assert b.status_code == 200

	r = get('//lmdb/www/a_tupl', remote = True)
	assert r.status_code == 200 and b.text[0:7] == r.text[0:7] and len(b.content) == len(r.content)		# Bytes before .created

	t = get('///424x4//lmdb/www/a_tupl')
	assert t.status_code == 200 and b.text[0:7] == t.text[0:7] and len(b.content) == len(t.content)		# Bytes before .created

	b = get('//lmdb/www/a_tupl:weights')
	assert b.status_code == 200

	r = get('//lmdb/www/a_tupl:weights', remote = True)
	assert r.status_code == 200 and b.text[0:7] == r.text[0:7] and len(b.content) == len(r.content)		# Bytes before .created

	r = get('///424x4//lmdb/www/a_tupl:weights')
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

	a = get('//deque/my_stack/~last=///424x4//lmdb/www/a_tupl:weights')
	assert a.status_code == 200

	a = get('//deque/my_stack/~plast.text')
	assert a.status_code == 200 and a.text == '[[17, 170], [112, 54], [207, 149]]'

	a = get('///424x4//lmdb/www/a_tupl:author')
	assert a.status_code == 200 and a.text == 'Billy'

	q = delete('//deque/my_stack')
	assert q.status_code == 200

	q = delete('///424x4//deque/my_stack')
	assert q.status_code == 200


#define APPLY_URL						 2		///< //base& any_url_encoded_url ; (A call to http or file)
#define APPLY_FUNCTION					 3		///< {///node}//base/entity/key(//r_base/r_entity/r_key) (A function call on a block.)
#define APPLY_FUNCT_CONST				 4		///< //base/entity/key(& any_url_encoded_const) (A function call on a const.)
#define APPLY_FILTER					 5		///< {///node}//base/entity/key[//r_base/r_entity/r_key] (A filter on a block.)
#define APPLY_FILT_CONST				 6		///< {///node}//base/entity/key[& any_url_encoded_const] (A filter on a const.)
#define APPLY_RAW						 7		///< {///node}//base/entity/key.raw (Serialize text to raw.)
#define APPLY_TEXT						 8		///< {///node}//base/entity/key.text (Serialize raw to text.)
#define APPLY_ASSIGN_NOTHING			 9		///< {///node}//base/entity/key=//r_base/r_entity/r_key (Assign block to block.)
#define APPLY_ASSIGN_NAME				10		///< {///node}//base/entity/key=//r_base/r_entity/r_key:name (Tuple item -> block)
#define APPLY_ASSIGN_URL				11		///< {///node}//base/entity/key=//r_base/r_entity/r_key:name (Tuple item -> block)
#define APPLY_ASSIGN_FUNCTION			12		///< {///node}//base/entity/key=//r_base/r_entity/r_key(//t_base/t_entity/t_key)
#define APPLY_ASSIGN_FUNCT_CONST		13		///< {///node}//base/entity/key=//r_base/r_entity/r_key(& any_url_encoded_const)
#define APPLY_ASSIGN_FILTER				14		///< {///node}//base/entity/key=//r_base/r_entity/r_key[//t_base/t_entity/t_key]
#define APPLY_ASSIGN_FILT_CONST			15		///< {///node}//base/entity/key=//r_base/r_entity/r_key[& any_url_encoded_const]
#define APPLY_ASSIGN_RAW				16		///< {///node}//base/entity/key=//r_base/r_entity/r_key.raw
#define APPLY_ASSIGN_TEXT				17		///< {///node}//base/entity/key=//r_base/r_entity/r_key.text
#define APPLY_ASSIGN_CONST				18		///< {///node}//base/entity/key=& any_url_encoded_const ; (Assign const to block.)
#define APPLY_NEW_ENTITY				19		///< {///node}//base/entity.new (Create a new entity)
#define APPLY_GET_ATTRIBUTE				20		///< {///node}//base/entity/key.attribute(123) (read attribute 123 with HTTP_GET)
#define APPLY_SET_ATTRIBUTE				21		///< //base/entity/key.attribute(123)=& url_encoded ; (set attribute 123 with HTTP_GET)



def test_AcrossNodesAllRemoteLeft():
	pass

def test_AcrossNodesAllRemoteBoth():
	pass


if __name__ == '__main__':
	test_AcrossNodesBasic()
	test_AcrossNodesAllRemoteRight()
	test_AcrossNodesAllRemoteLeft()
	test_AcrossNodesAllRemoteBoth()

	print('\n\nDone.')
