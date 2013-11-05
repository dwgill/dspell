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
from sp_bigram import Bigram

def get_sgts_tokens(tokens):
    uni_fd, bi_fd = FD(), FD()
    p_token = 'the'
    for c_token in tokens:
        uni_fd.inc(c_token)
        bi_fd.inc(Bigram(previous=p_token, current=c_token))
        p_token = c_token
    return ProbCalc(SGT(uni_fd), SGT(bi_fd))

def get_sgts_fds(uni_fd, bi_fd):
    return ProbCalc(SGT(uni_fd), SGT(bi_fd))

class ProbCalc(object):
    def __init__(self, uni_pd, bi_pd):
        self.uni_pd = uni_pd
        self.bi_pd = bi_pd

    def prob_unigram(self, unigram):
        return self.uni_pd.prob(unigram)

    def prob_bigram(self, bigram):
        return self.bi_pd.prob(bigram)

    def prob_c_given_p(self, c, p):
        pc = Bigram(current=c, previous=p)
        return self.prob_bigram(pc) / self.prob_unigram(p)
