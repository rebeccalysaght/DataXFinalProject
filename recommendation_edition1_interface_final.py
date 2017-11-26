from tkinter import *
from PIL import Image, ImageTk
import pandas as pd
import numpy as np
from tkinter import ttk
from scipy.sparse.linalg import svds
import ast

# recommendation function
# get the restaurants information we need for prediction from business file
restaurants = pd.read_csv('bus.csv')
# get the users information from user file
user = pd.read_csv('user_top1000.csv')
# get the rating information we need for prediction from review file
rating = pd.read_csv('usr.csv')

# change the format of ratings matrix to be one row per user id and one column per restautant id
Rating_df = rating.pivot(index='user_id', columns='business_id', values='stars').fillna(0)
Rating_df.head()
# de-mean the data (normalize by each users mean) and convert it from a dataframe to a numpy array.
Rating = Rating_df.as_matrix()
user_ratings_mean = np.mean(Rating, axis=1)
Rating_demeaned = Rating - user_ratings_mean.reshape(-1, 1)
# use the Scipy function svds to do the singular value decomposition
U, sigma, Vt = svds(Rating_demeaned, k=50)
# since I am going to leverage matrix multiplication to get predictions I will convert it to the diagonal matrix form
sigma = np.diag(sigma)
# Making Predictions from the Decomposed Matrices
all_user_predicted_ratings = np.dot(np.dot(U, sigma), Vt) + user_ratings_mean.reshape(-1, 1)
preds_df = pd.DataFrame(all_user_predicted_ratings, columns=Rating_df.columns)


def recommend_restaurants(predictions_df, user_number, restaurants, original_ratings_df, num_recommendations=5):
    # Get and sort the user's predictions
    user_row_number = user_number  # UserID starts at 1, not 0
    sorted_user_predictions = predictions_df.iloc[user_row_number].sort_values(ascending=False)

    # Get the user's data and merge in the restaurants information.
    user_data = original_ratings_df[original_ratings_df.user_id == str(user['user_id'][user_number])]
    user_full = (user_data.merge(restaurants, how='left', left_on='business_id', right_on='business_id').
                 sort_values(['stars'], ascending=False)
                 )

    # Recommend the highest predicted rating restaurants that the user hasn't seen yet.
    restaurants_new = restaurants[~restaurants['business_id'].isin(user_full['business_id'])]. \
        merge(pd.DataFrame(sorted_user_predictions).reset_index(), how='left', left_on='business_id',
              right_on='business_id'). \
        rename(columns={user_row_number: 'Predictions'}). \
        sort_values('Predictions', ascending=False)
    # choose the restautants in AZ to recommend
    recommendations = (restaurants_new[restaurants_new['state'] == 'AZ'].iloc[:100, :-1])
    recommendations = recommendations.reset_index()
    del recommendations['index']
    # find the fake restaurants (other service stores in yelp) and drop them
    for i in range(0, len(recommendations) - 1):
        if 'Restaurants' not in recommendations.loc[i]['categories']:
            recommendations = recommendations.drop(i)
    new_recommendations = recommendations.iloc[:num_recommendations, :-1]
    return new_recommendations


# based on the user_id, get the index(user_number) in the dataframe
num_user = user[user['user_id'] == 'DK57YibC5ShBmqQl97CKog'].index.tolist()
num = num_user[0]
predictions = recommend_restaurants(preds_df, int(num), restaurants, rating, 10)
user_name = user[user['user_id'] == 'DK57YibC5ShBmqQl97CKog']['name'].tolist()
name = user_name[0]
restaurants_chosen = predictions['name'].tolist()
# print("hi!" + name + " ! We will recommend you: ")
# print(predictions['name'])


window = Tk()
window.title('recommendation')
window.geometry('500x500')

# welcome to AZ
welcome = Image.open("picture.gif")
welcome = welcome.resize((500, 500))
canvas = Canvas(window, height=500, width=500)
image_file = ImageTk.PhotoImage(welcome)
image = canvas.create_image(0, 0, anchor='nw', image=image_file)
canvas.pack(side='top')

# recommendation text
textLabel1 = Label(window, text="we would like to recommend you:", font=('Cooper Black', 12), fg='red')
textLabel1.place(x=60, y=80)
textLabel2 = Label(window, text="star:", font=('Cooper Black', 12), fg='red')
textLabel2.place(x=60, y=200)
textLabel3 = Label(window, text="city:", font=('Cooper Black', 12), fg='red')
textLabel3.place(x=60, y=220)
textLabel4 = Label(window, text="open hour:", font=('Cooper Black', 12), fg='red')
textLabel4.place(x=60, y=240)
textLabel4_1 = Label(window, text="Monday:", font=('Arial', 11), fg='red')
textLabel4_1.place(x=60, y=260)
textLabel4_2 = Label(window, text="Tuesday:", font=('Arial', 11), fg='red')
textLabel4_2.place(x=60, y=280)
textLabel4_3 = Label(window, text="Wednesday:", font=('Arial', 11), fg='red')
textLabel4_3.place(x=60, y=300)
textLabel4_4 = Label(window, text="Thursday:", font=('Arial', 11), fg='red')
textLabel4_4.place(x=60, y=320)
textLabel4_5 = Label(window, text="Friday:", font=('Arial', 11), fg='red')
textLabel4_5.place(x=60, y=340)
textLabel4_6 = Label(window, text="Saturday:", font=('Arial', 11), fg='red')
textLabel4_6.place(x=60, y=360)
textLabel4_7 = Label(window, text="Sunday:", font=('Arial', 11), fg='red')
textLabel4_7.place(x=60, y=380)
textLabel5 = Label(window, text="categories", font=('Cooper Black', 12), fg='red')
textLabel5.place(x=60, y=400)

# recommended restaurant display
var1 = StringVar()
display_detail1 = Label(window, textvariable=var1, font=('Arial', 11), fg='red')
display_detail1.place(x=160, y=200)

var2 = StringVar()
display_detail2 = Label(window, textvariable=var2, font=('Arial', 11), fg='red')
display_detail2.place(x=160, y=220)

var3 = StringVar()
display_detail3 = Label(window, textvariable=var3, font=('Arial', 11), fg='red')
display_detail3.place(x=160, y=260)

var4 = StringVar()
display_detail4 = Label(window, textvariable=var4, font=('Arial', 11), fg='red')
display_detail4.place(x=160, y=280)

var5 = StringVar()
display_detail5 = Label(window, textvariable=var5, font=('Arial', 11), fg='red')
display_detail5.place(x=160, y=300)

var6 = StringVar()
display_detail6 = Label(window, textvariable=var6, font=('Arial', 11), fg='red')
display_detail6.place(x=160, y=320)

var7 = StringVar()
display_detail7 = Label(window, textvariable=var7, font=('Arial', 11), fg='red')
display_detail7.place(x=160, y=340)

var8 = StringVar()
display_detail8 = Label(window, textvariable=var8, font=('Arial', 11), fg='red')
display_detail8.place(x=160, y=360)

var9 = StringVar()
display_detail9 = Label(window, textvariable=var9, font=('Arial', 11), fg='red')
display_detail9.place(x=160, y=380)

var10 = StringVar()
display_detail9 = Label(window, textvariable=var10, font=('Arial', 11), fg='red')
display_detail9.place(x=160, y=420)

var11 = StringVar()
display_detail9 = Label(window, textvariable=var11, font=('Arial', 11), fg='red')
display_detail9.place(x=160, y=440)

# combobox
choice = StringVar()
restaurantChosen = ttk.Combobox(window, width=40, textvariable=choice)
restaurantChosen['values'] = restaurants_chosen
restaurantChosen.place(x=60, y=110)

# pre load the data
restaurants_all = pd.read_csv('business.csv')


# function
def hit_me():
    restaurant_name = restaurantChosen.get()
    restaurant_id = predictions[predictions['name'] == restaurant_name]['business_id'].tolist()
    id_chosen = restaurant_id[0]
    restaurant_info = restaurants_all[restaurants_all['business_id'] == id_chosen]
    info_index = restaurants_all[restaurants_all['business_id'] == id_chosen].index
    if restaurant_info.empty:
        var1.set("Nothing~")
        var2.set("")
        var3.set("")
        var4.set("")
        var5.set("")
        var6.set("")
        var7.set("")
        var8.set("")
        var9.set("")
        var10.set("")
        var11.set("")
    else:
        star_new = restaurant_info['stars'].tolist()
        star = star_new[0]
        city_new = restaurant_info['city'].tolist()
        city = city_new[0]
        #neighborhood_new = restaurant_info['neighborhood'].tolist()
        #neighborhood = neighborhood_new[0]
        open_hour_all = restaurant_info['hours']
        info_index = restaurant_info['hours'].index.tolist()
        index = info_index[0]
        open_hour = ast.literal_eval(open_hour_all[index])
        if 'Monday' in open_hour.keys():
            open_hour1 = open_hour['Monday']
        else:
            open_hour1 = ''
        if 'Tuesday' in open_hour.keys():
            open_hour2 = open_hour['Tuesday']
        else:
            open_hour2 = ''
        if 'Wednesday' in open_hour.keys():
            open_hour3 = open_hour['Wednesday']
        else:
            open_hour3 = ''
        if 'Thursday' in open_hour.keys():
            open_hour4 = open_hour['Thursday']
        else:
            open_hour4 = ''
        if 'Friday' in open_hour.keys():
            open_hour5 = open_hour['Friday']
        else:
            open_hour5 = ''
        if 'Saturday' in open_hour.keys():
            open_hour6 = open_hour['Saturday']
        else:
            open_hour6 = ''
        if 'Sunday' in open_hour.keys():
            open_hour7 = open_hour['Sunday']
        else:
            open_hour7 = ''
        categories_all = restaurant_info['categories'].tolist()
        d = re.findall(r"'(.*?)'", str(categories_all), re.DOTALL)
        categories_AZ = pd.read_csv('categories_AZ_new.csv')
        categories_AZ_new = categories_AZ['categories'].tolist()
        categories = []
        for i in range(0, len(categories_AZ_new)):
            if categories_AZ_new[i] in d:
                categories.append(categories_AZ_new[i])
        if len(categories) == 0:
            categories1 = ''
            categories2 = ''
        elif len(categories) == 1:
            categories1 = categories[0]
            categories2 = ''
        elif len(categories) >= 2:
            categories1 = categories[0]
            categories2 = categories[1]
        '''open_hour = ','.join(open_hour)
        open_hour = open_hour.split(',')
        open_hour1 = open_hour[0:2]
        open_hour2 = open_hour[2:4]
        open_hour3 = open_hour[4:6]
        open_hour4 = open_hour[6:7]
        categories = restaurant_info['categories'].tolist()
        categories = ','.join(categories)
        categories = categories.split(',')
        categories1 = categories[0:2]
        categories2 = categories[2:]'''

        var1.set(str(star))
        var2.set(str(city))
        var3.set(str(open_hour1))
        var4.set(str(open_hour2))
        var5.set(str(open_hour3))
        var6.set(str(open_hour4))
        var7.set(str(open_hour5))
        var8.set(str(open_hour6))
        var9.set(str(open_hour7))
        var10.set(str(categories1))
        var11.set(str(categories2))


# more info button
get_info = Button(window, text='more details', font=('Cooper Black', 12), width=10, height=1, command=hit_me,
                  bg='white', fg='red')
get_info.place(x=370, y=105)

window.mainloop()


