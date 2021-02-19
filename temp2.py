# import uniprot_database_helpets as uni


# def get_proteinID(query):
#     uniprot_data = uni.get_uniprot(query=query, query_type='ACC')
#     content = []
#     for d in uniprot_data:
#             content.append(d)   

#     for line in content:
#         if 'ID   ' in line: # Accession name of protein
#             line = line.strip().replace('ID   ','').split('   ')
#             if len(line[0]) > 2:
#                 return line[0]

# import os
# import helpers as hlp


# brain_part_correspond = {'OB':'Olfactory_balb',
#                         'HT':'Hipothalamus',
#                         'MD':'Medulla',
#                         'MB':'Mid_Brain',
#                         'HC':'Hipocampus',
#                         'CB':'Cerebellum',
#                         'CC':'Cortex'}

# frames = []
# undefined_proteins = []
# initial_papers = ['./MOUSE BRAIN 2DGE PROTEINS']
# for ini_paper in initial_papers:
#     print(ini_paper)
#     files = os.listdir(ini_paper)
#     for xlx_file in files:
#         if xlx_file == 'all.xls':
#             df = hlp.read_from_xlx(pathname=ini_paper+'/'+xlx_file, lbl_2d=True)
#             for index, row in df.iterrows():
#                 accession_name = row['Accession Name']
#                 print(accession_name)

#                 brain = row['Brain part']
#                 brain = brain.strip().replace(' ','').split(',')
#                 for b in brain:
#                     # print(b)
#                     print(brain_part_correspond[b])
#                 # if accession_name not in db_content:
#                 #     undefined_proteins.append(accession_name)

# import csv
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

import pymongo
protein1 = Protein(uniprot_entry=123, accession_name='lala', protein_name='protein1', organism='human', brain_parts=['part1', 'part2'], 
                    biological_process=['1','2','34','77'], molecular_function=[], cellular_component=['2222'], paper=['paper1'])
protein2 = Protein(uniprot_entry=133, accession_name='lolo', protein_name='protein2', organism='human', brain_parts=['part1', 'part2', 'part3'], 
                    biological_process=['1','34','77'], molecular_function=['1'], cellular_component=['2222'], paper=['paper1'])

mydict = {'key1':protein1, 'key2':protein2}

# header = ['Uniprot Entry', 'Accession Name', 'Protein Name', 'Organism', 'Brain Parts', 'Biological Process', 'Molecular Function', 'Cellular Component', 'Papers']
# with open('dict.csv', 'w') as csv_file:  
#     writer = csv.writer(csv_file)
#     writer.writerow(i for i in header)
#     for key, value in mydict.items():
#        writer.writerow([value.uniprot_entry, 
#                         value.accession_name, 
#                         value.protein_name, 
#                         value.organism, 
#                         value.brain_parts, 
#                         value.biological_process, 
#                         value.molecular_function, 
#                         value.cellular_component,
#                         value.paper])

# import os
# import helpers as hlp

# frames = []
# files = os.listdir('./MOUSE BRAIN PROTEOME HRMS')
# for xlx_file in files:
#     if xlx_file == 'all.xlsx':
#         df = hlp.read_from_xlx(pathname='./MOUSE BRAIN PROTEOME HRMS/'+xlx_file)
#         for index, row in df.iterrows():
#             brain_parts = []
#             accession_name = row['Entry name']
#             olfactory_balb = row['Olfactory Bulb']
#             cortex = row['Cerebral cortex']
#             hippocampus = row['Hippocampus']
#             midbrain = row['Mid brain']
#             hypothalamus = row['Hypothalamus']
#             cerebellum = row['Cerebellum']
#             medulla = row['Medulla']
#             if olfactory_balb == 1:
#                 brain_parts.append('Olfactory Bulb')
#             if cortex == 1:
#                 brain_parts.append('Cortex')
#             if hippocampus == 1:
#                 brain_parts.append('Hippocampus')
#             if hypothalamus == 1:
#                 brain_parts.append('Hypothalamus')
#             if midbrain == 1:
#                 brain_parts.append('Mid Brain')
#             if cerebellum == 1:
#                 brain_parts.append('Cerebellum')
#             if medulla == 1:
#                 brain_parts.append('Medulla')
#             print(brain_parts)    

    
    
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["mydatabase"]

mycol = mydb["proteins_temp"]


for key, value in mydict.items():
    x = mycol.insert_one({"UniprotEntry": value.uniprot_entry, 
                        "AccessionName": value.accession_name,
                        'Name': value.protein_name,
                        'Organism': value.organism,
                        'BrainParts': value.brain_parts,
                        'BiologicalProcess': value.biological_process,
                        'MolecularFunction': value.molecular_function,
                        'CellularComponent': value.cellular_component,
                        'Papers': value.paper})