import pandas as pd
import numpy as np
from os import path
from PIL import Image
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import xlsxwriter 


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

    for item in mylist : 
        worksheet.write(row, column, item) 
        row += 1
    excel_file.close()     

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
            brainpart_proteins_dict[key].append(protein)
        else:
            if cerebellum == 1:
                print('*'*40)
                print(cerebellum)
                print(cortex)    
                print(hipocampus)    
                print(hipothalamus)    
                print(medulla)    
                print(mid_brain)    
                print(olfactory_balb)    
                print('*'*40)



    for key, value in brainpart_proteins_dict.items():
        excel_filename = './MOUSE BRAIN PROTEOME HRMS/UNIQUE/'+key+'_UNIQUE.xlsx'
        excel_file = xlsxwriter.Workbook(excel_filename) 
        worksheet = excel_file.add_worksheet() 
        row = 1
        column = 0
        worksheet.write(0, 0, "Accession Name")

        for item in value : 
            worksheet.write(row, column, item) 
            row += 1
        excel_file.close() 
    print(counter)    
        