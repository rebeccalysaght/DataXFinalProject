from tkinter import *
from PIL import Image, ImageTk
import pandas as pd

window = Tk()
window.title('feedback')
window.geometry('500x500')

# welcome image
welcome = Image.open("picture.gif")
welcome = welcome.resize((500, 500))
canvas = Canvas(window, height=500, width=500)
image_file = ImageTk.PhotoImage(welcome)
image = canvas.create_image(0, 0, anchor='nw', image=image_file)
canvas.pack(side='top')

# list the feedback questions
Label(window, text='Your feedback will make us better !', font=('Cooper Black', 15),
      bg='white', fg='red').place(x=40, y=75)
#Label(window, text='(1 for totally not, 5 for definitely yes)', font=('Cooper Black', 12), bg='white', fg='red').place(
    #x=40, y=105)
Label(window, text='How comfortable were you traveling the distance ?', font=('Cooper Black', 13), bg='white', fg='red').place(x=40, y=150)
Label(window, text='How useful do you find the global star?', font=('Cooper Black', 13),
      bg='white', fg='red').place(x=40, y=230)
Label(window, text='would you mind putting in your thoughts here ?', font=('Cooper Black', 13), bg='white', fg='red').place(
    x=40, y=310)
comments = StringVar()
entry_comments = Entry(window, textvariable=comments, font=('Arial', 12), bg='white', fg='red', width=45, )
entry_comments.place(x=40, y=340)

v1 = IntVar()
v2 = IntVar()



for i in range(1, 6):
    Radiobutton1 = Radiobutton(window, variable=v1, text=i, value=i, font=('Cooper Black', 13), bg='white', fg='red')
    m = 70 * i
    Radiobutton1.place(x=m, y=190)


for i in range(1, 6):
    Radiobutton2 = Radiobutton(window, variable=v2, text=i, value=i, font=('Cooper Black', 13), bg='white', fg='red')
    m = 70 * i
    Radiobutton2.place(x=m, y=270)




def selection():
    alpha1 = v1.get()
    alpha2 = v2.get()
    feedback = comments.get()
    print("The user has given the feedback ! \nthe answers for 3 questions in feedback are:\n" \
          + "question1: " + str(alpha1) + "\n" "question2: " + str(alpha2) + "\n" + "question3: " + str(feedback))


checkButton = Button(window, text='finish', font=('Cooper Black', 14), bg='white', fg='red', command=selection)
checkButton.place(x=200, y=430)

window.mainloop()
