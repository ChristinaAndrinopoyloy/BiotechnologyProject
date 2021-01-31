import pymongo
import pandas as pd
import helpers as hlp


class Protein:
  def __init__(self, uniprot_entry, accession_name, name=None, organism=None):
    self.uniprot_entry = uniprot_entry
    self.accession_name = accession_name 
    self.name = name
    self.organism = organism 
    self.brain_parts = []
    self.biological_process = [] 
    self.molecular_function = [] 
    self.cellular_component = []
    self.paper = []

  def update_brain_parts(self, brain_part):
      self.brain_parts.append(brain_part)    



class GO_term:
    def __init__(self, go_id, go_name, kind, go_ancestors, go_children):
        self.go_id = go_id
        self.go_name = go_name 
        self.kind = kind
        self.go_ancestors = go_ancestors
        self.children = go_children


class Brain_Part:
    def __init__(self, brain_part, unique):
        self.brain_part = brain_part


class Paper:
    def __init__(self, title, authors):
        self.title = title
        self.authors - authors


def search_in_list(value, my_list):
    returned_value = []
    if my_list == []:
        return returned_value
    returned_value = [element for element in my_list if element.uniprot_entry == value]
    return returned_value


def collect_all_infos_about_proteins():
    brain_parts = ['Cerebellum', 'Cortex', 'Hipocampus', 'Hipothalamus', 'Medulla', 'Mid_Brain', 'Olfactory_balb']
    for bp in brain_parts:
        pathname1 = './MERGED/UNIQUE/'+bp+'/proteins_essential.csv'
        pathname2 = './MERGED/UNIQUE/'+bp+'/proteins_essential.csv'





















def create_DB():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    my_db = myclient["ProteinsDB"]
    my_collection = my_db["proteins"]

    brain_parts = ['Cerebellum', 'Cortex', 'Hipocampus', 'Hipothalamus', 'Medulla', 'Mid_Brain', 'Olfactory_balb']

    db_content = []
    
    for bp in brain_parts:
        pathname = './MERGED/UNIQUE/'+bp+'/proteins_essential.csv'
        df = pd.read_csv(pathname)
        for ind in df.index: 
            uniprot_entry = df['Uniprot Entry'][ind]
            temp_protein_obj = search_in_list(value=uniprot_entry, my_list=db_content)

            my_brain_part = Brain_Part(brain_part=hlp.correct_brainpart(bp))

            if temp_protein_obj !=[]:
                print(f'{temp_protein_obj[0].uniprot_entry} already exists')
                temp_protein_obj[0].update_brain_parts(vars(my_brain_part))
                print(f'{temp_protein_obj[0].brain_parts} update')

            else:    
                accession_name = df['Accession Name'][ind]
                my_protein = Protein(uniprot_entry=uniprot_entry,
                                    accession_name=accession_name[2:-2])
                my_protein.update_brain_parts(vars(my_brain_part))
                db_content.append(my_protein)

            

    db_content = [vars(item) for item in db_content]
    # print(db_content)
    x = my_collection.insert_many(db_content)

create_DB()    