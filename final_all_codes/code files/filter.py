import warnings
warnings.filterwarnings('ignore')
import re
import pandas as pd
import datetime
from datetime import date
import calendar
import ast

# categories filter
restaurants = pd.read_csv('restaurants_AZ.csv')
c = restaurants['categories']
required_restaurants_id = []
required_restaurants_name = []

# let the user input the categories:
user_c = input("Please tell me what kind of food you would like to have: ")

# get the required restaurants
for i in range(0, 2867):
    d = re.findall(r"'(.*?)'", c[i], re.DOTALL)
    if user_c in d:
        restaurant_id = restaurants['business_id'][i]
        restaurant_name = restaurants['name'][i]
        required_restaurants_id.append(restaurant_id)
        required_restaurants_name.append(restaurant_name)

df = pd.DataFrame()
for i in range(0, len(required_restaurants_id)):
    df = df.append(restaurants[restaurants['business_id'] == required_restaurants_id[i]])

# open time filter
# helper function that checks dataframe "hours" value against current time

df.reset_index(drop=True)


def is_open(date_string, time_now):
    open_close_list = date_string.split("-")
    opening_time = datetime.datetime.strptime(open_close_list[0], "%H:%M")
    closing_time = datetime.datetime.strptime(open_close_list[1], "%H:%M")
    current_time = datetime.datetime.strptime(time_now, "%H:%M")
    if opening_time <= current_time <= closing_time:
        return True
    return False


x = input("please tell me your meal time: ")


def open_restaurants(dataframe, time_now):
    day_of_week = str(calendar.day_name[date.today().weekday()])
    for i in range(0, len(dataframe)):
        all_time = dataframe['hours']
        try:
            time_dic = ast.literal_eval(all_time[i])
            if time_dic == {}:
                dataframe = dataframe.drop(i)
            elif is_open(time_dic[day_of_week], time_now) == False:
                dataframe = dataframe.drop(i)
        except KeyError:
            return dataframe


print(open_restaurants(df, x))
