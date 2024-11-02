import json
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import string
import os

# Download necessary NLTK data files (run only once)
nltk.download('punkt')
nltk.download('stopwords')

# Load the Wikipedia article data from JSON
def load_article(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        article = json.load(file)
    return article["content"]

# Preprocess text: tokenization, stop words removal, and stemming
def preprocess_text(text):
    # Initialize NLTK tools
    stop_words = set(stopwords.words('english'))
    stemmer = PorterStemmer()
    
    # Convert to lowercase, remove punctuation
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    
    # Tokenize the text
    tokens = word_tokenize(text)
    
    # Remove stop words and apply stemming
    processed_tokens = [stemmer.stem(word) for word in tokens if word not in stop_words]
    
    return processed_tokens

# Save the cleaned tokens to a JSON file
def save_cleaned_data(tokens, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(tokens, file, indent=4)
    print(f"Processed tokens saved to {output_file}")

# Main function to load, preprocess, and save the text
def main():
    # Load the article
    input_path = "data/greece_article.json"
    content = load_article(input_path)
    
    # Preprocess the content
    tokens = preprocess_text(content)
    
    # Save the cleaned data
    output_path = "data/cleaned_greece_article.json"
    save_cleaned_data(tokens, output_path)

if __name__ == "__main__":
    main()
