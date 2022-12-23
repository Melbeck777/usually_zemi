import pandas as pd

data = pd.read_excel('../member/2022_member.xlsx')
columns = data.columns
group_members = data[[columns[9],columns[11]]].drop_duplicates()
res = []
for index, element in enumerate(group_members[columns[11]]):
    if type(element) is float:
        continue
    res.append([group_members[columns[9]][index], element])
print(res)