#!/usr/bin/python2
#
# Utilities to calculate scores and fetch new words
#

import re, random, enchant
import database

# global reference dictionary
reference_wordlist = dict()

# global sorted wordlist
sorted_reference_wordlist = []

def percentile(): return 0.8
def words_in_language(): return len(reference_wordlist)
def wordlist_filename(): return "data/corpusrank.txt"

class Word:
    """
    Word class
    """
    def __init__(self,rank,freq):
        self.rank = rank
        self.freq = freq

def create_reference_wordlist(fname):
    """
    creates dict based on table of word occurences and normalizes it 
    
    keys are word strings
    values are Word class with members Word.rank Word.frequency

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

    d = dict()
    en_dict = enchant.Dict("en_GB")

    f = open(fname,'r')
    for line in f.readlines():
        data = line.split()
        try:
            word = data[2]
            # add word if in dictionary
            if en_dict.check(word) and word.isalpha():
                d[word] = Word(int(data[0]),float(data[1]))

        except:
            continue

    normalize()

    return d


def remove_quotes(string):
    """
    Remove all quotes from string
    """
    return re.sub(r'.*>.*', '', string)

def unique_words(string):
    """
    Returns list of unique (case insensitive) strings from a string.
    """
    string = remove_quotes(string)
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
    d = reference_wordlist
    
    # sort words, reverse for performance
    sorted_words = sorted(filter_words(wordlist), \
        key = lambda x: d.get(x).rank, reverse=True)
    
    threshold_word = sorted_words[ int( (1 - percentile()) * len(sorted_words))]
    score = float( d[threshold_word].rank ) / words_in_language()
    
    return score

def score(data):
    """
    Scores based on list of words or one string.
    """
    if type(data) is type('str'):
        return score_wordlist_percentile(filter_words(unique_words(data)))
    elif type(data) is type([]):
        return score_wordlist_percentile(data)
    else: 
        return None


def test_on_textfile(fname):
    """
    Loads text file and estimates number of words in vocabulary.
    """
    wl = filter_words( unique_words( open(fname, 'r').read()))
    return score(wl) * words_in_language()


# some testing functions
#def get_list(a):
#    return unique_words( open("../data/m.txt", 'r').read() )
#
#def get_score(a):
#    return test_on_textfile("../data/m.txt")


def choose_words(userid, nwords_to_send = 10):
    """
    Choose words for user to learn. 
    """
    # query database for known words of user
    userwords = database.get_list(userid)

    # query database for user score
    userscore = database.get_score(userid)

    target = int(percentile() * userscore * words_in_language())
    
    # add a word not yet known to user to wordlist (ugly solution)
    def add_word(target,wordlist):
        tries = 0
        while tries < 1000:
            candidate = int(target * (1.0 + random.random() \
                * (1 - percentile())))
            tries += 1
            if candidate > words_in_language() + 1: 
                continue
            word = sorted_reference_wordlist[candidate] 
            if word not in wordlist:         
                return wordlist + [word]
        
        # can't find unknown words, returning whatever I have
        return wordlist + [word]

    wordlist = []
    
    for i in range(nwords_to_send):
        wordlist = add_word(target,wordlist)
   
    database.store_user_words(userid, wordlist)
    newscore = score(wordlist + userwords)
    database.set_score(newscore)

    return wordlist

def score_user(email, text):
    """
    Score a new user based on text User is assumed to be in database.
    """
    wordlist = filter_words(unique_words(text))
    userscore = score(wordlist)
    print(wordlist)
    database.store_user_words(email, wordlist)
    database.set_score(email, userscore)

    return userscore

def get_score(email):
    return int( database.get_score(email) * words_in_language() )

def initialize_module():
    global reference_wordlist
    global sorted_reference_wordlist
    
    reference_wordlist = create_reference_wordlist(wordlist_filename())
    sorted_reference_wordlist = sorted(reference_wordlist,
            key=lambda x: reference_wordlist.get(x).freq, reverse=True)

initialize_module()


