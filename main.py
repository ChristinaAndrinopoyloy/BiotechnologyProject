import helpers as hlp

pathname_2D = './MOUSE BRAIN 2DGE PROTEINS/TARASLIA et al TABLE 7.xls'
pathname_HRMS = 'MOUSE BRAIN PROTEOME HRMS/mouse_brain_-_hipothalamus_7_weeks-01.xlsx'

df_2D = hlp.read_from_xlx(pathname_2D, lbl_2d=True)
df_HRMS = hlp.read_from_xlx(pathname_HRMS)

# Add a new column, which contains the Accesion Name for each protein
# We extract this information from the description
accession_names = []
for index, row in df_HRMS.iterrows():
    description = row['Description']
    splitted_description = hlp.split_string_based_on_char(description)
    accesion_name = splitted_description[1]
    accesion_name = accesion_name[:-1]
    accession_names.append(accesion_name)
print(df_HRMS.head())