##########################################################################################
#                               Andrinopoulou Christina                                  #
#                                             ds2200013                                  #
##########################################################################################

import helpers as hlp
import pandas as pd
import click

avaliable_approaches = ['unique', 'simple']
avaliable_GO = ['Biological_Process', 'Molecular_Function', 'Cellular_Component']
@click.command()
@click.option("--approach", type=click.Choice(avaliable_approaches, case_sensitive=False), default='simple', help="The approach that used in order to find the proteins of the two methods: 2DGE, HRMS", show_default=True)
@click.option("--go", type=click.Choice(avaliable_GO, case_sensitive=False), default='Biological Process', help="SubDAG of Gene Ontology", show_default=True)
def total_statistics(approach, go):
    '''A python program that creates barplots for all the brain parts'''

    brain_parts = ['Cerebellum', 'Cortex', 'Hipocampus', 'Hipothalamus', 'Medulla', 'Mid_Brain', 'Olfactory_balb']

    statistics_mf = []
    statistics_for_all = dict()

    for brain_part in brain_parts:
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

        if go == 'Biological_Process':
            pathname = './MERGED/'+approach.upper()+'/'+brain_part+'/statistical_'+brain_part+'_bp.csv'
        if go == 'Molecular_Function':
            pathname = './MERGED/'+approach.upper()+'/'+brain_part+'/statistical_'+brain_part+'_mf.csv'
        if go == 'Cellular_Component':
            pathname = './MERGED/'+approach.upper()+'/'+brain_part+'/statistical_'+brain_part+'_cc.csv'
        statistical_df = pd.read_csv(pathname)     

        for index, row in statistical_df.iterrows():
            term = row[0]
            occurs = row[1]

            if term not in statistics_for_all:
                statistics_for_all[term] = []
            statistics_for_all[term].append(occurs)
            
    df=pd.DataFrame.from_dict(statistics_for_all,orient='index').transpose()
    df = df.transpose()
    df = df.fillna(0)
    df.columns =['Cerebellum', 'Cortex', 'Hippocampus', 'Hypothalamus', 'Medulla', 'MidBrain', 'Olfactory Bulb']         
    df.to_csv('temp.csv',index=True)

    hlp.multiple_barplot(df, title=go)





if __name__ == '__main__':
    total_statistics()      