# coding=utf-8
import pymongo
import time


class Checker(object):
    keywords_list1 = {u'西藏', u'拉萨', u'青藏', u'昌都', u'日喀则', u'林芝', u'山南', u'那曲', u'阿里'}
    keywords_list2 = {u'发展', u'建设', u'成果', u'成绩', u'伟业', u'创举', u'事业', u'业绩', u'成就', u'果实', u'硕果',
                               u'进展'}

    def __init__(self):
        self.connection = pymongo.MongoClient()
        self.db = self.connection['TibetProject']
        self.collection = self.db['tibetInfo']
        self.collection_count = self.collection.find().count()
        self.count = 0

    def check_relevance(self, title, content):
        has_keyword_in_list1 = False
        kw2_count = 0

        for kw1 in Checker.keywords_list1:
            if title.find(kw1) != -1 and content.count(kw1) >= 3:
                has_keyword_in_list1 = True
                break

        if has_keyword_in_list1 is False:
            return False

        for kw2 in Checker.keywords_list2:
            if content.find(kw2) != -1:
                kw2_count += content.count(kw2)
                if kw2_count >= 3:
                    return True

        return False

    def check_all(self):
        for item in self.collection.find():
            relevance = self.check_relevance(item['title'], item['content'])
            if relevance is True:
                self.collection.update({"_id": item['_id']}, {"$set": {"relevance": 'True'}})
                print item['url'], item['title']
            else:
                self.collection.update({"_id": item['_id']}, {"$set": {"relevance": 'False'}})


if __name__ == '__main__':
    my_checker = Checker()
    my_checker.check_all()
    with open('../log/relevant_num_best_cluster.txt', 'a') as f:
        for info in my_checker.collection.find():
            if info['relevance'] == 'False':
                f.write(str(my_checker.count) + ' ')

            else:
                my_checker.count += 1
                f.write(str(my_checker.count) + ' ')

    print my_checker.count
