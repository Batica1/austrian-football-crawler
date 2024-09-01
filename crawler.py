import requests
from bs4 import BeautifulSoup
import pandas as pd
from config_variables import WEB_URL, SITE_NAME

def fetch_html(url):
    """
    Fetches the HTML content of the given URL.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    session = requests.Session()
    try:
        response = session.get(url, headers=headers, allow_redirects=True)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

def parse_html(html):
    """
    Parses the HTML content and extracts club info values.
    """
    soup = BeautifulSoup(html, 'html.parser')

    table = soup.find('div', class_='responsive-table').find('table', class_='items')

    clubs = []
    rows = table.tbody.find_all('tr')

    for row in rows:
        club_name = row.find('td', class_='hauptlink').get_text(strip=True)
        avg_age = row.find_all('td', class_='zentriert')[1].get_text(strip=True)
        total_market_value = row.find_all('td', class_='rechts')[1].get_text(strip=True)

        clubs.append({
            'club_name': club_name,
            'avg_age': avg_age,
            'total_market_value': total_market_value
        })

    return clubs

def save_to_csv(clubs, filename='clubs.csv'):
    """
    Saves the club data to a CSV file, checking for duplicates.
    """
    try:
        existing_data = pd.read_csv(filename)
    except FileNotFoundError:
        existing_data = pd.DataFrame(columns=['club_name', 'avg_age', 'total_market_value'])

    new_data = pd.DataFrame(clubs)

    combined_data = pd.concat([existing_data, new_data]).drop_duplicates(subset='club_name', keep=False)

    updated_data = pd.concat([existing_data, combined_data]).drop_duplicates(subset='club_name', keep='first')

    updated_data.to_csv(filename, index=False, encoding='utf-8-sig')

def main():
    """
    Main function to execute the crawler.
    """
    print(f"Starting crawler for {SITE_NAME}")
    html = fetch_html(WEB_URL)
    if html:
        clubs = parse_html(html)
        save_to_csv(clubs)
        print("Data saved to CSV file.")
    else:
        print("Failed to retrieve the webpage content.")

if __name__ == "__main__":
    main()
