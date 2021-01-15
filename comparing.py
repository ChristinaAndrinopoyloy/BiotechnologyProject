import helpers as hlp
import pandas as pd

brainpart_proteins_dict = {'OB':[],'HT':[],'MD':[],'MB':[],'HC':[],'CB':[],'CC':[]}
brain_parts = ['Cerebellum', 'Cortex', 'Hipocampus', 'Hipothalamus', 'Medulla', 'Mid_Brain', 'Olfactory_balb']
brain_part_correspond = {'Olfactory_balb':'OB',
                        'Hipothalamus':'HT',
                        'Medulla':'MD',
                        'Mid_Brain':'MB',
                        'Hipocampus':'HC',
                        'Cerebellum':'CB',
                        'Cortex':'CC'}

# read th excel file than contains the proteins from 2DGE
pathname_2D = './MOUSE BRAIN 2DGE PROTEINS/all.xls'
df_2D = hlp.read_from_xlx(pathname_2D, lbl_2d=True)
brain_parts_2DGE = []
for index, row in df_2D.iterrows():
    bp = row['Brain part']
    protein = row['Accession Name']
    splitted_brainpart = hlp.split_string_based_on_char(bp,separator=',')
    for key in splitted_brainpart:
        if " " in key:
            key = ''.join(key.split())   
        if key not in brainpart_proteins_dict:
            brainpart_proteins_dict[key] = []
        brainpart_proteins_dict[key].append(protein)
        

# for each excel fle from HRMS
for part in brain_parts:
    print(part)
    pathname_HRMS = './MOUSE BRAIN PROTEOME HRMS/'+part+'.xlsx'
    # common_name = './Results/'+part+'/common_proteins_'+part+'.xls'
    # unique_name1 = './Results/'+part+'/HRMS_unique_proteins_'+part+'.xls'
    # unique_name2 = './Results/'+part+'/2DGE_unique_proteins_'+part+'.xls'

    df_HRMS = hlp.read_from_xlx(pathname_HRMS)

    # Add a new column, which contains the Accesion Name for each protein
    # We extract this information from the description
    accession_names = []
    for index, row in df_HRMS.iterrows():
        description = row['Description']
        splitted_description = hlp.split_string_based_on_char(description)
        accesion_name = splitted_description[-1]
        accesion_name = accesion_name[:-1]
        accession_names.append(accesion_name)
    df_HRMS['Accession Name'] = accession_names


    # get the proteins (accession name) from the HRMS dataframe for the specific part of the brain
    proteins_from_HRMS = df_HRMS['Accession Name'].tolist()    
    # get the proteins (accession name) from the 2DGE dictionary for the specific part of the brain
    proteins_from_2DGE = brainpart_proteins_dict[brain_part_correspond[part]]

    # print("I am going to compare:")
    # print(len(proteins_from_HRMS))
    # print('with')
    # print(len(proteins_from_2DGE))

    # common proteins
    common_proteins = list(set(proteins_from_HRMS).intersection(proteins_from_2DGE))
    print(len(common_proteins))
    hlp.plot_results(common_proteins, part)
    print('='*100)
