import go_helpers as go

from goatools.gosubdag.gosubdag import GoSubDag
from goatools.base import get_godag

godag = get_godag('go-basic.obo', optional_attrs='relationship')

goid = 'GO:0008150'

# gosubdag = GoSubDag(goid, godag, relationships=True, prt=False)
# ntgo = gosubdag.go2nt[goid]
# prtfmt = '{GO_name}'
# print(prtfmt.format(**ntgo._asdict()))

lala = go.get_children(goid, godag, level=1)
print(len(lala))