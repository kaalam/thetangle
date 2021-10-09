import requests as http
import pytest


def test_ChannelZmq():
	a = 1

	assert isinstance(a, int)

	with pytest.raises(ZeroDivisionError):
		b = a/0

	assert 3*a == 3


def test_ChannelBash():
	a = 1

	assert isinstance(a, int)

	with pytest.raises(ZeroDivisionError):
		b = a/0

	assert 3*a == 3


def test_ChannelFile():
	a = 1

	assert isinstance(a, int)

	with pytest.raises(ZeroDivisionError):
		b = a/0

	assert 3*a == 3


def test_ChannelHttp():
	a = 1

	assert isinstance(a, int)

	with pytest.raises(ZeroDivisionError):
		b = a/0

	assert 3*a == 3
