"""
    Author: Eleuterio Juan Lillo Portero
    Github: lute47lillo
    
    Disclaimer: Orginal Idea extracted from blog ->
    https://www.analyticsvidhya.com/blog/2021/06/build-book-recommendation-system-unsupervised-learning-project/
"""
import numpy as np
import pandas as pd

# Using database from Kaggle: https://www.kaggle.com/datasets/rxsraghavagrawal/book-recommender-system?select=BX-Users.csv
# TODO: Find better solution for the low_memory problem
books = pd.read_csv("BX-Books.csv", sep=';', encoding="latin-1", on_bad_lines="skip", low_memory=False)
users = pd.read_csv("BX-Users.csv", sep=';', encoding="latin-1", on_bad_lines="skip", low_memory=False)
ratings = pd.read_csv("BX-Book-Ratings.csv", sep=';', encoding="latin-1", on_bad_lines="skip", low_memory=False)

# Drop URL image columns (Might be necesseary for web APP)
books = books[['ISBN', 'Book-Title', 'Book-Author', 'Year-Of-Publication', 'Publisher']]
#for title_col in books.columns:
 #   print(title_col)

# Format naming conventions
books.rename(columns = {'Book-Title':'title', 'Book-Author':'author', 'Year-Of-Publication':'year', 'Publisher':'publisher'}, inplace=True)
users.rename(columns = {'User-ID':'user_id', 'Location':'location', 'Age':'age'}, inplace=True)
ratings.rename(columns = {'User-ID':'user_id', 'Book-Rating':'rating'}, inplace=True)

# Users with more than 100 ratings
# Rated users User_id -> True/False Based on giving or not it has given review
min_ratings = 200
rated_users = ratings['user_id'].value_counts() > min_ratings

y = rated_users[rated_users].index  #user_ids

# Get rating DFs of user_ids that are on the category of users with rated reviews (rated_users)
ratings = ratings[ratings['user_id'].isin(y)]

# Merge Ratings and books DFs, so now we have User IDs + rating given to specific book.
rating_with_books = ratings.merge(books, on='ISBN')

# Count NAs on rating and reset index, and group them by title (On total count of ratings)
count_rating = rating_with_books.groupby('title')['rating'].count().reset_index()
count_rating.rename(columns= {'rating':'ratings'}, inplace=True)

# Merge with the previous all selected DF 
final_rating = rating_with_books.merge(count_rating, on='title')

# Select what is the minimum amount of ratings to be considered
rating_threshold = 50
final_rating = final_rating[final_rating['ratings'] >= rating_threshold]
final_rating.drop_duplicates(['user_id','title'], inplace=True)
print(final_rating.shape)


# Create Pivot table to organize better the data
'''
    This way we can look instantly, all the ratings a user has done, match it with the title and see the 
    numerical value of the rating
'''
book_pivot = final_rating.pivot_table(columns='user_id', index='title', values="rating")
book_pivot.fillna(0, inplace=True)

# Returns the pivot table DF
def return_df():
    return book_pivot

# Returns the full DF
def get_full_df():
    return final_rating

       

