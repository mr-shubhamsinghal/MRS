# importing pandas and numpy library
import pandas as pd
import numpy as np
import pickle

# importing metadata dataset
df_clean=pd.read_csv("metadata_clean.csv")
# print the head of metadata
#df_clean.head(5)
# importing movies_metadata
df_meta=pd.read_csv("movies_metadata.csv")
#df_meta.head()
df_clean['overview'], df_clean['id'] = df_meta['overview'], df_meta['id']

#df_clean.head()
df_clean=df_clean.iloc[:10000]
# import tfidfvectorizer 
from sklearn.feature_extraction.text import TfidfVectorizer
# define TF IDF Vestorizer object,remove all english stopword
tfidf=TfidfVectorizer(stop_words="english")
df_clean["overview"]=df_clean["overview"].fillna('')
# constructing IF-IDF Matrix by applying fit_transform mathed on overview feature
tfidf_matrix=tfidf.fit_transform(df_clean["overview"])
# import linear_kernal to calculate dot product
from sklearn.metrics.pairwise import linear_kernel
# compute the cosine similarity matrix
cosine_sim=linear_kernel(tfidf_matrix,tfidf_matrix)
#Construct a reverse mapping of indices and movie titles, and drop duplicate titles, if any
indices = pd.Series(df_clean.index, index=df_clean['title']).drop_duplicates()
# Function that takes in movie title as input and gives recommendations 
def content_recommender(title, cosine_sim=cosine_sim, df_clean=df_clean, indices=indices):
    # Obtain the index of the movie that matches the title
    idx = indices[title]

    # Get the pairwsie similarity scores of all movies with that movie
    # And convert it into a list of tuples as described above
    sim_scores = list(enumerate(cosine_sim[idx]))
    
    # Sort the movies based on the cosine similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the scores of the 10 most similar movies. Ignore the first movie.
    sim_scores = sim_scores[1:11]

    # Get the movie indices
    movie_indices = [i[0] for i in sim_scores]

    # Return the top 10 most similar movies
    return df_clean['title'].iloc[movie_indices]
#Get recommendations for The Lion King
#content_recommender("The Lion King")
pickle.dump(content_recommender, open('mypickmodel.pkl','wb'))
# Loading model to compare the results
model = pickle.load(open('mypickmodel.pkl','rb'))
a = model("The Lion King")
print(a)