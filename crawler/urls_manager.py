class UrlManager(object):
    def __init__(self):
        self.new_urls = list()  # besides url, include title and value info
        self.crawled_urls = list()  # only include url
        self.not_crawled_urls = list() # only include url

    def add_new_url(self, url):
        if url['url'] not in self.not_crawled_urls and url not in self.crawled_urls:
            self.new_urls.append(url)
            self.not_crawled_urls.append(url['url'])

    def add_new_urls(self, urls):
        if urls is None or len(urls) == 0:
            return
        else:
            for url in urls:
                self.add_new_url(url)

    def get_new_url(self):
        # new_url = self.new_urls.pop()  # FILO
        # new_url = self.new_urls.pop(0)  # FIFO
        self.new_urls = sorted(self.new_urls, key=lambda item: item['value'], reverse=True)
        new_url = self.new_urls.pop(0)
        self.crawled_urls.append(new_url['url'])
        return new_url

    def has_new_url(self):
        return len(self.new_urls) != 0
