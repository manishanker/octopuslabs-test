#!/usr/bin/env python2.7

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options
from tornado.template import Template
from scrape import parse, show
from sentiment import get_intent
import os
import urllib
from tornado.escape import json_decode, json_encode
import json

define("port", default=8888, help="run on the given port", type=int)

# application configuration
class Application(tornado.web.Application):
	def __init__(self):
		handlers = [
			(r"/", IndexHandler),
			(r"/result", ScrapedDataHandler),
			(r"/admin", AdminHandler),
			(r"/adminresult", AdminDataHandler)
		]
		settings = dict(
			template_path=os.path.join(os.path.dirname(__file__), "templates"),
			static_path=os.path.join(os.path.dirname(__file__), "static"),
			debug=True,
			)
		tornado.web.Application.__init__(self, handlers, **settings)


# This is index file handler. Here the render functions displays the HTML
# index.html on the browser when GET request is made on root
# GET on http://localhost:8000/
class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')


# This is admin file handler. Here the render functions displays the HTML
# index.html on the browser when GET request is made on root
# GET on http://localhost:8000/admin
class AdminHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('admin.html')

# This is to handle POST
# In the GET request, index page with a form is rendered on the browser.
# When user fills it and submits, this handler will handle that POST request
# i.e. the POST request is sent from index.html page
# The values in the POST request can be accessed by get_argument friendly 
# function which is provided by tornado.web.RequestHandler
class ScrapedDataHandler(tornado.web.RequestHandler): 
    def post(self):
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Headers', '*')
        self.set_header('Access-Control-Max-Age', 1000)
        self.set_header('Content-type', 'application/json')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.set_header('Access-Control-Allow-Headers',
                        'Content-Type, Access-Control-Allow-Origin, Access-Control-Allow-Headers, X-Requested-By, Access-Control-Allow-Methods')

        # use get_argument to get values by name
        # i.e. in the form whose name is 'noun1' is returned when get_argument
        # is called and stored in noun1 variable 
       	body=json.loads(self.request.body)
        url = body['url']
        token = body['token']
        result = parse(url)
        response = {'result': result}
        self.write(response)

# This is to handle POST
# In the GET request, admin page is rendered on the browser.
# function which is provided by tornado.web.RequestHandler
class AdminDataHandler(tornado.web.RequestHandler): 
    def post(self):
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Headers', '*')
        self.set_header('Access-Control-Max-Age', 1000)
        self.set_header('Content-type', 'application/json')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.set_header('Access-Control-Allow-Headers',
                        'Content-Type, Access-Control-Allow-Origin, Access-Control-Allow-Headers, X-Requested-By, Access-Control-Allow-Methods')

        # use get_argument to get values by name
        # i.e. in the form whose name is 'noun1' is returned when get_argument
        # is called and stored in noun1 variable 
        body=json.loads(self.request.body)
        token = body['token']
	if token:
	    result = show()
	else:
	    result = ""
        response = {'result': result}
        self.write(response)

def main():
	tornado.options.parse_command_line()
	http_server = tornado.httpserver.HTTPServer(Application())
	http_server.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
	main()
