import helpers as hlp
import pandas as pd
import xlsxwriter 


brainpart_proteins_dict = {'OB':[],'HT':[],'MD':[],'MB':[],'HC':[],'CB':[],'CC':[]}
brain_parts = ['Cerebellum', 'Cortex', 'Hipocampus', 'Hipothalamus', 'Medulla', 'Mid_Brain', 'Olfactory_balb']
brain_part_correspond = {'Olfactory_balb':'OB',
                        'Hipothalamus':'HT',
                        'Medulla':'MD',
                        'Mid_Brain':'MB',
                        'Hipocampus':'HC',
                        'Cerebellum':'CB',
                        'Cortex':'CC'}

# read the excel file than contains the proteins from 2DGE
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
    common_name = './Results/SIMPLE/'+part+'/common_proteins_'+part+'.xls'
    unique_name1 = './Results/SIMPLE/'+part+'/HRMS_unique_proteins_'+part+'.xls'
    unique_name2 = './Results/SIMPLE/'+part+'/2DGE_unique_proteins_'+part+'.xls'

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

    print(f"I am going to compare:{len(proteins_from_HRMS)} from HRMS with {len(proteins_from_2DGE)} from 2DGE")

    # common proteins
    common_proteins = list(set(proteins_from_HRMS).intersection(proteins_from_2DGE))
    print(len(common_proteins))
    hlp.plot_results(common_proteins, part)

    # different proteins
    unique_2DGE = [item for item in proteins_from_2DGE if item not in proteins_from_HRMS]
    unique_HRMS = [item for item in proteins_from_HRMS if item not in proteins_from_2DGE]

    # create common excels
    excel_file = xlsxwriter.Workbook(common_name) 
    worksheet = excel_file.add_worksheet() 
    row = 1
    column = 0
    worksheet.write(0, 0, "Accession Name")

    for item in common_proteins : 
        worksheet.write(row, column, item) 
        row += 1
    excel_file.close() 

    # create common excels
    hlp.write_on_excel(common_name, common_proteins)

    # create unique HRMS excels
    hlp.write_on_excel(unique_name1, unique_HRMS)
    
    # create unique 2DGE excels
    hlp.write_on_excel(unique_name2, unique_2DGE)

    # hlp.plot_results(common_proteins, part)
    print('='*100)
