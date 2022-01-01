# The Tangle: An entangled collection of English text for Jazz

# 	Jazz (c) 2021-2021 kaalam.ai (The Authors of Jazz)

# 		Code is licensed under the Apache License, Version 2.0 http://www.apache.org/licenses/LICENSE-2.0
#		Data is open source (see LICENSE_* files in kaalam/tng-data-* repositories for details.)


"""
	Welcome to The TangleExplorer !
"""


"""
	0. The first time you run the TNG server, you have to dowload and compile The Tangle

	Follow the instructions in: https://kaalam.github.io/jazz_reference/reference_docker_tangle_server.html
"""


"""
	I M P O R T A N T  N O T E : This is just a piece of software to help you get your hands on The Tangle and understand
	how to explore the tree. The Tangle was not created to be used via the http interface as such.

	If you may have different approaches, e.g.:

	- Use the dataset (or a subset of them) by hacking with the ETL
	- Think of an application for which the server is useful as it is
	- Get interested in Jazz as a technology and the science to https://kaalam.github.io/jazz_reference/contributing_welcome_all.html
	- Other ideas ...

"""


"""
	D A T A  S T R U C T U R E : The tangle is organized in `datasets`, `sections` and `blocks`. The main index is comma separated in
	`//lmdb/the_tangle/datasets` and it leads to:
		- `//lmdb/the_tangle/DATASET_sections` and each one to ..
		- `//lmdb/the_tangle/DATASET_SECTION_blocks` and each one to ..
		- `//lmdb/the_tangle/DATASET_SECTION_BLOCK-NUMBER_LAST-INDEX` where each block is a vector of strings from 0 to LAST-INDEX

	You will need https://kaalam.github.io/jazz_reference/api_ref_intro.html to understand the Jazz API.
	Also, see the source code of the python package. Its only ~200 lines of code very easy to follow.

	Good luck, and don't hesitate in contacting us!

	kaalam@kaalam.ai
"""

from thetangle import TangleExplorer

te = TangleExplorer()

ds = te.datasets()

print(ds)
print(te.datasets(urls_as_names = True))

ss = te.sections(ds[0])

print(ss)
print(te.sections('//lmdb/the_tangle/jeopardy_sections'))
print(te.sections('jeopardy', urls_as_names = True))

bl = te.blocks('jeopardy', 'question')

print(bl[0:2])
print(te.blocks('//lmdb/the_tangle/jeopardy_sections', '//lmdb/the_tangle/jeopardy_answer_blocks')[0:2])
