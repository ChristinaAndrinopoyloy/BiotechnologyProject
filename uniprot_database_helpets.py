##########################################################################################
#                               Andrinopoulou Christina                                  #
#                                             ds2200013                                  #
##########################################################################################
#                                                                                        #
#                           Some functions are based on the:                             #
#  https://chem-workflows.com/articles/2019/10/29/retrieve-uniprot-data-using-python/    #
#                                                                                        #
##########################################################################################

import urllib
from bs4 import BeautifulSoup
import pandas as pd
from progress.bar import FillingCirclesBar


# get data from uniprot
def get_uniprot (query='',query_type='PDB_ID'):
    flag = False
    url = 'https://www.uniprot.org/uploadlists/'
    params = {
    'from':query_type,
    'to':'ACC',
    'format':'txt',
    'query':query
    }
    data = urllib.parse.urlencode(params)
    data = data.encode('ascii')
    request = urllib.request.Request(url, data)
    while True:
        try:
            if flag:
                print('AGAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIIIIIIIIIIIIIIIINN')
                flag = False
            with urllib.request.urlopen(request) as response:
                res = response.read()
                page=BeautifulSoup(res,features="lxml").get_text()
                page=page.splitlines()
                break
        except:
            flag = True
            print(query)
            print('EXCEPTIONNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN')
            pass    
    return page


# write the uniprot data into a csv file
def write_uniprot_on_csv(pathname, df):
    df.to_csv(pathname, index = False)


# return code for a protein
def get_code_from_accession(accession):
    uniprot_answer = get_uniprot(query=accession,query_type='ACC') # do the query to the UniProt
    flag = False
    for line in uniprot_answer:
        if 'AC   ' in line: # Accession name of protein
            codes = line.strip().replace('AC   ','').split(';')
            protein_code = codes[0]
            flag = True    

    if flag == False:   # old proteins that are deleted by the uniprot
        old_protein = accession
        protein_code = None
    else:
        old_protein = None        
    return protein_code, old_protein


# get infos for some proteins
def get_proteins_based_on_uniprot(proteins, pathname=None, write_flag=False):
    if write_flag and pathname == None:
        pathname = 'proteins.csv'
        
    df=pd.DataFrame()
    proteins_go_dict = dict()
    keywords_dict = dict()

    bar = FillingCirclesBar('Get UniProt Data', max=len(proteins))
    for index,entry in enumerate(proteins):
        data = get_uniprot(query=entry[0],query_type='ACC') # do the query to the UniProt
        organism = []
        molecular_functions = []
        molecular_functions_id = []
        biological_processes = []
        biological_processes_id = []
        cellular_components = []
        cellular_components_id = []
        keywords = []

        # entry name
        df.loc[index,'Uniprot Entry']=entry[0]
        if entry[0] not in proteins_go_dict:
            proteins_go_dict[entry[0]] = None
        if entry[0] not in keywords_dict:
            keywords_dict[entry[0]] = None    
        
        for line in data:
            if 'ID   ' in line: # Accession name of protein
                line = line.strip().replace('ID   ','').split('   ')
                df.loc[index,'Accession Name']=line[0]

            if 'DE   RecName: Full=' in line:   # Full name of protein
                line = line.strip().replace('DE   RecName: Full=','').replace(';','')
                df.loc[index,'Name']=line

            if 'OS   ' in line: # Organism
                line = line.strip().replace('OS   ','').replace('.','')
                organism.append(line)
                df.loc[index,'Organism']=(", ".join(list(set(organism))))

            if 'KW   ' in line: # Keywords
                line = line.strip().replace('KW   ','').replace('.','').split(';')
                for kw in line:
                    if kw != '':
                        keywords.append(kw)
                df.loc[index,'Keywords']=(", ".join(list(set(keywords))))

            # Gene Ontology infos
            if 'DR   GO; GO:' in line:           
                line = line.strip().replace('DR   GO; GO:','').replace(';','').split(':')
                subgraph_of_GO = line[0][-1]
                GO_id = 'GO:'+line[0][:-2]

                # molecular function
                if subgraph_of_GO == 'F':
                    molecular_functions.append(line[1])     # description
                    molecular_functions_id.append(GO_id)    # GO id
                    df.loc[index,'GO Molecular Function']=(", ".join(list(set(molecular_functions))))
                    df.loc[index,'GO ID MF']=(", ".join(list(set(molecular_functions_id))))

                elif subgraph_of_GO == 'P':
                    biological_processes.append (line[1])   # description
                    biological_processes_id.append(GO_id)   # id
                    df.loc[index,'GO Biological Process']=(", ".join(list(set(biological_processes)))) 
                    df.loc[index,'GO ID BP']=(", ".join(list(set(biological_processes_id))))

                elif subgraph_of_GO == 'C':
                    cellular_components.append (line[1])    # description
                    cellular_components_id.append(GO_id)    # id
                    df.loc[index,'GO Cellular Components']=(", ".join(list(set(cellular_components)))) 
                    df.loc[index,'GO ID CC']=(", ".join(list(set(cellular_components_id))))

                else:
                    print(subgraph_of_GO)   
          
        # make a dictionary: {protein code: (list of GO ids of molecular functions, list of GO ids of biological processes, list of GO ids of cellular components)} 
        proteins_go_dict[entry[0]] = (molecular_functions_id,biological_processes_id,cellular_components_id)
        keywords_dict[entry[0]] = ", ".join(list(set(keywords)))
        bar.next()
    bar.finish()  
    
    if write_flag:
        write_uniprot_on_csv(pathname,df)
    return df, proteins_go_dict, keywords_dict    
            