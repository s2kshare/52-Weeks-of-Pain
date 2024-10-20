import configparser
from Models.ErrorHandler import ErrorHandler
from bs4 import BeautifulSoup

class TorrentSiteScrape:
    def __init__(self, config_file='config.conf'):
        self.config = configparser.ConfigParser()
        self.config.read(config_file)
        self.err = ErrorHandler()

        self.torrent_sites = {key: value for key, value in self.config['TorrentSites'].items()}
        self.torrent_site_row_index = {key: value for key, value in self.config['SiteRowIndexFormat'].items()}
        self.torrent_site_element_prefix = {key: value for key, value in self.config['ElementPrefix'].items()}
        self.torrent_site_item_index = {key: value for key, value in self.config['SiteItemIndexFormat'].items()}

    def scrape_html(self, site_name, content):
        try:
            if site_name in self.torrent_sites:
                soup = BeautifulSoup(content, "html.parser")
                elements = soup.find_all(self.torrent_site_row_index[site_name])
                element_prefix = self.torrent_site_element_prefix[site_name].split(',');

                for element in elements:
                    cells = element.find_all(self.torrent_site_item_index[site_name])
                    print("\n\n\n")
                    print(element)
                    print("\n\n\n")
                    for item in cells:
                        if element_prefix[0] in item.get('class', []):
                            print("[FOUND NAME] >> " + item.text)
                        if element_prefix[1] in item.get('class', []):
                            print("[FOUND SEEDS] >> " + item.text)
                        if element_prefix[2] in item.get('class', []):
                            print("[FOUND LEECH] >> " + item.text)
                        if element_prefix[3] in item.get('class', []):
                            # Formatting in case
                            # This right here is shotty logic
                            print("[FOUND SIZE] >> " + item.text.split("B")[0] + "B")
                        if element_prefix[4] in item.get('class', []):
                            print("[FOUND UPLOADERS] >> " + item.text)
                return elements
            else:
                self.err.set_error_title("Scrape Failure")
                self.err.set_error_message("Could not find site")
                self.err.log_error()
        except Exception as e:
            self.err.set_error_title("Scrape Failure")
            self.err.set_error_message("Error scraping the HTML content\n" + e)
            self.err.log_error()