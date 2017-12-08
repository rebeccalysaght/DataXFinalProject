import pandas as pd
nlp_similarity = pd.read_csv('feature_id_normalized.csv')
restaurants = pd.read_csv('restaurants_AZ.csv')
user_restaurants = pd.read_csv('new_user_restaurants.csv')
modified_stars = pd.read_csv('modified_global_star.csv')
re_after_filter = pd.read_csv('restaurant_after_filter.csv')
users = pd.read_csv('user_top1000.csv')

# make recommendation for a specific user
the_user = 'CxDOIDnH8gp9KXzpBHJYXw'
# get the restaurant the user hasn't been to
previous_re = user_restaurants[user_restaurants['user_id']==the_user]['business_id'].tolist()
for i in range(0, len(re_after_filter)):
    required_re = re_after_filter['business_id'].tolist()
    if required_re[i] in previous_re:
        re_after_filter = re_after_filter.drop(i)
re_after_fliter = re_after_filter.reset_index()

a = pd.read_csv('user_id_ordered.csv')
user_id_ordered = a['user_id_ordered'].tolist()
modified_stars.index = user_id_ordered
restaurants_id = restaurants['business_id'].tolist()
nlp_similarity.index = restaurants_id

# get the data we will train in our model
new_data = pd.DataFrame()
new_x1 = []
new_x2 = []
new_re_id = []
for i in range(0, len(re_after_filter)):
    re_id = re_after_fliter['business_id'].tolist()
    if (re_id[i] in modified_stars.columns) and (re_id[i] in nlp_similarity.index):
        new_x1.append(modified_stars.loc[the_user, re_id[i]])
        new_x2.append(nlp_similarity.loc[re_id[i], the_user])
        new_re_id.append(re_id[i])
new_data['x1'] = new_x1
new_data['x2'] = new_x2
new_data['business_id'] = new_re_id


from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
from sklearn import linear_model
data = pd.read_csv('regression_dataset.csv')
data = shuffle(data).reset_index(drop=True)
X = data.loc[:, data.columns != 'y']
Y = data['y']
x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.25, random_state=100)

# train logistic regression and get the prediction
logreg_model = linear_model.LogisticRegression()
logreg_model.fit(x_train, y_train)
new_X = new_data[['x1','x2']]
new_Y = logreg_model.predict(new_X)
new_data['y'] = new_Y

# check if the restaurant in the required restaurants after filter
for i in range(0, len(re_after_filter)):
    new_id = new_data['business_id'].tolist()
    all_id = re_after_filter['business_id'].tolist()
    if all_id[i] not in new_id:
        re_after_filter.drop(i)

re_after_train = pd.merge(new_data, re_after_filter, on='business_id')
re_after_train.to_csv('data_after_train.csv',  encoding='utf-8', index=False)

import geopy
import pandas as pd

df = pd.read_csv('data_after_train.csv')
# get the location of user
x = input("Please enter the location: ")


# the function of geo-feature
def location(x):
    from geopy.geocoders import Nominatim
    geolocator = Nominatim()
    location1 = geolocator.geocode(x)
    your_address = location1.address
    your_coordinates = [location1.latitude, location1.longitude]

    from geopy.distance import vincenty
    distance_list = []
    for i in range(0, len(df['latitude'])-1):
        distance_list.append([[df['latitude'][i], df['longitude'][i]]])
    df['Coordinate List'] = pd.DataFrame(distance_list)

    f = []
    for i in range(0, len(df['latitude'])-1):
        f.append(vincenty(your_coordinates,distance_list[i]).miles)
    df['Distance'] = pd.DataFrame(f)
    return df

Location = location(x)
geo_re = Location[['business_id', 'Distance']]
res_map = Location[['business_id', 'latitude', 'longitude']]

# normalize distance
dis = geo_re['Distance']
from sklearn import preprocessing
# dis contains NaN, so fisrt step is to replace the NaN with mean
dis.fillna(dis.dropna().mean(), inplace=True)
dis_new = 1/dis
min_max_scaler = preprocessing.MinMaxScaler()
dis_scaled = min_max_scaler.fit_transform(dis_new)
dis_normalized = pd.DataFrame(dis_scaled)
geo_re['Dis_norm'] = dis_normalized
del geo_re['Distance']
re_after_geo = pd.merge(re_after_train, geo_re, on='business_id')
re_after_geo.to_csv('data_after_geo.csv',  encoding='utf-8', index=False)

# let user decide the weight of distance and get the predicted score for each restaurant
Beta = input('how important is the distance to you? ')
distance = re_after_geo['Dis_norm'].tolist()
global_star = re_after_geo['y'].tolist()
prediction_star = []
param = float(Beta)
for i in range(0, len(distance)):
    star = float(global_star[i])
    dis = float(distance[i])
    value = (0.5 *star + 0.5*param*dis*5)/(0.5+0.5*param)
    prediction_star.append(value)

# recommend the restaurant
re_after_geo['predicted_star']=prediction_star
re_after_geo.to_csv('data_prediction.csv',  encoding='utf-8', index=False)
re_after_geo = re_after_geo.sort_values(by=['predicted_star'], ascending=False)
recommended_re = re_after_geo['name']