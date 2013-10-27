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

    def avg_cost(self):
        costs = (self.cost_add, self.cost_flp, self.cost_nop, self.cost_rem, self.cost_sub)
        return sum(costs) / float(len(values))


    def _calc_edit_dist(self, str_src, str_tar):
        # Get the length of the strings.
        len_src = len(str_src)
        len_tar = len(str_tar)

        if len_src == 0:
            # If the source string is zero, then the transformation is going to be len_tar number of additions.
            return len_tar * self.cost_add

        elif len_tar == 0:
            # If the target string is zero, then the transformation is going to be len_src number of deletions.
            return len_src * self.cost_rem

        else:
            # How much would it cost if we transformed str_src into str_tar[:-1] and then added str_tar[-1] afterwards?
            dist_add = self[(str_src, str_tar[:-1])] + self.cost_add

            # How much would it cost if we deleted str_src[-1] and then transformed str_src[:-1] into str_tar?
            dist_rem = self[(str_src[:-1], str_tar)] + self.cost_rem

            # How much would it cost if we replaced str_src[-1] with str_tar[-1] and then transformed str_src[:-1] into str_tar[:-1]?
            dist_sub = self[(str_src[:-1], str_tar[:-1])] + self.cost_sub

            # If str_src[-2:] is reversed(str_tar[-2:]), then what does it cost to flip str_src[-2:] and transform str_src[:-2] into str_tar[:-2]
            if reversed(str_src[-2:]) == str_tar[-2:]:
                dist_flp = self[(str_src[:-2], str_tar[:-2])] + self.cost_flp
            else:
                dist_flp = sys.maxint

            # If the last characters of both strings are the same, then what does it cost to ignore them and transform str_src[:-1] into str_tar[:-1]
            if str_src[-1] == str_tar[-1]:
                dist_nop = self[(str_src[:-1], str_tar[:-1])] + self.cost_nop
            else:
                dist_nop = sys.maxint

            # Return the smallest cost found.
            return min(dist_add, dist_rem, dist_sub, dist_flp, dist_nop)

