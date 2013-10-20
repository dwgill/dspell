'''
Created on Oct 15, 2013
Taken from PythonDecoratorLibrary
@author: dwgill
'''
class memoize(dict):
    def __init__(self, func):
        self.func = func

    def __call__(self, *args):
        return self[args]

    def __missing__(self, key):
        result = self[key] = self.func(*key)
        return result
