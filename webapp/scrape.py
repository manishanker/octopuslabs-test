#!/usr/bin/env python2.7

from bs4 import BeautifulSoup as bs
from bs4.element import Comment
from urllib2 import urlopen
from salt import hash_word
from database import update_table
import re
import spacy
from collections import Counter
import config
import unicodedata

def fetch_url(url):
    """ Tries to fetch the url that user has given. 
        IF the url cannot be downloaded, alert will be shown
    """
    try:
        soup = bs(urlopen(url).read(), 'html.parser')
        return soup
    except:
        print "Couldnot download the content from the URL", url
        return ""

def tag_visible(element):
    """Utility function to exclude text present inside html tags"""

    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


def text_from_html(soup):
    """Function to extract the text from the html"""

    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)

    return u" ".join(t.strip() for t in visible_texts)

def pos_text(text):
    """ This function uses Spacy, open source NLP
        toolkit to find the most frequent words
        and parts of speech and return only nouns and 
        verbs for word cloud
    """
    nlp = spacy.load('en')
    doc = nlp(text)
    # all tokens that arent stop words or punctuations
    words = [token.text.encode('ascii', 'ignore') for token in doc if token.is_stop != True and token.is_punct != True]

    # noun tokens that arent stop words or punctuations
    final_tokens = [token.text.encode('ascii', 'ignore') for token in doc if token.is_stop != True and \
                    token.is_punct != True and (token.pos_ == "NOUN" or token.pos_ == "VERB")]

    # frequency dictionary for all tokens
    word_freq = Counter(words)

    #top 100 words to display in wordcloud which are noun or verb
    #frequency will be used to show big/small words in wordcloud
    final_tokens_freq = Counter(final_tokens)
    result = final_tokens_freq.most_common(config.config["MAX_FREQUENCY"])
    #print result
    return result

def parse(url):
    """ Parses the data fetched from fetch_url
        If its not empty, frequency, POS, sentiment of the text are
        returned back to front-end.
    """
    soup = fetch_url(url)
    result = {}
    if soup:
        text = text_from_html(soup)
        text = re.sub(' +', ' ', text)
        result_list = pos_text(text)
	#print "result_list", result_list
	word_tuple = []
	for x in result_list:
	    res = hash_word(x)
	    word_tuple.append(res)
	print "word_tuple", word_tuple
	for y in word_tuple:
	    update_table(y)
        for (x,y) in result_list:
            result[x]=y
        return result
    else:
        print "Alert the url could not be found"
        return ""
#parse('https://www.geeksforgeeks.org/python-map-function/')
