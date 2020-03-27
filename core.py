### core functions for operating the algorithm

import random

def rating_index(ratings):

    # computes the ratings index
    # for the user ratings selected

    r_index = 0
    for r in ratings:
        r_index += abs(r)

    return r_index


def dprod(a, b):

    # computes the dot product
    # between the two specified ratings vectors

    if len(a) != len(b):    # raise a ValueError if the vectors are incompatible for dot product, as this isn't really something the user could change
        raise ValueError('The specified rating vectors have different lengths. FIX: make sure the vectors are all the same size, i.e. there is the same number of ratings for every user.')
    else:
        dprod_tot = 0
        for i in range(len(a)):
            prod = a[i] * b[i]
            dprod_tot += prod

        return dprod_tot


def compute_similarity(user, userb, ratings):
    
    # computes the similarity score
    # for the two specified users

    rating_a, rating_b = ratings[user][1], ratings[userb][1]    # get the ratings vectors from the users
    try:
        dprod(rating_a, rating_b)
    except ValueError:      # if thrown, ripple up the ValueError from the dprod() function
        raise
    else:
        dot_product = dprod(rating_a, rating_b)

    return dot_product


def compute_sorted_scores(user, ratings):

    # computes the similarities scores
    # for the specified user
    # coupled with all other users
    # then stores them in a list
    # sorted based on the score:
    # [(user, index, score), ...]

    scores = []
    for userb in ratings.keys():
        if user != userb:
            userb_index = ratings[userb][0]
            similarity = compute_similarity(user, userb, ratings)
            scores.append((userb, userb_index, similarity))

    sorted_scores = sorted(scores, key=lambda x: -x[2])
    return sorted_scores


def recommend(user, n, ratings, scores, rating_thr=1, score_thr=None):

    # core algorithm for making the recommendations
    # ---------------------------------------------
    # computes 'n' book recommendations
    # for the specified user
    # considering the various thresholds
    # and returns them:
    # {(user, index, score): [(book, rating), ...]}
    # all while logging the process to
    # 'logs/recommend-{user}_log.txt'

    with open(f'logs/recommend-{user}_log.txt', 'w') as log:
        recommended = []                                    # list of indices of books that have already been recommended
        recommendations = {}                                # dictionary with all the recommendations data, ready to be sent out
        user_index, user_rating = ratings[user]             # current user ratings index and ratings, looked up from the ratings dictionary
        top = [0, 5]                                        # data about the current top recommendation...

        log.write(f'''logging recommendation algorithm run for\t{user}...
\t\t\t\t\t\t\t\t\t\t\t{user_index} index:
\t\t\t{user_rating}\n\n''')

        # make one new recommendation per loop until the number of recommendations is satisfied:
        while len(recommended) < n:
            top_user, top_rating = tuple(top)               # ...as [user, rating], in a list to be modifiable
            userb = scores[top_user]                        # data from the current top recommended user
            userb_name, userb_index, userb_score = userb    # unpacked in username, ratings index and similarity score
            userb_rating = ratings[userb_name][1]           # ratings from the current top recommended user
            
            log.write(f'''looping through user\t{top_user}: {userb_name}...
\t\t\t\t\t\t{userb_index} index:
\t\t\t{userb_rating}
\twith top rating\t\t{top_rating}\n''')

            lower_rating = True                 # (re)set the flag for lowering the current top user's top rating

            # loop through all the ratings in the ratings vector:
            for i in range(len(userb_rating)):

                log.write(f'''\titem {i}:
\t{userb_rating[i]}\tfor {userb_name}; 
\t{user_rating[i]}\tfor {user};
\tout of top rating of {top_rating}.\n''')

                # if the loop has got to the end of the ratings vector but found no suitable rating:
                if i not in recommended and user_rating[i] == 0 and userb_rating[i] == top_rating:
                    lower_rating = False        # set the flag in order to keep the current top rating
                    recommended.append(i)       # add the recommended book to the list of recommended indices 
                    recommendations.update({    # and update the dictionary of recommendations
                        userb:
                        recommendations.get(
                            userb,
                            []) + [(i, top_rating)]
                    })

                    log.write(f'''\t\tdeactivating lower rating flag. updating:
\t\trecommended:\t\t{recommended}
\t\trecommendations:\t{recommendations}.\n''')

                    break
            
            # after the loop, if no book with the current top rating was found, lower it...
            if lower_rating:
                log.write('\t\tlower rating flag active.\n')
                top[1] -= 1
                log.write(f'\t\tlowering top rating to {top[1]}...\n')

                # ...and if the top rating exceeds the rating threshold, skip to the next user
                if top[1] < rating_thr:
                    log.write(f'specified rating threshold of {rating_thr} exceeded by {top[1]}\n')
                    top[0] += 1
                    top[1] = 5
                    log.write(f'\tprogressing top user to user {top[0]}...\n')
            
            # if a similarity score threshold is specified
            # check if the current top recommended user's score exceeds it
            if score_thr is not None:               
                if scores[top[0]][1] < score_thr:

                    log.write(f'''\nRECOMMENDATIONS HALTED:
specified similarity score threshold of\t{score_thr}
exceeded by\t\t\t{scores[top[0]][1]}.
CURRENT RECOMMENDATIONS ({len(recommended)}/{n}):
{recommendations}
FIX: lower the similarity score threshold and retry.\n''')
                    print('''RECOMMENDATIONS HALTED:
specified similarity score threshold exceeded.
check the log at /logs/recommend_log.txt for more information.''')

                    break

            # (a rating threshold is specified by default to 1,
            # thanks to its improved reliability
            # compared to the similarity score threshold)
            # check if there are no more users to recommend --
            # which would cause an error next loop, as the top tuple is unpacked:
            # the current top recommended user would be out of the list
            if top[0] == len(scores):

                log.write(f'''\nRECOMMENDATIONS HALTED:
ran out of the\t\t\t{len(scores)} users
above the specified rating threshold of\t{rating_thr}.
CURRENT RECOMMENDATIONS ({len(recommended)}/{n}):
{recommendations}
FIX: lower the rating threshold or extend the ratings list and retry.\n''')
                print('''RECOMMENDATIONS HALTED:
ran out of users above the specified rating score threshold.
check the log at /logs/recommend_log.txt for more information.''')

                break
    
        log.write(f'\nCheck the output file at /data/output/output-{user}.txt for the formatted output delivered by this logged run of the recommendation algorithm.')
    return recommendations


def random_recommend(n, books):

    # randomly picks 'n' book recommendations
    # for the specified user
    # and returns them in a plain list:
    # [book, ...]

    to_recommend = [i for i in range(len(books))]
    r_recommendations = []

    # simply loop n times, picking a new random recommendation each time
    for i in range(n):
        n = random.choice(to_recommend)
        to_recommend.remove(n)
        r_recommendations.append(n)
    
    return r_recommendations
