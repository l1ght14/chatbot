from tkinter import *

import re
import pickle
import random
import numpy as np

# todo: trim user input

# GUI
root = Tk()
root.title("Chatbot")

BG_GRAY = "#ffffff"
BG_COLOR = "#810034"  # '#2C3E50'
TEXT_COLOR = "#FFF600"
FONT = "Helvetica 14"
FONT_BOLD = "Helvetica 13 bold"
root.configure(background=BG_COLOR)

# loading pickle files
popular_df = pickle.load(open('popular.pkl', 'rb'))
pt = pickle.load(open('pt.pkl', 'rb'))
books = pickle.load(open('books.pkl', 'rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl', 'rb'))


# For finding similar recommendation
def recommend(user_input):
    user_input = user_input.capitalize()

    index = np.where(pt.index == user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:5]

    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

        data.append(item)
        book_suggestion = "Here are some similar books \n"
    for book in data:
        book_suggestion += "Book Name: " + book[0] + "\n" + "Author: " + book[1].capitalize() + "\n" + "URL: " + book[
            2] + "\n \n"

    return book_suggestion


# Send function
def send_it(self):
    send = "You -> " + e.get()
    txt.insert(END, "\n" + send)

    user = e.get().lower()

    # Picking a Random Book from Top Selling books
    book_name = list(popular_df['Book-Title'].values)
    img_url = list(popular_df['Image-URL-M'].values)
    rand = random.randint(0, 49)
    book = book_name[rand]
    img = img_url[rand]

    if "recommend:" in user:
        term = user[10:]
        term = term.capitalize()
        txt.insert(END, "\n" + str(recommend(term)))

    else:
        user = re.sub('[^A-Za-z0-9 ]+', '', user)

        if user == "hello":
            txt.insert(END, "\n" + "Bot -> Hi there, how can I help? 😊\n")

        elif user == "hi" or user == "hii" or user == "hiiii":
            txt.insert(END, "\n" + "Bot -> Hi there, what can I do for you?🙂\n")

        elif user == "how are you" or user == "how are you?":
            txt.insert(END, "\n" + "Bot -> Fine! and you?\n")

        elif user == "show me a recommendation" or user == "show me a book":
            txt.insert(END, "\n" + "Bot -> Here you go! 🙂 \nBook Name: " + book + "\nURL: " + img + "\n")

        elif user == "recommend me a book" or user == "show me a book":
            txt.insert(END, "\n" + "Bot -> I hope you like it!😊 \nBook Name: " + book + "\nURL: " + img + "\n")

        elif user == "what should i read today" or user == "recommend me something":
            txt.insert(END, "\n" + "Bot -> This one seems interesting enough! \nBook Name: " + book + "\nURL: " + img + "\n")

        elif user == "fine" or user == "i am fine" or user == "i m fine" or user == "i am good" or user == "i am doing good":
            txt.insert(END, "\n" + "Bot -> Great! how can I help you.\n")

        elif user == "thanks" or user == "thank you" or user == "now its my time":
            txt.insert(END, "\n" + "Bot -> My pleasure !👌😄\n")

        elif (
                user == "what do you sell" or user == "what kinds of items are there" or user == "have you something" + "\n"):
            txt.insert(END, "\n" + "Bot -> We have coffee and tea\n")

        elif user == "tell me a joke" or user == "tell me something funny" or user == "crack a funny line":
            txt.insert(END, "\n" + "Bot -> What did the buffalo say when his son left for college? Bison.! " + "\n")

        elif user == "goodbye" or user == "good bye" or user == "bye" or user == "see you later" or user == "see yaa":
            txt.insert(END, "\n" + "Bot -> Have a nice day!" + "\n")

        else:
            txt.insert(END, "\n" + "Bot -> Sorry! I didn't understand that😥😓" + "\n")
    e.delete(0, END)


lable1 = Label(root, bg=BG_COLOR, fg=TEXT_COLOR, text="Welcome", font=FONT_BOLD, pady=10, width=20, height=1).grid(
    row=0)
txt = Text(root, bg=BG_COLOR, fg=TEXT_COLOR, font=FONT, width=60)
txt.grid(row=1, column=0, columnspan=2)

lable2 = Label(root, bg=BG_COLOR, fg=TEXT_COLOR, text="<< Type Message Here", font=FONT_BOLD, pady=10, width=20,
               height=1).grid(row=2, column=1)
e = Entry(root, bg="#FF005C", fg="#26001B", font=FONT, width=40)
e.grid(row=2, column=0)

# sendBtn = Button(root, text="Send", font=FONT_BOLD, bg=BG_GRAY,command=send_it).grid(row=2, column=1)

root.bind('<Return>', send_it)

root.mainloop()
