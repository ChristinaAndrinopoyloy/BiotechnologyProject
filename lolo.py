import uniprot_database_helpets as uni

data = uni.get_uniprot(query='gabra6',query_type='GENENAME') # do the query to the UniProt
print(data[0])
# content = []
# full_data = []
# # data2 = " ".join(data)
# # data3 = data2.replace('// ID', '########').split('########')
# for d in data:
#     if d == '//':
#         print('change')
#         full_data.append(content)
#         content = []
#     else:
#         content.append(d)    
# # for i in full_data:
# #     for line in i:
# #         print(line)
# #     print('==============================================================')            
# for i in range(2):
#     for line in full_data[i]:
#         print(line)
#     print('----------------')    