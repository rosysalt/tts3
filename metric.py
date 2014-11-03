from __future__ import division

import utility

import pdb

class Metric():
    def __init__(self, hypothesis, truth):
        self.hypothesis = hypothesis
        self.truth = truth

        self.H = len(self.hypothesis)
        self.T = len(self.truth)

        self.TP = self.hypothesis.intersection(self.truth)
        self.FP = self.hypothesis.difference(self.TP)
        self.FN = self.truth.difference(self.hypothesis)

    def accuracy(self):
        return len(self.TP) / self.T

    def precison(self):
        return len(self.TP) / self.H

    def recall(self):
        return len(self.TP) / self.T

    def is_data_correct(self):
        if self.hypothesis and self.truth:
            return True
        else:
            return False

    def summarize(self):
        if self.is_data_correct():
            print "Accuracy: %f" % self.accuracy()
            print "Precison: %f" % self.precison()
            print "Recall: %f" % self.recall()

        self.print_FP()
        self.print_TP()

    def print_FP(self):
        print "False Positive pairs: %d" % len(self.FP)
        utility.write_result('false_positive.result', list(self.FP))

    def print_TP(self):
        utility.write_result('true_positive.result', list(self.TP))