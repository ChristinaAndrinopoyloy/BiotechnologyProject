##########################################################################################
#                               Andrinopoulou Christina                                  #
#                                             ds2200013                                  #
##########################################################################################

import helpers as hlp
import go_helpers as go
import pandas as pd
from collections import Counter
from progress.bar import FillingCirclesBar



def find_the_appropriate_files(approach, brain_part,paper=1):
    if brain_part == 'cerebellum':
        brain_part = 'Cerebellum'
    if brain_part == 'cortex':
        brain_part = 'Cortex' 
    if brain_part == 'hippocampus':
        brain_part = 'Hipocampus'      
    if brain_part == 'hypothalamus':
        brain_part = 'Hipothalamus'
    if brain_part == 'medulla':
        brain_part = 'Medulla'
    if brain_part == 'mid_brain':
        brain_part = 'Mid_Brain'
    if brain_part == 'olfactory_bulb':
        brain_part = 'Olfactory_balb'            

    if approach != 'BONUS_PAPERS':
        common_name = './Results/'+approach.upper()+'/'+brain_part+'/common_proteins_'+brain_part+'.xls'
        unique_name1 = './Results/'+approach.upper()+'/'+brain_part+'/HRMS_unique_proteins_'+brain_part+'.xls'
        unique_name2 = './Results/'+approach.upper()+'/'+brain_part+'/2DGE_unique_proteins_'+brain_part+'.xls'
        merged_pathname = './MERGED/'+approach.upper()+'/'+brain_part+'/proteins_merged.csv'
        pathname = './MERGED/'+approach.upper()+'/'+brain_part+'/proteins_essential.csv'
        pathname_all_infos = './MERGED/'+approach.upper()+'/'+brain_part+'/all_infos.csv'
        pathname_all_infos2 = './MERGED/'+approach.upper()+'/'+brain_part+'/all_infos2.csv'
        mf_pathname = './MERGED/'+approach.upper()+'/'+brain_part+'/molecular_function.csv'
        bp_pathname = './MERGED/'+approach.upper()+'/'+brain_part+'/biological_process.csv'
        cc_pathname = './MERGED/'+approach.upper()+'/'+brain_part+'/cellular_component.csv'
        kw_pathname = './MERGED/'+approach.upper()+'/'+brain_part+'/kewords.csv'
        statistical_pathname_mf = './MERGED/'+approach.upper()+'/'+brain_part+'/statistical_'+brain_part+'_mf.csv'
        statistical_pathname_bp = './MERGED/'+approach.upper()+'/'+brain_part+'/statistical_'+brain_part+'_bp.csv'
        statistical_pathname_cc = './MERGED/'+approach.upper()+'/'+brain_part+'/statistical_'+brain_part+'_cc.csv'
    else:
        common_name = None
        unique_name1 = None
        unique_name2 = None
        merged_pathname = None
        pathname = './MERGED/'+approach+'/PAPER'+str(paper)+'/'+brain_part+'/proteins_essential.csv'
        pathname_all_infos = './MERGED/'+approach+'/PAPER'+str(paper)+'/'+brain_part+'/all_infos.csv'
        pathname_all_infos2 = './MERGED/'+approach+'/PAPER'+str(paper)+'/'+brain_part+'/all_infos2.csv'
        mf_pathname = './MERGED/'+approach+'/PAPER'+str(paper)+'/'+brain_part+'/molecular_function.csv'
        bp_pathname = './MERGED/'+approach+'/PAPER'+str(paper)+'/'+brain_part+'/biological_process.csv'
        cc_pathname = './MERGED/'+approach+'/PAPER'+str(paper)+'/'+brain_part+'/cellular_component.csv'
        kw_pathname = './MERGED/'+approach+'/PAPER'+str(paper)+'/'+brain_part+'/kewords.csv'
        statistical_pathname_mf = './MERGED/'+approach+'/PAPER'+str(paper)+'/'+brain_part+'/statistical_'+brain_part+'_mf.csv'
        statistical_pathname_bp = './MERGED/'+approach+'/PAPER'+str(paper)+'/'+brain_part+'/statistical_'+brain_part+'_bp.csv'
        statistical_pathname_cc = './MERGED/'+approach+'/PAPER'+str(paper)+'/'+brain_part+'/statistical_'+brain_part+'_cc.csv'

    return common_name, unique_name1, unique_name2, merged_pathname, pathname, pathname_all_infos, pathname_all_infos2, mf_pathname, bp_pathname, cc_pathname, kw_pathname, statistical_pathname_mf, statistical_pathname_bp, statistical_pathname_cc

def speak_with_the_user(bp_labels, mf_labels, cc_labels, godag):
    # ask about the subontology(ies) that he/she want to "break"
    subontology_numbers = {1:bp_labels, 2:mf_labels, 3:cc_labels}
    print('1: Biological Process\n2: Molecular Function\n3: Cellular Component')
    finish = True
    subontologies = []
    while finish:
        while True:
            try:
                subontology_answer = int(input('Type just the number:'))
                if subontology_answer >=1 and subontology_answer <= 3:
                    subontologies.append(subontology_answer)
                else:
                    pass
                break
            except ValueError:
                print("Not a valid answer. Try again!")
                pass
        finish_answer = input("Are you ready?[y/n]")
        if finish_answer == 'y':
            finish = False
        else:
            finish = True
    subontologies = hlp.remove_duplicates_of_list(subontologies)   
    answer1 = [subontology_numbers[subont] for subont in subontologies]     

    # ask about the specific go term(s)
    answer2 = []
    for subont in subontologies:
        print('GO terms:')
        counter = 1
        go_term_numbers = dict()
        for go_term in subontology_numbers[subont]:
            print(f'{counter} for {go.get_name_of_GOid(go_term, godag)} ({go_term})')
            go_term_numbers[counter] = go_term
            counter += 1

        finish = True
        terms = []
        while finish:
            while True:
                try:
                    go_term_answer = int(input('Type just the number:'))
                    if go_term_answer >=1 and go_term_answer <= counter:
                        terms.append(go_term_answer)
                    else:
                        pass
                    break
                except ValueError:
                    print("Not a valid answer. Try again!")   
                    pass
            finish_answer = input("Are you ready?[y/n]")
            if finish_answer == 'y':
                finish = False
            else:
                finish = True         
        terms = hlp.remove_duplicates_of_list(terms) 
        answer2.append([go_term_numbers[trm] for trm in terms])   

    return answer1, answer2       


def statistics_routine(my_list, godag, statistical_pathname, title='BarPlot'):
    # index = 60
    # bar = FillingCirclesBar(title, max=len(occurances))
    # for i in range(len(my_list)):
    #     my_list[i] = go.get_name_of_GOid(my_list[i], godag)
    #     # if len(my_list[i]) > index:
    #     #     my_list[i] = hlp.split_string_into2(my_list[i], index)
    #     bar.next()
    # bar.finish()
    occurances = Counter(my_list)
    occurances2 = dict()
    bar = FillingCirclesBar(title, max=len(occurances))
    for key, value in occurances.items():
        name = go.get_name_of_GOid(key, godag)
        occurances2[name] = value
        bar.next()
    bar.finish()
    # save the results
    df = pd.DataFrame.from_dict(occurances2, orient='index')
    df.columns = ['Occurences']
    df.to_csv(statistical_pathname, header='Occurances')

    # hlp.barplot(occurances, title=title) 