import utility
import time

from news import *
from simhash import *

import pdb

class Type():
    def __init__(self, input_file_name, max_line=10000, window_size=20, max_distance=4):
        self.input_file_name = input_file_name

        self.max_line = max_line
        self.window_size = window_size
        self.max_distance = max_distance

        print "Max line: %d" % max_line
        print "Window size: %d" % window_size
        print "Max distance: %d" % max_distance

        ids, fingerprint_values = utility.get_fingerprints_for_file(input_file_name, max_line)

        self.simhash = SimHash(ids, fingerprint_values)
        self.simhash.sort()

        self.similar_pairs = [] # result

    def naive_detector(self):
        t = time.time()

        """
        http://www.matpalm.com/resemblance/simhash/
        Sort the fingerprint (simhash) values
        Go through the sorted list, find fingerprints with small Hamstring distance
        """

        # # bits_division = [8, 8, 8, 8]
        # bits_division = [4, 4, 4, 4, 4, 4, 4, 4]
        # self.simhash.get_similar_pairs(bits_division)

        self.simhash.sort()

        sorted_ids = self.simhash.get_sorted_ids()
        sorted_fingerprints = self.simhash.get_sorted_values()

        window_size = self.window_size
        self.simhash.calculate_distance(window_size=self.window_size)

        self.add_similar_pairs()

        # print "**** Finish naive_detector: %f" % (time.time() - t)

    def add_similar_pairs(self):
        t = time.time()

        max_distance = self.max_distance

        rows = len(self.simhash.distance)
        cols = len(self.simhash.distance[0])

        for i in range(0, rows):
            for j in range(0, cols):
                if self.simhash.distance[i][j] <= max_distance:
                    id_1 = self.get_news_id(i)
                    id_2 = self.get_news_id(i + j - cols)
                    self.similar_pairs.append((id_1, id_2))

    def analyze_similar_pairs(self):
        set_sim_pairs = set(self.similar_pairs)
        print "# distinct similar pairs: %d" % len(set_sim_pairs)


    def print_distance_info(self, pos):
        value_1 = self.simhash.get_sorted_value(pos-1)
        value_2 = self.simhash.get_sorted_value(pos)
        print ("%d - %d - %d - %s - %s\n" % (value_1, value_2, bin(value_1), bin(value_2)))

    def get_news_id(self, sorted_pos):
        return self.simhash.get_sorted_id(sorted_pos)

    def filter_true_similar_pairs(self):
        print "**** Start filtering for true similar pairs"
        # reload news
        news = News(self.input_file_name, self.max_line)

        set_sim_pairs = set(self.similar_pairs)
        true_similar_pairs = set()

        self.type1_pairs = set()
        for (id_1, id_2) in set_sim_pairs:
            type = news.get_news_type(id_1, id_2)
            if type == 2:
                true_similar_pairs.add((id_1, id_2))
            elif type == 1:
                self.type1_pairs.add((id_1, id_2))

        self.similar_pairs = set()
        self.similar_pairs = true_similar_pairs

    def detector(self):
        """
        Run naive_detector() multiple times,
        while rotating the bit of simhash_values
        """
        t = time.time()
        for i in range(0, 16):
            self.naive_detector()
            self.simhash.rotate_left(r_bits = 8, max_bits = 128)
            self.simhash.sort()

        # free memory
        self.simhash = None

        self.analyze_similar_pairs()
        self.filter_true_similar_pairs()

        print "**** Finish type2 detector(): %f" % (time.time() - t)





