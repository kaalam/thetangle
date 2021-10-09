import requests as http
import pytest


def test_TangleDemo():
	a = 1

	assert isinstance(a, int)

	with pytest.raises(ZeroDivisionError):
		b = a/0

	assert 3*a == 3
