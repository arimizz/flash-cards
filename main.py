from tkinter import *
import pandas
from random import choice
import time

BACKGROUND_COLOR = "#B1DDC6"
FONT_LANGUAGE = ("Arial", 40, "italic")
FONT_WORD = ("Arial",60,"bold")
current_card = {}
to_learn = {}

# ---------------------------- Words SETUP ------------------------------- #

try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


# ---------------------------- RIGHT SETUP ------------------------------- #
def is_known():
    to_learn.remove(current_card)
    data = pandas.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv",index=False)
    next_card()

def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = choice(to_learn)
    canvas.itemconfig(card_title, text="French", fill="black", font=FONT_LANGUAGE)
    canvas.itemconfig(card_word, text=current_card["French"], fill="black", font=FONT_WORD)
    canvas.itemconfig(current_image,image=card_image_front)
    flip_timer = window.after(3000,func=flip_card)

def flip_card():
    canvas.itemconfig(card_title, text="English", fill="white", font=FONT_LANGUAGE)
    canvas.itemconfig(card_word, text=current_card["English"], fill="white", font=FONT_WORD)
    canvas.itemconfig(current_image,image=card_image_back)



# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Flash Card App")
window.config(padx=50,pady=50, bg=BACKGROUND_COLOR)
flip_timer = window.after(3000,func=flip_card)


#making canvas
canvas = Canvas(width=800,height=600, bg=BACKGROUND_COLOR, highlightthickness=0)
card_image_front = PhotoImage(file="./images/card_front.png")
card_image_back = PhotoImage(file="./images/card_back.png")

current_image = canvas.create_image(400,300,image=card_image_front)
canvas.grid(row=0,column=0,columnspan=2)

#language text
card_title = canvas.create_text(400, 150,text="",fill="black",font=FONT_LANGUAGE)
card_word = canvas.create_text(400,300,text=f"",fill="black",font=FONT_WORD)

#button
wrong_image = PhotoImage(file="./images/wrong.png")
wrong = Button(image=wrong_image, highlightthickness=0,bd=0, activebackground=BACKGROUND_COLOR,command=next_card)
wrong.grid(row=1,column=0)

right_image = PhotoImage(file="./images/right.png")
right = Button(image=right_image, highlightthickness=0,bd=0, activebackground=BACKGROUND_COLOR,command=is_known)
right.grid(row=1,column=1)


next_card()
window.mainloop()