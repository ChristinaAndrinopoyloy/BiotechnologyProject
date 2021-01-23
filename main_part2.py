import uniprot_database_helpets as uni
import go_helpers as go
import helpers as hlp
import pandas as pd
import click

avaliable_pipelines = ['full', 'go']
@click.command()
@click.option("--pipeline", type=click.Choice(avaliable_pipelines, case_sensitive=False), default='full', help="The pipeline of the program", show_default=True)
@click.option('--common_name', default='./Results/UNIQUE/Olfactory_balb/common_proteins_Olfactory_balb.xls', help='Name of the common excel file')
@click.option('--unique_name1', default='./Results/UNIQUE/Olfactory_balb/HRMS_unique_proteins_Olfactory_balb.xls', help='Name of the unique excel file 1')
@click.option('--unique_name2', default='./Results/UNIQUE/Olfactory_balb/2DGE_unique_proteins_Olfactory_balb.xls', help='Name of the unique excel file 2')
@click.option('--merged_pathname', default='./MERGED/UNIQUE/Olfactory_balb/proteins_merged.csv', help='Path of the merged csv')
@click.option('--pathname', default='./MERGED/UNIQUE/Olfactory_balb/proteins_essential.csv', help='Path of the csv')
@click.option('--mf_pathname', default='./MERGED/UNIQUE/Olfactory_balb/molecular_function.csv', help='Path of the molecular function csv')
@click.option('--bp_pathname', default='./MERGED/UNIQUE/Olfactory_balb/biological_process.csv', help='Path of the biological process csv')
@click.option('--cc_pathname', default='./MERGED/UNIQUE/Olfactory_balb/cellular_component.csv', help='Path of the cellular component csv')

def protein_GO_relationship(pipeline, common_name, unique_name1, unique_name2, merged_pathname, pathname, mf_pathname, bp_pathname, cc_pathname):
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
   
    if pipeline == 'go':
        proteins_df = pd.read_csv(pathname)
        proteins = proteins_df.values.tolist()
        
        print('Find the proteins\' GO terms')      
        protein_table, proteins_GO_dict = uni.get_proteins_based_on_uniprot(proteins, write_flag=True, pathname='proteins.csv')

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

        df_mf_anc.to_csv(mf_pathname)
        df_bp_anc.to_csv(bp_pathname)
        df_cc_anc.to_csv(cc_pathname)





    print('END')   
    

if __name__ == '__main__':
    protein_GO_relationship()    