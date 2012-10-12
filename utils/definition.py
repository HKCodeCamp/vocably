
import urllib
import ast
import sys

def format(string):
    return string.replace("&#39;","'").replace("&quot;",'"')
    
def definition(word):
    """
    Returns the first definition of a word.

    >>> definition("automobile")
    'car: a motor vehicle with four wheels; usually propelled by an internal combustion engine; "he needs a car to get to work"'

    """
    lhs = "http://www.google.com/dictionary/json?callback=s&q="
    rhs = "&sl=en&tl=en&restrict=pr,de&client=te"
    url = lhs + word + rhs;
    try:
	obj=urllib.urlopen(url);
    except:
        print "Please check your internet connection and try again"
        return

    content = obj.read()
    obj.close()
    content = content[2:-10]
    dict_ = ast.literal_eval(content)
    if dict_.has_key("webDefinitions"):
        def_ = dict_["webDefinitions"][0]["entries"][0]["terms"][0]["text"]
        return format(def_)
    else:
        print "Definition unavailable"

if __name__ == "__main__":
    import doctest
    doctest.testmod()
