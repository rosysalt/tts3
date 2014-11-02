import utility
import time

import pdb

class Type2():
    simhash_values = []

    def __init__(self, news):
        self.news = news

        self.distance = []
        self.similar_pairs = [] # result

    def calculate_simhash(self):
        t = time.time()
        for news in self.news.all:
            self.simhash_values.append(utility.simhash(news))

        print "**** Finish calculating simhash: %f" % (time.time() - t)

    def naive_detector(self):
        t = time.time()

        """
        http://www.matpalm.com/resemblance/simhash/
        Sort the fingerprint (simhash) values
        Go through the sorted list, find fingerprints with small Hamstring distance
        """
        self.sorted_indices = [i[0] for i in sorted(enumerate(self.simhash_values), key=lambda x:x[1])]
        self.sorted_simhash_values = [self.simhash_values[i] for i in self.sorted_indices]

        l = len(self.simhash_values)
        self.distance = [0 for i in range(l)]

        a = self.sorted_simhash_values[0]
        for i in range(1, l):
            b = self.sorted_simhash_values[i]
            self.distance[i] = bin(a ^ b).count('1');

        self.add_similar_pairs()

        print "**** Finish naive_detector: %f" % (time.time() - t)

    def add_similar_pairs(self, max_distance = 3):
        t = time.time()

        l = len(self.sorted_simhash_values)

        for i in range(1, l):
            if self.distance[i] <= max_distance:
                id_1 = self.get_news_id(i - 1)
                id_2 = self.get_news_id(i)
                self.similar_pairs.append([id_1, id_2])

    def detector(self):
        """
        Run naive_detector() multiple times, 
        while rotating the bit of simhash_values
        """
        t = time.time()
        for i in range(0, 32):
            self.naive_detector()
            self.rotate_bit_left()

        print "**** Finish type2 detector(): %f" % (time.time() - t)

    def rotate_bit_left(self, pos = 1):
        """
        """
        self.new_simhash_values = []

        for (index, value) in enumerate(self.simhash_values):
            # Step 0: value = 5 = 0b101 = binary number
            msb = bin(value)[2] # most significant bit
            # Step 1: value = 10 = 0b1010
            value = value << pos

            # Step 2: value = 11 = 0b1011
            # set the least-significant bit to msb
            if (msb == "1"):
                value = value | 1

            # Step 3: value = 3 = 0b011
            # reset the most significant bit
            num_of_bits = len(bin(value)) - 2
            value = value & ~ (1 << (num_of_bits - 1))

            self.simhash_values[index] = value

    def get_news_id(self, pos):
        original_pos = self.sorted_indices[pos]
        return self.news.pos_map[original_pos]
    

