import os
import pandas as pd
from progress.bar import FillingCirclesBar
import helpers as hlp
import uniprot_database_helpets as uni


def paper1_routine():
    brainpart_proteins_dict = {
                            'Mid_Brain':[],
                            'Cerebellum':[],
                            'Cortex_Subplate':[],
                            'Medulla':[],
                            'Striatum':[],
                            'Thalamus':[],
                            'Olfactory_Bulb':[],
                            'Cortex':[],
                            'Pallidum':[],
                            'Hypothalamus':[]}
    pathname1 = './bonus_papers/paper1/table1.xlsx'
    df = hlp.read_from_xlx(pathname1)

    proteins = []
    bar = FillingCirclesBar('Read data from paper and get the uniprot code from UNIPROT', max=df.shape[0])
    for index, row in df.iterrows():
        bar.next()
        data = uni.get_uniprot(query=row['protein'],query_type='GENENAME')
        if data == []:
            continue
        protein = data[1].strip().replace('AC   ','').split(';')
        protein = protein[0]
        protein = protein.split('_', 1)[0]
        protein += '_MOUSE'
        proteins.append(protein)
        for i in range(1,11):
            if df.iloc[index][i] > 0.05:
                brainpart_proteins_dict[hlp.get_brainpart_based_on_index2(i)].append(protein)
    bar.finish()

    df_for_proteins = pd.DataFrame(proteins,columns =['Uniprot Entry']) 
    df_for_proteins.to_csv('./MERGED/BONUS_PAPERS/PAPER1/all/proteins_essential.csv')

    return brainpart_proteins_dict



def paper2_routine():
    pathname1 = './bonus_papers/paper2/table1.xlsx'
    pathname2 = './bonus_papers/paper2/table2.xlsx'

    df1 = hlp.read_from_xlx(pathname1)
    df2 = hlp.read_from_xlx(pathname2)

    df1 = df1.fillna(0)
    df2 = df2.fillna(0)

    df1 = df1.iloc[1:]
    df2 = df2.iloc[1:]

    # table 1
    proteins_list = []
    bar = FillingCirclesBar('Read data from paper', max=df1.shape[0])
    for index, row in df1.iterrows():
        proteins = row[-1]
        lfq_of_brain_total = 0
        for i in range(2,6):
            lfq_of_brain_total += int(row[i])

        ibaq_of_brain_total = 0
        for i in range(33,37):
            ibaq_of_brain_total += int(row[i])
        
        if lfq_of_brain_total != 0 and ibaq_of_brain_total != 0:
            proteins_list.append(proteins)
        bar.next()
    bar.finish()

    # table 2
    counter = 0
    proteins_brainpart_dict = dict()
    bar = FillingCirclesBar('Read data from paper', max=df2.shape[0])
    for index, row in df2.iterrows():
        proteins = row[-1]
        if proteins in proteins_list:
            counter += 1
            for i in range(7,17):
                if row[i] != 0:
                    keys = proteins.split(';')
                    for key in keys:
                        if '-' in key:
                            continue
                        if key not in proteins_brainpart_dict:
                            proteins_brainpart_dict[key] = []
                        proteins_brainpart_dict[key].append(hlp.get_brainpart_based_on_index(i))
        bar.next()
    bar.finish()
    df_for_proteins = pd.DataFrame.from_dict(proteins_brainpart_dict, orient='index')
    df_for_proteins.index.name='Uniprot Entry'
    df_for_proteins.to_csv('./MERGED/BONUS_PAPERS/PAPER2/all/proteins_essential.csv')

    brainparts_proteins = {
                            'Brainstem':[],
                            'Cerebellum':[],
                            'Corpus_Callosum':[],
                            'Motor_Cortex':[],
                            'Olfactory_Bulb':[],
                            'Optic_Nerve':[],
                            'Prefrontal_Cortex':[],
                            'Striatum':[],
                            'Thalamus':[],
                            'Ventral_Hippocampus':[]}	
    for key, value in proteins_brainpart_dict.items():
        for bp in value:
            brainparts_proteins[bp].append(key)
    return brainparts_proteins
