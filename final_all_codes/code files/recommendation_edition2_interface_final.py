from tkinter import *
from PIL import Image, ImageTk
import pandas as pd
from tkinter import ttk

window = Tk()
window.title('recommendation')
window.geometry('500x500')

# welcome image
welcome = Image.open("picture.gif")
welcome = welcome.resize((500, 500))
canvas = Canvas(window, height=500, width=500)
image_file = ImageTk.PhotoImage(welcome)
image = canvas.create_image(0, 0, anchor='nw', image=image_file)
canvas.pack(side='top')

label1 = Label(window, text='Your Location is:  ', font=('Cooper Black', 12), bg='white', fg='red')
label1.place(x=70, y=70)
label2 = Label(window, text='How important is the distance to you?  ', font=('Cooper Black', 12), bg='white', fg='red')
label2.place(x=70, y=130)
location = StringVar()
entry_location = Entry(window, textvariable=location, font=('Arial', 12), bg='white', fg='red', width=35)
entry_location.place(x=70, y=100)
v = IntVar()
for i in range(1, 6):
    button = Radiobutton(window, variable=v, text=i, value=i, font=('Cooper Black', 12), bg='white', fg='red')
    m = 70 * i
    button.place(x=m, y=150)
# show the recommendations
textLabel1 = Label(window, text="name:", font=('Cooper Black', 12), bg='white', fg='red')
textLabel1.place(x=60, y=250)
textLabel2 = Label(window, text="star:", font=('Cooper Black', 12), bg='white', fg='red')
textLabel2.place(x=60, y=270)
textLabel3 = Label(window, text="distance:", font=('Cooper Black', 12), bg='white', fg='red')
textLabel3.place(x=60, y=290)
textLabel4 = Label(window, text="categories:", font=('Cooper Black', 12), bg='white', fg='red')
textLabel4.place(x=60, y=310)

var1 = StringVar()
display_detail1 = Label(window, textvariable=var1, font=('Arial', 11), bg='white', fg='red')
display_detail1.place(x=160, y=250)

var2 = StringVar()
display_detail2 = Label(window, textvariable=var2, font=('Arial', 11), bg='white', fg='red')
display_detail2.place(x=160, y=270)

var3 = StringVar()
display_detail3 = Label(window, textvariable=var3, font=('Arial', 11), bg='white', fg='red')
display_detail3.place(x=160, y=290)

var4 = StringVar()
display_detail4 = Label(window, textvariable=var4, font=('Arial', 11), bg='white', fg='red')
display_detail4.place(x=160, y=310)

var5 = StringVar()
display_detail5 = Label(window, textvariable=var5, font=('Arial', 11), bg='white', fg='red')
display_detail5.place(x=160, y=330)


# take the distance as a feature


def recommend():
    Beta = v.get()
    re_after_geo = pd.read_csv('data_with_distance.csv')
    distance = re_after_geo['Dis_norm'].tolist()
    global_star = re_after_geo['y'].tolist()
    average_star = re_after_geo['stars'].tolist()
    prediction_star = []
    param = float(Beta / 5)
    print(param)
    for i in range(0, len(distance)):
        star = float(global_star[i])
        dis = float(distance[i])
        mean_star = float(average_star[i])
        value = (0.5 * mean_star + 0.5 * star + 0.5 * param * dis*5) / (0.5 + 0.5 + 0.5 * param)
        prediction_star.append(value)
    re_after_geo['predicted_star'] = prediction_star
    re_after_geo = re_after_geo.sort_values(by=['predicted_star'], ascending=False)
    name_list = re_after_geo['name'].tolist()
    name = name_list[0]
    star_list =re_after_geo['stars'].tolist()
    star_show = star_list[0]
    distance_list = re_after_geo['Distance'].tolist()
    distance_show = round(distance_list[0], 2)

    categories_all = re_after_geo['categories'].tolist()
    d = re.findall(r"'(.*?)'", str(categories_all[0]), re.DOTALL)
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
    var1.set(str(name))
    var2.set(str(star_show))
    var3.set(str(distance_show))
    var4.set(str(categories1))
    var5.set(str(categories2))


def next():
    Beta = v.get()
    re_after_geo = pd.read_csv('data_with_distance.csv')
    distance = re_after_geo['Dis_norm'].tolist()
    global_star = re_after_geo['y'].tolist()
    average_star = re_after_geo['stars'].tolist()
    prediction_star = []
    param = float(Beta / 5)
    print(param)
    for i in range(0, len(distance)):
        star = float(global_star[i])
        dis = float(distance[i])
        mean_star = float(average_star[i])
        value = (0.5 * mean_star + 0.5 * star + 0.5 * param * dis*5) / (0.5 + 0.5 + 0.5 * param)
        prediction_star.append(value)
    re_after_geo['predicted_star'] = prediction_star
    re_after_geo = re_after_geo.sort_values(by=['predicted_star'], ascending=False)
    name_list = re_after_geo['name'].tolist()
    name = name_list[1]
    star_list =re_after_geo['stars'].tolist()
    star_show = star_list[1]
    distance_list = re_after_geo['Distance'].tolist()
    distance_show = round(distance_list[1], 2)
    categories_all = re_after_geo['categories'].tolist()
    d = re.findall(r"'(.*?)'", str(categories_all[1]), re.DOTALL)
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
    var1.set(str(name))
    var2.set(str(star_show))
    var3.set(str(distance_show))
    var4.set(str(categories1))
    var5.set(str(categories2))

recommendation_button = Button(window, text='See Recommendations', font=('Cooper Black', 13), bg='white', fg='red', command=recommend)
recommendation_button.place(x=130, y=200)
next_button = Button(window, text='NEXT', font=('Cooper Black', 13), bg='white', fg='red', command=next)
next_button.place(x=200, y=360)

window.mainloop()