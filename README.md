# octopuslabs-test
This repo contains code that was written for the test given by Octopuslabs

#How to run locally
create a virtualenv with python 2.7.13
    `virtualenv -p python2.7.13 .venv --no-site-packages`
activate virtualenv using 
    `source .venv/bin/activate`

install the required depencies using 
    `pip install -r requirements.txt`

We need to separately install the spacy english model using
    `python -m spacy download en`


Create a mysql database named `scraped_data` with following configuration refer config.py:
    "host": "localhost",
     port": 3306,
     "user": "newuser",
     "passwd": "password",
     "db": "scraped_data"

Once the database is setup and all the depencies are working properly, we can go ahead and start
tornado server using :
    `python app.py`

Once the server is running, you can navigate to :

http://localhost:8888/

Paste the url and you will see the wordcloud[only Nouns, Verbs] render on the same page
Nouns and Verb filtering has been done by spacy.

At the same time, the encrypted data will be saved in the tables url_data and word_data in the
database.

I am using wit.ai for getting the sentiment of the text. wit has limitation of 256 characters,
hence, I am extracting the title of the url and sending it to wit and savind it back in DB




#TODO

1. Have a script like init.sql to create database
2. Make sure no local ips are in code
3. Admin page still doesnt get the data from backend

#Note
1. spacy to get frequency of words and parts of speech [verbs, nouns]
2. spacy en model has to be downloaded `python -m spacy download en`
3. using wordcloud.js for showing the wordcloud in the front-end
4. using crypto to store the encrypted message in backend
5. salt.txt and mykey.pem will be used for encryption
