import os
import csv
import pymongo
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


class Paper:
    def __init__(self, title, authors, journal, date, link):
        self.title = title
        self.authors = authors
        self.journal = journal
        self.date = date
        self.link = link



def get_the_content_from_tsagkaris_papers():
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

    # #save at a csv all the content
    # header = ['Uniprot Entry', 'Accession Name', 'Protein Name', 'Organism', 'Brain Parts', 'Biological Process', 'Molecular Function', 'Cellular Component', 'Papers']
    # with open('DB_CONTENT.csv', 'w') as csv_file:  
    #     writer = csv.writer(csv_file)
    #     writer.writerow(i for i in header)
    #     for key, value in db_content.items():
    #     writer.writerow([value.uniprot_entry, 
    #                         value.accession_name, 
    #                         value.protein_name, 
    #                         value.organism, 
    #                         value.brain_parts, 
    #                         value.biological_process, 
    #                         value.molecular_function, 
    #                         value.cellular_component,
    #                         value.paper])



def sharma_routine():
    reader = csv.reader(open('DB_CONTENT.csv', 'r'))
    db_content = {}
    for row in reader:
        uniprot_entry, accession_name, protein_name, organism, brain_parts, biological_process, molecular_function, cellular_component  = row
        protein = Protein(uniprot_entry=uniprot_entry, 
                        accession_name=accession_name, 
                        protein_name=protein_name, 
                        organism=organism, 
                        brain_parts=brain_parts, 
                        biological_process=biological_process,
                        molecular_function=molecular_function,
                        cellular_component=cellular_component,
                        paper=[])
    if uniprot_entry not in db_content:
        db_content[uniprot_entry] = protein
    else:
        print(f'duplicate {uniprot_entry}')

    df_sharma = hlp.read_from_xlx(pathname='AllProteinsSharma.xlsx', lbl_2d=False)
    bar = FillingCirclesBar('Sharma', max=df_sharma.shape[0])
    for index, row in df_sharma.iterrows():
        accession_name = row['Entry name']
        uniprot_entry = row['Entry']
        if uniprot_entry not in db_content:
            # print(uniprot_entry)
            brain_parts = []
            olfactory_balb = row['Olfactory Bulb']
            cortex = row['Cerebral cortex']
            hippocampus = row['Hippocampus']
            thalamus = row['Thalamus']
            hypothalamus = row['Hypothalamus']
            cerebellum = row['Cerebellum']
            medulla = row['Brainstem']
            if olfactory_balb == 1:
                brain_parts.append('Olfactory Bulb')
            if cortex == 1:
                brain_parts.append('Cortex')
            if hippocampus == 1:
                brain_parts.append('Hippocampus')
            if hypothalamus == 1:
                brain_parts.append('Hypothalamus')
            if thalamus == 1:
                brain_parts.append('Mid Brain')
            if cerebellum == 1:
                brain_parts.append('Cerebellum')
            if medulla == 1:
                brain_parts.append('Medulla')
            # df2, _, _ = uni.get_proteins_based_on_uniprot([protein_code])
            protein_name = row['Protein names'].strip().replace(';','')
            protein = Protein(uniprot_entry=uniprot_entry, 
                            accession_name=accession_name, 
                            protein_name=protein_name, 
                            organism='Mus musculus (Mouse)', 
                            brain_parts=brain_parts, 
                            biological_process=[],
                            molecular_function=[],
                            cellular_component=[],
                            paper=[])
            db_content[uniprot_entry] = protein 
        bar.next()
    bar.finish()        

    #save at a csv all the content
    header = ['Uniprot Entry', 'Accession Name', 'Protein Name', 'Organism', 'Brain Parts', 'Biological Process', 'Molecular Function', 'Cellular Component']
    with open('DB_CONTENT_sharma.csv', 'w') as csv_file:  
        writer = csv.writer(csv_file)
        writer.writerow(i for i in header)
        for key, value in db_content.items():
            if value.accession_name == 'SRPK2_MOUSE':
                print(value.uniprot_entry)
                print(value.accession_name)
                print(value.protein_name)
                print(value.organism)
                print(value.brain_parts)

            writer.writerow([value.uniprot_entry, 
                            value.accession_name, 
                            value.protein_name, 
                            value.organism, 
                            value.brain_parts, 
                            value.biological_process, 
                            value.molecular_function, 
                            value.cellular_component])



def find_papers_for_each_paper():
    df_2dge = hlp.read_from_xlx(pathname='MOUSE BRAIN 2DGE PROTEINS/all.xls', lbl_2d=True)
    df_hrms = hlp.read_from_xlx(pathname='MOUSE BRAIN PROTEOME HRMS/all.xlsx', lbl_2d=False)
    df_sharma = hlp.read_from_xlx(pathname='AllProteinsSharma.xlsx', lbl_2d=False)

    accession_names_2dge = df_2dge['Accession Name'].tolist()
    accession_names_hrms = df_hrms['Entry name'].tolist()
    accession_names_sharma = df_sharma['Entry name'].tolist()

    paper_2dge = Paper(title='Proteomic Analysis of Normal Murine Brain Parts',
                        authors=['VASILIKI K. TARASLIA', 'ALEXANDROS KOUSKOUKIS', 'ATHANASIOS K. ANAGNOSTOPOULOS', 'DIMITRIOS J. STRAVOPODIS', 'LUKAS H. MARGARITIS', 'GEORGE TH. TSANGARIS'],
                        journal='Cancer Genomics & Proteomics',
                        date='May 2013',
                        link='https://pubmed.ncbi.nlm.nih.gov/23741028/')
    paper_hrms = Paper(title='Normal Mouse Brain Proteome II: Analysis of Brain Regions by High-resolution Mass Spectrometry',
                        authors=['ARTEMIS G. KOROVESI', 'ATHANASIOS K. ANAGNOSTOPOULOS', 'VASILEIOS PIERROS', 'DIMITRIOS J. STRAVOPODIS', 'GEORGE TH. TSANGARIS'],
                        journal='Cancer Genomics & Proteomics',
                        date='October 2020',
                        link='https://pubmed.ncbi.nlm.nih.gov/33099477/')
    paper_sharma = Paper(title='Cell type– and brain region–resolved mouse brain proteome',
                        authors=['Kirti Sharma', 'Sebastian Schmitt', 'Caroline G Bergner', 'Stefka Tyanova', 'Nirmal Kannaiyan', 'Natalia Manrique-Hoyos', 'Karina Kongi', 'Ludovico Cantuti', 'Uwe-Karsten Hanisch', 'Mari-Anne Philips', 'Moritz J Rossner', 'Matthias Mann', 'Mikael Simons'],
                        journal='nature neuroscience',
                        date='November 2015',
                        link='https://www.nature.com/articles/nn.4160')

    reader = csv.reader(open('DB_CONTENT_FINAL.csv', 'r'))
    db_content = {}
    for row in reader:
        papers_list = []

        uniprot_entry, accession_name, protein_name, organism, brain_parts, biological_process, molecular_function, cellular_component  = row
  
        if accession_name in accession_names_2dge:
            papers_list.append(paper_2dge)
        if accession_name in accession_names_hrms:
            papers_list.append(paper_hrms)    
        if accession_name in accession_names_sharma:
            papers_list.append(paper_sharma) 

        protein = Protein(uniprot_entry=uniprot_entry, 
                        accession_name=accession_name, 
                        protein_name=protein_name, 
                        organism=organism, 
                        brain_parts=brain_parts, 
                        biological_process=biological_process,
                        molecular_function=molecular_function,
                        cellular_component=cellular_component,
                        paper=papers_list)
        if uniprot_entry not in db_content:                    
            db_content[uniprot_entry] = protein
        else:
            print(f'duplicate {uniprot_entry}')
    return db_content



def construct_database(db_content):
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["PROTEINS_DB"]
    mycol = mydb["proteins"]
    for key, value in db_content.items():
        brain_parts_list = value.brain_parts.strip().replace('[','').replace(']','').replace('\'','').split(',')
        bp_list = value.biological_process.strip().replace('[','').replace(']','').replace('\'','').split(',')
        mf_list = value.molecular_function.strip().replace('[','').replace(']','').replace('\'','').split(',')
        cc_list = value.cellular_component.strip().replace('[','').replace(']','').replace('\'','').split(',')

        x = mycol.insert_one({"UniprotEntry": value.uniprot_entry, 
                            "AccessionName": value.accession_name,
                            'Name': value.protein_name,
                            'Organism': value.organism,
                            'BrainParts': brain_parts_list,
                            'BiologicalProcess': bp_list,
                            'MolecularFunction': mf_list,
                            'CellularComponent': cc_list,
                            'Papers': [{'Title': p.title, 'Authors': p.authors, 'Journal': p.journal, 'Date': p.date, 'Link': p.link} for p in value.paper]})           


def check_for_duplicates():
    reader = csv.reader(open('DB_CONTENT.csv', 'r'))
    db_content = {}
    papers_list = []
    for row in reader:
        uniprot_entry, accession_name, protein_name, organism, brain_parts, biological_process, molecular_function, cellular_component  = row
        if uniprot_entry not in db_content:
            protein = Protein(uniprot_entry=uniprot_entry, 
                            accession_name=accession_name, 
                            protein_name=protein_name, 
                            organism=organism, 
                            brain_parts=brain_parts, 
                            biological_process=biological_process,
                            molecular_function=molecular_function,
                            cellular_component=cellular_component,
                            paper=[])
            db_content[uniprot_entry] = protein
        else:
            brain_parts_list1 = brain_parts.strip().replace('[','').replace(']','').replace('\'','').split(',')
            brain_parts_list2 = db_content[uniprot_entry].brain_parts.strip().replace('[','').replace(']','').replace('\'','').split(',')

            new_brain_parts = brain_parts_list1 + brain_parts_list2
            new_brain_parts = hlp.flatten_of_list([new_brain_parts])
            new_brain_parts = hlp.remove_duplicates_of_list(new_brain_parts)

            db_content[uniprot_entry].protein_name = protein_name
            db_content[uniprot_entry].brain_parts = new_brain_parts
            header = ['Uniprot Entry', 'Accession Name', 'Protein Name', 'Organism', 'Brain Parts', 'Biological Process', 'Molecular Function', 'Cellular Component']
            with open('DB_CONTENT_FINAL.csv', 'w') as csv_file:  
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
                                    value.cellular_component])




            


if __name__ == "__main__":
    # check_for_duplicates()
    # db_content = sharma_routine()
    db_content = find_papers_for_each_paper()  
    construct_database(db_content)                
    # print('Check Database')            