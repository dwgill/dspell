#!/usr/bin/python
'''
Crated on Oct 15, 2013

@author: tvandrun
'''

import nltk
from nltk.corpus import PlaintextCorpusReader
import sys
from nltk.model import NgramModel
from memoize import memoize

def _main():
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

def correct_spelling(word):
    return word

if __name__ == "__main__":
    _main()
