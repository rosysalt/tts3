import re
import time

from news import *


import pdb

C = 100

class Finn():
    def __init__(self, input_file):
        self.news = News(input_file)

        self.create_feature_vector()
        self.finn_method()

        # self.finn_method_daniel()

        self.out()

        # pdb.set_trace()
        # a = 2

    def create_feature_vector(self):
        self.features = list()
        # regex = '\d+( \. \d+)'
        regex = '\d+'

        for news in self.news.all:
            vector = [1 for i in range(len(news))]
            for (index, token) in enumerate(news):
                if re.match(regex, token):
                    vector[index] = 0
            self.features.append(vector)

    def finn_method(self):
        t = time.time()
        self.a_b = list()

        for x in self.features:
            y = [0 for i in range(len(x))]

            for i in range(len(x)):
                y[i] = C * (1 - x[i]) - x[i]

            S = 0
            s = 0
            a = 0
            b = 0
            best = 0
            for i in range(len(x)):
                S += y[i]

                if S <= 0:
                    s = i + 1
                    S = 0
                if S > best:
                    a = s
                    b = i
                    best = S

            self.a_b.append((a, b))

        print "**** Finish finn_method: %f" % (time.time() - t)

    def out(self):
        with open('finn.out', 'w') as output:
            for (index, news) in enumerate(self.news.all):
                (a, b) = self.a_b[index]
                if a != b:
                    output.write('%s %s\n' % (self.news.ids[index], " ".join(news[a:b+1])))

if __name__ == '__main__':
    INPUT_FILE = "./data.finn"
    finn = Finn(INPUT_FILE)
