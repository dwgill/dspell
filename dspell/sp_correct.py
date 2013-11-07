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
import sp_corpus, sp_prob, sp_dist, sp_itertools
import itertools
from collections import namedtuple

ed_calc = sp_dist.EDCalc()

acceptable_distance = 4
acceptable_prob = 0.001
check_context = False
use_unix_wordlist = False
num_candidates_per_word = 50

dist_calc = sp_dist.EDCalc()
word_path = "./res/new_vocab.txt"

tri_pcalc = None
def trigram_pdcalc():
    global tri_pcalc
    if tri_pcalc:
        return tri_pcalc
    else:
        tri_pcalc = sp_prob.ProbCalc(ngram='tri')
        return tri_pcalc

bi_pcalc = None
def bigram_pdcalc():
    global bi_pcalc
    if bi_pcalc:
        return bi_pcalc
    else:
        bi_pcalc = sp_prob.ProbCalc(ngram='bi')
        return bi_pcalc

uni_pcalc = None
def unigram_pdcalc():
    global uni_pcalc
    if uni_pcalc:
        return uni_pcalc
    else:
        uni_pcalc = sp_prob.ProbCalc(ngram='uni')
        return uni_pcalc

def get_wordset():
    if use_unix_wordlist:
        with open(word_path) as words:
            for word in words:
                yield word.strip()
    else:
        for word in unigram_pdcalc().pd.freqdist().keys():
            yield word[0]

def valid_word(word):
    for other_word in get_wordset():
        if word == other_word:
            return True
    else:
        return False

def main():
    if 1 < len(sys.argv[1:]) < 2:
        print("Improper format. Please give mode (file/dir/str) + data")
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
        correct_string(data)

    else:
        print("Unrecognized mode.")

def print_words(words):
    print " ".join(words)

def correct_string(string):
    return print_words(correct_words(sp_corpus.tokenize(string)))

def correct_words(words):
    trigrams = sp_itertools.tri_iter(words)

    first_keyf= lambda trigram: lambda x: trigram_pdcalc().prob((x, trigram[1], trigram[2]))
    second_keyf = lambda trigram: lambda x: trigram_pdcalc().prob((trigram[0], x, trigram[2]))
    first_trigram = None

    try:
        first_trigram = trigrams.next()
    except StopIteration:
        yield "NO INPUT?"
        return


    # Have we only been given a single word?
    if len(first_trigram) == 1:
        yield correct_unigram(first_trigram)
        return

    # Have we only been given two words?
    elif len(first_trigram) == 2:
        pass

    # We have been given three or more words.
    else:
        # Find the replacement for the first word in the context of the next two
        yield correct_trigram(first_trigram, index_to_check=0, keyf=first_keyf)
        # Find the replacement for the second word in the context of the two around it.
        yield correct_trigram(first_trigram, index_to_check=1, keyf=second_keyf)
        # Find the replacement for the third in the context of the two previous.
        yield correct_trigram(first_trigram)

    # Find the replacement for the rest of the words using the two previous etc.
    for trigram in trigrams:
        yield correct_trigram(trigram)

def not_probable_enough(ngram):
    if check_context:
        if len(ngram) == 1:
            return unigram_pdcalc().prob(ngram) <= acceptable_prob
        elif len(ngram) == 2:
            return bigram_pdcalc().prob(ngram) <= acceptable_prob
        else:
            return trigram_pdcalc().prob(ngram) <= acceptable_prob
    else:
        return False

def correct_unigram(unigram):
    first = unigram[0]
    if not valid_word(first) or not_probable_enough(unigram):
        candidates = find_first_n_words_under_dist(first, ed_calc, num_candidates_per_word)
        keyf = lambda x: unigram_pdcalc().prob((x,))
        return max(candidates, key=keyf)
    else:
        return first

def correct_bigram(bigram, index_to_check=1):
    word_to_check = bigram(index_to_check)
    if not valid_word(word_to_check) or not_probable_enough(bigram):

        if index_to_check == 0:
            keyf = lambda bigram: lambda x: bigram_pdcalc().prob((bigram[0], x))
        else:
            keyf = lambda bigram: lambda x: bigram_pdcalc().prob((x, bigram[1]))

        candidates = find_first_n_words_under_dist(word_to_check, ed_calc, num_candidates_per_word)
        return max(candidates, key=keyf(bigram))
    else:
        return word_to_check

keyf_standard = lambda trigram: lambda x: trigram_pdcalc().prob((trigram[0], trigram[1], x))

def correct_trigram(trigram, index_to_check=2, keyf=keyf_standard):
    word_to_check = trigram[index_to_check]

    if not valid_word(word_to_check) or not_probable_enough(trigram):
        candidates = find_first_n_words_under_dist(word_to_check, ed_calc, num_candidates_per_word)

        return max(candidates, key=keyf(trigram))
    else:
        return word_to_check

def find_first_n_words_under_dist(word, ed_calc, n):
    candidates = []
    for candidate in get_wordset():
        if len(candidates) > n:
            break
        else:
            if ed_calc[(word, candidate)] <= acceptable_distance:
                candidates.append(candidate)
    ed_calc.clear()
    return candidates



if __name__ == "__main__":
    main()
