##########################################################################################
#                               Andrinopoulou Christina                                  #
#                                             ds2200013                                  #
##########################################################################################

import uniprot_database_helpets as uni
import go_helpers as go
import helpers as hlp
import routines as rout
import bonus_papers as papers
import pandas as pd
import click
import numpy as np
from progress.bar import FillingCirclesBar

avaliable_pipelines = ['full', 'go', 'analysis', 'statistics', 'bonus_paper']
avaliable_approaches = ['unique', 'simple']
avaliable_brain_parts = ['cerebellum', 'cortex', 'hippocampus', 'hypothalamus', 'medulla', 'mid_brain', 'olfactory_bulb']
avaliable_bonus_papers = ['1', '2']
@click.command()
@click.option("--pipeline", type=click.Choice(avaliable_pipelines, case_sensitive=False), default='full', help="The pipeline of the program", show_default=True)
@click.option("--approach", type=click.Choice(avaliable_approaches, case_sensitive=False), default='unique', help="The approach that used in order to find the proteins of the two methods: 2DGE, HRMS", show_default=True)
@click.option("--brain_part", type=click.Choice(avaliable_brain_parts, case_sensitive=False), default='cerebellum', help="Brain part", show_default=True)
@click.option("--paper_no", type=click.Choice(avaliable_bonus_papers, case_sensitive=False), default='2', help="Paper1:jung2017 and Paper2:sharma", show_default=True)
@click.option('--expand_labels', is_flag=False, help='Give the opportunity to replace a GO term with the corresponding children terms', show_default=True)
def protein_GO_relationship(pipeline, approach, brain_part, paper_no, expand_labels):
    '''A python program that discovers the relationship between some proteins and the Gene Ontology'''

    # find the excel files and the pathnames that we are going to use later on
    if pipeline != 'bonus_paper':
        common_name, \
        unique_name1, unique_name2, \
        merged_pathname, \
        pathname, pathname_all_infos, pathname_all_infos2, \
        mf_pathname, bp_pathname, cc_pathname, kw_pathname, \
        statistical_pathname_mf, statistical_pathname_bp, statistical_pathname_cc = rout.find_the_appropriate_files(approach, brain_part)
    else:
        approach = 'BONUS_PAPERS'
        brain_part = 'all'
        _, _, _, _, pathname, pathname_all_infos, pathname_all_infos2, \
        mf_pathname, bp_pathname, cc_pathname, kw_pathname, \
        statistical_pathname_mf, statistical_pathname_bp, statistical_pathname_cc = rout.find_the_appropriate_files(approach, brain_part, paper=paper_no)


    # Gene Ontology
    godag = go.load_basic_go()

    if pipeline == 'full':
        # merge the excel files from part 1 of the project
        proteins_df = hlp.merge_excels(common_name, 
                                        unique_name1, 
                                        unique_name2, 
                                        write_flag=True,
                                        pathname=merged_pathname)
        accesion_names_of_proteins = proteins_df.values.tolist()
        print('\nThe proteins from the different excel files are merged')

        proteins = []
        deleted_proteins = []

        bar = FillingCirclesBar('Find the protein code for each protein, based on the accession name', max=len(accesion_names_of_proteins))
        # find the uniprot entry code
        for protein in accesion_names_of_proteins:
            code, old_protein = uni.get_code_from_accession(protein[0])
            if old_protein == None:
                proteins.append((code,protein))
            else:
                print(f'\nThe protein {old_protein} was deleted!')
                deleted_proteins.append(protein)
            bar.next()
        bar.finish()    
        hlp.write_on_csv(list_of_tuples=proteins, pathname=pathname)    # save the results    
   
    if pipeline == 'bonus_paper':
        if paper_no == str(1):
            brainpart_proteins_dictionary = papers.paper1_routine()
        else:      
            brainpart_proteins_dictionary = papers.paper2_routine()

        df_temp = pd.DataFrame.from_dict(brainpart_proteins_dictionary, orient='index')
        df_temp.to_csv('temp.csv')

    # GO Step
    if pipeline == 'go' or pipeline == 'full' or pipeline == 'bonus_paper':
        print(pathname)
        proteins_df = pd.read_csv(pathname)
        proteins = proteins_df['Uniprot Entry'].values.tolist()
        if pipeline == 'bonus_paper':
            if paper_no == str(1):
                bar = FillingCirclesBar('Find the protein code for each protein, based on the accession name', max=len(proteins))
                # find the uniprot entry code
                proteins2 = []
                for protein in proteins:
                    code, old_protein = uni.get_code_from_accession(protein)
                    if old_protein == None:
                        proteins2.append((code,protein))
                    else:
                        print(f'\nThe protein {old_protein} was deleted!')
                    bar.next()
                bar.finish()    
                hlp.write_on_csv(list_of_tuples=proteins2, pathname=pathname)    # save the results 
            else:
                temp_proteins = proteins
                proteins = []
                bar = FillingCirclesBar('Check for obselete proteins', max=len(temp_proteins))
                for prot in temp_proteins:
                    if uni.check_protein_existance(prot) == prot:
                        proteins.append(prot)
                    else:
                        print('hello')
                    bar.next()
                bar.finish()    

        print(proteins)
        proteins = hlp.remove_duplicates_of_list(proteins)
        print(len(proteins))
              
        # find the GO terms for each protein      
        protein_table, proteins_GO_dict, keywords_dict = uni.get_proteins_based_on_uniprot(proteins, write_flag=True, pathname=pathname_all_infos)

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

        # save the results
        df_mf_anc = pd.DataFrame.from_dict(molecular_function_ancestors, orient='index')
        df_bp_anc = pd.DataFrame.from_dict(biological_processes_ancestors, orient='index')
        df_cc_anc = pd.DataFrame.from_dict(cellular_components_ancestors, orient='index')
        df_kw = pd.DataFrame.from_dict(keywords_dict, orient='index')
        df_mf_anc.to_csv(mf_pathname, header=False)
        df_bp_anc.to_csv(bp_pathname, header=False)
        df_cc_anc.to_csv(cc_pathname, header=False)
        df_kw.to_csv(kw_pathname, header=False)

    # Analysis Step
    if pipeline == 'analysis' or pipeline == 'full' or pipeline == 'bonus_paper':
        # take all the GO terms of a specific level of the DAG
        bp_labels = go.get_children('GO:0008150', godag, level=1)
        mf_labels = go.get_children('GO:0003674', godag, level=1)
        cc_labels = go.get_children('GO:0005575', godag, level=1)
    
        # take the children of some go terms based on the user's preferences
        if expand_labels:
            subontologies, go_terms = rout.speak_with_the_user(bp_labels, mf_labels, cc_labels, godag)

            for i in range(len(subontologies)):     
                terms = go_terms[i]
                for trm in terms:       
                    children = go.get_children(trm, godag, level=1)
                    if trm in bp_labels:
                        bp_labels.remove(trm)
                        bp_labels.extend(children)
                    if trm in mf_labels:
                        mf_labels.remove(trm)
                        mf_labels.extend(children)
                    if trm in cc_labels:
                        cc_labels.remove(trm)
                        cc_labels.extend(children)

        molecular_function_ancestors = hlp.from_csv_to_dict(pathname=mf_pathname)
        biological_processes_ancestors = hlp.from_csv_to_dict(pathname=bp_pathname)
        cellular_components_ancestors = hlp.from_csv_to_dict(pathname=cc_pathname)

        df = pd.read_csv(pathname_all_infos)
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
                    labels_1.append(hlp.intersection_of_lists(bp_labels, biological_processes_ancestors[bp].strip().replace(' ','').split(',')))
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
                    labels_2.append(hlp.intersection_of_lists(mf_labels, molecular_function_ancestors[mf].strip().replace(' ','').split(',')))
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
                    labels_3.append(hlp.intersection_of_lists(cc_labels, cellular_components_ancestors[cc].strip().replace(' ','').split(',')))
                    if labels_3 == []:  # the cellular component of the protein is a label
                        labels_3.append(cc)
                labels_3 = hlp.flatten_of_list(labels_3)
                labels_3 = hlp.remove_duplicates_of_list(labels_3)
                df.loc[index, 'Cellular Component Label'] = (", ".join(list(set(labels_3))))
            bar.next()
        bar.finish()

        df.to_csv(pathname_all_infos2)


    # Statistics Step: make bar plots
    if pipeline == 'statistics' or pipeline == 'full' or pipeline == 'analysis' or pipeline == 'bonus_paper':
        print('Statistics step')      
        df = pd.read_csv(pathname_all_infos2)
        print(pathname_all_infos2)

        if pipeline == 'bonus_paper':
            col_names = list(df.columns)
            for key, value in brainpart_proteins_dictionary.items():    # for each brain part
                print('=======================--------------------======================')
                print(key)
                print(value)
                temp_pathname = './MERGED/'+approach+'/PAPER'+str(paper_no)+'/'+key+'/all_infos2.csv'
                temp_content_of_df = []
                for index, row in df.iterrows():    # for each protein of the paper
                    if row['Uniprot Entry'] in value:   # if the protein belongs to the current brain part
                        temp_content_of_df.append(row.tolist())  # keep it
                df_brainpart = pd.DataFrame(temp_content_of_df, columns =col_names)   # and save it  
                df_brainpart.to_csv(temp_pathname)
                biological_process_labels = df_brainpart["Biological Process Label"].tolist()
                molecular_function_labels = df_brainpart["Molecular Function Label"].tolist()
                cellular_component_labels = df_brainpart["Cellular Component Label"].tolist()

                biological_process_labels = hlp.split_items_of_list(biological_process_labels)
                molecular_function_labels = hlp.split_items_of_list(molecular_function_labels)
                cellular_component_labels = hlp.split_items_of_list(cellular_component_labels)

                rout.statistics_routine(molecular_function_labels, godag, './MERGED/'+approach.upper()+'/PAPER'+str(paper_no)+'/'+key+'/statistical_'+key+'_mf.csv', title='Molecular Function')
                rout.statistics_routine(cellular_component_labels, godag, './MERGED/'+approach.upper()+'/PAPER'+str(paper_no)+'/'+key+'/statistical_'+key+'_cc.csv', title='Cellular Component')
                rout.statistics_routine(biological_process_labels, godag, './MERGED/'+approach.upper()+'/PAPER'+str(paper_no)+'/'+key+'/statistical_'+key+'_bp.csv', title='Biological Process')
        else:    
            biological_process_labels = df["Biological Process Label"].tolist()
            molecular_function_labels = df["Molecular Function Label"].tolist()
            cellular_component_labels = df["Cellular Component Label"].tolist()

            biological_process_labels = hlp.split_items_of_list(biological_process_labels)
            molecular_function_labels = hlp.split_items_of_list(molecular_function_labels)
            cellular_component_labels = hlp.split_items_of_list(cellular_component_labels)

            rout.statistics_routine(molecular_function_labels, godag, statistical_pathname_mf, title='Molecular Function')
            rout.statistics_routine(cellular_component_labels, godag, statistical_pathname_cc, title='Cellular Component')
            rout.statistics_routine(biological_process_labels, godag, statistical_pathname_bp, title='Biological Process')


    print('END')   
    

if __name__ == '__main__':
    protein_GO_relationship()    