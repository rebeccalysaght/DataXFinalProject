import warnings
warnings.filterwarnings('ignore')
import pandas as pd
review = pd.read_csv('review.csv')
user = pd.read_csv('user.csv')

review_user_count = review.groupby(['user_id']).count()
df = review_user_count.sort_values(['review_id'], ascending=0)
df = df.reset_index()
user_list = df['user_id'].tolist()
top1000 = user_list[0:1000]

df1 = pd.DataFrame()
for people in top1000[0:1000]:
    df = user[user['user_id'] == str(people)]
    df1 = df1.append(df)

user_top1000.to_csv('user_top1000.csv',encoding='utf-8',index=False)