import requests as http

SERVER_URL = 'http://192.168.1.19:8899'


def get(qq):
	return http.get(SERVER_URL + qq)

def put(qq, string):
	return http.put(SERVER_URL + qq, string)

def delete(qq):
	return http.delete(SERVER_URL + qq)
