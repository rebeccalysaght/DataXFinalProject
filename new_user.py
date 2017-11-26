import pandas as pd

# old user: users who have several reviews already
user_like = pd.read_csv('user_like_categories.csv')
user = pd.read_csv('user_top1000.csv')
user_id = user['user_id'].tolist()
new_user_cuisine = ['Chinese', 'Greek', 'Italian', 'Japanese', 'Russian']
new_user_food = ['Barbeque', 'Chicken Wings', 'Donuts', 'Fondue', 'Hot Pot']


similarity = []
for i in range(0, len(user_id)):
    cuisine_alike = 0
    food_alike = 0
    # get the categories the old users like
    old_user_like = user_like[user_id[i]].tolist()
    # if the new_user have a same preference as old user, we will add 1 to alike_acount
    for j in range(0, len(new_user_cuisine)):
        if new_user_cuisine[j] in old_user_like:
            cuisine_alike = cuisine_alike + 1
    for k in range(0, len(new_user_food)):
        if new_user_food[k] in old_user_like:
            food_alike = food_alike + 1
    alike_acount = cuisine_alike + food_alike
    # we can get the alike_acount by comparing the old and the new, and regard it as the degree of similarity between
    # the new user and old users
    similarity.append(alike_acount)

# find the similar users (the same as finding highest similarity)
user_index = similarity.index(max(similarity))
similar_user = user_id[user_index]
print(similar_user)

