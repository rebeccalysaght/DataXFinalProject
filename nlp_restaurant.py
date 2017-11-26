# import the packages we need
import warnings

warnings.filterwarnings('ignore')
import pandas as pd
import numpy as np
from sklearn.utils import shuffle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import bs4 as bs
import nltk
import re
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# import the relative files
review = pd.read_csv('review_AZ.csv')
restaurants = pd.read_csv('restaurants_AZ.csv')
# define the function of review_cleaner
eng_stopwords = stopwords.words('english')
ps = PorterStemmer()
wnl = WordNetLemmatizer()


def review_cleaner(reviews, lemmatize=True, stem=False):
    ps = PorterStemmer()
    wnl = WordNetLemmatizer()
    cleaned_reviews = []
    for i, review in enumerate(reviews):
        review = bs.BeautifulSoup(review).text
        emoticons = re.findall('(?::|;|=)(?:-)?(?:\)|\(|D|P)', review)
        review = re.sub("[^a-zA-Z]", " ", review)
        review = review.lower().split()
        eng_stopwords = set(stopwords.words("english"))
        clean_review = []
        for word in review:
            if word not in eng_stopwords:
                if lemmatize is True:
                    word = wnl.lemmatize(word)
                elif stem is True:
                    if word == 'oed':
                        continue
                    word = ps.stem(word)
                clean_review.append(word)
        review_processed = ' '.join(clean_review + emoticons)
        cleaned_reviews.append(review_processed)
    return (cleaned_reviews)


# define the feature extraction function
def feature(restaurant_number):
    restaurant_num = restaurant_number
    review_re = review[review['business_id'] == str(restaurants.loc[restaurant_num]['business_id'])]
    # get the cleaned review of the user by using the review_cleaner function
    lemmatized_review_re = review_cleaner(review_re['text'], lemmatize=True, stem=False)

    # train the nlp model
    np.random.seed(0)
    vectorizer = CountVectorizer(analyzer="word", \
                                 tokenizer=None, \
                                 preprocessor=None, \
                                 stop_words=None, \
                                 max_features=3000)
    lemmatized_review_re = shuffle(lemmatized_review_re)
    X_train, X_test, y_train, y_test = train_test_split( \
        lemmatized_review_re, review_re['stars'], random_state=0, test_size=.2)
    train_bag = vectorizer.fit_transform(X_train).toarray()
    test_bag = vectorizer.transform(X_test).toarray()
    forest = RandomForestClassifier(n_estimators=50)
    forest = forest.fit(train_bag, y_train)
    train_predictions = forest.predict(train_bag)
    test_predictions = forest.predict(test_bag)
    train_acc = metrics.accuracy_score(y_train, train_predictions)
    valid_acc = metrics.accuracy_score(y_test, test_predictions)
    # extract feature importance
    importances = forest.feature_importances_
    indices = np.argsort(importances)[::-1]
    # get the top 2000 important features
    a = [vectorizer.get_feature_names()[ind] for ind in indices[:2000]]
    # since we want to find the user's likes in his positive reviews, the adjectives means nothing, we just choose nouns
    # as features
    str_b = review_cleaner(a, lemmatize=True, stem=False)
    str_c = ' '.join(str(v) for v in str_b)
    token_tag = nltk.tokenize.word_tokenize(str_c)
    pos_tuples = nltk.pos_tag(token_tag)
    noun = []
    abjective = []
    for pair in pos_tuples:
        tag = pair[1]
        if tag == 'NN':
            noun.append(pair[0])
        elif tag == 'JJ':
            abjective.append(pair[0])
    return noun


feature_df = pd.DataFrame()
df = pd.DataFrame()
for i in range(0, 2867):
    re_feature = feature(i)
    df = pd.DataFrame(re_feature)
    feature_df = pd.concat([feature_df, df], ignore_index=True, axis=1)

restaurant_name = restaurants['business_id'].tolist()
feature_df.columns = restaurant_name
feature_df.to_csv('restaurant_feature.csv', encoding='utf-8', index=False)
