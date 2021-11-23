# CompileTheTangle().compile()

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

print('Done.')
