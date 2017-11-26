import pandas as pd
import datetime
from datetime import date
import calendar
import ast

# read in business.csv file
df = pd.read_csv("restaurants_AZ.csv")


# helper function that checks dataframe "hours" value against current time
def is_open(date_string, time_now):
    open_close_list = date_string.split("-")
    opening_time = datetime.datetime.strptime(open_close_list[0], "%H:%M")
    closing_time = datetime.datetime.strptime(open_close_list[1], "%H:%M")
    current_time = datetime.datetime.strptime(time_now, "%H:%M")
    if opening_time <= current_time <= closing_time:
        return True
    return False


day_of_week = str(calendar.day_name[date.today().weekday()])
x = input("please tell me your meal time: ")
for i in range(0, len(df)):
    try:
       all_time = df['hours']
       time_dic = ast.literal_eval(all_time[i])
    except KeyError:
       if time_dic == {}:
          df = df.drop(i)
       elif is_open(time_dic[day_of_week], x) == False:
          df = df.drop(i)


print(df)
