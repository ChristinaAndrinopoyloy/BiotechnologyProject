import pandas as pd

def read_from_xlx(pathname, lbl_2d=False):
    if lbl_2d:
        df = pd.read_excel (pathname, header=1)
    else:
        df = pd.read_excel (pathname)
    return df

def split_string_based_on_char(my_string):
    splited_string = my_string.split(sep='[')
    return splited_string