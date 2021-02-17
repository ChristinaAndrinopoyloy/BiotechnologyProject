import os
import pandas as pd
import uniprot_database_helpets as uni

class Protein:
  def __init__(self, uniprot_entry, accession_name, protein_name, organism, brain_parts, 
                biological_process,
                molecular_function,
                cellular_component):
    self.uniprot_entry = uniprot_entry
    self.accession_name = accession_name 
    self.protein_name = protein_name
    self.organism = organism 
    self.brain_parts = brain_parts
    self.biological_process = biological_process
    self.molecular_function = molecular_function
    self.cellular_component = cellular_component
    self.paper = []



frames = []
files = os.listdir('MERGED/SIMPLE')
for xlx_file in files:
    if xlx_file != 'figures':
        df = pd.read_csv('MERGED/SIMPLE/'+xlx_file+'/all_infos2.csv')
        df = df[['Uniprot Entry', 'Accession Name', 'Name', 'Organism', 'Biological Process Label', 'Molecular Function Label', 'Cellular Component Label']]
        new_column = [xlx_file for i in range(df.shape[0])]
        df.insert(5, "Brain Part", new_column, True)
        frames.append(df)
        
sum_up_df = pd.concat(frames)
sum_up_df.to_csv('all_proteins_for_now.csv',index=False)

db_content = dict()
for index, row in sum_up_df.iterrows():
    uniprot_entry = row['Uniprot Entry']
    accession_name = row['Accession Name']
    if len(accession_name) < 3:
        print(uniprot_entry)
        uniprot_data = uni.get_uniprot(query=uniprot_entry, query_type='ACC+ID')
        print(uniprot_data)
    # print(uniprot_entry)

    mask = sum_up_df['Uniprot Entry'] == uniprot_entry
    duplicates = sum_up_df.loc[mask]
    brain_parts = duplicates['Brain Part'].tolist() 
    # accession_names = duplicates['Accession Name'].tolist()
    # print(accession_names)
    if uniprot_entry not in db_content:
        protein = Protein(uniprot_entry=uniprot_entry, accession_name=row['Accession Name'], protein_name=row['Name'], organism=row['Organism'], brain_parts=brain_parts, 
                            biological_process=row['Biological Process Label'],
                            molecular_function=row['Molecular Function Label'],
                            cellular_component=row['Cellular Component Label'])
        db_content[uniprot_entry] = protein
      

# for key, protein in db_content.items():
#     print(key)
#     print(protein.accession_name)  
#     print(protein.protein_name)    
#     print(protein.biological_process)    
#     print(protein.molecular_function)    
#     print(protein.cellular_component)   
#     print('************************************************************************************') 




# dupl = sum_up_df.duplicated(['Uniprot Entry'])
# duplicate_rows = sum_up_df[sum_up_df.duplicated(['Uniprot Entry'], keep=False)]
# print("Duplicate Rows based on a single column are:", duplicate_rows, sep='\n')

# sum_up_df.sort_values(by=['Uniprot Entry'])
# proteins = sum_up_df.to_dict('index')
# print(proteins)
