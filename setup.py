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
