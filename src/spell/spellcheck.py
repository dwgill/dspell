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

def_costs = {'rem' : 2, 'sub' : 3, 'add' : 2, 'flp' : 3, 'nop' : 0}

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

class memoize(dict):
    def __init__(self, func):
        self.func = func 

    def __call__(self, *args):
        return self[args]

    def __missing__(self, key):
        result = self[key] = self.func(*key)
        return result

@memoize
def edit_distance(str_src, str_tar, 
        cost_add = def_costs['add'], cost_sub = def_costs['sub'],
        cost_flp = def_costs['flp'], cost_rem = def_costs['rem'],
        cost_nop = def_costs['nop']):
    len_src = len(str_src)
    len_tar = len(str_tar)
    if len_src == 0:
        return len_tar * cost_add
    elif len_tar == 0:
        return len_src * cost_rem
    else:
        dist_add = edit_distance(str_src, str_tar[:-1]) + cost_add
        dist_rem = edit_distance(str_src[:-1], str_tar) + cost_rem
        dist_sub = edit_distance(str_src[:-1], str_tar[:-1]) + cost_sub if len_src == len_tar else sys.maxint
        dist_flp = edit_distance(str_src[:-2], str_tar[:-2]) + cost_flp if reversed(str_src[-2:]) == str_tar[-2:] else sys.maxint
        dist_nop = edit_distance(str_src[:-1], str_tar[:-1]) + cost_nop if str_src[-1] == str_tar[-1] else sys.maxint
        return min(dist_add, dist_rem, dist_sub, dist_flp, dist_nop)

if __name__ == "__main__":
    _main()
