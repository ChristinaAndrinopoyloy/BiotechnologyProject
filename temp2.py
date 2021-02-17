import uniprot_database_helpets as uni

uniprot_data = uni.get_uniprot(query='P08113', query_type='ACC+ID')
print(uniprot_data)