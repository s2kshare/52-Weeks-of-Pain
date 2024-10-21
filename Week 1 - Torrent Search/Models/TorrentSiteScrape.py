import configparser
from Models.ErrorHandler import ErrorHandler
from Models.TorrentSearchResults import Torrent
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
        self.torrent_site_item_restrictions = {key: value for key, value in self.config['ElementRestrictions'].items()}

    def scrape_html(self, site_name, content):
        try:
            if site_name in self.torrent_sites:
                soup = BeautifulSoup(content, "html.parser")
                elements = soup.find_all(self.torrent_site_row_index[site_name])
                element_prefix = self.torrent_site_element_prefix[site_name].split(',');

                # Creating an array for returned torrents
                torrents = []

                # Iterate through each row index
                for element in elements:
                    
                    # Find all child elements within each row index
                    cells = element.find_all(self.torrent_site_item_index[site_name])

                    # Create empty torrent file
                    torrent = Torrent()

                    # For each child item within parent container (Row Index)
                    for item in cells:

                        # Capturing Name of Torrent
                        if element_prefix[0] in item.get('class', []):
                            a_tags = item.find_all('a')
                            
                            # If restrictions have been set, avoid them to extract content
                            # For example, two nested <a> tags within 1337.
                            # We avoid the first one as it is not relevant, rather it grabs additional characters for the comment amount
                            # Leading to [name][comment count]

                            if self.torrent_site_item_restrictions[site_name]:
                                for a_tag in a_tags:
                                    if self.torrent_site_item_restrictions[site_name] not in a_tag.get('class', []):
                                        
                                        # Fetch href link from title
                                        href = a_tag.get('href')
                                        if not href.startswith("http"):
                                            torrent.set_url(self.torrent_sites[site_name] + href)
                                        else:
                                            torrent.set_url(href)

                                        # Set name of torrent
                                        torrent.set_name(a_tag.text)

                        # If no restrictions are set, return item.text
                            else:
                                torrent.set_name(item.text)

                        # Capturing Seeds of Torrent
                        if element_prefix[1] in item.get('class', []):
                            # print("[FOUND SEEDS] >> " + item.text)
                            torrent.set_seeds(item.text)

                        # Capturing Leechers of Torrent
                        if element_prefix[2] in item.get('class', []):
                            # print("[FOUND LEECH] >> " + item.text)
                            torrent.set_leechers(item.text)

                        # Capturing Size of Torrent
                        if element_prefix[3] in item.get('class', []):
                            # Formatting in case
                            # This right here is shotty logic
                            # print("[FOUND SIZE] >> " + item.text.split("B")[0] + "B")
                            torrent.set_size(item.text)

                        # Capturing Uploader of Torrent
                        if element_prefix[4] in item.get('class', element_prefix[4].split("|")):
                            torrent.set_uploader(item.text)

                    # Append the newly made torrent to the torrents list then return
                    torrents.append(torrent)
                    
                return torrents
            else:
                self.err.set_error_title("Scrape Failure")
                self.err.set_error_message("Could not find site")
                self.err.log_error()
        except Exception as e:
            self.err.set_error_title("Scrape Failure")
            self.err.set_error_message("Error scraping the HTML content\n" + e)
            self.err.log_error()