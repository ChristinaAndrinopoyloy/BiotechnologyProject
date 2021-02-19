import os
import csv
import pandas as pd
from progress.bar import FillingCirclesBar

import helpers as hlp
import uniprot_database_helpets as uni

class Protein:
  def __init__(self, uniprot_entry, accession_name, protein_name, organism, brain_parts, 
                biological_process,
                molecular_function,
                cellular_component,
                paper):
    self.uniprot_entry = uniprot_entry
    self.accession_name = accession_name 
    self.protein_name = protein_name
    self.organism = organism 
    self.brain_parts = brain_parts
    self.biological_process = biological_process
    self.molecular_function = molecular_function
    self.cellular_component = cellular_component
    self.paper = paper


# common (not unique)
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

bar = FillingCirclesBar('Get UniProt Data', max=sum_up_df.shape[0])
for index, row in sum_up_df.iterrows():
    uniprot_entry = row['Uniprot Entry']
    accession_name = row['Accession Name']
    if len(accession_name) < 3:
        accession_name = uni.get_proteinID(query=uniprot_entry)

    mask = sum_up_df['Uniprot Entry'] == uniprot_entry
    duplicates = sum_up_df.loc[mask]
    brain_parts = duplicates['Brain Part'].tolist() 
    if uniprot_entry not in db_content:
        protein = Protein(uniprot_entry=uniprot_entry, accession_name=accession_name, 
                            protein_name=row['Name'], 
                            organism=row['Organism'], 
                            brain_parts=brain_parts, 
                            biological_process=row['Biological Process Label'],
                            molecular_function=row['Molecular Function Label'],
                            cellular_component=row['Cellular Component Label'],
                            paper=['Proteomic Analysis of Normal Murine Brain Parts (VASILIKI K. TARASLIA, ALEXANDROS KOUSKOUKIS, ATHANASIOS K. ANAGNOSTOPOULOS, DIMITRIOS J. STRAVOPODIS, LUKAS H. MARGARITIS, GEORGE TH. TSANGARIS)',
                                    'Normal Mouse Brain Proteome II: Analysis of Brain Regions by High-resolution Mass Spectrometry (ARTEMIS G. KOROVESI, ATHANASIOS K. ANAGNOSTOPOULOS, VASILEIOS PIERROS, DIMITRIOS J. STRAVOPODIS, GEORGE TH. TSANGARIS'])
        db_content[uniprot_entry] = protein
    bar.next()
bar.finish()     
      

# # uncommon 2DGE
# brain_part_correspond = {'OB':'Olfactory Bulb',
#                         'HT':'Hypothalamus',
#                         'MD':'Medulla',
#                         'MB':'Mid Brain',
#                         'HC':'Hippocampus',
#                         'CB':'Cerebellum',
#                         'CC':'Cortex'}

# frames = []
# undefined_proteins = []
# undefined_proteins_dict = dict()
# files = os.listdir('./MOUSE BRAIN 2DGE PROTEINS')
# for xlx_file in files:
#     if xlx_file == 'all.xls':
#         df = hlp.read_from_xlx(pathname='./MOUSE BRAIN 2DGE PROTEINS/'+xlx_file, lbl_2d=True)
#         for index, row in df.iterrows():
#             accession_name = row['Accession Name']
#             brain = row['Brain part']
#             brain = brain.strip().replace(' ','').split(',')
#             brain = [brain_part_correspond[b] for b in brain]

#             protein_code, old_protein = uni.get_code_from_accession(accession_name)
#             if old_protein != None:
#                 if protein_code not in db_content:
#                     print('Find 2DGE')
#                     df2 = uni.get_proteins_based_on_uniprot([protein_code])
#                     protein = Protein(uniprot_entry=df2['Uniprot Entry'], 
#                                     accession_name=accession_name, 
#                                     protein_name=df2['Name'], 
#                                     organism=df2['Organism'], 
#                                     brain_parts=brain, 
#                                     biological_process=[],
#                                     molecular_function=[],
#                                     cellular_component=[],
#                                     paper=['Proteomic Analysis of Normal Murine Brain Parts (VASILIKI K. TARASLIA, ALEXANDROS KOUSKOUKIS, ATHANASIOS K. ANAGNOSTOPOULOS, DIMITRIOS J. STRAVOPODIS, LUKAS H. MARGARITIS, GEORGE TH. TSANGARIS)'])
#                     db_content[protein_code] = protein

# for key, protein in db_content.items():
#     print(protein.accession_name)  
#     # print(protein.protein_name)    
#     # print(protein.biological_process)    
#     # print(protein.molecular_function)    
#     # print(protein.cellular_component)   
#     print(protein.brain_parts)   
#     print(protein.paper)   
#     print('************************************************************************************') 

# uncommon HRMS
frames = []
undefined_proteins = []
undefined_proteins_dict = dict()
files = os.listdir('./MOUSE BRAIN PROTEOME HRMS')
for xlx_file in files:
    if xlx_file == 'all.xlsx':
        df = hlp.read_from_xlx(pathname='./MOUSE BRAIN PROTEOME HRMS/'+xlx_file)
        for index, row in df.iterrows():
            accession_name = row['Entry name']
            protein_code, old_protein = uni.get_code_from_accession(accession_name)
            if old_protein == None:
                if protein_code not in db_content:
                    print('Find HRMS')
                    brain_parts = []
                    olfactory_balb = row['Olfactory Bulb']
                    cortex = row['Cerebral cortex']
                    hippocampus = row['Hippocampus']
                    midbrain = row['Mid brain']
                    hypothalamus = row['Hypothalamus']
                    cerebellum = row['Cerebellum']
                    medulla = row['Medulla']
                    if olfactory_balb == 1:
                        brain_parts.append('Olfactory Bulb')
                    if cortex == 1:
                        brain_parts.append('Cortex')
                    if hippocampus == 1:
                        brain_parts.append('Hippocampus')
                    if hypothalamus == 1:
                        brain_parts.append('Hypothalamus')
                    if midbrain == 1:
                        brain_parts.append('Mid Brain')
                    if cerebellum == 1:
                        brain_parts.append('Cerebellum')
                    if medulla == 1:
                        brain_parts.append('Medulla')

                    df2, _, _ = uni.get_proteins_based_on_uniprot([protein_code])
                    protein = Protein(uniprot_entry=df2.iloc[0]['Uniprot Entry'], 
                                    accession_name=accession_name, 
                                    protein_name=row['Protein names'], 
                                    organism=df2.iloc[0]['Organism'], 
                                    brain_parts=brain_parts, 
                                    biological_process=[],
                                    molecular_function=[],
                                    cellular_component=[],
                                    paper=['Normal Mouse Brain Proteome II: Analysis of Brain Regions by High-resolution Mass Spectrometry (ARTEMIS G. KOROVESI, ATHANASIOS K. ANAGNOSTOPOULOS, VASILEIOS PIERROS, DIMITRIOS J. STRAVOPODIS, GEORGE TH. TSANGARIS'])
                    db_content[protein_code] = protein


#save at a csv all the content
header = ['Uniprot Entry', 'Accession Name', 'Protein Name', 'Organism', 'Brain Parts', 'Biological Process', 'Molecular Function', 'Cellular Component', 'Papers']
with open('DB_CONTENT.csv', 'w') as csv_file:  
    writer = csv.writer(csv_file)
    writer.writerow(i for i in header)
    for key, value in db_content.items():
       writer.writerow([value.uniprot_entry, 
                        value.accession_name, 
                        value.protein_name, 
                        value.organism, 
                        value.brain_parts, 
                        value.biological_process, 
                        value.molecular_function, 
                        value.cellular_component,
                        value.paper])