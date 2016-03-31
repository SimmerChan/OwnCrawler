import re
import urlparse
import lxml.etree
import lxml.html
import socket
import time
from utils import value_calculator, relevance_checker
from utils import clustering
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By


def extract_content(raw_url, dom):
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


def extract_urls(raw_url, dom):
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
        if url_tag.text_content() == '':
            continue
        url = url_tag.get('href')
        if url is not None and re.search('javascript', url) is None:
            if re.search('/', url):  # filter the invalid href like '#'.
                absolute_url = urlparse.urljoin(raw_url, url)
                anchor_text = url_tag.text_content()
                value = value_calculator.value_calculator_url(anchor_text, relevance_checker.Checker.keywords_list1,
                                                          relevance_checker.Checker.keywords_list2)
                url_info = {'url': absolute_url, 'anchor_text': anchor_text, 'value': value}
                new_urls.append(url_info)
    return new_urls


def extract_urls_content_from_cluster(raw_url, clusters_info):
    new_urls = []
    content = ''
    clusters_info_with_value = value_calculator.value_calculator_cluster(clusters_info)
    for info in clusters_info_with_value:
        for e in info['cluster']:
            if e['url'] is None:
                content += e['text']
            else:
                url = e['url']
                if re.search('javascript', url) is None:
                    absolute_url = urlparse.urljoin(raw_url, url)
                    anchor_text = e['text']
                    # 0.1 * info['value'] + 0.9 *
                    value = 0.1 * info['value'] + 0.9 * value_calculator.value_calculator_url(
                            anchor_text, relevance_checker.Checker.keywords_list1,
                            relevance_checker.Checker.keywords_list2)
                    url_info = {'url': absolute_url, 'anchor_text': anchor_text, 'value': round(value, 1)}
                    new_urls.append(url_info)
    return new_urls, content


def get_xpath(dom):
    xpath_list = []
    for a in dom.xpath('//p|//a'):
        ele = lxml.etree.ElementTree(a)
        xpath = ele.getpath(a)
        xpath_list.append(xpath)
    return xpath_list


def get_elements_from_xpaths(xpaths, browser):
    elements = []
    elements_info = []
    for xpath in xpaths:
        try:
            element = WebDriverWait(browser, 3).until(EC.presence_of_element_located((By.XPATH, xpath)))
            elements.append(element)
            elements_info.append({'xpath': xpath})
        except NoSuchElementException:
            return None, None

        except TimeoutException:
            return None, None

        except WebDriverException:
            return None, None

        except socket.timeout:
            time.sleep(10)
            return None, None

        except socket.error:
            time.sleep(10)
            return None, None

    return elements, elements_info


def get_element_info(self, elements, elements_info, browser):
        msg = browser.execute_script(self.script, elements)
        for i in range(0, len(msg)):
            elements_info[i]['top'] = msg[i]['top']
            elements_info[i]['left'] = msg[i]['left']
            elements_info[i]['height'] = msg[i]['height']
            elements_info[i]['width'] = msg[i]['width']
            elements_info[i]['url'] = msg[i]['url']
            elements_info[i]['text'] = msg[i]['text'].strip()
        return elements_info


class Parser(object):
    def __init__(self):
        self.script = '''
        var elements_info = new Array()
            for(var i=0; i<arguments[0].length; i++ ){
                elements_info[i] = {'top':arguments[0][i].getBoundingClientRect().top + document.documentElement.scrollTop,
                'left':arguments[0][i].getBoundingClientRect().left + document.documentElement.scrollLeft,
                'height':arguments[0][i].offsetHeight, 'width':arguments[0][i].offsetWidth, 'text':arguments[0][i].textContent,
                'url': arguments[0][i].getAttribute('href')};
            }
        return elements_info;
        '''

    def parse(self, in_url, dom=None, page_source=None, browser=None):
        if page_source is None:
            new_urls = extract_urls(in_url, dom)
            new_data = extract_content(in_url, dom)
            if len(new_data['content']) < 50:
                return new_urls, None
            return new_urls, new_data
        else:
            dom = lxml.html.document_fromstring(page_source)
            title = dom.xpath('//title')[0].text_content()
            xpaths = get_xpath(dom)
            elements, elements_info = get_elements_from_xpaths(xpaths=xpaths, browser=browser)
            if elements is None:
                return None, None
            else:
                elements_info = get_element_info(self, elements, elements_info, browser)
                if elements_info < 2:
                    return None, None
                clusters_info = clustering.page_segmentation(elements_info)
                if len(clusters_info) < 2 or clusters_info is None:
                    return None, None
                new_urls, content = extract_urls_content_from_cluster(in_url, clusters_info)
                if len(content) < 50:
                    return new_urls, None
                new_data = {'url': in_url, 'title': title, 'content': content}
                return new_urls, new_data


