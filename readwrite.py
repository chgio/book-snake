### functions for reading from and writing to input files

from core import rating_index

def read_books(books_file='data/input/books.txt'):

    # reads the file containing the books
    # ('books.txt' by default)
    # and returns the list of tuples:
    # [(author, title), ...]

    books = []
    try:
        with open(books_file) as file:
            for line in file:
                line = line.strip()
                if len(line) != 0:
                    line = line
                    book = line.split(',')
                    books.append(tuple(book))
    except FileNotFoundError:
        raise FileNotFoundError(f'Books file at {books_file} not found. FIX: make sure the file exists, is in the correct directory and has the correct name')
    
    return books


def read_ratings(ratings_file='data/input/ratings.txt'):

    # reads the file containing the rating vectors
    # ('ratings.txt' by default)
    # computes the rating index for every user
    # and returns the dictionary of tuples:
    # {user: (index, (rating, ...)), ...}

    ratings = {}
    try:
        with open(ratings_file) as file:
            user_flag = True
            for line in file:
                line = line.strip()
                if len(line) != 0:
                    if user_flag:
                        user = line
                    else:
                        rating = line.split()
                        rating = tuple(int(r) for r in rating)
                        r_index = rating_index(rating)
                        ratings.update({user: (r_index, rating)})
                    user_flag = not user_flag
    except FileNotFoundError:
        raise FileNotFoundError(f'Ratings file at {ratings_file} not found. FIX: make sure the file exists, is in the correct directory and has the correct name')

    return ratings


def write_ratings(user, ratings, ratings_file='data/input/ratings.txt'):

    # takes the new user and their new ratings:
    # (rating, ...)
    # and writes them to the file containing the rating vectors
    # ('ratings.txt' by default)

    with open(ratings_file, 'a') as file:
        print(user, file=file)

        for elt in ratings:
            print(str(elt) + ' ', end='', file=file)
        print('', file=file)


def printer(recommendations, user, books, ratings, rating_thr, score_thr):

    # takes the recommendations:
    # {(user, index, score): [(book, rating), ...], ...}
    # and outputs them both to standard output
    # and to the main output file
    # 'output-{name}.txt'

    with open(f'data/output/output-{user}.txt', 'w') as file:
        s = f'* Recommendations for: {user} *'
        stars = '*' * len(s)
        s = stars + '\n' + s + '\n' + stars
        print(f'Here are your recommendations based on the similarity algorithm, {user}:')
        print(s, end='\n\n\n', file=file)

        j = 0
        for key, val in recommendations.items():
            r_user, r_index, r_score = key
            s0 = f'Recommended from: {r_user}'
            s1 = f'({r_score} similarity)'
            s2 = f'({r_index} ratings index)'

            s0a = s0.ljust(55)
            s1a = s1.rjust(16)
            sa = s0a + s1a + '\n' + '-' * (len(s0a+s1a) - len(s2)) + s2
            print(sa, end='\n')
            s0b = s0.ljust(45)
            s1b = s1.rjust(18)
            sb = s0b + s1b + '\n' + s2.rjust(len(s0b+s1b)) + '\n' + '-' * len(s0b+s1b)
            print(sb, end='\n\n', file=file)

            for i, elt in enumerate(val):
                n, rating = elt
                author, book = books[n]
                j += 1
                s = f'\t{j:2d}.\t{book}'.ljust(51) + f'(rated {rating})'.rjust(9) + f'\n\t\t\tby {author}'
                print(s, end='\n')
                print(s, end='\n\n', file=file)
            
            print('')
            print('', file=file)
        
        s = f'''{j}\tRecommendations based on the similarity algorithm:
for user:\t\t\t{user}
with ratings index:\t{ratings[user][0]}
and ratings:\t{ratings[user][1]}
with  rating      threshold of:\t{rating_thr}
and   similarity  threshold of:\t{score_thr}\n'''
        print(s, file=file)

        print(f'Check the output file at /data/output/output-{user}.txt and the algorithm log at logs/recommend-{user}_log.txt for more details.')
        print(f'Check the recommendation algorithm log at logs/recommend-{user}_log.txt for more details about the recommendation process.', file=file)


def random_printer(r_recommendations, user, books):

    # takes the random recommendations:
    # [book, ...]
    # and outputs them both to standard output
    # and to the main output file
    # 'output-{user}.txt'
 
    with open(f'data/output/output-{user}.txt', 'w') as file:
        s = f'* Random recommendations for: {user} *'
        stars = '*' * len(s)
        s = stars + '\n' + s + '\n' + stars
        print(f'Here are your random recommendations, {user}:')
        print(s, end='\n\n\n', file=file)

        for i, n in enumerate(r_recommendations):
            author, book = books[n]
            s = f'\t{j}.\t{book}'.ljust(50) + f'\n\t\t\tby {author}'
            print(s, end='\n')
            print(s, end='\n\n', file=file)
            
        print('')
        print('', file=file)

        s = f'''{len(r_recommendations)}\tRandom recommendations:
for:\t\t\t\t{user}
\tsince your rating index is 0:\t{ratings[user][0]}
\t\t({ratings[user][1]})'''
        print(s, file=file)
