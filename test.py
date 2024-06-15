from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Sample news titles
title1 = "JCh-2026 saralashi. O‘zbekiston safarda Eron bilan durang qayd etib, guruhda 2-o‘rinni egalladi"
title2 = "JCH—2026 saralashi. O‘zbekiston Eron bilan durang qayd etdi"

# Initialize the TF-IDF Vectorizer
vectorizer = TfidfVectorizer()

# Transform the titles into TF-IDF vectors
tfidf_matrix = vectorizer.fit_transform([title1, title2])

# Compute cosine similarity between the two vectors
cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])

print(f"Cosine Similarity: {cosine_sim[0][0]}")
print(f"Can save?: {cosine_sim[0][0] > 0.5}")
