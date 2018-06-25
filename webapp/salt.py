import os
import uuid
import hashlib
from Crypto.PublicKey import RSA
from asymmetric_encryption import encrypt_message

salt_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'webapp', '..'))
key_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'webapp', '..' ))

def hash_word(word):
    # uuid is used to generate a random number
    if not os.path.isfile( salt_path + '/salt.txt'): 
	salt = uuid.uuid4().hex
	with open(salt_path + '/salt.txt', 'a') as f:
	    f.write(salt)
    else:
	print "using existing salt"
	k = open(salt_path + '/salt.txt')
	salt = k.read()
    print "word", word
    word_original = word[0]
    freq = word[1]
    f = open(key_path + '/mykey.pem','r')
    key = RSA.importKey(f.read())
    print "freq", freq    
    word_salted = hashlib.sha256(salt.encode() + word_original.encode()).hexdigest() + ':' + salt
    word_encrypt = encrypt_message(word_original, key)
    final = (word_salted, word_encrypt, freq)
    return final
    
def check_word(hashed_word, user_word):
    word, salt = hashed_word.split(':')
    return word == hashlib.sha256(salt.encode() + user_word.encode()).hexdigest()

#t=("mani", 5)
#k=hash_word(t)
#print k
