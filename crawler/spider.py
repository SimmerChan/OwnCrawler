# coding=utf-8
import time
import traceback

from crawler import parser, urls_manager, downloader, container


class Spider(object):
    db_name = 'TibetProject'
    collection_name = 'tibetInfo'

    def __init__(self):
        self.exec_time = time.strftime('%Y_%m_%d_%Hh%Mm%Ss', time.localtime(time.time()))
        self.urlsManager = urls_manager.UrlManager()
        self.downloader = downloader.Downloader(self.exec_time)
        self.parser = parser.Parser()
        self.container = container.Container(db_name=Spider.db_name, collection_name=Spider.collection_name)
        self.crawled_urls = []

    def crawl(self, seedurls):
        count = 1
        flag = 1
        self.urlsManager.add_new_urls(seedurls)
        filename = '..\log\crawl_log_' + self.exec_time + '.txt'
        while self.urlsManager.has_new_url():
            try:
                new_url_info = self.urlsManager.get_new_url()
                new_url = new_url_info['url']
                dom = self.downloader.download(new_url)
                if dom is None:
                    continue
                new_urls, data = self.parser.parse(new_url, dom)
                self.urlsManager.add_new_urls(new_urls)
                self.container.collect_data(data)
                self.crawled_urls.append(new_url_info)

                # Todo print all the urls in the queue
                if count > 500:
                    if flag == 1:
                        flag = 0
                        for url in self.urlsManager.new_urls:
                            with open('..\log\left_' + self.exec_time + '.txt', 'a') as j:
                                j.write(str(url) + "\n")

                        for ourl in self.urlsManager.crawled_urls:
                            with open('..\log\old_' + self.exec_time + '.txt', 'a') as k:
                                k.write(str(ourl) + "\n")

                        for curl in self.crawled_urls:
                            with open('..\log\crawled_' + self.exec_time + '.txt', 'a') as l:
                                l.write(str(curl) + "\n")
                    break

                # Todo save crawling log
                msg = 'crawl %d : %s,  [%d urls left in queue]\n' % (count, new_url_info, len(self.urlsManager.new_urls))
                print msg
                with open(filename, 'a') as f:
                    f.write(msg)

                with open('..\log\left_len_best.txt', 'a') as m:
                    m.write(str(len(self.urlsManager.new_urls)) + ' ')

                count += 1
            except:
                traceback.print_exc()
                print 'crawl failed'


if __name__ == '__main__':
    my_spider = Spider()
    seeds = [{'url': 'http://tibet.news.cn/gdbb/2011-05/27/content_22874841_1.htm', 'value': 3,
              'anchor_text': u'西藏60年文化建设成果综述：文化工程惠及各族群众'},
             {'url': 'http://www.xizang.gov.cn/index.jhtml', 'value': 1, 'anchor_text': u'西藏自治区人民政府'},
             {'url': 'http://www.tibet.cn/2009shipin/news/sp/201102/t20110221_930304.html', 'value': 3,
              'anchor_text': u'2011年西藏进一步扩大新农村建设成果'},
             {'url': 'http://www.tibet.cn/jiaotong_pd/xzlsnjtfz/jkfdzhh/gl/201104/t20110425_1011223.html', 'value': 3,
              'anchor_text': u'西藏交通建设成果显著 农牧民出行更加便利'},
             {'url': 'http://www.xzxw.com/rkz/mswh/201601/t20160114_1034847.html', 'value': 3,
              'anchor_text': u'日喀则基层公安警营文化建设成果文艺汇演'},
             {'url': 'http://www.vtibet.com/tbch/2016zt/zgmxzgs_7608/ypgj/201601/t20160113_369802.html', 'value': 1,
              'anchor_text': u'习近平的西藏情：“藏族和汉族是一家人”'},
             {'url': 'http://info.tibet.cn/newzt/yuanzang/yzcg/200505/t20050531_33920.htm', 'value': 3,
              'anchor_text': u'对口支援西藏经济建设的丰硕成果'}
             ]
    my_spider.crawl(seeds)
