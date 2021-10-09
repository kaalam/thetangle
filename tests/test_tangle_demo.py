import pytest, requests

from http_requests import get, put, delete


def test_TangleDemo():
	a = 1

	assert isinstance(a, int)

	with pytest.raises(ZeroDivisionError):
		b = a/0

	assert 3*a == 3
