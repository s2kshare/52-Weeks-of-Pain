import requests # type: ignore
from bs4 import BeautifulSoup
from Models.ErrorHandler import ErrorHandler
from Models.TorrentSiteModel import TorrentSiteModel
from Models.TorrentSiteScrape import TorrentSiteScrape

# Variable Initializing
err = ErrorHandler()
tsm = TorrentSiteModel()
tss = TorrentSiteScrape()

print("_"*25 + "\n\n     TORRENT  SEARCH     \n" + "_"*25 + "\n")
user_input = input("  Search Query:  ")

# Fetching Webpages
try:
    # Using TorrentSiteModel to fetch search query
    search_query = tsm.search_url('1337', user_input, "1")

    # Headers used to trick block scrapers
    # Setting user agent
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    # Fetching HTML to a specified URL
    response = requests.get(search_query, headers=headers)
    
    # Raise an HTTPError for bad responses (4xx and 5xx)
    response.raise_for_status()
    
    # Store html content
    html_content = response.content

    # Print HTML
    elements = tss.scrape_html('1337', html_content)

    # Print all torrent elements if exists
    for torrent in elements:
        if torrent.name != "No Name Found":
            print("-"*25)
            print(f"Name: {torrent.name}")
            print(f"Seeders: {torrent.seeds}")
            print(f"Leechers: {torrent.leechers}")
            print(f"Size: {torrent.size}")
            print(f"Uploader: {torrent.uploader}")
            print(f"URL: {torrent.url}")
            print()


except requests.exceptions.RequestException as e:
    err.set_error_title("Unable to GET HTML.")
    err.set_error_message(str(e))
    err.log_error()