import helpers as hlp
import pandas as pd

brain_parts = ['Cerebellum', 'Cortex', 'Hipocampus', 'Hipothalamus', 'Medulla', 'Mid_Brain', 'Olfactory_balb', 'all']

# for each excel
for part in brain_parts:
    print(part)
    pathname_2D = './MOUSE BRAIN 2DGE PROTEINS/'+part+'.xls'
    pathname_HRMS = './MOUSE BRAIN PROTEOME HRMS/'+part+'.xlsx'
    # temp_name= 'temp'+part+'.xls'
    common_name = './Results/'+part+'/common_proteins_'+part+'.xls'
    unique_name1 = './Results/'+part+'/HRMS_unique_proteins_'+part+'.xls'
    unique_name2 = './Results/'+part+'/2DGE_unique_proteins_'+part+'.xls'


    df_2D = hlp.read_from_xlx(pathname_2D, lbl_2d=True)
    df_HRMS = hlp.read_from_xlx(pathname_HRMS)

    # Add a new column, which contains the Accesion Name for each protein
    # We extract this information from the description
    if part != 'all':
        accession_names = []
        for index, row in df_HRMS.iterrows():
            description = row['Description']
            splitted_description = hlp.split_string_based_on_char(description)
            accesion_name = splitted_description[-1]
            accesion_name = accesion_name[:-1]
            accession_names.append(accesion_name)
        df_HRMS['Accession Name'] = accession_names
        # df_HRMS.to_excel(temp_name) 
    else:
        df_HRMS.rename(columns = {'Entry name': 'Accession Name'}, inplace=True)

    # Find the common proteins of the two dataframes and save the results
    common_proteins = pd.merge(df_2D, df_HRMS, on=['Accession Name'], how='inner')
    # print(common_proteins)
    common_proteins.to_excel(common_name) 
    print(f"Please check: {common_name}")

    # find the unique proteins of HRMS
    unique_proteins = pd.merge(df_HRMS, df_2D, how='outer', indicator=True)
    unique_proteins_df = unique_proteins.loc[unique_proteins._merge == 'left_only', ['Accession Name']]
    unique_proteins_df.to_excel(unique_name1) 
    print(f"Please check: {unique_name1}")

    # find the unique proteins of 2DGE
    unique_proteins = pd.merge(df_2D, df_HRMS, how='outer', indicator=True)
    unique_proteins_df = unique_proteins.loc[unique_proteins._merge == 'left_only', ['Accession Name']]
    unique_proteins_df.to_excel(unique_name2) 
    print(f"Please check: {unique_name2}")
    
    print("=======================")