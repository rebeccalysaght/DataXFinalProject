import warnings

warnings.filterwarnings('ignore')
import pandas as pd
import re

restaurants = pd.read_csv('restaurants_AZ.csv')
c = restaurants['categories']
required_restaurants_id = []
required_restaurants_name = []
required_restaurants = pd.DataFrame()

# let the user input the categories:
user_c = input("Please tell me what kind of food you would like to have: ")

# get the required restaurants
for i in range(0, 2867):
    d = re.findall(r"'(.*?)'", c[i], re.DOTALL)
    if user_c in d:
        restaurant_id = restaurants['business_id'][i]
        restaurant_name = restaurants['name'][i]
        df = restaurants[restaurants['business_id'] == restaurant_id]
        required_restaurants_id.append(restaurant_id)
        required_restaurants_name.append(restaurant_name)
        required_restaurants = pd.concat([required_restaurants, df], ignore_index=True, axis=0)
#print("There are " + str(len(required_restaurants_name)) + ' ' + str(user_c) + ' ' + "restaurants here, enjoy your meal!")
#print(required_restaurants_name)
#print(required_restaurants_id)
print(required_restaurants)