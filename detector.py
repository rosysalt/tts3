import binascii

from news import *
from bucket import *
from type1 import *
from type2 import *
from type import *
from metric import *

import utility

import pdb

"""
Receive object News()
"""
class Detector():
    HASH_SIZE = 619

    # def __init__(self, input_file_name, output_file_name, normal_read=True, window_size = 20, max_distance = 4):
    #     self.output_file_name = output_file_name
    #     self.news = News(input_file_name)

    #     self.window_size = window_size
    #     self.max_distance = max_distance

    #     self.bucket = Bucket(self.HASH_SIZE)

    #     print normal_read

    #     if normal_read:
    #         self.news.read_news()
    #     else:
    #         self.news.read_news_2(100000)

    #     self.checksum = dict()

    def __init__(self, input_file_name, output_file_name, max_line=10000, window_size = 20, max_distance = 4):
        self.type = Type(input_file_name, max_line, window_size, max_distance)

    def detect(self):
        self.type.detector()

        type1_result = self.type.type1_pairs
        type2_result = self.type.similar_pairs

        utility.write_result("./type1.result", type1_result)
        utility.write_result("./type2.result", type2_result)

    def adler32(self):
        self.checksum = dict()

        for news_id in self.news.id_map:
            checksum = self.news.adler32(news_id)
            self.checksum[news_id] = checksum
            self.bucket.add(news_id, checksum)

    def check_type_1(self):
        self.adler32()
        duplicated_doc_list = self.bucket.get_duplicated_hash_value()

        type1 = Type1(self.news, self.checksum, duplicated_doc_list)
        type1_result = type1.naive_compare()

        utility.write_result(self.output_file_name, type1_result)

    def check_type_2(self):
        type2 = Type2(self.news, window_size=self.window_size, max_distance=self.max_distance)
        # type2.calculate_simhash()
        # type2.naive_detector()
        type2.detector()
        type2_result = type2.similar_pairs

        utility.write_result("./type1.result", type2.type1_pairs)
        utility.write_result(self.output_file_name, type2_result)

def type1():
    INPUT_FILE_NAME = "./data.train"
    OUTPUT_FILE_NAME = './type1.result'

    detector = Detector(INPUT_FILE_NAME, OUTPUT_FILE_NAME)
    # detector.check_type_1()

    # Comparison
    ref = utility.read_result('./type1.truth')
    hypo = utility.read_result('./type1.result')
    metric = Metric(hypo, ref)
    metric.summarize()

def type2(normal_read=True, window_size=20, max_distance=4):
    INPUT_FILE_NAME = "./data.train"
    # INPUT_FILE_NAME = "./data.type2"
    # INPUT_FILE_NAME = "./data.train.small"
    OUTPUT_FILE_NAME = './type2.result'

    detector = Detector(INPUT_FILE_NAME, OUTPUT_FILE_NAME, normal_read, window_size, max_distance)
    detector.check_type_2()

    # Comparison
    print "Comparion Type 2"
    ref = utility.read_result('./type2.truth')
    hypo = utility.read_result('./type2.result')
    metric = Metric(hypo, ref)
    metric.summarize()

    # Comparison
    print "Comparion Type 1"
    ref = utility.read_result('./type1.truth')
    hypo = utility.read_result('./type1.result')
    metric = Metric(hypo, ref)
    metric.summarize()

def type2_small(normal_read=True, window_size=20, max_distance=4):
    INPUT_FILE_NAME = "./data.type2"
    OUTPUT_FILE_NAME = './type2.result'

    detector = Detector(INPUT_FILE_NAME, OUTPUT_FILE_NAME, normal_read, window_size, max_distance)
    detector.check_type_2()

    # Comparison
    ref = utility.read_result('./type2.truth')
    hypo = utility.read_result('./type2.result')
    metric = Metric(hypo, ref)
    metric.summarize()

def type3(normal_read=True, window_size=20, max_distance=4):
    INPUT_FILE_NAME = "./finn.out"
    # INPUT_FILE_NAME = "./data.train.small"
    OUTPUT_FILE_NAME = './type3.result'

    detector = Detector(INPUT_FILE_NAME, OUTPUT_FILE_NAME, normal_read, window_size, max_distance)
    detector.check_type_2()

def type3_1(normal_read=True, window_size=20, max_distance=4):
    INPUT_FILE_NAME = "./finn.out"
    # INPUT_FILE_NAME = "./data.train.small"
    OUTPUT_FILE_NAME = './type3_1.result'

    detector = Detector(INPUT_FILE_NAME, OUTPUT_FILE_NAME, normal_read)
    detector.check_type_1()

def test(normal_read=True, window_size=20, max_distance=4):
    INPUT_FILE_NAME = "./data.test"
    # INPUT_FILE_NAME = "./xaa"
    OUTPUT_FILE_NAME = './test1.result'

    print "test() %s" % normal_read
    detector = Detector(INPUT_FILE_NAME, OUTPUT_FILE_NAME, normal_read, window_size, max_distance)
    detector.check_type_2()
    # detector.check_type_1()

def compare(hypo, truth):
    ref = utility.read_result(truth)
    hypo = utility.read_result(hypo)
    metric = Metric(hypo, ref)
    metric.summarize()

def all_type(max_line=10000, window_size=5, max_distance=32):
    INPUT_FILE_NAME = "./data.train"
    # INPUT_FILE_NAME = "./data.test"
    OUTPUT_FILE_NAME = './type2.result'

    detector = Detector(INPUT_FILE_NAME, OUTPUT_FILE_NAME, max_line, window_size, max_distance)
    detector.detect()

    # Comparison
    print "Comparion Type 2"
    ref = utility.read_result('./type2.truth')
    hypo = utility.read_result('./type2.result')
    metric = Metric(hypo, ref)
    metric.summarize()

    # Comparison
    print "Comparion Type 1"
    ref = utility.read_result('./type1.truth')
    hypo = utility.read_result('./type1.result')
    metric = Metric(hypo, ref)
    metric.summarize()

if __name__ == "__main__":
    # type1()
    # type2(normal_read=False)
    # type2(window_size=5, max_distance=32)
    # compare('./true_type2.result', 'type2.truth')
    # type2(normal_read=False, window_size=16, max_distance=7)
    # type2()
    # type3(window_size=20, max_distance=6)
    # type3_1()
    # test(normal_read=False, window_size = 5, max_distance=32)
    # test(normal_read=True)

    max_line = 10000
    window_size = 5
    max_distance = 32
    all_type(max_line, window_size, max_distance)
    # TEST_FILE_NAME = "./data.test"
    # 12:32
    # 04:31
    # 04:48