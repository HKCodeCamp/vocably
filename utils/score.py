#!/usr/bin/python2
#
# Utilities to calculate scores and fetch new words
#

import re

# global reference wordlist
reference_wordlist = create_reference_wordlist('../data/corpusrank.txt')

class Word:
    """
    Word class
    """
    def __init__(self,rank,freq):
        self.rank = rank
        self.freq = freq

def create_reference_wordlist(fname):
    """
    d = create_dict(fname) create dictionary: d[word] = Word

    creates dict based on table of word occurences and normalizes it 
    
    rank: Word.rank
    frequency: Word.frequency

    fname is of the form:
    rank1 occurences1 word1
    rank2 occurences2 word2
    """
    def normalize():
        count = 0
        for i in d:
            count += d[i].freq
        for i in d:
            d[i].freq /= count

    d=dict()
    f = open(fname,'r')
    for line in f.readlines():
        data = line.split()
        try:
            d[data[2]] = Word(int(data[0]),float(data[1]));
        except:
            continue

    normalize()

    return d

def unique_words(string):
    """
    Returns list of unique (case insensitive) strings from a string.
    """
    return list(set(re.findall("[a-z]+", string.lower())))

def get_score(wordlist):
    pass

