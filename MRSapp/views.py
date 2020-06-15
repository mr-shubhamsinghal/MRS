from django.shortcuts import render, redirect
import pickle
import os
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from django.contrib import messages
from django.core import serializers

# Create your views here.

# importing metadata dataset
df_clean=pd.read_csv("metadata_clean.csv")
# importing movies_metadata
df_meta=pd.read_csv("movies_metadata.csv")#error_bad_lines=False
#df_meta.head()
df_clean['overview'], df_clean['id'] = df_meta['overview'], df_meta['id']

#df_clean.head()
df_clean=df_clean.iloc[:10000]

# define TF IDF Vestorizer object,remove all english stopword
tfidf=TfidfVectorizer(stop_words="english")
df_clean["overview"]=df_clean["overview"].fillna('')
# constructing IF-IDF Matrix by applying fit_transform mathed on overview feature
tfidf_matrix=tfidf.fit_transform(df_clean["overview"])

# compute the cosine similarity matrix
cosine_sim=linear_kernel(tfidf_matrix,tfidf_matrix)
#Construct a reverse mapping of indices and movie titles, and drop duplicate titles, if any
indices = pd.Series(df_clean.index, index=df_clean['title']).drop_duplicates()
n = False
# Function that takes in movie title as input and gives recommendations 
def content_recommender(title, cosine_sim=cosine_sim, df_clean=df_clean, indices=indices):
    # Obtain the index of the movie that matches the title
    global n
    # print(title)
    try:
        # print(bool(indices[title]))
        idx = indices[title]
        # print(idx)
        n = True
    except KeyError:
        n = False
        return n
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
    
# pickle.dump(content_recommender, open('mypickmodel.pkl','wb'))
# Loading model to compare the results

modulePath = os.path.dirname(__file__)
filePath = os.path.join(modulePath,'mypickmodel.pkl')
model = pickle.load(open('mypickmodel.pkl','rb'))

# def index(request):
#     if request.method=="POST":
#         a = request.POST['movie']
#         o = model(a)
#         o = serializers.serialize('xml', o)
#         return HttpResponse(o, content_type="application/xml")
#     return render(request,'index.html')



def index(request):
    if request.method=="POST":
        a = request.POST['movie']
        #Get recommendations for The Lion King
        #content_recommender("The Lion King")
        output = model(a)
        # print(np.dtype(output))
        # print(bool(output))
        if n:
            # print('yes')
            return render(request,'index.html',{'output':output})
            
        else:
            # print('no')
            messages.info(request,'We don\'t have this movie')
            return redirect('index')
    return render(request,'index.html')