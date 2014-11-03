import utility
import time
import pdb

"""
Data structure for SIMHASH algorithm
To ease the process of rotating bits in SimHash
"""
class SimHash():
    def __init__(self, ids, values):
        self.data = []
        self.sorted_indices = []
        self.distance = []

        if len(ids) != len(values):
            print "ERROR SimHash init()"
            return

        for i in range(len(ids)):
            self.data.append((ids[i], values[i]))

    def get_values(self):
        return [i[1] for i in self.data]

    def get_ids(self):
        return [i[0] for i in self.data]

    def get_value(self, pos):
        return self.data[pos][1]

    def get_id(self, pos):
        return self.data[pos][0]

    def get_sorted_id(self, sorted_pos):
        pos = self.sorted_indices[sorted_pos]
        return self.data[pos][0]

    def get_sorted_value(self, sorted_pos):
        pos = self.sorted_indices[sorted_pos]
        return self.data[pos][1]

    def rotate_left(self, r_bits = 1, max_bits=32):
        for (index, (_id, value)) in enumerate(self.data):
            self.data[index] = (_id, utility.rotate_left(value, r_bits, max_bits))

    def sort(self):
        self.sorted_indices = [i[0] for i in sorted(enumerate(self.get_values()), key=lambda x:x[1])]

    def get_sorted_ids(self):
        return [self.data[i][0] for i in self.sorted_indices]

    def get_sorted_values(self):
        return [self.data[i][1] for i in self.sorted_indices]

    def calculate_distance(self, window_size = 1):
        l = len(self.data)
        self.distance = [[0 for j in range(window_size)] for i in range(l)]

        sorted_fingerprints = self.get_sorted_values()

        a = sorted_fingerprints[0]
        for i in range(window_size, l):
            for j in range(window_size):
                # [  [(....)   (....)   (....) ]  ]
                # [  [(0, 1)   (....)   (....) ]  ]
                # [  [(0, 2)   (1, 2)   (....) ]  ]
                # [  [(0, 3)   (1, 3)   (2, 3) ]  ]
                # [  [(1, 4)   (2, 4)   (3, 4) ]  ]
                # [  [(2, 5)   (3, 5)   (4, 5) ]  ]
                b = sorted_fingerprints[i + j - window_size]
                self.distance[i][j] = bin(a ^ b).count('1');

    def get_value_for_bits(self, min_bit, max_bit, pos):
        value = self.get_value(pos)
        return int(bin(value)[2:][min_bit:max_bit], 2)

    def get_similar_pairs(self, bits_division):
        """
        Create 4 hash tables, each with 256 buckets

        bits_division = [8, 8, 8, 8]
        """
        tables = dict()

        for (index, bits) in enumerate(bits_division):
            tables[index] = [[] for i in range(pow(2, bits))]

        # create min_bit, max_bit array to loop through
        min = 0
        max = 0
        mm_array = []
        for i in bits_division:
            min = max
            max = min + i
            mm_array.append((min, max))

        # create multiple hash table
        t = time.time()
        for (hash_table_index, (min, max)) in enumerate(mm_array):
            for (index, (id, value)) in enumerate(self.data):
                v = self.get_value_for_bits(min, max, index)
                tables[hash_table_index][v].append(index)

        for table in tables.values():
            self.analyze_hashtable(table)

        print "**** Finish creating hash table: %f" % (time.time() - t)

        # create set of similar documents to check
        t = time.time()
        similar_pairs = list()
        for table in [tables[i] for i in [2, 3, 0]]:
            for bucket in table:
                if len(bucket) > 1:
                    similar_pairs.append(self.create_pair(bucket))

        print "**** Finish finding similar pairs to check: %f" % (time.time() - t)
        pdb.set_trace()
        a = 2


    def create_pair(self, bucket):
        l = len(bucket)
        pairs = []
        for i in range(0, l-1):
            for j in range(1, l):
                pairs.append((bucket[i], bucket[j]))

        # print pairs
        return pairs


    def analyze_hashtable(self, table):
        l = [len(i) for i in table]
        for (index, v) in enumerate(l):
            if v == 1:
                l[index] = 0
            else:
                l[index] = v

        print "Max bucket: %d" % max(l)
        print "Average bucket: %d" % ( sum(l) / len(l))

    def __len__(self):
        return len(self.data)
