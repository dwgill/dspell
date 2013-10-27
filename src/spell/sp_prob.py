'''
Created on Oct 24, 2013

@author: Daniel Gill
'''

from nltk.probability import FreqDist
import sys

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
                inlcude(dist_flp = self[(str_src[:-2], str_tar[:-2])] + self.cost_flp)

            # No operation
            if str_src[-1] == str_tar[-1]:
                include(dist_nop = self[(str_src[:-1], str_tar[:-1])] + self.cost_nop)

            return min(distances)

