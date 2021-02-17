##########################################################################################
#                               Andrinopoulou Christina                                  #
#                                             ds2200013                                  #
##########################################################################################

import pandas as pd
import numpy as np
import os.path
from os import path
from PIL import Image
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import xlsxwriter 
import PyPDF2 
import csv
import go_helpers as go


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


def barplot(my_dict, title):
    fig, ax = plt.subplots()
    plt.barh(*zip(*my_dict.items()),color='#39c0ba', align='center')
    ax.set_xlabel('Number of Proteins')
    ax.set_title(title)
    plt.tight_layout()
    plt.show()


def multiple_barplot(df, title):
    df.plot.barh(logx=False)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    title = title.replace('_', ' ')
    plt.title(title)
    plt.show()

def split_string_into2(my_string,index=40):
    my_string = my_string[:index] + '-\n' + my_string[index:]
    return my_string


def correct_brainpart(brain_part):
    if brain_part == 'Cerebellum':
        brain_part = 'Cerebellum'
    if brain_part == 'Cortex':
        brain_part = 'Cortex' 
    if brain_part == 'Hipocampus':
        brain_part = 'Hippocampus'     
    if brain_part == 'Hipothalamus':
        brain_part = 'Hypothalamus'
    if brain_part == 'Medulla':
        brain_part = 'Medulla'
    if brain_part == 'Mid_Brain':
        brain_part = 'Mid Brain'
    if brain_part == 'Olfactory_balb':
        brain_part = 'Olfactory Bulb'  
    return brain_part    


def get_brainpart_based_on_index(index):
    if index == 7:
        return 'Brainstem'
    if index == 8:
        return 'Cerebellum'  
    if index == 9:
        return 'Corpus_Callosum'
    if index == 10:
        return 'Motor_Cortex'
    if index == 11:
        return 'Olfactory_Bulb'
    if index == 12:
        return 'Optic_Nerve'  
    if index == 13:
        return 'Prefrontal_Cortex'
    if index == 14:
        return 'Striatum'    
    if index == 15:
        return 'Thalamus'
    if index == 16:
        return 'Ventral_Hippocampus'    
    else:
        print('ERRORRRRRRRRRRRR')
        return None              


def get_brainpart_based_on_index2(index):
    if index == 1:
        return 'Mid_Brain'
    if index == 2:
        return 'Cortex_Subplate'
    if index == 3:
        return 'Medulla'
    if index == 4:
        return 'Striatum'
    if index == 5:
        return 'Cerebellum'
    if index == 6:
        return 'Thalamus'
    if index == 7:
        return 'Olfactory_Bulb'
    if index == 8:
        return 'Cortex'
    if index == 9:
        return 'Pallidum'
    if index == 10:
        return 'Hypothalamus'



def read_table_from_pdf(filename):  
    returned_codes = []
    pdf_object = open(filename, 'rb') 
    pdf_reader = PyPDF2.PdfFileReader(pdf_object) 
    pages = pdf_reader.numPages

    # for each page get the content 
    for i in range(pages):
        page = pdf_reader.getPage(i) 
        text = page.extractText()
        line = text.replace('\n', ' ').split('gi|')
        for j in range(len(line)):
            code = line[j].split(' ')
            code = code[0]
            # print(code)
            digits = []
            for s in code:
                if s.isdigit():
                    digits.append(s)
                else:
                    break    
            code = ''.join([str(elem) for elem in digits]) 
            code = 'gi|'+code
            # print(code)
            returned_codes.append(code)

    # closing the pdf file object 
    pdf_object.close() 
    returned_codes.remove('gi|')
    returned_codes = [c for c in returned_codes if len(c) > 4]
    return returned_codes