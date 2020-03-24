### user interface functions
### and main wrapper function 
### plus execution (*this is the file to run!*)

import random
from readwrite import *
from core import *

def rater(user, books, percentage=20):

    # asks the user to rate a specified percentage of the books
    # (20% by default)
    # and returns the ratings vector

    legend = """3:\tLoved it!!
2:\tLiked it!
1:\tIt was OK.
0:\tHaven't read it (yet).
-1:\tDidn't really like it...
-2\tHated it!"""
    print(f"""Let's get you to rate some books! Here's the legend of the 6 levels:\n{legend}""")

    rating_dict = {
        '3':   (5,
        "Ooh, great!"),
        '2':   (3,
        "Good."),
        '1':   (1,
        "Alright."),
        '0':   (0,
        "Oh, fair enough."),
        '-1': (-3,
        "Kinda meh, right?"),
        '-2': (-5,
        "Ouch!")
    }

    len_books = len(books)
    new_ratings = [0 for i in range(len_books)]     # ratings for all books asked for rating
    to_ask = [i for i in range(len_books)]          # list of books still to be asked for rating
    read = 0                                        # counter for books with a non-0 rating
    while read < len_books*percentage/100 and len(to_ask) > 0:
        n = random.choice(to_ask)
        to_ask.remove(n)

        # ask the user for a rating, sanitise the input and apply it
        while True:                     # loop asking the user to rate the book
            author, title = books[n]    # and handle improper ratings
            s = f"How would you rate:\t{title} ".ljust(40) + f"by\t{author}?\n".ljust(30)
            raw = input(s).strip()

            if raw in rating_dict:      # if proper, break out from the loop
                new_rating, reply = rating_dict[raw]
                break
            else:                       # otherwise ask again, after printing a type-based message
                try:
                    int(raw)
                    print("Out of range! Was it really that good -- or that bad?")
                except ValueError:
                    try:
                        float(raw)
                        print("Ah, I see you're a man of culture as well. We don't ask for that level of precision, though: round numbers will do.")
                    except ValueError:
                        print("That's not a valid rating -- unless you want to go all the way to base 64.")

                print(f"""Please try again, referring to the legend:\n{legend}""")
                continue
        
        # if the new rating is non-0, substitute it in the ratings and increase the counter
        if new_rating != 0:
            read += 1
            new_ratings[n] = new_rating
        print(reply)

    if len(to_ask) == 0:
        print("Ow, we ran out of books to ask you to review. But fear not: we'll expand our database soon!")
    print(f"Alright {user}, you're done with the chores!")
    return tuple(new_ratings)


def wrap():

    # core wrapper for providing the user interface
    # ---------------------------------------------
    # takes care of:
    # prompting the user to rate some books if they're new
    # prompting the user for the number and nature of the recommendations
    # handling general invalid input errors from the user
    # connecting all other functions

    # read the data from the input files
    books = read_books()
    ratings = read_ratings()

    # ask user for identification
    user = input("What's your username? ").strip()
    print("Hold on, lookin' you up...")

    # if the user doesn't appear in the file, get them to rate some books 
    if not user in ratings:
        print(f"Oh hey {user}! You aren't in the database. You must be new!")
        new_ratings = rater(user, books)
        write_ratings(user, new_ratings)
        ratings.update({user: new_ratings})

    else:
        print(f"Welcome back, {user}!")
    scores = compute_sorted_scores(user, ratings)

    # ask the user for the number of recommendations, sanitise the input and apply it
    while True:
        n = input("So, how many recommendations would you like to get? ").strip()
        try:
            n = int(n)
            if n > len(books):
                print("Sorry bookworm, we don't have that many books. But fear not: we'll expand our database soon!")
                continue
            break
        except ValueError:
            print("That's not a valid input. Please try again:")
            continue
    
    # ask the user for a rating threshold, sanitise the input and apply it
    while True:
        rating_thr = input("Do you want to set a rating threshold for the recommended books? value/[N]: ").strip().lower()
        if len(rating_thr) == 0 or rating_thr[0] == 'n':
            rating_thr = 1
            break
        else:
            try:
                rating_thr = int(rating_thr)
                break
            except ValueError:
                print("That's not a valid input. Please try again:")
                continue
    
    # ask the user for a similarity threshold, sanitise the input and apply it
    while True:
        score_thr = input("Do you want to set a similarity threshold for the recommended books? value/[N]: ").strip().lower()
        if len(score_thr) == 0 or score_thr[0] == 'n':
            score_thr = None
            break
        else:
            try:
                score_thr = int(score_thr)
                break
            except ValueError:
                print("That's not a valid input. Please try again:")
                continue

    # check if the user's rating index is zero (meaning they only have 0-ratings)
    r_index = rating_index(ratings[user])

    # if so, compute and print the specified number of recommendations, picked randomly
    if r_index == 0:
        r_recommendations = random_recommend(n, books)
        random_printer(r_recommendations, user, books)

    # otherwise, compute and print the specified number of recommendations, according to the similarity algorithm
    else:
        recommendations = recommend(user, n, ratings, scores, rating_thr, score_thr)
        printer(recommendations, user, books, ratings, rating_thr, score_thr)



## main execution
## **************

wrap()