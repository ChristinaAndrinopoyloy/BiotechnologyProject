from goatools.gosubdag.gosubdag import GoSubDag
from goatools.base import get_godag

godag = get_godag('go-basic.obo', optional_attrs='relationship')

goid = 'GO:0050807'

gosubdag = GoSubDag(goid, godag, relationships=True, prt=False)
ntgo = gosubdag.go2nt[goid]
prtfmt = '{GO_name}'
print(prtfmt)
print(prtfmt.format(**ntgo._asdict()))
