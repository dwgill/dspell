#!/usr/bin/python2
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
