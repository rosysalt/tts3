from news import *

import pdb

if __name__ == '__main__':
    TRAIN_FILE = "./data.train"
    TEST_FILE = "./data.test"

    news = News(TEST_FILE);
    news.read_news();
    news.preprocess();
    # news.calculate_tf();

    # pdb.set_trace()
    a = 2