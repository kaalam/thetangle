# The Tangle: An entangled collection of English text for Jazz

# 	Jazz (c) 2021-2023 kaalam.ai (The Authors of Jazz)

# 		Code is licensed under the Apache License, Version 2.0 http://www.apache.org/licenses/LICENSE-2.0
#		Data is open source (see LICENSE_* files in kaalam/tng-data-* repositories for details.)


from distutils.core import setup

from thetangle import __version__


setup(
	name		 = 'thetangle',
	packages	 = ['thetangle'],
	version		 = __version__,
	license		 = 'MIT',
	description  = 'A minimalistic utility to explore The Tangle',
	author		 = 'kaalam',
	author_email = 'kaalam@kaalam.ai',
	url			 = 'https://github.com/kaalam/thetangle',
	download_url = 'https://github.com/kaalam/thetangle/dist/thetangle-%s.tar.gz' % __version__,
	keywords	 = ['utilities', 'nlp', 'datasets'],
	classifiers  = [
		'Development Status :: 3 - Alpha',
		'Intended Audience :: Developers',
		'Topic :: Software Development :: Build Tools',
		'License :: OSI Approved :: MIT License',
		'Programming Language :: Python :: 3']
)
