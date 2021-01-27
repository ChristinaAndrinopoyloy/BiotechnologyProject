import pandas as pd
import helpers as hlp

occurances = {'bla':22, "blo":3, "lili":12}
df1 = pd.DataFrame.from_dict(occurances, orient='index')
df1.columns = ['Occurences']
df1.to_csv('lala.csv', header='Occurances')

occurances = {'bla':2, "blo":2, "lili":2, 'lolo':11}
df2 = pd.DataFrame.from_dict(occurances, orient='index')
df2.columns = ['Occurences']
df2.to_csv('l0la.csv', header='Occurances')

df_merged = df1.merge(df2, how='outer', left_index=True, right_index=True)
df_merged = df_merged.fillna(0)
sum_column = df_merged["Occurences_x"] + df_merged["Occurences_y"]
df_merged["total"] = sum_column
print(df_merged)
hlp.multiple_barplot(df_merged)