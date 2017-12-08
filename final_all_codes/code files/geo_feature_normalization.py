import geopy
import pandas as pd

df = pd.read_csv('restaurants_AZ.csv')
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
min_max_scaler = preprocessing.MinMaxScaler()
dis_scaled = min_max_scaler.fit_transform(dis)
dis_normalized = pd.DataFrame(dis_scaled)
# for distance feature, generally, we want restaurants with shorter distance have higher score on this feature
# so we just replace the normalized distance with (1-dis_normalized)
dis_new = 1-dis_normalized
geo_re['Dis_norm'] = dis_new
del geo_re['Distance']
