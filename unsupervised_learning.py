import pandas as pd
import numpy as np
from sklearn.cluster import KMeans

global_stars = pd.read_csv('res_stars_AZ.csv')
distance = pd.read_csv('geo_re1.csv')
nlp_similarity = pd.read_csv('feature_id_normalized.csv')

# define the user
user_id = 'CxDOIDnH8gp9KXzpBHJYXw'
# let the global feature be the feature1
feature1 = global_stars['stars'].tolist()
# let the nlp similarity be the feature2
feature2 = (nlp_similarity[user_id]*5).tolist()
# let the distance be the feature3
feature3 = (distance['Dis_norm']*5).tolist()

# combine all the three features to get the training data
feature=np.array([feature1, feature2, feature3])
feature = feature.T

# choose kmeans to do unsupervised learning
kmeans = KMeans(n_clusters=10)
kmeans.fit(feature)
centroids = kmeans.cluster_centers_
labels = kmeans.labels_
print(centroids)
print(labels)
for i in range(len(feature)):
    print("coodinate:",feature[i],'label:',labels[i])