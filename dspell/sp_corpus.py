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
Created on Oct 24, 2013

@author: Daniel Gill
'''

import re
import os

_token_re = r"(\w+'\w+)|(\w+)"

def tokenize(line):
    def has_valid_contraction(tup):
        return len(tup[0]) > 0

    for matching_tuple in re.findall(_token_re, line):
        string = ""
        if has_valid_contraction(matching_tuple):
            string = matching_tuple[0]
            was_contraction_last_time = True
        else:
            string = matching_tuple[1]

        if len(string) > 1 or string in ['I', 'a']:
            yield string.lower()

def process_file(file_path):
    with open(name=file_path, mode='r') as open_file:
        for line in open_file:
            for word in tokenize(line):
                yield word

def process_dir(dir_path):
    for file_path in os.listdir(dir_path):
        for word in process_file(os.path.join(dir_path, file_path)):
            yield word
