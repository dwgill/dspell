# Copyright (c) 2013 Daniel Gill
#
# Permission is hereby granted, free of charge, to any person obtaining 
# a copy of this software and associated documentation files 
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
# The above copyright notice and this permission notice shall be
#
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT.
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

'''
Created on Nov 6, 2013

@author: Daniel Gill
'''
from itertools import islice

def tri_iter(seq, strict_front=True, strict_back=True):
    """
    Given a sequence of values, generate a sequences of trigrams
    corresponding to that sequence.
    If strict_front is set to False, then the first two provided generated
    elements of the sequences will be a unigram and bigram corresponding
    to the first two elements of the provided sequence. Similarly with
    strict_back.
    """
    seq = seq.__iter__()

    def common_gen(first, second, third, stict):
        yield first, second, third
        for next_word in seq:
            first, second, third = second, third, next_word
            yield (first, second, third)
        else:
            if not strict_back:
                yield (second, third)
                yield (third,)

    if strict_front:
        first_three = list(islice(seq, 3))
        if len(first_three) == 3:
            first, second, third = first_three
            for x in common_gen(first, second, third, True):
                yield x

    else:
        first = seq.next()
        yield (first,)
        second = seq.next()
        yield (first, second)
        third = seq.next()
        for x in common_gen(first, second, third, False):
            yield x
