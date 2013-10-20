#!/usr/bin/python
'''
Created on Oct 11, 2013

@author: tvandrun
'''

import nltk
from nltk.corpus import PlaintextCorpusReader
import sys

def correct_spell(word):
    return word

source_file = open(sys.argv[1], 'r')

for line in source_file :
    tokens_raw = nltk.word_tokenize(line)
    
    corrected_line = ''
    for word in tokens_raw :
        if word.isalpha() :
            corrected_line += correct_spell(word) + ' '
        else :
            corrected_line += word + ' '
    print corrected_line
    
source_file.close()