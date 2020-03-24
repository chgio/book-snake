import statistics as st

ratings = []
with open('data/input/ratings.txt') as file:
    user_flag = True
    for line in file:
        if not user_flag:
            rating = line.strip().split()
            rating = [int(r) for r in rating]
            zero, total = 0, 0
            for elt in rating:
                total += 1
                if elt == 0:
                    zero += 1
            #ratings.append(zero / total)
            ratings.append(1 - zero / total)
        user_flag = not user_flag

others, user = ratings[:-1], ratings[-1]
print(others)
print()
print(user)

t_mean, t_median = st.mean(ratings), st.median(ratings)
o_mean, o_median = st.mean(others), st.median(others)

print(f'''
\t\tmean:\t\tmedian:
total:\t\t{t_mean:.3f}\t\t{t_median:.3f}
others:\t\t{o_mean:.3f}\t\t{o_median:.3f}
user:\t\t\t{user:.3f}
''')