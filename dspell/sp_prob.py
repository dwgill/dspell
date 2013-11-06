# Copyright (c) 2013 Daniel Gill
#
# Permission is hereby granted, free of charge, to any person obtaining 
# a copy of this software and associated documentation files 
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
# The above copyright notice and this permission notice shall be
#
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT.
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

'''
Created on Nov 2, 2013

@author: Daniel Gill
'''

import nltk
from nltk.probability import FreqDist as FD
from nltk.probability import SimpleGoodTuringProbDist as SGT
import sp_corpus
import os
import sp_itertools

training_dir = "./res/training_data/"
tri_data  = "./res/trigrams.txt"
bi_data = "./res/bigrams.txt"
uni_data = "./res/unigrams.txt"

ngrams = {'uni':(uni_data, sp_itertools.uni_iter, 1), 'bi':(bi_data, sp_itertools.bi_iter, 2), 'tri':(tri_data, sp_itertools.tri_iter, 3)}


def get_sgt(seq):
    fd = FD()
    for ngram in seq:
        fd.inc(ngram)
    return SGT(fd)

def retrieve_data(path):
    fd = FD()
    with open(path) as data:
        for line in data:
            split_data = line.split("||")
            freq = split_data.pop()
            fd.inc(tuple(split_data), int(freq))
    return SGT(fd)

def write_data(fd, path):
    with open(path) as out:
        for ngram, count in fd.iteritems():
            seq = list(ngram)
            seq.append(str(count))
            out.write("||".join(seq))

class ProbCalc(object):
    def __init__(self, ngram='tri'):
        ngram = ngram.lower()[:3]
        if ngram not in ngrams.keys():
            raise UnsupportedNgramError(ngram + "grams are not supported.")

        data, iterator, self.length = ngrams[ngram]

        if os.path.exists(data):
            self.pd = retrieve_data(data)
        else:
            self.pd = get_sgt(iterator(sp_corpus.process_dir(training_dir)))
            write_data(self.pd.freqdist(), data)

    def prob(x):
        if len(x) < self.length:
            raise UnsupportedNgramError("ProbCalc calibrated for ngrams of length " +
                    str(self.length) + ", not " + len(x) + ".")
        return self.pd.prob(tuple(x))

class UnsupportedNgramError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
