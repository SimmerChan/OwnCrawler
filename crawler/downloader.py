import urllib2
import re
import ssl
import socket
import lxml.html

class Downloader(object):
    def __init__(self, exec_time):
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36'}
        self.error_count = 1
        self.exec_time = exec_time

    def download(self, url):
        if url is None:
            return None
        else:
            request = urllib2.Request(url, headers=self.header)
            try:
                response = urllib2.urlopen(request, timeout=1)
                content_type = response.info().getheader('Content-type')
                if re.search('text', content_type) is None:
                        return None
                dom = lxml.html.document_fromstring(response.read())
                title = dom.xpath('//title')
                if len(title) == 0:
                    return None

                else:
                    paras = dom.xpath('//p')
                    content = ''
                    for i in paras:
                        text_content = i.text_content()
                        if text_content != '':
                            content += text_content.strip()
                    if content is not None:
                        return dom

                    else:
                        return None

            except Exception, e:
                if isinstance(e, urllib2.HTTPError):
                    with open('..\log\error_log_' + self.exec_time + '.txt', 'a') as f:
                        msg = '(Error %d, HTTPError)(Code:%d) Message:%s.[Failed request:%s]\n' % \
                              (self.error_count, e.code, e.reason, url)
                        f.write(msg)
                    self.error_count += 1
                    return None

                elif isinstance(e, urllib2.URLError):
                    with open('..\log\error_log_' + self.exec_time + '.txt', 'a') as f:
                        msg = '(Error %d, URLError) Message:%s.[Failed request:%s]\n' % \
                              (self.error_count, e.reason, url)
                        f.write(msg)
                    self.error_count += 1
                    return None

                elif isinstance(e, ssl.SSLError):
                    with open('..\log\error_log_' + self.exec_time + '.txt', 'a') as f:
                        msg = '(Error %d, SSLError) Message:%s.[Failed request:%s]\n' % \
                              (self.error_count, e.strerror, url)
                        f.write(msg)
                    self.error_count += 1
                    return None

                elif isinstance(e, socket.timeout):
                    with open('..\log\error_log_' + self.exec_time + '.txt', 'a') as f:
                        msg = '(Error %d, TimeoutError) Message:%s.[Failed request:%s]\n' % \
                              (self.error_count, e.strerror, url)
                        f.write(msg)
                    self.error_count += 1
                    return None



                    # except urllib2.HTTPError, e:
                    #     with open(self.cwd + '\log\error_log_' + self.exec_time + '.txt', 'a') as f:
                    #         msg = 'Error %d(Error code:%d);Reason:%s.[Failed request:%s]\n' % \
                    #               (self.error_count, e.code, e.reason, url)
                    #         f.write(msg)
                    #     self.error_count += 1
                    #     return None
                    #
                    # except urllib2.URLError, e:
                    #     with open(self.cwd + '\log\error_log_' + self.exec_time + '.txt', 'a') as f:
                    #         msg = 'Error %d:Reason:%s.[Failed request:%s]\n' % \
                    #               (self.error_count, e.reason, url)
                    #         f.write(msg)
                    #     self.error_count += 1
                    #     return None
                    #
                    # except ssl.SSLError, e:
                    #     with open(self.cwd + '\log\error_log_' + self.exec_time + '.txt', 'a') as f:
                    #         msg = 'Error %d(Errno:%d);Message:%s.[Failed request:%s]\n' % \
                    #               (self.error_count, e.errno, e.message, url)
                    #         f.write(msg)
                    #     self.error_count += 1
                    #     return None
