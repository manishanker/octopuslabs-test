#!/usr/bin/env python2.7
import MySQLdb
import base64
from asymmetric_encryption import encrypt_message, decrypt_message
import config

class DBConnection:
    def __init__(self, DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME):
        self.host = DB_HOST
        self.port = DB_PORT
        self.name = DB_NAME
        self.user = DB_USER
        self.password = DB_PASSWORD
        self.conn = None

    def get_conn(self):
	if self.conn is None:
        	self.conn = MySQLdb.connect(host = self.host,
                	                    port = self.port,
                        	            db = self.name,
                                	    user = self.user,
                                    	    passwd = self.password)
	return self.conn
    
def create_table(key):
    mydbconnobj = DBConnection(config.config["host"],config.config["port"],\
				config.config["user"],config.config["passwd"],config.config["db"])
    mydbconn = mydbconnobj.get_conn()

    # Create table as per requirement
    if key=="tuple":
	sql = """CREATE TABLE IF NOT EXISTS word_data (\
         word LONGTEXT NOT NULL,\
         word_encrypted LONGTEXT,\
         frequency INT,\
	 PRIMARY KEY(word(100)),\
	 FULLTEXT (word)\
	 )"""
    else:
	sql = """CREATE TABLE IF NOT EXISTS url_data (\
         url LONGTEXT NOT NULL,\
         senti LONGTEXT,\
         PRIMARY KEY(url(100)),\
         FULLTEXT (url)\
         )"""
    cursor = mydbconn.cursor()
    try:
        cursor.execute(sql)
    except:
        print "sql create", sql, key

    mydbconn.close()

def update_table(word_tuple, key):
    mydbconnobj = DBConnection(config.config["host"],config.config["port"],\
                                config.config["user"],config.config["passwd"],config.config["db"])
    mydbconn = mydbconnobj.get_conn()
    
    #print "word_tuple", word_tuple 
	# Create table as per requirement
    if key=="tuple":
	sql = "INSERT INTO word_data(\
	     word, word_encrypted, frequency)\
	    VALUES ('%s', '%s', '%d') ON DUPLICATE KEY UPDATE frequency = frequency + values(frequency)"  %\
	    (word_tuple[0], word_tuple[1], word_tuple[2])
	    #print "sql update", sql
    else:
	sql = "INSERT INTO url_data(\
             url, senti)\
            VALUES ('%s', '%s')"  %\
            (word_tuple[0], word_tuple[1])

    cursor = mydbconn.cursor()
    try:
	cursor.execute(sql)
    except:
	create_table(key)
    mydbconn.commit()
    mydbconn.close()

def show_data():
    mydbconnobj = DBConnection(config.config["host"],config.config["port"],\
                                config.config["user"],config.config["passwd"],config.config["db"])
    mydbconn = mydbconnobj.get_conn()
    sql1 = "select * from url_data"
    sql2 = "select * from word_data"
    cursor = mydbconn.cursor()
    cursor.execute(sql1)
    data_url = cursor.fetchall()
    
    cursor.execute(sql2)
    data_word = cursor.fetchall()
    
    #print "data", data_url, data_word
    return (data_url, data_word)
    mydbconn.close()

#create_table()
#t = ('mani123', 'mani', 3)
#update_table(t, "tuple")
#u=('urlhashed', 'neutral')
#update_table(u,"str")
#show_data()
