"""
    Author: Eleuterio Juan Lillo Portero
    Github: lute47lillo
"""
from data_processing import return_df, get_full_df
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
import numpy as np

# A sparse matrix just reduces time of computation by compressing rows
books_df = return_df()
full_df = get_full_df()
book_sparse = csr_matrix(books_df)

# Fit the model using the non_sparsed DF (ball_tree), otherwise -> brute algorithm
amount_recommended = 5
model = NearestNeighbors(n_neighbors=amount_recommended, algorithm='ball_tree')
model.fit(books_df)

# This is just showing off and example
"""
    books_df.iloc[row, from_col:to_col]
    .values (What value is given(Rating))
    .reshape(-1,1) -> Flattens out the matrix
"""


def get_predictions(pred):
    return pred
    

# This now is giving a concrete example (237, but what if user just wants some recommendation based on similarity)

""" 
    SITUATIONS TO BE SOLVED:
        - Input a particular title that is not exact -> Autocompletition extracting form actual values of the dataframe???
        - Input a title that does not exist.
        - How to parse the titles? (Could create some parsing logic)
        - How to find the specific title
        - Might be interesting to prompt what is the average rating that the book recommended has.
        - Pull image based on recommendations
"""
# Commented out for DEVELOPMENT PURPOSES OF FRONT_END
#input_book = input("Based on what book you'd like your recommendation?:")
#input_book = "Harry Potter and the Chamber of Secrets (Book 2)" -> IS the example for test

"""
    Indexed by title, then it must look closer kneighbors by title inserted based on collaborative filtering
    Dropping closest since its the input book itself.
    TODO:
        Instead based on book, get suggestion from author -> Will imply other model.
"""
distances, suggestions = model.kneighbors(books_df.loc[input_book, :].values.reshape(1, -1))
sug = np.delete(suggestions, 0)
dist = np.delete(distances, 0)
author_input = full_df.loc[full_df['title'] == input_book, 'author'].values[0]

for i in range(len(sug)):
    
    author = full_df.loc[full_df['title'] == books_df.index[sug[i]], 'author'].values[0]
    
    print(books_df.index[sug[i]], "of author", author.title(), "at index row at: ", sug[i], "and distance of: ", dist[i])
  

example_prediction = books_df.index[sug[0]]
#get_predictions(example_prediction)



