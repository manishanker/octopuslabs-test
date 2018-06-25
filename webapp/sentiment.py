#!/usr/bin/env python2.7
import requests
import config
import urllib
from goose import Goose
import re
import json

def get_article(url):
	g = Goose()
	article = g.extract(url=url)
	regex = re.compile('[^a-zA-Z]')
	article = regex.sub(' ', article.title)
	article = re.sub(' +', ' ', article)
	return article

def get_intent(url_target):
	"""	This function makes a curl request to wit.ai api since
		the client is only for python3
		using Goose to extract the main article and sending it to wit
	"""
	version = config.config["wit_version"]
	article = get_article(url_target)
	print article
	url = 'https://api.wit.ai/message?v=' + str(version) + '&q=' + urllib.quote(article)
	headers = {'Authorization': 'Bearer '+config.config["wit_token"]}
	response = requests.get(url, headers=headers)
	response.encoding = 'utf-8'
	try:

	    print response.json()["entities"]
	    result_list= response.json()["entities"]["sentiment"]
	    if len(result_list):
		print "sent", result_list[0]["value"]
		return result_list[0]["value"]
	    else:
		print "unknown"
		return "unknown"
	except:
	    return "unknown"
