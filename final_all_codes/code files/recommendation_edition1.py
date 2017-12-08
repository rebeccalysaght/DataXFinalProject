import pandas as pd
import numpy as np
from scipy.sparse.linalg import svds

# get the restaurants information we need for prediction from business file
restaurants = pd.read_csv('bus.csv')
# get the users information from user file
user = pd.read_csv('user_top1000.csv')
# get the rating information we need for prediction from review file
rating = pd.read_csv('usr.csv')

# change the format of ratings matrix to be one row per user id and one column per restautant id
Rating_df = rating.pivot(index='user_id', columns='business_id', values='stars').fillna(0)
Rating_df.head()
# de-mean the data (normalize by each users mean) and convert it from a dataframe to a numpy array.
Rating = Rating_df.as_matrix()
user_ratings_mean = np.mean(Rating, axis=1)
Rating_demeaned = Rating - user_ratings_mean.reshape(-1, 1)
# use the Scipy function svds to do the singular value decomposition
U, sigma, Vt = svds(Rating_demeaned, k=50)
# since I’m going to leverage matrix multiplication to get predictions I’ll convert it to the diagonal matrix form
sigma = np.diag(sigma)
# Making Predictions from the Decomposed Matrices
all_user_predicted_ratings = np.dot(np.dot(U, sigma), Vt) + user_ratings_mean.reshape(-1, 1)
preds_df = pd.DataFrame(all_user_predicted_ratings, columns=Rating_df.columns)


def recommend_restaurants(predictions_df: object, user_number: object, restaurants: object, original_ratings_df: object,
                          num_recommendations: object = 5) -> object:
    # Get and sort the user's predictions
    user_row_number = user_number   # UserID starts at 1, not 0
    sorted_user_predictions = predictions_df.iloc[user_row_number].sort_values(ascending=False)

    # Get the user's data and merge in the restaurant information.
    user_data = original_ratings_df[original_ratings_df.user_id == str(user['user_id'][user_number])]
    user_full = (user_data.merge(restaurants, how='left', left_on='business_id', right_on='business_id').
                 sort_values(['stars'], ascending=False)
                 )

    print('User {0} has already rated {1} restaurant.'.format(user_number, user_full.shape[0]))
    print('Recommending the highest {0} predicted ratings restaurant not already rated.'.format(num_recommendations))

    # Recommend the highest predicted rating restaurants that the user hasn't seen yet.
    restaurants_new = restaurants[~restaurants['business_id'].isin(user_full['business_id'])]. \
        merge(pd.DataFrame(sorted_user_predictions).reset_index(), how='left', left_on='business_id',
              right_on='business_id'). \
        rename(columns={user_row_number: 'Predictions'}). \
        sort_values('Predictions', ascending=False)
    recommendations = (restaurants_new[restaurants_new['state'] == 'AZ'].iloc[:100, :-1])
    recommendations = recommendations.reset_index()
    del recommendations['index']
    # find the fake restaurants (other service stores in yelp) and drop them
    for i in range(0, len(recommendations) - 1):
        if 'Restaurants' not in recommendations.loc[i]['categories']:
            recommendations = recommendations.drop(i)
    new_recommendations = recommendations.iloc[:num_recommendations, :-1]
    return user_full, new_recommendations


# based on the user_id, get the index(user_number) in the dataframe
num_user = user[user['user_id'] == 'DK57YibC5ShBmqQl97CKog'].index.tolist()
num = num_user[0]
already_rated, predictions = recommend_restaurants(preds_df, int(num), restaurants, rating, 10)
user_name = user[user['user_id'] == 'DK57YibC5ShBmqQl97CKog']['name'].tolist()
name = user_name[0]
print("hi!" + name + " ! We will recommend you: ")
print(predictions['name'])
