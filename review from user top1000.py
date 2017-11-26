# Remove warnings
import warnings
warnings.filterwarnings('ignore')
import pandas as pd


review = pd.read_csv('review.csv')
review_user_count = review.groupby(['user_id']).count()
df = review_user_count.sort_values(['review_id'],ascending=0)
df = df.reset_index()
user_list = df['user_id'].tolist()
top1000 = user_list[0:1000]

review_top1000=pd.DataFrame()
for user in top1000[0:1000]:
    df_review = review[review['user_id'] == str(user)]
    user_top1000 = user_top1000.append(df_review)

review_top1000.to_csv('review_top1000.csv', encoding='utf-8', index=False)