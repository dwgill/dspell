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
import sp_corpus
from collections import namedtuple
from bigram import Bigram

WordCorrection = namedtuple('WordCorrection', ['original', 'corrected'])

tolerable_distance = 5

def _main():
    if 1 < len(sys.arv[1:]) < 3:
        print("Improper format. Please give mode (file/dir/line) + data")
        return

    mode, data = sys.argv[1:]
    mode = mode.lower()

    # Data given is file path.
    if mode == 'file':
        if not os.path.isfile(data):
            print('provided path is not to a file.')
            return
        correct_words(sp_corpus.process_file(data))

    # Data given is directory path.
    elif mode == 'dir':
        if not os.path.isdir(data):
            print('provided path is not to a directory.')
            return
        correct_words(sp_corpus.process_dir(data))

    # Data given is string.
    else:
        correct_words(sp_corpus.tokenize(data))


def correct_words(words):
    previous_word = None
    for current_word in words:
        current_pair = Bigram(current=current_word, previous=previous_word)
        yield correct_word(current_pair)
        previous_word = current_word

def correct_word(bigram):
    pass

if __name__ == "__main__":
    _main()
