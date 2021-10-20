import requests as http

SERVER_URL = 'http://192.168.1.19:8899'
REMOTE_URL = 'http://192.168.1.141:8888'


def get(qq, remote = False):
	if remote:
		return http.get(REMOTE_URL + qq)

	return http.get(SERVER_URL + qq)

def put(qq, string, remote = False):
	if remote:
		return http.put(REMOTE_URL + qq, string)

	return http.put(SERVER_URL + qq, string)

def delete(qq, remote = False):
	if remote:
		return http.delete(REMOTE_URL + qq)

	return http.delete(SERVER_URL + qq)
