import binascii

from news import *
from bucket import *
from type1 import *
from type2 import *

import utility

import pdb

"""
Receive object News()
"""
class Detector():
    HASH_SIZE = 619

    def __init__(self, input_file_name, output_file_name):
        self.output_file_name = output_file_name

        self.news = News(input_file_name)
        self.bucket = Bucket(self.HASH_SIZE)

        # self.news.read_news_2()
        self.news.read_news()
        self.news.preprocess()

        self.checksum = dict()

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
        type2 = Type2(self.news)
        type2.calculate_simhash()
        # type2.naive_detector()
        type2.detector()
        type2_result = type2.similar_pairs

        utility.write_result(self.output_file_name, type2_result)

if __name__ == "__main__":
    INPUT_FILE_NAME = "./data.train"
    OUTPUT_FILE_NAME = './type1.result'

    # TEST_FILE_NAME = "./data.test"
    # detector = Detector(TEST_FILE_NAME, OUTPUT_FILE_NAME)

    OUTPUT_FILE_NAME = './type2.result'
    detector = Detector(INPUT_FILE_NAME, OUTPUT_FILE_NAME)        
    detector.check_type_2()
