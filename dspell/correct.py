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
"""
Crated on Oct 15, 2013

@author: Daniel Gill
"""

from collections import namedtuple
import os
import sys
import corpus, prob, dist, ngram_iter

ed_calc = dist.EDCalc()
num_candidates_per_word = 50
tri_pcalc = prob.ProbCalc(ngram='tri')
bi_pcalc = prob.ProbCalc(ngram='bi')
uni_pcalc = prob.ProbCalc(ngram='uni')

def get_wordset():
    """
    Iterate over the types of words encountered in the
    training data.
    """
    for word in uni_pcalc.pd.freqdist().keys():
        yield word[0]

def valid_word(word):
    """
    Determine if the provided word is found in the training
    data.
    """
    for other_word in get_wordset():
        if word == other_word:
            return True
    return False

def _main():
    """
    Determine format of provided user data and correct any misspelled words.
    """
    if len(sys.argv) < 3:
        print('Improper format. Please give mode (file/dir/str) + "data"')
        return

    mode, data = sys.argv[1:]
    mode = mode.lower()

    # Data given is file path.
    if mode == 'file':
        if not os.path.isfile(data):
            print('provided path is not to a file.')
            return
        else:
            print_words(correct_words(corpus.process_file(data)))

    # Data given is directory path.
    elif mode == 'dir':
        if not os.path.isdir(data):
            print('provided path is not to a directory.')
        else:
            print_words(correct_words(corpus.process_dir(data)))

    # Data given is string.
    elif mode == 'str':
        correct_string(data)
    else:
        print("Unrecognized mode.")

def print_words(words):
    """
    Print a list of strings.
    """
    print " ".join(words)

def correct_string(string):
    """
    Correct the spelling of a string of words.
    """
    return print_words(correct_words(corpus.tokenize(string)))

def correct_words(words):
    """
    Replace any improperly spelled words in the provided sequence with
    correctly spelled words most probable to occur in that context.
    """
    trigrams = ngram_iter.tri_iter(words)

    first_keyf = lambda trigram: (lambda x: 
            tri_pcalc.prob((x, trigram[1], trigram[2])))
    second_keyf = lambda trigram: (lambda x: 
            tri_pcalc.prob((trigram[0], x, trigram[2])))
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
        yield correct_bigram(first_trigram)

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

def correct_unigram(unigram):
    """
    Return the word calculated to be most probable that has an
    acceptable levenshtein distance to the provided word.
    """
    first = unigram[0]
    if not valid_word(first):
        candidates = find_first_n_words_under_dist(first, num_candidates_per_word)
        keyf = lambda x: uni_pcalc.prob((x,))
        return max(candidates, key=keyf)
    else:
        return first

def correct_bigram(bigram, index_to_check=1):
    """
    Return a bigram equal to the provided bigram but with
    bigram[index_to_check] replaced with a word
    that maximizes the probability of the bigram.
    """
    word_to_check = bigram(index_to_check)
    if not valid_word(word_to_check):
        if index_to_check == 0:
            keyf = lambda bigram: lambda x: bi_pcalc.prob((bigram[0], x))
        else:
            keyf = lambda bigram: lambda x: bi_pcalc.prob((x, bigram[1]))

        candidates = find_first_n_words_under_dist(word_to_check, num_candidates_per_word)
        return max(candidates, key=keyf(bigram))
    else:
        return word_to_check

keyf_standard = lambda trigram: lambda x: tri_pcalc.prob((trigram[0], trigram[1], x))

def correct_trigram(trigram, index_to_check=2, keyf=keyf_standard):
    """
    Return a trigram equal to the provided trigram but with
    trigram[index_to_check] replaced with a word
    that maximizes the probability of the trigram.
    """
    word_to_check = trigram[index_to_check]

    if not valid_word(word_to_check):
        candidates = find_first_n_words_under_dist(word_to_check, num_candidates_per_word)
        return max(candidates, key=keyf(trigram))
    else:
        return word_to_check

acceptable_distance = 4
def find_first_n_words_under_dist(word, n):
    """
    Return the n words most frequently encountered in the training
    data that demonstrate a levenshtein distance to the provided word
    equal to or less than acceptable_distance.
    """
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
    _main()
