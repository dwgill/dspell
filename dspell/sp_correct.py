#!/usr/bin/python2
# Copyright (c) 2013 Daniel Gill
#
# Permission is hereby granted, free of charge, to any person obtaining 
# a copy of this software and associated documentation files 
# (the "Software"), to deal in the Software without restriction, 
# including without limitation the rights to use, copy, modify, merge, 
# publish, distribute, sublicense, and/or sell copies of the Software, 
# and to permit persons to whom the Software is furnished to do so, 
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be 
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, 
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF 
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY 
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, 
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE 
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''
Crated on Oct 15, 2013

@author: Daniel Gill
'''

import sys
import os
import sp_corpus, sp_prob, sp_dist
from collections import namedtuple
from itertools import islice

tolerable_distance = 6
tolerable_prob = 0.001
dist_calc = sp_dist.EDCalc()
prob_calc = sp_prob.ProbCalc()
get_words = prob_calc.uni_pd.freqdist().iterkeys

def main():
    if 1 < len(sys.argv[1:]) < 2:
        print("Improper format. Please give mode (file/dir/line) + data")
        return

    mode, data = sys.argv[1:]
    mode = mode.lower()

    # Data given is file path.
    if mode == 'file':
        if not os.path.isfile(data):
            print('provided path is not to a file.')
            return
        print_words(correct_words(sp_corpus.process_file(data)))

    # Data given is directory path.
    elif mode == 'dir':
        if not os.path.isdir(data):
            print('provided path is not to a directory.')
            return
        print_words(correct_words(sp_corpus.process_dir(data)))

    # Data given is string.
    elif mode == 'str':
        print_words(correct_words(sp_corpus.tokenize(data)))

    else:
        print("Unrecognized mode.")

def print_words(words):
    print " ".join(words)

def correct_string(string):
    return " ".join(correct_words(sp_corpus.tokenize(string)))

def correct_words(words):
    previous_word = None
    for current_word in words:
        current_pair = Bigram(current=current_word, previous=previous_word)
        cw = correct_word(current_pair)
        yield cw
        previous_word = current_word

def correct_word(bigram):
    if prob_calc.bi_pd.prob(bigram) > tolerable_prob:
        return bigram.current

    typo = bigram.current
    prev = bigram.previous

    dist_filter = dist_calc.make_filter(typo, tolerable_distance)
    candidates = filter(dist_filter, get_words())
    b = lambda x: Bigram(previous=prev, current=x)
    return max(candidates, key=lambda x: prob_calc.bi_pd.prob(b(x)))



if __name__ == "__main__":
    main()
