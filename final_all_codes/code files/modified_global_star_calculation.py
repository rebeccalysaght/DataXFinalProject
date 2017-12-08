import pandas as pd
import numpy as np
from scipy.sparse.linalg import svds

import pandas as pd
import numpy as np
from scipy.sparse.linalg import svds

# get the restaurants information we need for prediction from business file
restaurants = pd.read_csv('bus.csv')
# get the users information from user file
user = pd.read_csv('user_top1000.csv')
# get the rating information we need for prediction from review file
rating = pd.read_csv('usr.csv')
rating_info = pd.merge(rating, restaurants, on='business_id')
rating_matrix = rating_info.pivot(index = 'user_id', columns ='business_id', values = 'stars').fillna(0)
rating_matrix.head()

re_id_ordered = rating_matrix.columns.tolist()
user_id_ordered = rating_matrix.index.tolist()

from sklearn.metrics.pairwise import pairwise_distances
user_similarity = pairwise_distances(rating_matrix, metric='cosine')
Rating = rating.as_matrix()
user_ratings_mean = np.mean(Rating, axis=1)
user_ratings_mean_reshaped = user_ratings_mean.reshape(-1, 1)
Rating_demeaned = Rating - user_ratings_mean_reshaped


def predict(ratings, similarity, type='user'):
    if type == 'user':
         pred = user_ratings_mean[:, np.newaxis] + similarity.dot(Rating_demeaned) / np.array([np.abs(similarity).sum(axis=1)]).T
    elif type == 'item':
        pred = ratings.dot(similarity) / np.array([np.abs(similarity).sum(axis=1)])
    return pred

user_prediction = predict(rating_matrix, user_similarity, type='user')
