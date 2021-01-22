import uniprot_database_helpets as uni
import helpers as hlp

common_name = './Results/UNIQUE/Olfactory_balb/common_proteins_Olfactory_balb.xls'
unique_name1 = './Results/UNIQUE/Olfactory_balb/HRMS_unique_proteins_Olfactory_balb.xls'
unique_name2 = './Results/UNIQUE/Olfactory_balb/2DGE_unique_proteins_Olfactory_balb.xls'

proteins_df = hlp.merge_excels(common_name, 
                                unique_name1, 
                                unique_name2, 
                                write_flag=True,
                                pathname='./temp.csv')

accesion_names_of_proteins = proteins_df.values.tolist()
proteins = []
deleted_proteins = []

code, old_protein = uni.get_code_from_accession('TSNAX_MOUSE')
# for protein in accesion_names_of_proteins:
#     print(protein[0])
#     code, old_protein = uni.get_code_from_accession(protein[0])
#     if old_protein == None:
#         print(code)
#         proteins.append((code,protein))
#     else:
#         print(f'The protein {old_protein} was deleted!')
#         deleted_proteins.append(protein)
# print(deleted_proteins)        
# protein_table = uni.get_proteins_based_on_uniprot(proteins, write_flag=True, pathname='proteins.csv')