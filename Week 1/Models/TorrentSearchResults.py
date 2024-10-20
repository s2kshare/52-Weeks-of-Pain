class Torrent:
    def __init__(self, name = "No Name Found",
                 seeds = 0, leechers = 0, size = "No Size Set",
                 uploader = "No Uploader Set", url = "No URL Set"):
        self.name = name;
        self.seeds = seeds;
        self.leechers = leechers;
        self.size = size;
        self.uploader = uploader;
        self.url = url;

    def set_name(self, name):
        self.name = name
    
    def set_seeds(self, seeds):
        self.seeds = int(seeds)

    def set_leechers(self, leechers):
        self.leechers = int(leechers)
    
    def set_size(self, size):
        self.size = size
    
    def set_uploader(self, uploader):
        self.uploader = uploader

    def set_url(self, url):
        self.url = url