import os
from goatools.obo_parser import GODag
from goatools.base import get_godag
from goatools.gosubdag.gosubdag import GoSubDag


godag = get_godag("go-basic.obo")

# # Load a small test GO DAG and all the optional relationships,
# # like 'regulates' and 'part_of'
# godag = GODag('../tests/data/i126/viral_gene_silence.obo',
#               optional_attrs={'relationship'})

GO_ID = 'GO:0019222'  # regulation of metabolic process

gosubdag_r0 = GoSubDag([GO_ID], godag, prt=None)
print('{GO} ancestors: {P}'.format(GO=GO_ID,P=gosubdag_r0.rcntobj.go2ancestors[GO_ID]))