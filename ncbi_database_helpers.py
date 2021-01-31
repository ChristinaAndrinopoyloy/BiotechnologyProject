from Bio import Entrez
import xmltodict


def get_content_from_ncbi(query=None):
    Entrez.email = "Your.Name.Here@example.org"

    flag = False
    while True:
        try:
            if flag:
                flag = False
            with Entrez.efetch(db="Protein", id=query, rettype="gb", retmode="text") as handle:
                content = handle.read().strip().split('//')
                break    
        except:
            flag = True
            print('NCBI: Try again!')
            print(query)
            pass    

    ncbi_infos = dict()
    for cnt in content:
        protein_content = cnt.strip().split('\n')
        for line in protein_content:
            line = line.replace('   ', ' ').split(' ')
            if line[0] == 'DEFINITION':
                definition = line
                definition.remove('DEFINITION')
                definition.remove('')
                definition = " ".join(definition) 
            if line[0] == 'VERSION':
                version = line
                version.remove('VERSION')
                version.remove('')
                version = "".join(version) 
        if version[:2] != 'XP_':
            ncbi_infos[version] = definition

    return ncbi_infos
    