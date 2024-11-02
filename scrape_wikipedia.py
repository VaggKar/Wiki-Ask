import requests
from bs4 import BeautifulSoup
import json
import os

# Function to scrape a Wikipedia article and save it to a JSON file
def scrape_wikipedia_article(url, output_file):
    response = requests.get(url)
    
    # Check if the response is successful
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Extract the title of the article
        title = soup.find('h1', {'id': 'firstHeading'}).text
        
        # Extract all paragraphs in the content
        paragraphs = soup.find_all('p')
        content = "\n".join([p.text for p in paragraphs])
        
        # Structure the article data
        article_data = {
            "title": title,
            "content": content
        }
        
        # Save the data in JSON format
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(article_data, f, indent=4, ensure_ascii=False)
        print(f"Article saved to {output_file}")
    else:
        print(f"Error fetching page: {url} (Status code: {response.status_code})")

# Scrape the Greece Wikipedia article and save it
url = "https://en.wikipedia.org/wiki/Greece"
output_path = "data/greece_article.json"
scrape_wikipedia_article(url, output_path)
