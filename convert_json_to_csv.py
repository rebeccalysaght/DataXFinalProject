import json
import pandas as pd


def read_json_as_dataframe(filepath):
    with open(filepath, 'rb') as file:
        full_data = [json.loads(row) for row in file]
    dataframe=pd.DataFrame(full_data)
    return dataframe


df1 = read_json_as_dataframe('review.json')
df1.to_csv('review.csv', encoding='utf-8', index=False)
df2 = read_json_as_dataframe('user.json')
df2.to_csv('user.csv', encoding='utf-8', index=False)
df3 = read_json_as_dataframe('business.json')
df3.to_csv('business.csv', encoding='utf-8', index=False)

