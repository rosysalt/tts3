import codecs
import binascii
import re
from nltk.corpus import stopwords

import time
import pdb

class News():
    file_name = ""

    def __init__(self, file_name):
        self.file_name = file_name
        self.id_map = {}
        self.pos_map = {}
        self.all = []
        self.all_tf = []

    def read_news(self):
        t = time.time()

        with codecs.open(self.file_name, "r", "utf-8") as f:
            for line in f:
                separator_pos   = line.find(" ")
                _id             = line[:separator_pos]
                _news            = line[separator_pos + 1:]

                self.all.append(_news)
                l = len(self.all) - 1
                self.id_map[_id] = l
                self.pos_map[l] = _id

        print "**** Finish read_news: %f" % (time.time() - t)

    def preprocess(self):
        t = time.time()

        # regex = '[\s\\~`!@#$%^&\*\(\)_\-\+=\[\]\{\}\|:;"\'<>,\.\?/]'
        regex = '[\W]'
        stop = stopwords.words('english')
        stop.append("")
        
        for (index, news) in enumerate(self.all):
            news = news.lower()
            news = re.split(regex, news)
            news = [token for token in news if token not in stop]
            self.all[index] = news

        print "**** Finish preprocess: %f" % (time.time() - t)

    def calculate_tf(self):
        for news in self.all:
            set_news = set(news)
            d = dict()
            for token in set_news:
                d[token] = news.count(token)
            self.all_tf.append(d)

    # def read_news(self):
    def read_news_2(self):
        count = 0
        with open(self.file_name) as f:
            for line in f:
                if count < 1000:
                    count += 1
                    separator_pos   = line.find(" ")
                    _id             = line[:separator_pos]
                    _news            = line[separator_pos + 1:]

                    self.all.append(_news)
                    l = len(self.all) - 1
                    self.id_map[_id] = l
                    self.pos_map[l] = _id
                else:
                    break

    def get_news(self, news_id):
        return self.all[self.id_map[news_id]]

    def adler32(self, news_id):
        prime = 65521

        try:
            news = self.get_news(news_id)
        except KeyError:
            print "Error news.py, adler32"

        A = 0
        B = 0
        for char in news:
            c = long(binascii.hexlify(char), 16)
            B += c
            A += B

        A = A % prime
        B = B % prime

        return (A << 16 | B)

    def compare(self, news_id_1, news_id_2):
        """
        return 1 if news with id_1 is identify to news with id_2
        """
        news_1 = self.get_news(news_id_1)
        news_2 = self.get_news(news_id_2)

        return news_1 == news_2
            




