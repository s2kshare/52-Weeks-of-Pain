import requests # type: ignore
from bs4 import BeautifulSoup
from Models.ErrorHandler import ErrorHandler
from Models.TorrentSiteModel import TorrentSiteModel

# Variable Initializing
err = ErrorHandler()
tsm = TorrentSiteModel()

try:
    # Fetching HTML to a specified URL
    response = requests.get("https://www.google.com/");
    
    # Raise an HTTPError for bad responses (4xx and 5xx)
    response.raise_for_status()
    
    # Store html content
    html_content = response.content

    # Use bs4 to parse the HTML
    soup = BeautifulSoup(html_content, "html.parser")
except requests.exceptions.RequestException as e:
    err.set_error_title("Unable to GET HTML.")
    err.set_error_message(str(e))
    err.log_error()

print("_"*25 + "\n\n     TORRENT  SEARCH     \n" + "_"*25 + "\n")

user_input = input("  Search Query:  ")