import binascii
import re
import zlib
import time

from nltk.corpus import stopwords

import utility

import pdb

class News():
    file_name = ""

    def __init__(self, file_name, max_line=10000):
        self.file_name = file_name
        self.max_line = max_line

        self.id_map = {}
        self.all = []
        self.ids = []
        self.all_tf = []

        self.read_news()

    def read_news(self):
        t = time.time()

        regex = '[\W]+'

        count = 0
        with open(self.file_name) as f:
            for line in f:
                if count < self.max_line:
                    count += 1
                    separator_pos   = line.find(" ")
                    _id             = line[:separator_pos]
                    _news            = re.split(regex, line[separator_pos + 1:].lower())

                    self.all.append(_news)
                    l = len(self.all) - 1
                    self.id_map[_id] = l
                    self.ids.append(_id)
                else:
                    break

        print "Len read_news(): %d" % len(self.all)

        print "**** Finish read_news: %f" % (time.time() - t)

    def get_ids(self):
        """
        NOTE: this is not a getter function.

        we can use this function to return the self.ids, instead of saving self.ids

        The result for self.ids and self.get_ids() are the same.
        """
        ids = self.id_map.keys()
        positions = self.id_map.values()

        sorted_indices = [i[0] for i in sorted(enumerate(positions), key=lambda x:x[1])]
        return [ids[i] for i in sorted_indices]

    def preprocess(self, tokenize=False, stopword=False):
        if tokenize:
            self.tokenize()
        if stopword:
            self.remove_stopwords()

    def tokenize(self):
        t = time.time()

        # regex = '[\s\\~`!@#$%^&\*\(\)_\-\+=\[\]\{\}\|:;"\'<>,\.\?/]'
        regex = '[\W]'
        for (index, news) in enumerate(self.all):
            news = re.split(regex, news)
            self.all[index] = news

        print "**** Finish tokenize: %f" % (time.time() - t)

    def remove_stopwords(self):
        t = time.time()

        stop = stopwords.words('english')
        stop.append("")

        for (index, news) in enumerate(self.all):
            news = [token for token in news if token not in stop]
            self.all[index] = news

        print "**** Finish remove_stopwords: %f" % (time.time() - t)

    def calculate_tf(self):
        for news in self.all:
            set_news = set(news)
            d = dict()
            for token in set_news:
                d[token] = news.count(token)
            self.all_tf.append(d)



    def get_news(self, news_id):
        return self.all[self.id_map[news_id]]

    def adler32(self, news_id):
        news = " ".join(self.get_news(news_id))
        return zlib.adler32(news)
        # prime = 65521

        # try:
        #     news = self.get_news(news_id)
        # except KeyError:
        #     print "Error news.py, adler32"

        # A = 0
        # B = 0
        # for char in news:
        #     c = long(binascii.hexlify(char), 1
        #     B += c
        #     A += B

        # A = A % prime
        # B = B % prime

        # return (A << 16 | B)

    def compare(self, news_id_1, news_id_2):
        """
        return 1 if news with id_1 is identify to news with id_2
        """
        news_1 = self.get_news(news_id_1)
        news_2 = self.get_news(news_id_2)

        if len(news_1) != len(news_2):
            return False
        else:
            for i in range(len(news_1)):
                if news_1[i] != news_2[i]:
                    return False

        return True

    def extract_news_from_ids(self, ids):
        with open('data.type2', 'w') as output:
            with open(self.file_name) as f:
                for line in f:
                    separator_pos   = line.find(" ")
                    _id             = line[:separator_pos]
                    if ids.count(_id) > 0:
                        output.write(line)

    def get_news_type(self, id_1, id_2):
        val_1 = self.get_news(id_1)
        val_2 = self.get_news(id_2)

        l1 = len(val_1)
        l2 = len(val_2)
        val_1 = set(val_1)
        val_2 = set(val_2)

        jd = len(val_1.intersection(val_2)) * 1.0 / len(val_1.union(val_2))

        if jd > 0.98:
            if l1 == l2 and jd == 1:
                return 1
            elif abs(l1 - l2) == 1:
                return 2
            else:
                return -1









