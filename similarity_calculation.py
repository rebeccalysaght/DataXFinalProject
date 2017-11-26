import numpy as np
import pandas as pd

user_feature = pd.read_csv('user_feature.csv')
re_feature = pd.read_csv('restaurant_feature.csv')
restaurant = pd.read_csv('restaurants_AZ.csv')
user = pd.read_csv('user_top1000.csv')

user_id = user['user_id'].tolist()
restaurant_id = restaurant['business_id'].tolist()

import difflib

feature_matrix = pd.DataFrame()
# get the similarity of each user's feature and each restaurant's feature, form a Matrix
for i in range(0, len(user_id)):
    user_f = user_feature[user_id[i]]
    user_f_clean = [x for x in user_f if str(x) != 'nan']
    user_re = []
    for j in range(0, len(restaurant_id)):
        re_f = re_feature[restaurant_id[j]]
        re_f_clean = [x for x in re_f if str(x) != 'nan']
        s = difflib.SequenceMatcher(None, user_f_clean, re_f_clean).ratio()
        user_re.append(s)
    df = pd.DataFrame(user_re)
    feature_matrix = pd.concat([feature_matrix, df], ignore_index=True, axis=1)



feature_matrix.to_csv('feature_matrix.csv', encoding='utf-8', index=False)


# normalized the feature matrix
from sklearn import preprocessing
min_max_scaler = preprocessing.MinMaxScaler()
feature_scaled = min_max_scaler.fit_transform(feature_matrix)
feature_normalized = pd.DataFrame(feature_scaled)

feature_normalized.columns = user_id
feature_normalized.index = restaurant_id
feature_normalized.to_csv('feature_id_normalized.csv', encoding='utf-8', index=False)
