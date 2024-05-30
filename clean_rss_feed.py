# clean_rss_feed.py
import json

file_path = 'rss.json'

with open(file_path, 'r') as f:
    data = json.load(f)

non_reddit_links = []

def extract_links(data, title=None, publication_date=None, text=None):
    if isinstance(data, dict):
        for key, value in data.items():
            if key == 'Title':
                title = value
            elif key == 'Publication Date':
                publication_date = value
            elif key == 'Text':
                text = value
            elif key == 'Link' and value is not None:
                if not any(value.startswith(url) for url in ['https://www.reddit.com', 'https://i.redd.it', 'https://v.redd.it', 'https://twitter.com']):
                    non_reddit_links.append({
                        'Title': title,
                        'Publication Date': publication_date,
                        'Link': value,
                        'Text': text
                    })
            else:
                extract_links(value, title, publication_date, text)
    elif isinstance(data, list):
        for item in data:
            extract_links(item, title, publication_date, text)

extract_links(data)

result = []
temp_title = None
temp_date = None
temp_links = []

for link in non_reddit_links:
    if link['Title'] != temp_title or link['Publication Date'] != temp_date:
        if temp_title is not None:
            result.append({'Title': temp_title, 'Publication Date': temp_date, 'Links': temp_links})
        temp_title = link['Title']
        temp_date = link['Publication Date']
        temp_links = [{'Link': link['Link'], 'Text': link['Text']}]
    else:
        temp_links.append({'Link': link['Link'], 'Text': link['Text']})

if temp_title is not None:
    result.append({'Title': temp_title, 'Publication Date': temp_date, 'Links': temp_links})

with open('rss_cleaned.json', 'w') as f:
    json.dump(result, f, indent=4)
