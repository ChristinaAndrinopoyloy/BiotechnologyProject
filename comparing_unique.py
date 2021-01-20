import helpers as hlp
import pandas as pd

df_HRMS_all = hlp.read_from_xlx('./MOUSE BRAIN PROTEOME HRMS/all.xlsx')
hlp.find_unique_proteins_per_brainpart(df_HRMS_all)

brain_parts = ['Cerebellum', 'Cortex', 'Hipocampus', 'Hipothalamus', 'Medulla', 'Mid_Brain', 'Olfactory_balb']

# for each excel
for part in brain_parts:
    print(part)
    pathname_2D = './MOUSE BRAIN 2DGE PROTEINS/'+part+'.xls'
    pathname_HRMS = './MOUSE BRAIN PROTEOME HRMS/UNIQUE/'+part+'_UNIQUE.xlsx'
    common_name = './Results/UNIQUE/'+part+'/common_proteins_'+part+'.xls'
    unique_name1 = './Results/UNIQUE/'+part+'/HRMS_unique_proteins_'+part+'.xls'
    unique_name2 = './Results/UNIQUE/'+part+'/2DGE_unique_proteins_'+part+'.xls'

    df_2D = hlp.read_from_xlx(pathname_2D, lbl_2d=True)
    df_HRMS = hlp.read_from_xlx(pathname_HRMS)
    print(df_HRMS.tail())


    # Find the common proteins of the two dataframes and save the results
    common_proteins = pd.merge(df_2D, df_HRMS, on=['Accession Name'], how='inner')[['Accession Name', 'Description']]
    if not common_proteins.empty:
        common_proteins.to_excel(common_name) 
        print(f"Please check: {common_name}")

    # find the unique proteins of HRMS
    unique_proteins = pd.merge(df_HRMS, df_2D, how='outer', indicator=True)
    unique_proteins_df = unique_proteins.loc[unique_proteins._merge == 'left_only', ['Accession Name', 'Description']]
    unique_proteins_df.to_excel(unique_name1) 
    print(f"Please check: {unique_name1}")

    # find the unique proteins of 2DGE
    unique_proteins = pd.merge(df_2D, df_HRMS, how='outer', indicator=True)
    unique_proteins_df = unique_proteins.loc[unique_proteins._merge == 'left_only', ['Accession Name', 'Protein name']]
    unique_proteins_df.to_excel(unique_name2) 
    print(f"Please check: {unique_name2}")
    print("="*100)