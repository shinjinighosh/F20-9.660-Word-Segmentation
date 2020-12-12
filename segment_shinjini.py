"""
Code based on Peter Norvig's book "Beautiful Data"

Code to segment words based on n-gram models
"""

import re, string, random, glob, operator, heapq
from collections import defaultdict
from math import log10
import os

def memo(f):
    """Memoize function f."""
    table = {}
    def fmemo(*args):
        if args not in table:
            table[args] = f(*args)
        return table[args]
    fmemo.memo = table
    return fmemo

def test(verbose=None):
    """Randomized testing"""
    import doctest
    print('Running tests...')
    doctest.testfile('segment_shinjini_test.txt', verbose=verbose)

# Word Segmentation

@memo
def segment(text):
    """Return a list of words that is the best segmentation of text."""
    if not text:
        return []
    candidates = ([first] + segment(rem) for first, rem in splits(text))
    return max(candidates, key=Pwords)

def splits(text, L=20):
    """Return a list of all possible (first, rem) pairs, len(first)<=L."""
    return [(text[:i+1], text[i+1:]) for i in range(min(len(text), L))]

def Pwords(words):
    """The Naive Bayes probability of a sequence of words."""
    return product(Pw(w) for w in words)

# Utility functions

def product(nums):
    """Return the product of a sequence of numbers."""
    return reduce(operator.mul, nums, 1)

class Pdist(dict):
    """A probability distribution estimated from counts in datafile."""

    def __init__(self, data=[], N=None, missingfn=None):
        for key,count in data:
            self[key] = self.get(key, 0) + int(count)
        self.N = float(N or sum(self.itervalues()))
        self.missingfn = missingfn or (lambda k, N: 1.0/N)

    def __call__(self, key):
        if key in self: return self[key]/self.N
        else: return self.missingfn(key, self.N)

def get_data(name, sep='\t'):
    """Read key,value pairs from file."""
    for line in open(os.path.join('data', name), 'r'):
        yield line.split(sep)

def handle_unknown_token(key, N):
    """Estimate the probability of an unknown word."""
    # Laplace additive smoothing
    return 10.0/(N * 10**len(key))

N = 1024908267229 # Number of tokens
# N = 1e12

Pw  = Pdist(get_data('count_1w.txt'), N, handle_unknown_token)

#### segment2: second version, with bigram counts

def cPw(word, prev):
    """Conditional probability of word, given previous word."""
    try:
        return P2w[prev + ' ' + word]/float(Pw[prev])
    except KeyError:
        return Pw(word)

P2w = Pdist(get_data('count_2w.txt'), N)

@memo
def segment2(text, prev='<S>'):
    """Return (log P(words), words), where words is the best segmentation."""
    if not text:
        return 0.0, []
    candidates = [combine(log10(cPw(first, prev)), first, segment2(rem, first))
                  for first,rem in splits(text)]
    return max(candidates)

def combine(prob_first, first, remaining):
    """Combine first and rem results into one (probability, words) pair."""
    Prem, rem = remaining
    return prob_first + Prem, [first] + rem
