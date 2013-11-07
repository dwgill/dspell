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


def tri_iter(seq, strictfront=True, strictback=True):
    seq = seq.__iter__()

    def common_gen(first, second, third, stict):
        yield first, second, third
        for next_word in seq:
            first, second, third = second, third, next_word
            yield (first, second, third)
        else:
            if not strictback:
                yield (second, third)
                yield (third,)

    if strictfront:
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


def bi_iter(seq):
    first_two = list(islice(seq, 2))
    if len(first_two) == 2:
        first, second = first_two
        yield (first, second)
        for next_word in seq:
            first, second = second, next_word
            yield first, second
    elif not strict:
        yield tuple(first_two)

def uni_iter(seq):
    for item in seq:
        yield (item,)
