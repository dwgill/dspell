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

import nltk
import sys

def _main():
    if len(sys.argv) < 2:
        print("Please provide a file to correct.")
    elif len(sys.argv) > 2:
        for param in sys.argv[2:]:
            if '=' not in param:
                continue

            param_name, param_val = param.split('=')
            for op in costs.keys():
                if op in param_name:
                    costs[op] = float(param_val)
                    break

    print(correct_file(sys.argv[1]))

def correct_file(file_path):
    with open(file_path) as opened_file:
        return correct_lines(opened_file)

def correct_lines(lines):
    corrected_lines = []
    for line in lines:
        tokens_raw = nltk.word_tokenize(line)
        corrected_line = ''
        for word in tokens_raw:
            if word.isalpha():
                corrected_line += correct_spelling(word) + ' '
            else:
                corrected_line += word + ' '
        corrected_lines.append(corrected_line)
    return corrected_lines

# TO BE IMPLEMENTED
def correct_spelling(word):
    return word

if __name__ == "__main__":
    _main()
