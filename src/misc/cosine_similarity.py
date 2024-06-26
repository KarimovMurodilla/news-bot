from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from fuzzywuzzy import fuzz

# def calculate(title1: str, title2: str):
#     vectorizer = TfidfVectorizer()
#     tfidf_matrix = vectorizer.fit_transform([title1, title2])
#     cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])

#     return cosine_sim[0][0]


def calculate(title1: str, title2):
    result = fuzz.ratio(title1, title2)
    return result

