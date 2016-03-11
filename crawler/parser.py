import re
import urlparse
from utils import value_calculator, relevance_checker


class Parser(object):
    def parse(self, in_url, dom):
        # Todo get the encoding of the web page
        new_urls = self._extract_urls(in_url, dom)
        new_data = self._extract_content(in_url, dom)
        return new_urls, new_data

    def _extract_urls(self, raw_url, dom):
        """
        TO extract all the urls of the web page and dump the invalid ones.
        """
        url_tags = dom.xpath('//a')
        # Todo data structure used for depth-first and breadth-first
        # new_urls = set()
        # for url in url_tags:
        #     url = url.get('href')
        #     if url is not None and re.search('javascript', 'url') is None:
        #         if re.search('/', url):  # filter the invalid href including '#', 'javascript', etc.
        #             absolute_url = urlparse.urljoin(raw_url, url)
        #             new_urls.add(absolute_url)
        # return new_urls

        # Todo data structure used for best-first
        new_urls = []
        for url_tag in url_tags:
            url = url_tag.get('href')
            if url is not None and re.search('javascript', 'url') is None:
                if re.search('/', url):  # filter the invalid href like '#'.
                    absolute_url = urlparse.urljoin(raw_url, url)
                    anchor_text = url_tag.text_content()
                    value = value_calculator.value_calculator(anchor_text,relevance_checker.Checker.keywords_list1,
                                                              relevance_checker.Checker.keywords_list2)
                    url_info = {'url': absolute_url, 'anchor_text': anchor_text, 'value': value}
                    new_urls.append(url_info)
        return new_urls

    def _extract_content(self, raw_url, dom):
        """
        To extract the main content of the web page for latter analysis.
        """
        data = {}

        title = dom.xpath('//title')
        data['title'] = title[0].text_content()

        result = dom.xpath('//p')
        content = ''
        for i in result:
            text_content = i.text_content()
            if text_content != '':
                content += text_content.strip()
        data['content'] = content

        data['url'] = raw_url
        return data
