import pickle
import random
import re

import numpy as np
import requests
from flask import Flask, render_template, request

# loading pickle files
popular_df = pickle.load(open('popular.pkl', 'rb'))
pt = pickle.load(open('pt.pkl', 'rb'))
books = pickle.load(open('books.pkl', 'rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl', 'rb'))

# For finding similar recommendation :used in getResponse():
def recommend(inp):
    if inp == "":
        return "Please Enter a book name."
    else:
        index = np.where(pt.index == inp)[0][0]
        similar_items = sorted(
            list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:5]
        data = []
        for i in similar_items:
            item = []
            temp_df = books[books['Book-Title'] == pt.index[i[0]]]
            item.extend(list(temp_df.drop_duplicates(
                'Book-Title')['Book-Title'].values))
            item.extend(list(temp_df.drop_duplicates(
                'Book-Title')['Book-Author'].values))
            item.extend(list(temp_df.drop_duplicates(
                'Book-Title')['Image-URL-M'].values))

            data.append(item)
            strr = "<h3>Here are some similar books </h3></br> \n"
        for book in data:
            strr += """
                        <p><b>Book Name: </b>""" + book[0]+""" </p><br/>
                        <p><b>Author: </b>"""+book[1].capitalize() + """</p>
                        <br/><a  target='_blank' href='https://www.google.com/search?q=""" + book[0] + """ book'><img src=' """ + book[2] + """ ' ></a><br/><br/>
                    """
        return strr

# Output random responses as if it didn't understand :Used in responses():
def ambiguityResponse():
    rand = random.randint(0, 5)
    response = [
        "Sorry! I didn't understand that😥😓",
        "I beg your pardon?", "Sorry, I’m afraid I don’t follow you.",
        "Excuse me, could you repeat the question?",
        "I’m sorry, I don’t understand.",
        "I’m confused. Could you tell me again?",
        "I don’t get it…"
    ]
    return response[rand]

# This contain list of rules and responses.:Used in GetTopBook():
def responses(msg, book_suggestion):
    inp = sanitizeText(msg)

    if inp == "hello":
        return "Hi there, how can I help? 😊"

    elif inp == "hi" or inp == "hii" or inp == "hiiii":
        return "Hi there, what can I do for you?🙂"

    elif inp == "how old are you" or inp == "what is your age" or inp == "are you younger than me":
        return "I'm just a few weeks old?🙂😅"
    
    elif inp == "how are you" or inp == "how are you?":
        return "Fine! and you?"

    elif inp == "fine" or inp == "i am fine" or inp == "i m fine" or inp == "i am good" or inp == "i am doing good":
        return "Great! how can I help you."

    elif inp == "thanks" or inp == "thank you" or inp == "now its my time":
        return "My pleasure !👌😄"

    elif inp == "what do you do" or inp == "have you something":
        return "Well I can give you recommendation."

    elif inp == "tell me a joke" or inp == "tell me something funny" or inp == "crack a funny line":
        return "What did the buffalo say when his son left for college? Bison!"

    elif inp == "okay" or inp == "hmm" or inp == "yup":
        return "Okay"

    elif inp == "ok" or inp == "okk" or inp == "okkkkk":
        return "Hmm"

    elif inp == "goodbye" or inp == "good bye" or inp == "bye" or inp == "see you later" or inp == "see yaa":
        return "Have a nice day!"

    elif inp == "show me a recommendation" or inp == "show me a book" or inp == "give me a book to read":
        return "<p> Here you go! 🙂 " + book_suggestion + "</p>"

    elif inp == "i am bored" or inp == "im bored" or inp == "i m bored" or inp == "i'm bored":
        return "<p> Read this book 🙂 " + book_suggestion + "</p>"

    elif inp == "recommend me a book" or inp == "suggest me a book" or inp == "suggest me something interesting":
        return "<p> I hope you like it!😊 " + book_suggestion + "</p>"

    elif inp == "what should i read today" or inp == "recommend me something":
        return "<p> This one seems interesting enough! " + book_suggestion + "</p>"

    else:
        return ambiguityResponse()


# This function will sanitize the user input and prepare the text for passing to the function :Used in responses():
def sanitizeText(inp):
    # removing extra spaces
    " ".join(inp.split())

    # Converting to Lower
    inp = inp.lower()

    # Removing unnecessary symbols & punctuation
    inp = re.sub('[^A-Za-z0-9 ]+', '', inp)
    return inp


def formatResponse(data, title, author, thumbnail, infoLink):
    book_suggestion = """
    <div class='book'>
        <a style='margin:5px' target='_blank' href='"""+infoLink+"""'><img src='""" + data[thumbnail] + """' /></a>
        <p><b>Book Name: </b>""" + data[title] + """ </p>
        <p><b>Author: </b>""" + data[author] + """</p>
    </div>
    """
    return book_suggestion

# for getting top books :Used in GenerateRecommendation():
def getTopBook():
    # Picking a Random Book from Top Selling books
    book_name = list(popular_df['Book-Title'].values)
    book_author = list(popular_df['Book-Author'].values)
    img_url = list(popular_df['Image-URL-M'].values)
    rand = random.randint(0, 49)
    book = book_name[rand]
    author = book_author[rand]
    img = img_url[rand]
    data = {"book": book, "img": img, "author": author}
    return data

# This function will return a random book recommendation.
def GenerateRecommendation(inp):
    TopBook = getTopBook()
    infoLink = "https://www.google.com/search?q=" + TopBook['book'] + " book"
    book_suggestion = formatResponse(
        TopBook, "book", "author", "img", infoLink)

    return responses(inp, book_suggestion)


# fetch results from google books api
def fetchBooksFromAPI(term):
    bookUrl = "https://www.googleapis.com/books/v1/volumes"
    apiKey = "key=AIzaSyDtXC7kb6a7xKJdm_Le6_BYoY5biz6s8Lw"
    placeHldr = '<img src="https://via.placeholder.com/150">'
    # Here wil come the keyword that user is searching for from (User Input)
    searchData = ""
    searchData = {"q": term}
    if searchData == "" or searchData == None:
        print("Search Term cannot be blank")
    else:
        x = requests.get(bookUrl, params=searchData, headers={
                         'Accept': 'application/json'})
        data = x.json()

    return data


def extractProps(items):
    rows = []
    for r in items:
        if 'title' not in r['volumeInfo'] or 'authors' not in r['volumeInfo'] or 'subtitle' not in r['volumeInfo'] or 'imageLinks' not in r["volumeInfo"]:
            continue

        title = r['volumeInfo']['title']
        subtitle = r['volumeInfo']['subtitle']
        infoLink = r['volumeInfo']['infoLink']
        author = r['volumeInfo']['authors'][0]
        thumbnail = r['volumeInfo']['imageLinks']['thumbnail']
        rows += [dict(title=title, subtitle=subtitle, author=author,
                      thumbnail=thumbnail, infoLink=infoLink)]
    return rows


app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/api/<category>')
def api(category):
    # Responses: infoLink, subtitle, title, thumbnail, authors
    response = fetchBooksFromAPI(category)
    books = extractProps(response['items'])
    return books  # iterate over books
    # return books[0]['title']


@app.route('/getResponse')
def getResponse():
    data = request.args.get("msg")
    words = ["related", "to", "show"]
    if any(x in data for x in words):
        # Example: Show me something related to "Travelling"
        keyword = re.findall('"([^"]*)"', data)
        keyword = keyword[0]

        # searching for books with similar keyword
        response = fetchBooksFromAPI(keyword)
        books = extractProps(response['items'])
        res = ""
        for book in books:
            res += formatResponse(book, "title", "author",
                                  "thumbnail", book["infoLink"])
        return res

    elif "recommend:" in data:
        term = data[10:]
        try:
            response = recommend(term)
            return response
        except:
            return "I can't find what you are looking for, try with different terms.😅😅"

    else:
        return GenerateRecommendation(data)


if __name__ == '__main__':
    # fetchBookFromAPI("Travelling")
    app.run(debug=True)
