from tkinter import *
from PIL import Image, ImageTk
import pandas as pd

window = Tk()
window.title('sign up')
window.geometry('500x500')

# welcome image
welcome = Image.open("picture.gif")
welcome = welcome.resize((500, 500))
canvas = Canvas(window, height=500, width=500)
image_file = ImageTk.PhotoImage(welcome)
image = canvas.create_image(0, 0, anchor='nw', image=image_file)
canvas.pack(side='top')

# get the data the new user may use for preference choosing
user_like = pd.read_csv('user_like_categories.csv')
user = pd.read_csv('user_top1000.csv')
user_id = user['user_id'].tolist()
food = pd.read_csv('particular food preference.csv')
food_preference = food['special_preference'].tolist()
cuisine = pd.read_csv('cuisine.csv')
cuisine_preference = cuisine['cuisines'].tolist()
# build the frame of interface
Label(window, text='email address: ', font=('Cooper Black', 12), bg='white', fg='red').place(x=40, y=90)
Label(window, text='Password: ', font=('Cooper Black', 12), bg='white', fg='red').place(x=40, y=120)
Label(window, text='Password confirm: ', font=('Cooper Black', 12), bg='white', fg='red').place(x=40, y=150)
Label(window, text='cuisine preference ', font=('Cooper Black', 12), bg='white', fg='red').place(x=40, y=200)
Label(window, text='food preference ', font=('Cooper Black', 12), bg='white', fg='red').place(x=290, y=200)
var_usr_id = StringVar()
entry_usr_id = Entry(window, textvariable=var_usr_id, font=('Arial', 12), fg='red', width=25)
entry_usr_id.place(x=210, y=90)
var_usr_pwd = StringVar()
entry_usr_pwd = Entry(window, textvariable=var_usr_pwd, font=('Arial', 12), fg='red', width=25, show='*')
entry_usr_pwd.place(x=210, y=120)
var_usr_pwd_confirm = StringVar()
entry_usr_pwd_confirm = Entry(window, textvariable=var_usr_pwd_confirm, font=('Arial', 12), fg='red', width=25,
                              show='*')
entry_usr_pwd_confirm.place(x=210, y=150)

# get the preferences the new user choose
selected_preference = []
similar_user = ''


def CurSelet(event):
    widget = event.widget
    selection = widget.curselection()
    for i in range(0, len(selection)):
        widget.itemconfigure(selection[i], fg='red')
        picked = widget.get(selection[i])
        if picked not in selected_preference:
            selected_preference.append(picked)
    similarity = []
    for i in range(0, len(user_id)):
        preference_alike = 0
        # get the categories the old users like
        old_user_like = user_like[user_id[i]].tolist()
        # if the new_user have a same preference as old user, we will add 1 to alike_acount
        for j in range(0, len(selected_preference)):
            if selected_preference[j] in old_user_like:
                preference_alike = preference_alike + 1
        similarity.append(preference_alike)
    user_index = similarity.index(max(similarity))
    similar_user = user_id[user_index]
    print(similar_user)
    print(selected_preference)
    return similar_user


cuisine_choice = Listbox(window, selectmode=MULTIPLE, height=10)
cuisine_choice.bind('<<ListboxSelect>>', CurSelet)
cuisine_choice.place(x=40, y=220)
for item in cuisine_preference:
    cuisine_choice.insert(END, item)
food_choice = Listbox(window, selectmode=MULTIPLE, height=10)
food_choice.place(x=290, y=220)
food_choice.bind('<<ListboxSelect>>', CurSelet)
for item in food_preference:
    food_choice.insert(END, item)


Signup_Button = Button(window, text='Sign Up', font=('Cooper Black', 14), bg='white', fg='red')
Signup_Button.place(x=190, y=430)

window.mainloop()
