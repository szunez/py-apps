import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs

def scrape_topic_excluding_site(topic, exclude_site, num_pages=5):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    search_url = f"https://www.google.com/search?q={topic.replace(' ', '+')}"
    references = []
    pages_scraped = 0

    while pages_scraped < num_pages:
        try:
            print(f"Fetching URL: {search_url}")
            response = requests.get(search_url, headers=headers)
            if response.status_code != 200:
                print(f"Failed to fetch {search_url}. Status code: {response.status_code}")
                break
            
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extracting search results
            search_results = soup.find_all('div', class_='tF2Cxc')
            for result in search_results:
                link = result.find('a', href=True)
                if link:
                    url = link['href']
                    parsed_url = urlparse(url)
                    if parsed_url.netloc and exclude_site not in parsed_url.netloc:
                        references.append(url)

            # Check if there's a next page
            next_page_url = soup.find('a', {'id': 'pnnext'})
            if not next_page_url:
                print("No more pages found.")
                break
            
            search_url = f"https://www.google.com{next_page_url['href']}"
            pages_scraped += 1

        except Exception as e:
            print(f"Error fetching or parsing page: {str(e)}")
            break

    return references

topic = "Accounting Based Valuation Rice University final exam"
exclude_site = "rice.edu"  # Replace with your exclude site
num_pages = 50  # Number of Google search result pages to scrape

references = scrape_topic_excluding_site(topic, exclude_site, num_pages)
for idx, ref in enumerate(references, start=1):
    print(f"{idx}. {ref}")
