'''
Created on Oct 24, 2013

@author: Daniel Gill
'''

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
        cost_add = costs['add'], cost_rem = costs['rem'],
        cost_sub = costs['sub'], cost_flp = costs['flp'],
        cost_nop = costs['nop']):
    # Get the length of the strings.
    len_src = len(str_src)
    len_tar = len(str_tar)
    if len_src == 0:
        # If the source string is zero, then the transformation is going to be len_tar number of additions.
        return len_tar * cost_add

    elif len_tar == 0:
        # If the target string is zero, then the transformation is going to be len_src number of deletions.
        return len_src * cost_rem

    else:
        # How much would it cost if we transformed str_src into str_tar[:-1] and then added str_tar[-1] afterwards?
        dist_add = edit_distance(str_src, str_tar[:-1]) + cost_add

        # How much would it cost if we deleted str_src[-1] and then transformed str_src[:-1] into str_tar?
        dist_rem = edit_distance(str_src[:-1], str_tar) + cost_rem

        # How much would it cost if we replaced str_src[-1] with str_tar[-1] and then transformed str_src[:-1] into str_tar[:-1]?
        dist_sub = edit_distance(str_src[:-1], str_tar[:-1]) + cost_sub

        # If str_src[-2:] is reversed(str_tar[-2:]), then what does it cost to flip str_src[-2:] and transform str_src[:-2] into str_tar[:-2]
        dist_flp = edit_distance(str_src[:-2], str_tar[:-2]) + cost_flp if reversed(str_src[-2:]) == str_tar[-2:] else sys.maxint

        # If the last characters of both strings are the same, then what does it cost to ignore them and transform str_src[:-1] into str_tar[:-1]
        dist_nop = edit_distance(str_src[:-1], str_tar[:-1]) + cost_nop if str_src[-1] == str_tar[-1] else sys.maxint

        # Return the smallest cost found.
        return min(dist_add, dist_rem, dist_sub, dist_flp, dist_nop)

