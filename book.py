import numpy as np
import pandas as pd

books = pd.read_csv('books.csv', low_memory=False)
users = pd.read_csv('users.csv', low_memory=False)
ratings = pd.read_csv('ratings.csv', low_memory=False)
books.head()
# print(books.isnull().sum())
# print(users.isnull().sum())
# print(ratings.isnull().sum())
ratings_with_name = ratings.merge(books, on='ISBN')
num_rating_df = ratings_with_name.groupby('Book-Title').count()['Book-Rating'].reset_index() #df = dataframe
num_rating_df.rename(columns={'Book-Rating': 'num_ratings'}, inplace=True )
# print(num_rating_df)

avg_rating_df = ratings_with_name.groupby('Book-Title').mean(numeric_only=True)['Book-Rating'].reset_index() #df = dataframe
avg_rating_df.rename(columns={'Book-Rating': 'avg_rating'}, inplace=True )
# print(avg_rating_df)

popular_df = num_rating_df.merge(avg_rating_df, on='Book-Title')
popular_df[popular_df['num_ratings']>= 250].sort_values('avg_rating', ascending=False).head(50)

popular_df = popular_df.merge(books, on='Book-Title').drop_duplicates('Book-Title')[['Book-Title', 'Book-Author', 'Image-URL-M', 'num_ratings', 'avg_rating']]
# print(popular_df) # << Popularity Based Data

#For Collaborative Filtering Based Rcc
x = ratings_with_name.groupby('User-ID').count()['Book-Rating'] > 200
experienced_users = x[x].index

filtered_rating = ratings_with_name[ratings_with_name['User-ID'].isin(experienced_users)]
filtered_rating.groupby('Book-Title').count()
print(filtered_rating)