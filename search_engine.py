import json
import math
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import string

# Load stop words and initialize stemmer
stop_words = set(stopwords.words('english'))
stemmer = PorterStemmer()

# Load the inverted index and cleaned data
def load_inverted_index(index_path):
    with open(index_path, 'r', encoding='utf-8') as file:
        index = json.load(file)
    return index

# Tokenize, remove stop words, and stem words in a query
def preprocess_query(query):
    query = query.lower().translate(str.maketrans('', '', string.punctuation))
    tokens = word_tokenize(query)
    return [stemmer.stem(word) for word in tokens if word not in stop_words]

# Boolean retrieval function
def boolean_retrieval(query_terms, index, operation="AND"):
    result_docs = set(index.get(query_terms[0], []))  # Start with the first term
    for term in query_terms[1:]:
        term_docs = set(index.get(term, []))
        if operation == "AND":
            result_docs.intersection_update(term_docs)
        elif operation == "OR":
            result_docs.update(term_docs)
        elif operation == "NOT":
            result_docs.difference_update(term_docs)
    return result_docs

# Calculate TF-IDF for ranking documents
def calculate_tf_idf(term, doc_id, index, total_docs):
    # Term frequency (TF): count of the term in the document
    tf = index[term].count(doc_id) if doc_id in index[term] else 0
    # Inverse document frequency (IDF): log(total_docs / number of docs containing the term)
    idf = math.log(total_docs / len(index[term])) if term in index else 0
    return tf * idf

# Rank documents based on query terms using TF-IDF scores
def rank_documents(query_terms, result_docs, index, total_docs):
    doc_scores = {doc_id: 0 for doc_id in result_docs}
    for term in query_terms:
        for doc_id in result_docs:
            doc_scores[doc_id] += calculate_tf_idf(term, doc_id, index, total_docs)
    ranked_docs = sorted(doc_scores.items(), key=lambda item: item[1], reverse=True)
    return [doc[0] for doc in ranked_docs]  # Return only doc IDs in sorted order

# Main search function that processes queries and returns ranked results
def search(query, index, total_docs):
    query_terms = preprocess_query(query)
    if " AND " in query:
        result_docs = boolean_retrieval(query_terms, index, operation="AND")
    elif " OR " in query:
        result_docs = boolean_retrieval(query_terms, index, operation="OR")
    elif " NOT " in query:
        result_docs = boolean_retrieval(query_terms, index, operation="NOT")
    else:
        result_docs = boolean_retrieval(query_terms, index, operation="AND")
    return rank_documents(query_terms, result_docs, index, total_docs)

# User interface to enter a query and see results
def main():
    # Load inverted index and initialize total docs (assuming 1 for this example)
    index_path = "data/inverted_index.json"
    index = load_inverted_index(index_path)
    total_docs = 1  # Adjust if multiple documents are added
    
    while True:
        query = input("Enter your search query (type 'exit' to quit): ")
        if query.lower() == 'exit':
            break
        result_docs = search(query, index, total_docs)
        if result_docs:
            print(f"Documents matching query '{query}': {result_docs}")
        else:
            print(f"No documents found for query '{query}'.")

if __name__ == "__main__":
    main()
