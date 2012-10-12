#!/usr/bin/python2
#
# Utilities to calculate scores and fetch new words
#

import re, operator

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

# global reference wordlist
reference_wordlist = create_reference_wordlist('../data/corpusrank.txt')

def unique_words(string):
    """
    Returns list of unique (case insensitive) strings from a string.
    """
    return list(set(re.findall("[a-z]+", string.lower())))

def filter_words(wordlist):
    """
    Remove words we don't have in our dictionary
    """
    return [word for word in wordlist if word in reference_wordlist]

def score_wordlist_percentile(wordlist):
    """
    Score user based on list of unique words in wordlist. Percentile approach.
    """
    percentile = 0.67
    d = reference_wordlist
    sorted_words = sorted(filter_words(wordlist), \
        key = lambda x: d.get(x).rank, reverse=True)
    threshold_word = sorted_words[ int( (1 - percentile) * len(sorted_words))]
    score = float( d[threshold_word].rank ) / len(d)
    return score


def test_on_textfile(fname):
    """
    Loads text file and estimates number of words in vocabulary.
    """
    wl = filter_words( unique_words( open(fname, 'r').read()))
    return score_wordlist_percentile(wl) * len(reference_wordlist)
    
