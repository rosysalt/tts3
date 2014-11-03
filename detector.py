import binascii

from news import *
from bucket import *
from type1 import *
from type2 import *
from type import *
from metric import *

from finn import *

import utility

import pdb

"""
Receive object News()
"""
class Detector():
    def __init__(self, input_file_name, max_line=10000, window_size = 20, max_distance = 4):
        self.type = Type(input_file_name, max_line, window_size, max_distance)

    def detect(self):
        self.type.detector()

        type1_result = self.type.type1_pairs
        type2_result = self.type.similar_pairs

        utility.write_result("./type1.dup", type1_result)
        utility.write_result("./type2.dup", type2_result)

    def detect_type3(self):
        self.type.detector_type3()

        type3_result = self.type.similar_pairs

        utility.write_result("./type3.dup", type3_result)

def all_type(max_line=10000, window_size=5, max_distance=32):
    # INPUT_FILE_NAME = "./data.train"
    INPUT_FILE_NAME = "./data.test"

    detector = Detector(INPUT_FILE_NAME, max_line, window_size, max_distance)
    detector.detect()

    # Comparison
    print "Comparion Type 2"
    ref = utility.read_result('./type2.truth')
    hypo = utility.read_result('./type2.dup')
    metric = Metric(hypo, ref)
    metric.summarize()

    # Comparison
    print "Comparion Type 1"
    ref = utility.read_result('./type1.truth')
    hypo = utility.read_result('./type1.dup')
    metric = Metric(hypo, ref)
    metric.summarize()

if __name__ == "__main__":
    max_line = 150000
    window_size = 5
    max_distance = 32

    all_type(max_line, window_size, max_distance)

    finn = Finn("./data.finn")
    detector = Detector("./finn.out", max_line, window_size, max_distance)
    detector.detect_type3()