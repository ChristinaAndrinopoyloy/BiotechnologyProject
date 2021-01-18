import helpers as hlp
import pandas as pd

pathname_2D = './MOUSE BRAIN 2DGE PROTEINS/all.xls'
pathname_HRMS = './MOUSE BRAIN PROTEOME HRMS/all.xlsx'
common_name = './Results/ALL/common_proteins_all.xls'
unique_name1 = './Results/ALL/HRMS_unique_proteins_all.xls'
unique_name2 = './Results/ALL/2DGE_unique_proteins_all.xls'


df_2D = hlp.read_from_xlx(pathname_2D, lbl_2d=True)
df_HRMS = hlp.read_from_xlx(pathname_HRMS)
df_HRMS.rename(columns = {'Entry name': 'Accession Name'}, inplace=True)

# Find the common proteins of the two dataframes and save the results
common_proteins = pd.merge(df_2D, df_HRMS, on=['Accession Name'], how='inner')[['Accession Name',"Protein names"]]
common_proteins.to_excel(common_name) 
print(f"Please check: {common_name}")

# find the unique proteins of HRMS
unique_proteins = pd.merge(df_HRMS, df_2D, how='outer', indicator=True)
unique_proteins_df = unique_proteins.loc[unique_proteins._merge == 'left_only', ['Accession Name',"Protein names"]]
unique_proteins_df.to_excel(unique_name1) 
print(f"Please check: {unique_name1}")

# find the unique proteins of 2DGE
unique_proteins = pd.merge(df_2D, df_HRMS, how='outer', indicator=True)
unique_proteins_df = unique_proteins.loc[unique_proteins._merge == 'left_only', ['Accession Name',"Protein name"]]
unique_proteins_df.to_excel(unique_name2) 
print(f"Please check: {unique_name2}")
print("="*100)