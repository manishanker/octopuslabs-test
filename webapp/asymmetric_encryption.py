import os
from Crypto import Random
from Crypto.PublicKey import RSA
import base64

key_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'webapp', '..' ))

def generate_keys():
	# RSA modulus length must be a multiple of 256 and >= 1024
	modulus_length = 256*4 # use larger value in production
	privatekey = RSA.generate(modulus_length, Random.new().read)
	publickey = privatekey.publickey()
	print "key_path", key_path
	if not os.path.isfile( key_path + '/mykey.pem'):
	    print "no pem file, creating"
	    f = open(key_path + '/mykey.pem', 'w')
	    f.write(privatekey.exportKey('PEM'))
	    f.close()

def encrypt_message(a_message , publickey):
	encrypted_msg = publickey.encrypt(a_message, 32)[0]
	encoded_encrypted_msg = base64.b64encode(encrypted_msg) # base64 encoded strings are database friendly
	return encoded_encrypted_msg

def decrypt_message(encoded_encrypted_msg, privatekey):
	decoded_encrypted_msg = base64.b64decode(encoded_encrypted_msg)
	decoded_decrypted_msg = privatekey.decrypt(decoded_encrypted_msg)
	return decoded_decrypted_msg
