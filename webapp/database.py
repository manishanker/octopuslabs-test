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
    
def create_table():
    mydbconnobj = DBConnection(config.config["host"],config.config["port"],\
				config.config["user"],config.config["passwd"],config.config["db"])
    mydbconn = mydbconnobj.get_conn()

    # Create table as per requirement
    sql = """CREATE TABLE IF NOT EXISTS word_data (\
         word LONGTEXT NOT NULL,\
         word_encrypted LONGTEXT,\
         frequency INT,\
	 PRIMARY KEY(word(100)),\
	 FULLTEXT (word)\
	 )"""
    cursor = mydbconn.cursor()
    try:
	cursor.execute(sql)
    except:
	print "sql create", sql
    mydbconn.close()

def update_table(word_tuple):
    mydbconnobj = DBConnection(config.config["host"],config.config["port"],\
                                config.config["user"],config.config["passwd"],config.config["db"])
    mydbconn = mydbconnobj.get_conn()
    
    #print "word_tuple", word_tuple 
    # Create table as per requirement
    sql = "INSERT INTO word_data(\
         word, word_encrypted, frequency)\
	 VALUES ('%s', '%s', '%d') ON DUPLICATE KEY UPDATE frequency = frequency + values(frequency)"  %\
	 (word_tuple[0], word_tuple[1], word_tuple[2])
    #print "sql update", sql
    cursor = mydbconn.cursor()
    try:
	cursor.execute(sql)
    except:
	create_table()
    mydbconn.commit()
    mydbconn.close()

#create_table()
#t = ('mani123', 'mani', 3)
#update_table(t)
