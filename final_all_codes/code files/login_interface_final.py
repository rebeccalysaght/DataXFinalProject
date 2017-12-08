from tkinter import *
from PIL import Image, ImageTk
import pandas as pd

window = Tk()
window.title('log in')
window.geometry('500x500')

# welcome image
welcome = Image.open("picture.gif")
welcome = welcome.resize((500, 500))
canvas = Canvas(window, height=500, width=500)
image_file = ImageTk.PhotoImage(welcome)
image = canvas.create_image(0, 0, anchor='nw', image=image_file)
canvas.pack(side='top')

# user information
Label(window, text='User ID: ', font=('Cooper Black', 12), bg='white', fg='red').place(x=80, y=110)
Label(window, text='Password: ', font=('Cooper Black', 12), bg='white', fg='red').place(x=80, y=150)
var_usr_id = StringVar()
entry_usr_id = Entry(window, textvariable=var_usr_id, font=('Arial', 12), bg='white', fg='red', width=25)
entry_usr_id.place(x=180, y=110)
var_usr_pwd = StringVar()
entry_usr_pwd = Entry(window, textvariable=var_usr_pwd, font=('Arial', 12), bg='white', fg='red', width=25, show='*')
entry_usr_pwd.place(x=180, y=150)

# check if remember the password
check = Checkbutton(window, text="remember the password", font=('Cooper Black', 12), bg='white', fg='red')
check.place(x=80, y=190)

# login display
var = StringVar()
display_name = Label(window, textvariable=var, bg='white', fg='red', font=('Cooper Black', 15))
display_name.place(x=40, y=400)

# function


def hit_me():
    user_id = var_usr_id.get()
    user = pd.read_csv('user_top1000.csv')
    user_name = user[user['user_id'] == user_id]['name'].tolist()
    print(user_name)

    name = user_name[0]
    var.set("Hi! "+name+" ! Let's start your food journey!")


# login and sign up button

btn_login = Button(window, text='Login', font=('Cooper Black', 13), bg='white', fg='red', command=hit_me)
btn_login.place(x=220, y=240)
new_user = Button(window, text="I'm a new user", font=('Cooper Black', 13), bg='white', fg='red')
new_user.place(x=190, y=300)

window.mainloop()
