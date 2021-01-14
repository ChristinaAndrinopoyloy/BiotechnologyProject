import helpers as hlp
import pandas as pd

brainpart_proteins_dict = {'OB':[],'HT':[],'MD':[],'MB':[],'HC':[],'CB':[],'CC':[]}

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
    for key, value in brainpart_proteins_dict.
        

#     accession_names.append(accesion_name)
# df_HRMS['Accession Name'] = accession_names

# brain_parts = ['Cerebellum', 'Cortex', 'Hipocampus', 'Hipothalamus', 'Medulla', 'Mid_Brain', 'Olfactory_balb', 'all']

# # for each excel
# for part in brain_parts:
#     print(part)
#     pathname_HRMS = './MOUSE BRAIN PROTEOME HRMS/'+part+'.xlsx'
#     # common_name = './Results/'+part+'/common_proteins_'+part+'.xls'
#     # unique_name1 = './Results/'+part+'/HRMS_unique_proteins_'+part+'.xls'
#     # unique_name2 = './Results/'+part+'/2DGE_unique_proteins_'+part+'.xls'