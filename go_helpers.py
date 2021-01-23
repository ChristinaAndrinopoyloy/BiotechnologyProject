import os
from goatools.obo_parser import GODag
from goatools.base import get_godag
from goatools.gosubdag.gosubdag import GoSubDag
# from goatools.cli.gosubdag_plot import PlotCli

def load_basic_go():
    godag = get_godag("go-basic.obo")
    return godag

# returns the ancestors of a GO id
def get_ancestors(godag, GO_ID, print_flag=False):
    gosubdag_r0 = GoSubDag([GO_ID], godag, prt=None)
    if gosubdag_r0.rcntobj.go2ancestors == {}:
        return None
    ancestors = gosubdag_r0.rcntobj.go2ancestors[GO_ID]
    if print_flag:
        print(f'{GO_ID} ancestors: {ancestors}')
    return ancestors

def get_name_of_GOid(GO_ID):
    gosubdag = GoSubDag(GO_ID, godag, relationships=True, prt=False)
    ntgo = gosubdag.go2nt[GO_ID]
    prtfmt = '{GO_name}'
    return prtfmt.format(**ntgo._asdict())