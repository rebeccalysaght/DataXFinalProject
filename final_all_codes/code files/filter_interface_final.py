from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk
import warnings

warnings.filterwarnings('ignore')
import re
import pandas as pd
import datetime
from datetime import date
import calendar
import ast

window = Tk()
window.title('preference filter')
window.geometry('500x500')

# background
start = Image.open("picture.gif")
start = start.resize((500, 500))
canvas = Canvas(window, height=500, width=500)
image_file = ImageTk.PhotoImage(start)
image = canvas.create_image(0, 0, anchor='nw', image=image_file)
canvas.pack(side='top')

# text label
textLabel1 = Label(window, text="what kind of food would you like today? ", font=('Cooper Black', 11), bg='white',
                   fg='red')
textLabel1.place(x=80, y=80)
textLabel2 = Label(window, text="what time would you like to have your meal? ", font=('Cooper Black', 11), bg='white',
                   fg='red')
textLabel2.place(x=80, y=180)
textLabel3 = Label(window, text="See the available restaurants:  ", font=('Cooper Black', 11), bg='white',
                   fg='red')
textLabel3.place(x=80, y=320)
# combobox
category_choice = StringVar()
restaurantChosen1 = ttk.Combobox(window, width=40, textvariable=category_choice)
restaurantChosen1.place(x=80, y=110)
categories_info = pd.read_csv('categories_AZ_new.csv')
categories = categories_info['categories'].tolist()
restaurantChosen1['values'] = categories
time_choice = StringVar()
restaurantChosen2 = ttk.Combobox(window, width=40, textvariable=time_choice)
restaurantChosen2.place(x=80, y=210)
time_to_choose = pd.read_csv('time_to_choose.csv')
time = time_to_choose['time'].tolist()
restaurantChosen2['values'] = time


def is_open(date_string, time_now):
    open_close_list = date_string.split("-")
    opening_time = datetime.datetime.strptime(open_close_list[0], "%H:%M")
    closing_time = datetime.datetime.strptime(open_close_list[1], "%H:%M")
    current_time = datetime.datetime.strptime(time_now, "%H:%M")
    if opening_time <= current_time <= closing_time:
        return True
    return False


def filter(category_user, meal_time):
    restaurants = pd.read_csv('restaurants_AZ.csv')
    c = restaurants['categories']
    required_restaurants = pd.DataFrame()
    
    user_c = category_user
    x = meal_time
    final_choice = []
    if user_c=='' or x=='':
        return final_choice
    
    # function for categories choosing:
    for i in range(len(c)):
        d = re.findall(r"'(.*?)'", c[i], re.DOTALL)
        if user_c in d:
            restaurant_id = restaurants['business_id'][i]
            df = restaurants[restaurants['business_id'] == restaurant_id]
            required_restaurants = pd.concat([required_restaurants, df], ignore_index=True, axis=0)
    
    if 'name' not in required_restaurants:
        return final_choice
    
    # function for time choosing
    day_of_week = str(calendar.day_name[date.today().weekday()])
    for i in range(len(required_restaurants)):
        try:
            all_time = required_restaurants['hours']
            time_dic = ast.literal_eval(all_time[i])
            if is_open(time_dic[day_of_week], x) == False:
                required_restaurants = required_restaurants.drop(i)
        except KeyError:
            required_restaurants = required_restaurants.drop(i)
    
    #print(required_restaurants)
    if 'name' not in required_restaurants:
        return final_choice
    else:
        required_restaurants.to_csv('restaurant_after_filter.csv', encoding='utf-8', index=False)
        final_choice = required_restaurants['name'].unique().tolist()
        return final_choice

category_user = ''
meal_time = ''
final_choice = filter(category_user, meal_time)
see_restaurants = ttk.Combobox(window, width=40, textvariable=[])
see_restaurants['values'] = final_choice
see_restaurants.place(x=80, y=350)

def hit_me():
    global category_user
    global meal_time
    category_user = restaurantChosen1.get()
    meal_time = restaurantChosen2.get()
    #print('Your choice is:')
    #print('Category: {}\tMeal time: {}\n'.format(category_user,meal_time))
    final_choice = filter(category_user, meal_time)
    choice = StringVar()
    see_restaurants = ttk.Combobox(window, width=40, textvariable=choice)
    see_restaurants['values'] = final_choice
    see_restaurants.place(x=80, y=350)

confirm = Button(window, text='confirm my choices', font=('Cooper Black', 11), bg='white', fg='red', command=hit_me)
confirm.place(x=160, y=280)

window.mainloop()


