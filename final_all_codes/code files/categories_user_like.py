import numpy as np
import pandas as pd
user = pd.read_csv('user_top1000.csv')
review = pd.read_csv('review_top1000.csv')
business = pd.read_csv('business.csv')

# for each user, get the categories he likes
user_like = pd.DataFrame()
import re
for i in range(0, 1000):
    categories = []
    user_id = user['user_id'][i]
    # find the positive restaurants the user has been to
    business_user = review[review['user_id']==user_id]
    positive_b = business_user[business_user['stars']>=4]['business_id'].tolist()
    # for each of the restaurant, get its categories
    for j in range(0,len(positive_b)):
        user_c = business[business['business_id']==positive_b[j]]['categories']
        c = str(user_c)
        d = re.findall(r"'(.*?)'", c, re.DOTALL)
        if "Restaurants" in d:
            for element in d:
                if element not in categories:
                    categories.append(element)
    df = pd.DataFrame(categories)
    user_like = pd.concat([user_like, df], ignore_index=True, axis=1)

user_id = user['user_id'].tolist()
user_like.columns = user_id
user_like.to_csv('user_like_categories.csv',encoding='utf-8', index=False)