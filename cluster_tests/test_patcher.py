from http_requests import patch_broken_requests


def test_patcher():

	assert patch_broken_requests(True)


# if __name__ == '__main__':
# 	test_patcher()

# 	print('\n\nDone.')
