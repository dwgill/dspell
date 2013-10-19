#!/usr/bin/python
'''
Created on Oct 9, 2013

@author: tvandrun
'''

import sys
import nltk
from nltk.corpus import PlaintextCorpusReader

def edit_distance(source, target, scores=[2,3,2,3,0], cut_off=sys.maxint):

    # Make a zeroed out matrix of len(target)+1 by len(source)+1.
    distances = [[0 for j in range(len(source) + 1)] for i in range(len(target) + 1)]

    # Make all values distances[0..len(target)+1][0] = range(len(target) + 1)
    # i.e. for any given target, it will take i insertions to turn an empty string into that target.
    for i in range(len(target) + 1) :
        distances[i][0] = scores[0] * i

    # Make all values distances[0][0..len(source)] = range(len(source))
    # i.e. for any given empty string
    for j in range(len(source) + 1) :
        distances[0][j] = scores[1] * j



    for i in range(1, len(target) + 1) :
        for j in range(1, len(source) + 1) :
            candidate_edits = [distances[i-1][j]+scores[0],  # insert
                               distances[i-1][j-1] + scores[1],  # substitute
                               distances[i][j-1] + scores[2],  # delete
                               distances[i-2][j-2] + scores[3]   # flip
                               if i > 1 and j > 1 and target[i-1] == source[j-2] and  target[i-2] == source[j-1]
                               else sys.maxint,
                               distances[i-1][j-1] + scores[4]  # nop
                               if target[i-1] == source[j-1] else sys.maxint]
            distances[i][j] = min(candidate_edits)
        if min(distances[i]) >= cut_off :
            return sys.maxint
    return distances[len(target)][len(source)]

reader = PlaintextCorpusReader('.', '.*\.txt')
text = [x.lower() for x in nltk.Text(reader.words('baum-train.txt'))]
vocab = set([x for x in text if x.isalpha()])

test_word = 'lave'

ed_dists = {}

for w in vocab :
    dist = edit_distance(test_word, w, cut_off=25)
    if dist <= 5 :
        print w, dist
    if dist != sys.maxint :
        if dist not in ed_dists.keys() :
            ed_dists[dist] = 1
        else:
            ed_dists[dist] += 1

print "*********"
        
for d in ed_dists.keys() :
    print d, ed_dists[d]



                                   
    
