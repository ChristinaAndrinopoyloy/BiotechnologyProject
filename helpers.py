import pandas as pd
import numpy as np
import os.path
from os import path
from PIL import Image
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import xlsxwriter 
import csv
import go_helpers as go
from collections import Counter


def write_on_csv(list_of_tuples,pathname):
    with open(pathname,'w') as out:
        my_csv=csv.writer(out)
        my_csv.writerow(['Uniprot Entry','Accession Name'])
        for row in list_of_tuples:
            my_csv.writerow(row)


def from_csv_to_dict(pathname):
    my_dict = dict()
    with open(pathname, mode='r') as infile:
        my_csv = csv.reader(infile)
        my_dict = {rows[0]:rows[1].replace('{','').replace('}','').replace('\'','') for rows in my_csv}
    return my_dict    


def read_from_xlx(pathname, lbl_2d=False):
    if lbl_2d:
        df = pd.read_excel (pathname, header=1)
    else:
        df = pd.read_excel (pathname)
    return df


def write_on_excel(pathname, mylist):
    excel_file = xlsxwriter.Workbook(pathname) 
    worksheet = excel_file.add_worksheet() 
    row = 1
    column = 0
    worksheet.write(0, 0, "Accession Name")
    worksheet.write(0, 1, "Description")

    for item in mylist : 
        print(item[0])
        print(item[1])
        worksheet.write(row, column, item[0]) 
        worksheet.write(row, column + 1, item[1]) 
        row += 1
    excel_file.close()   


def merge_excels(excel_1, excel_2, excel_3, write_flag=False, pathname=None):
    df_2 = read_from_xlx(excel_2)[['Accession Name']]
    df_3 = read_from_xlx(excel_3)[['Accession Name']]

    if path.exists(excel_1):
        df_1 = read_from_xlx(excel_1)[['Accession Name']]
        dfs = [df_1, df_2, df_3]
    else:
        dfs = [df_2, df_3]    
    total_df = pd.concat(dfs)
    total_df.drop_duplicates(subset=['Accession Name'])

    if write_flag:
        total_df.to_csv(pathname, index = False)
    return total_df

def split_string_based_on_char(my_string,separator='['):
    splited_string = my_string.split(sep=separator)
    return splited_string

def plot_results(words, title):
    mask = np.array(Image.open(path.join("./mouse.png")))

    listToStr = ' '.join([elem for elem in words]) 

    # Create and generate a word cloud image:
    wordcloud = WordCloud(width=1600, height=800,
                        background_color="white", max_words=2000, mask=mask,
                        max_font_size=8, min_font_size=8, colormap="Purples",
                        contour_width=2, contour_color='black').generate(listToStr)

    # Display the generated image:
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.title(title)
    plt.show()    

def find_unique_proteins_per_brainpart(df):
    brainpart_proteins_dict = {'Olfactory_balb':[],
                        'Hipothalamus':[],
                        'Medulla':[],
                        'Mid_Brain':[],
                        'Hipocampus':[],
                        'Cerebellum':[],
                        'Cortex':[]}
    counter = 0

    for index, row in df.iterrows():
        if row['Cerebral cortex'] != 0 and row['Cerebral cortex'] != 1:
            continue

        protein = row['Entry name']
        description = row['Protein names']
        if description != description:
            description = 'None'
        cortex = int(row['Cerebral cortex'])
        olfactory_balb = int(row['Olfactory Bulb'])
        hipocampus = int(row['Hippocampus'])
        hipothalamus = int(row['Hypothalamus'])
        mid_brain = int(row['Mid brain'])
        cerebellum = int(row['Cerebellum'])
        medulla = int(row['Medulla'])

        sum_of_brainparts = cortex + olfactory_balb + hipocampus + hipothalamus + mid_brain + cerebellum + medulla

        if sum_of_brainparts == 1:
            if cortex == 1:
                key = 'Cortex'

            if olfactory_balb == 1:
                key = 'Olfactory_balb'  

            if hipocampus == 1:
                key = 'Hipocampus'

            if hipothalamus == 1:
                key = 'Hipothalamus'

            if mid_brain == 1:
                key = 'Mid_Brain'

            if cerebellum == 1:
                counter = counter + 1
                key = 'Cerebellum'

            if medulla == 1:
                key = 'Medulla'
            
            if key not in brainpart_proteins_dict:
                brainpart_proteins_dict[key] = []
            brainpart_proteins_dict[key].append((protein, description))

    for key, value in brainpart_proteins_dict.items():
        excel_filename = './MOUSE BRAIN PROTEOME HRMS/UNIQUE/'+key+'_UNIQUE.xlsx'
        excel_file = xlsxwriter.Workbook(excel_filename) 
        worksheet = excel_file.add_worksheet() 
        row = 1
        column = 0
        worksheet.write(0, 0, "Accession Name")
        worksheet.write(0, 1, "Description")


        for item in value : 
            worksheet.write(row, column, item[0]) 
            worksheet.write(row, column+1, item[1]) 

            row += 1
        excel_file.close()    


def find_description_from_accession_name(proteins, df, flag_2dge=False):
    info_protein = []

    if flag_2dge:
        descriptin_index = 'Function'
    else:
        descriptin_index = 'Description'

    for prot in proteins:
        row = df[df['Accession Name'].str.contains(prot)]
        description = row[descriptin_index].values[0]
        info_protein.append((prot,description))
    return info_protein    


def get_values_from_dict(my_dict, godag):
    temp_list = []
    all_ancestors = []
    for key, value in my_dict.items():
        for v in value.strip().replace(' ','').split(','):
            temp_list.append(go.get_name_of_GOid(v,godag))
    [all_ancestors.append(item) for item in temp_list if item not in all_ancestors]   # remove duplicates
    return all_ancestors


def intersection_of_lists(list1, list2): 
    returned_list = [item for item in list1 if item in list2] 
    return returned_list 


def flatten_of_list(my_list):
    returned_list = [term for sublist in my_list for term in sublist]   # flatten
    return returned_list


def remove_duplicates_of_list(my_list):
    returned_list = []  
    [returned_list.append(term) for term in my_list if term not in returned_list]  
    return returned_list


def split_items_of_list(my_list):
    returned_list = []
    for item in my_list:
        if not item != item:
            item = item.strip().replace(' ','').split(',')
            for i in item:
                returned_list.append(i)
    return returned_list    


def barplot(my_dict,title):
    fig, ax = plt.subplots()
    plt.barh(*zip(*my_dict.items()),color='#39c0ba', align='center')
    ax.set_xlabel('Number of Proteins')
    ax.set_title(title)
    plt.tight_layout()
    plt.show()


def split_string_into2(my_string):
    my_string = my_string[:40] + '-\n' + my_string[40:]
    return my_string


def statistics_routine(my_list, godag, title):
    for i in range(len(my_list)):
        my_list[i] = go.get_name_of_GOid(my_list[i], godag)
        if len(my_list[i]) > 40:
            my_list[i] = split_string_into2(my_list[i])
    occurances = Counter(my_list)
    barplot(occurances, title=title)    