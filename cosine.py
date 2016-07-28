import pprint
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# http://lindsayvass.com/2016/05/27/003-building-a-podcast-recommendation-algorithm/

pp = pprint.PrettyPrinter(indent=4)

documents = (
    "The soccer ball is black and white",
    "A football is brown and white",
    "Boblsedding is a winter sport",
    "A tennis ball is green"
)

tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix = tfidf_vectorizer.fit_transform(documents)
print "Shape: {}".format(tfidf_matrix.shape)

print "\nsingle:"
result = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix)
print result
pp.pprint(zip(documents, result.flatten()))

print "\nall:"
all_results = cosine_similarity(tfidf_matrix[0:4], tfidf_matrix)
print all_results
for z in all_results:
    print ""
    # print set(z.flat)
    pp.pprint(zip(z, documents))
