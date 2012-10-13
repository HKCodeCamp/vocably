#!/usr/bin/python2
#
# Utilities to calculate scores and fetch new words
#

import re
import random, enchant
import database

# global reference dictionary
reference_wordlist = dict()

# global sorted wordlist
sorted_reference_wordlist = []

def percentile():
    return 0.8
def words_in_language():
    return len(reference_wordlist)
def wordlist_filename():
    return "data/corpusrank.txt"


class Word:
    """
    Word class
    """
    def __init__(self, rank,freq):
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

    f = open(fname, 'r')
    for line in f.readlines():
        data = line.split()
        try:
            word = data[2]
            # add word if in dictionary
            if en_dict.check(word) and word.isalpha():
                d[word] = Word(int(data[0]), float(data[1]))

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
    sorted_words = sorted(filter_words(wordlist),
        key= lambda x: d.get(x).rank, reverse=True)

    threshold_word = sorted_words[int( (1 - percentile()) * len(sorted_words))]
    score = float(d[threshold_word].rank ) / words_in_language()

    return score


def score(data):
    """
    Scores based on list of words or one string.
    """
    if isinstance(data, type('')):
        return score_wordlist_percentile(filter_words(unique_words(data)))
    elif isinstance(data, type([])):
        return score_wordlist_percentile(data)
    else: 
        return None


def test_on_textfile(fname):
    """
    Loads text file and estimates number of words in vocabulary.
    """
    wl = filter_words(unique_words( open(fname, 'r').read()))
    return score(wl) * words_in_language()

def choose_words(email, nwords_to_send = 10):
    """
    Choose nwords_to_send words for user to learn. If less words are available
    only the available words will be sent.
    Words chosen will be assumed to be learned by user and are added to the
    user vocabulary in the db. User score in db is updated.
    """
    # query database for known words of user
    userwords = database.get_list(email)

    # create complete dict and remove known words
    unknown_words = reference_wordlist.copy()
    for w in userwords:
        unknown_words.pop(w,0)
 
    # convert unknown words dict to sorted list
    unknown_words = sorted(unknown_words,
            key=lambda x: unknown_words.get(x).freq, reverse=True)

    # at best we can send all the unknown words
    nwords_to_send = min(nwords_to_send, len(unknown_words))

    # query database for user score
    userscore = database.get_score(email)

    def add_word():
        target = int(percentile() * userscore * len(unknown_words))
        candidate = int(target * (1 + random.random() * (1 - percentile())))
        return unknown_words.pop(candidate)

    wordlist = [add_word() for i in range(nwords_to_send)]
   
    database.store_user_words(email, wordlist)
    newscore = score(wordlist + userwords)
    database.set_score(email, newscore)

    return wordlist

def score_user(email, text):
    """
    Score a new user based on text. User is assumed to be in database.
    """
    wordlist = filter_words(unique_words(text))
    userscore = score(wordlist)
    database.store_user_words(email, wordlist)
    database.set_score(email, userscore)
    print 'User %s knows %i words' % (email, userscore * words_in_language())
    return userscore

def get_score(email):
    return int(database.get_score(email) * words_in_language() )

def initialize_module():
    global reference_wordlist
    global sorted_reference_wordlist
    
    reference_wordlist = create_reference_wordlist(wordlist_filename())
    sorted_reference_wordlist = sorted(reference_wordlist,
            key=lambda x: reference_wordlist.get(x).freq, reverse=True)

initialize_module()


