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
Created on Oct 24, 2013

@author: Daniel Gill
'''

from lib import sgt

costs = {'rem' : 1.0, 'sub' : 1.5, 'add' : 1.0, 'flp' : 1.5, 'nop' : 0.0}

class EDCalc(dict):
    def __init__(self, cost_add = costs['add'], cost_rem = costs['rem'],
            cost_sub = costs['sub'], cost_flp = costs['flp'],
            cost_nop = costs['nop']):
        self.cost_add = cost_add
        self.cost_rem = cost_rem
        self.cost_sub = cost_sub
        self.cost_flp = cost_flp
        self.cost_nop = cost_nop

    def edit_distance(self, *args):
        result = self[args]
        self.clear()
        return result

    def __missing__(self, key):
        result = self[key] = self._calc_edit_dist(*key)
        return result

    @property
    def avg_cost(self):
        costs = (self.cost_add, self.cost_flp, self.cost_nop, self.cost_rem, self.cost_sub)
        return sum(costs) / float(len(values))


    def _calc_edit_dist(self, str_src, str_tar):
        len_src = len(str_src)
        len_tar = len(str_tar)

        # Source is empty string
        if len_src == 0:
            return len_tar * self.cost_add

        # Target is empty string
        elif len_tar == 0:
            return len_src * self.cost_rem

        # Target & Source are not empty
        else:
            distances = []
            include = lambda item: distances.append(item)

            # Addition
            include(self[(str_src, str_tar[:-1])] + self.cost_add)

            # Deletion
            include(self[(str_src[:-1], str_tar)] + self.cost_rem)

            # Substitution
            include(self[(str_src[:-1], str_tar[:-1])] + self.cost_sub)

            # Transposition
            if reversed(str_src[-2:]) == str_tar[-2:]:
                inlcude(self[(str_src[:-2], str_tar[:-2])] + self.cost_flp)

            # No operation
            if str_src[-1] == str_tar[-1]:
                include(self[(str_src[:-1], str_tar[:-1])] + self.cost_nop)

            return min(distances)

