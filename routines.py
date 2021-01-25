
def find_the_appropriate_files(approach, brain_part):
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

    return common_name, unique_name1, unique_name2, merged_pathname, pathname, pathname_all_infos, pathname_all_infos2, mf_pathname, bp_pathname, cc_pathname, kw_pathname



