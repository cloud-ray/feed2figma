# get_rss_feed.py
import feedparser
from bs4 import BeautifulSoup
import html
import json

# URL of the RSS feed
url = "https://buttondown.email/ainews/rss"

# Parse the RSS feed
feed = feedparser.parse(url)

# Prepare an empty list to store the results
results = []

# Iterate over each entry (item) in the feed
for entry in feed.entries:
    # Extract the title
    title = entry.title

    # Extract the publication date
    pub_date = entry.published

    # Extract the description and unescape HTML entities
    description = html.unescape(entry.description)

    # Parse the description using BeautifulSoup
    soup = BeautifulSoup(description, 'html.parser')

    # Find the required h1 tags
    h1_tags = soup.find_all('h1', {'id': ['ai-reddit-recap', 'ai-twitter-recap', 'ai-discord-recap']})

    # Prepare an empty dictionary to store the details for each h1 tag
    h1_details = {}

    # Iterate over each h1 tag
    for h1 in h1_tags:
        # Prepare an empty list to store the elements in order
        elements = []

        # Get the next sibling of the h1 tag
        sibling = h1.find_next_sibling()

        # Iterate over the siblings until the next h1 tag is reached
        while sibling and sibling.name != 'h1':
            if sibling.name == 'blockquote':
                elements.append({'Blockquote': sibling.get_text(strip=True)})
            elif sibling.name == 'p':
                elements.append({'P Tag': sibling.get_text(strip=True)})
            elif sibling.name == 'ul':
                list_items = []
                for li in sibling.find_all('li'):
                    text = li.get_text(strip=True)
                    link = li.a['href'] if li.a else None
                    list_items.append({'Text': text, 'Link': link})
                elements.append({'List': list_items})

            # Get the next sibling
            sibling = sibling.find_next_sibling()

        # Add the details to the dictionary
        h1_details[h1.text] = elements

    # Add the result to the list
    results.append({
        'Title': title,
        'Publication Date': pub_date,
        'H1 Details': h1_details
    })

# Write the results to a JSON file
with open('./testing/rss.json', 'w') as f:
    json.dump(results, f, indent=4)

print("Results have been written to 'rss.json'")
