import uniprot_database_helpets as uni
import go_helpers as go
import helpers as hlp
import pandas as pd
import click
from collections import Counter

avaliable_pipelines = ['full', 'go', 'analysis']
@click.command()
@click.option("--pipeline", type=click.Choice(avaliable_pipelines, case_sensitive=False), default='full', help="The pipeline of the program", show_default=True)
@click.option('--common_name', default='./Results/UNIQUE/Olfactory_balb/common_proteins_Olfactory_balb.xls', help='Name of the common excel file')
@click.option('--unique_name1', default='./Results/UNIQUE/Olfactory_balb/HRMS_unique_proteins_Olfactory_balb.xls', help='Name of the unique excel file 1')
@click.option('--unique_name2', default='./Results/UNIQUE/Olfactory_balb/2DGE_unique_proteins_Olfactory_balb.xls', help='Name of the unique excel file 2')
@click.option('--merged_pathname', default='./MERGED/UNIQUE/Olfactory_balb/proteins_merged.csv', help='Path of the merged csv')
@click.option('--pathname', default='./MERGED/UNIQUE/Olfactory_balb/proteins_essential.csv', help='Path of the csv')
@click.option('--pathname_all_infos', default='./MERGED/UNIQUE/Olfactory_balb/all_infos.csv', help='Path of the csv which contains all infos for each protein')
@click.option('--mf_pathname', default='./MERGED/UNIQUE/Olfactory_balb/molecular_function.csv', help='Path of the molecular function csv')
@click.option('--bp_pathname', default='./MERGED/UNIQUE/Olfactory_balb/biological_process.csv', help='Path of the biological process csv')
@click.option('--cc_pathname', default='./MERGED/UNIQUE/Olfactory_balb/cellular_component.csv', help='Path of the cellular component csv')
@click.option('--kw_pathname', default='./MERGED/UNIQUE/Olfactory_balb/kewords.csv', help='Path of the keywords csv')
def protein_GO_relationship(pipeline, common_name, unique_name1, unique_name2, merged_pathname, pathname, pathname_all_infos, mf_pathname, bp_pathname, cc_pathname, kw_pathname):
    '''A python program for the relationship of some proteins with the Gene Ontology'''
    
    # Gene Ontology
    godag = go.load_basic_go()

    ########################################## pipeline #################################################
    if pipeline == 'full':
        proteins_df = hlp.merge_excels(common_name, 
                                        unique_name1, 
                                        unique_name2, 
                                        write_flag=True,
                                        pathname=merged_pathname)
        accesion_names_of_proteins = proteins_df.values.tolist()
        print('The proteins from the different excel files are merged')

        proteins = []
        deleted_proteins = []

        print('Find the protein code for each protein, based on the accession name')
        for protein in accesion_names_of_proteins:
            code, old_protein = uni.get_code_from_accession(protein[0])
            if old_protein == None:
                proteins.append((code,protein))
            else:
                print(f'The protein {old_protein} was deleted!')
                deleted_proteins.append(protein)
        hlp.write_on_csv(list_of_tuples=proteins, pathname=pathname)        
        print('The protein codes are ready')
    #######################################################################################################
   
    if pipeline == 'go' or pipeline == 'full':
        proteins_df = pd.read_csv(pathname)
        proteins = proteins_df.values.tolist()
        
        print('Find the proteins\' GO terms')      
        protein_table, proteins_GO_dict, keywords_dict = uni.get_proteins_based_on_uniprot(proteins, write_flag=True, pathname=pathname_all_infos)

        print('Divide the GO terms into 3')
        molecular_function_ancestors = dict()
        biological_processes_ancestors = dict()
        cellular_components_ancestors = dict()
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

        df_mf_anc = pd.DataFrame.from_dict(molecular_function_ancestors, orient='index')
        df_bp_anc = pd.DataFrame.from_dict(biological_processes_ancestors, orient='index')
        df_cc_anc = pd.DataFrame.from_dict(cellular_components_ancestors, orient='index')
        df_kw = pd.DataFrame.from_dict(keywords_dict, orient='index')

        df_mf_anc.to_csv(mf_pathname, header=False)
        df_bp_anc.to_csv(bp_pathname, header=False)
        df_cc_anc.to_csv(cc_pathname, header=False)
        df_kw.to_csv(kw_pathname, header=False)

    if pipeline == 'analysis':
        # keyword labels
        # keywords_dict = hlp.from_csv_to_dict(pathname=kw_pathname)
        # temp_list = []
        # all_keywords = []
        # for key, value in keywords_dict.items():
        #     for v in value.strip().split(','):
        #         while v[0] == ' ':
        #             v = v[1:]
        #         temp_list.append(v.lower())
        # [all_keywords.append(item) for item in temp_list if item not in all_keywords]   # remove duplicates
        # print(all_keywords)
        # print('-'*100)

        molecular_function_ancestors = hlp.from_csv_to_dict(pathname=mf_pathname)
        # all_ancestors = hlp.get_values_from_dict(molecular_function_ancestors, godag)
        # print(all_ancestors)
        # print('-'*100) 
        # labels = list(set(all_ancestors).intersection(all_keywords))
        # print(labels)
        # print('='*100)

        biological_processes_ancestors = hlp.from_csv_to_dict(pathname=bp_pathname)
        # all_ancestors = hlp.get_values_from_dict(biological_processes_ancestors, godag)
        # print(all_ancestors)
        # print('-'*100)
        # labels = list(set(all_ancestors).intersection(all_keywords))
        # print(labels)
        # print('='*100)

        cellular_components_ancestors = hlp.from_csv_to_dict(pathname=cc_pathname)
        # all_ancestors = hlp.get_values_from_dict(cellular_components_ancestors, godag)
        # print(all_ancestors)
        # print('-'*100)
        # labels = list(set(all_ancestors).intersection(all_keywords))
        # print(labels)
        # print('='*100)
        df = pd.read_csv(pathname_all_infos)
        for index, row in df.iterrows():
            print(row['Uniprot Entry'])
            biological_process = row['GO ID BP']
            if not pd.isna(row['GO ID BP']):
                biological_process = biological_process.strip().replace(' ','').split(',')
                common_ancestors = go.find_common_ancestors(biological_process,godag)
                print(common_ancestors)
            molecular_function = row['GO ID MF']
            if not pd.isna(row['GO ID MF']):
                molecular_function = molecular_function.strip().replace(' ','').split(',')
            cellular_component = row['GO ID CC']
            if not pd.isna(row['GO ID CC']):
                cellular_component = cellular_component.strip().replace(' ','').split(',')

            
                

    print('END')   
    

if __name__ == '__main__':
    protein_GO_relationship()    