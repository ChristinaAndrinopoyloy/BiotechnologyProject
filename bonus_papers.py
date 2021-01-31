import helpers as hlp
# import ncbi_database_helpers as ncbi

# codes = hlp.read_table_from_pdf1(filename='./bonus_papers/paper2/table.PDF1')
# print(codes)

# # for code in codes:
# ncbi_infos = ncbi.get_content_from_ncbi(query=codes)
# for key, value in ncbi_infos.items():
#     print(key)
#     print(value)
#     # print(version)
#     print('-'*20)


pathname1 = './bonus_papers/paper2/table1.xlsx'
pathname2 = './bonus_papers/paper2/table2.xlsx'

df1 = hlp.read_from_xlx(pathname1)
df2 = hlp.read_from_xlx(pathname2)

df1 = df1.fillna(0)
df2 = df2.fillna(0)

df1 = df1.iloc[1:]
df2 = df2.iloc[1:]

# table 1
proteins_list = []
for index, row in df1.iterrows():
    proteins = row[-1]
    lfq_of_brain_total = 0
    for i in range(2,6):
        lfq_of_brain_total += int(row[i])

    ibaq_of_brain_total = 0
    for i in range(33,37):
        ibaq_of_brain_total += int(row[i])
    
    if lfq_of_brain_total != 0 and ibaq_of_brain_total != 0:
        proteins_list.append(proteins)
print(len(proteins_list))

# table 2
proteins_brainpart_dict = dict()
for index, row in df2.iterrows():
    proteins = row[-1]
    if proteins in proteins_list:
        for i in range(7,17):
            if row[i] != 0:
                if proteins not in proteins_brainpart_dict:
                    proteins_brainpart_dict[proteins] = []
                proteins_brainpart_dict[proteins].append(hlp.get_brainpart_based_on_index(i))

for key, value in proteins_brainpart_dict.items():
    print(key)
    print(value)
    print('-'*20) 
