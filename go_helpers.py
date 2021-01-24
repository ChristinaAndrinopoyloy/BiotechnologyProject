import os
from goatools.obo_parser import GODag
from goatools.base import get_godag
from goatools.gosubdag.gosubdag import GoSubDag
from goatools.godag.go_tasks import *
from goatools.semantic import *
import pandas as pd

# from goatools.cli.gosubdag_plot import PlotCli

def load_basic_go():
    # godag = get_godag("go-basic.obo")
    godag = get_godag('go-basic.obo', optional_attrs='relationship')
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


def get_name_of_GOid(GO_ID, godag):
    gosubdag = GoSubDag(GO_ID, godag, relationships=True, prt=False)
    ntgo = gosubdag.go2nt[GO_ID]
    prtfmt = '{GO_name}'
    return prtfmt.format(**ntgo._asdict())


def get_popular_go_terms(my_dict):
    temp_ancestors = list(my_dict.values())
    all_the_ancestors = []
    for item in temp_ancestors:
        item = item.strip().replace('[','').replace(']','').replace(' ','').split(',')
        all_the_ancestors.append(item)
    all_the_ancestors = [item for sublist in all_the_ancestors for item in sublist] # flatten list
   # count each go term
    anc_counter = Counter(all_the_ancestors)
    for key, value in anc_counter.items():
        if value == len(my_dict): # remove the root
            del my_dict[key] 
    print(anc_counter)
    print(len(my_dict))

def find_common_ancestors(go_ids, godag):
    print(go_ids)
    return deepest_common_ancestor(go_ids, godag)


def get_children(go_id, godag, level=1):
    level_counter = 1
    all_hierarchy = get_go2children_isa(godag)
    # df = pd.DataFrame.from_dict(all_hierarchy, orient='index')
    # df.to_csv('IS_A_hierarchyGO.csv', header=False)
    if go_id in all_hierarchy:
        children = list(all_hierarchy[go_id])
        all_children = []
        while level_counter != level:
            temp_children = []
            for child in children:
                if child in all_hierarchy:
                    temp_children.append(list(all_hierarchy[child]))
                    print(len(temp_children))
            level_counter += 1
            children = temp_children
            # print(children)
            all_children.append(children)
            # print(all_children)
        if level > 1:
            print('hello i lve U would U tell me your name')
            children = [go_term for sublist in all_children for go_term in sublist]    
            print(len(children))

    else:
        return None
    return children    