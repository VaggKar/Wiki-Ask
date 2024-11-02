import json
from collections import defaultdict
import os

# Load the cleaned data (tokenized, preprocessed) from JSON
def load_cleaned_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        tokens = json.load(file)
    return tokens

# Build the inverted index
def build_inverted_index(tokens, document_id):
    index = defaultdict(list)  # Use defaultdict to handle lists of document IDs for each term
    
    # Iterate through tokens and add document ID to each token's list in the index
    for token in tokens:
        if document_id not in index[token]:  # Avoid duplicate entries
            index[token].append(document_id)
    
    return index

# Merge inverted indices from multiple documents (in case there are several)
def merge_indices(*indices):
    merged_index = defaultdict(list)
    
    for index in indices:
        for term, doc_ids in index.items():
            for doc_id in doc_ids:
                if doc_id not in merged_index[term]:  # Avoid duplicate entries
                    merged_index[term].append(doc_id)
                    
    return merged_index

# Save the inverted index to a JSON file
def save_inverted_index(index, output_file):
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(index, file, indent=4)
    print(f"Inverted index saved to {output_file}")

# Main function to build and save the inverted index
def main():
    # Load tokens from cleaned data
    input_path = "data/cleaned_greece_article.json"
    tokens = load_cleaned_data(input_path)
    
    # Build inverted index for the article (assuming document ID = 1 for this example)
    document_id = 1
    index = build_inverted_index(tokens, document_id)
    
    # Save the inverted index
    output_path = "data/inverted_index.json"
    save_inverted_index(index, output_path)

if __name__ == "__main__":
    main()
