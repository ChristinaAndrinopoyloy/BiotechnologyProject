import os
import csv
import pymongo
import pandas as pd
import numpy as np
from progress.bar import FillingCirclesBar

import helpers as hlp
import go_helpers as go
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
    # bar = FillingCirclesBar('Sharma', max=df_sharma.shape[0])
    for index, row in df_sharma.iterrows():
        accession_name = row['Entry name']
        uniprot_entry = row['Entry']
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
            brain_parts.append('Thalamus')
        if cerebellum == 1:
            brain_parts.append('Cerebellum')
        if medulla == 1:
            brain_parts.append('Medulla')
        if uniprot_entry not in db_content:
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
        else:
            print(db_content[uniprot_entry].brain_parts)

            if type(db_content[uniprot_entry].brain_parts) == str:
                temp = db_content[uniprot_entry].brain_parts.strip().replace('[','').replace(']','').replace('\'','').replace(' ','').split(',')
                db_content[uniprot_entry].brain_parts = temp
            for bp in brain_parts:
                if bp not in db_content[uniprot_entry].brain_parts:
                    db_content[uniprot_entry].brain_parts.append(bp)
            print(db_content[uniprot_entry].brain_parts)
            print('-'*100)

            # print(db_content[uniprot_entry].brain_parts)   

        # bar.next()
    # bar.finish()        

    #save at a csv all the content
    header = ['Uniprot Entry', 'Accession Name', 'Protein Name', 'Organism', 'Brain Parts', 'Biological Process', 'Molecular Function', 'Cellular Component']
    with open('DB_CONTENT_sharma.csv', 'w') as csv_file:  
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
        brain_parts_list = value.brain_parts.strip().replace('[','').replace(']','').replace('\'','').replace(' ','').split(',')
        for index in range(len(brain_parts_list)):
            if brain_parts_list[index] == 'Hipothalamus':
                brain_parts_list[index] = 'Hypothalamus'
            if brain_parts_list[index] == 'Hipocampus':
                brain_parts_list[index] = 'Hippocampus'
            if brain_parts_list[index] == 'Olfactory_balb':
                brain_parts_list[index] = 'Olfactory bulb'
            if brain_parts_list[index] == 'OlfactoryBulb':
                brain_parts_list[index] = 'Olfactory bulb'
            if brain_parts_list[index] == 'Mid_Brain':
                brain_parts_list[index] = 'Midbrain'            
        bp_list = value.biological_process.strip().replace('[','').replace(']','').replace('\'','').replace(' ','').split(',')
        mf_list = value.molecular_function.strip().replace('[','').replace(']','').replace('\'','').replace(' ','').split(',')
        cc_list = value.cellular_component.strip().replace('[','').replace(']','').replace('\'','').replace(' ','').split(',')

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



def find_GO_labels_sharma():
    godag = go.load_basic_go()


    df_sharma = hlp.read_from_xlx(pathname='AllProteinsSharma.xlsx', lbl_2d=False)
    proteins = []
    proteins = df_sharma['Entry'].tolist()

    # protein_table, proteins_GO_dict, keywords_dict = uni.get_proteins_based_on_uniprot(proteins)
    protein_table, proteins_GO_dict, keywords_dict = uni.get_proteins_based_on_uniprot(proteins, write_flag=True, pathname='sharma_uniprot.csv')
    
    molecular_function_ancestors = dict()
    biological_processes_ancestors = dict()
    cellular_components_ancestors = dict()
            
    bar = FillingCirclesBar('Divide the GO terms into 3', max=len(proteins_GO_dict))
    # divide the GO terms in: Biological Process terms, Molecular Function terms and Cellular Component terms
    # and find all the ancestors for each term of each protein
    for protein_code, go_subgraphs in proteins_GO_dict.items():
        # molecular function
        for go_id in go_subgraphs[0]:
            if go_id not in molecular_function_ancestors:
                molecular_function_ancestors[go_id] = []
                ancestors = go.get_ancestors(godag=godag, GO_ID=go_id)
                molecular_function_ancestors[go_id].append(ancestors)

        # biological process
        for go_id in go_subgraphs[1]:
            if go_id not in biological_processes_ancestors:
                biological_processes_ancestors[go_id] = []
                ancestors = go.get_ancestors(godag=godag, GO_ID=go_id)
                biological_processes_ancestors[go_id].append(ancestors)        
        
        # cellular components
        for go_id in go_subgraphs[2]:
            if go_id not in cellular_components_ancestors:
                cellular_components_ancestors[go_id] = []
                ancestors = go.get_ancestors(godag=godag, GO_ID=go_id)
                cellular_components_ancestors[go_id].append(ancestors)      
        bar.next()
    bar.finish()

    # take all the GO terms of a specific level of the DAG
    bp_labels = go.get_children('GO:0008150', godag, level=1)
    mf_labels = go.get_children('GO:0003674', godag, level=1)
    cc_labels = go.get_children('GO:0005575', godag, level=1)

    df = pd.read_csv('sharma_uniprot.csv')
    df["Biological Process Label"] = np.nan
    df["Molecular Function Label"] = np.nan
    df["Cellular Component Label"] = np.nan        

    bar = FillingCirclesBar('Find the GO term labels for each protein', max=df.shape[0])
    # find the GO labels for each protein
    for index, row in df.iterrows():    # for each protein
        labels_1 = []
        labels_2 = []
        labels_3 = []

        biological_process = row['GO ID BP']    # get all the corresponding biological processes
        if not pd.isna(row['GO ID BP']):
            biological_process = biological_process.strip().replace(' ','').split(',')
            for bp in biological_process:   # for each biological process of a protein
                # get the intersection of the general biological processes labels and the ancestors of this specific biological process
                labels_1.append(hlp.intersection_of_lists(bp_labels, list(biological_processes_ancestors[bp][0])))
                if labels_1 == []:  # the biological process of the protein is a label
                    labels_1.append(bp)
            labels_1 = hlp.flatten_of_list(labels_1)
            labels_1 = hlp.remove_duplicates_of_list(labels_1)
            df.loc[index, 'Biological Process Label'] = (", ".join(list(set(labels_1))))
                        
        molecular_function = row['GO ID MF']
        if not pd.isna(row['GO ID MF']):
            molecular_function = molecular_function.strip().replace(' ','').split(',')
            for mf in molecular_function:   # for each molecular function of a protein
                # get the intersection of the general molecular function labels and the ancestors of this specific molecular function
                labels_2.append(hlp.intersection_of_lists(mf_labels, list(molecular_function_ancestors[mf][0])))
                if labels_2 == []:  # the molecular function of the protein is a label
                    labels_2.append(mf)
            labels_2 = hlp.flatten_of_list(labels_2)
            labels_2 = hlp.remove_duplicates_of_list(labels_2)
            df.loc[index, 'Molecular Function Label'] = (", ".join(list(set(labels_2))))

        cellular_component = row['GO ID CC']
        if not pd.isna(row['GO ID CC']):
            cellular_component = cellular_component.strip().replace(' ','').split(',')
            for cc in cellular_component:   # for each cellular component of a protein
                # get the intersection of the general cellular component labels and the ancestors of this specific cellular component
                labels_3.append(hlp.intersection_of_lists(cc_labels, list(cellular_components_ancestors[cc][0])))
                if labels_3 == []:  # the cellular component of the protein is a label
                    labels_3.append(cc)
            labels_3 = hlp.flatten_of_list(labels_3)
            labels_3 = hlp.remove_duplicates_of_list(labels_3)
            df.loc[index, 'Cellular Component Label'] = (", ".join(list(set(labels_3))))
        bar.next()
    bar.finish()

    df.to_csv('sharma_uniprot2.csv')

if __name__ == "__main__":
    find_GO_labels_sharma()
    # check_for_duplicates()
    # db_content = sharma_routine()
    # db_content = find_papers_for_each_paper()  
    # construct_database(db_content)                
    # print('Check Database')            