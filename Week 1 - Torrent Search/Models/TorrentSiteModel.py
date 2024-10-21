import configparser
from Models.ErrorHandler import ErrorHandler

class TorrentSiteModel:
    def __init__(self, config_file='config.conf'):
        self.config = configparser.ConfigParser()
        self.config.read(config_file)
        self.err = ErrorHandler()

        # Load all torrent site urls into a dictionary
        self.torrent_sites = {key: value for key, value in self.config['TorrentSites'].items()}
        self.torrent_search_queries = {key: value for key, value in self.config['SiteQueryFormat'].items()}
        self.torrent_increment_format = {key: value for key, value in self.config['SiteIncrementFormat'].items()}

    def search_url(self, site_name, query, increment):
        if site_name in self.torrent_sites:
            url = self.torrent_sites[site_name] + "/"
            search_query = self.torrent_search_queries[site_name]
            query = query.replace(" ", "+")
            increment_format = self.torrent_increment_format[site_name]

            if (site_name == "1337"):
                increment_format = increment_format + increment + increment_format
                full_query = f"{url}{search_query}{query}{increment_format}"
            if (site_name == "bitsearch"):
                full_query = f"{url}{search_query}{query}{increment_format}{increment}"

            print(f"\n\n[URL] >> {full_query}\n\n")
            return full_query
        else:
            self.err.set_error_title("Site not found")
            self.err.set_error_message(f"The following site: {site_name} could not be found")
            self.err.log_error()