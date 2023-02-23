from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes

import sys
import argparse

# Create an instance of the argument parser
parser=argparse.ArgumentParser(description="Argument parser")

# Define the valid arguments
parser.add_argument("-key", type=str)		# The key
parser.add_argument("-encdec", type=int)	# Whether to encrypt or decrypt (0 = encrypt; 1 = decrypt)
parser.add_argument("-noncefile", type=str)	# The name of the nonce file
parser.add_argument("-tagfile", type=str)	# The name of the TAG file
parser.add_argument("-infile", type=str)	# The name of the input file
parser.add_argument("-outfile", type=str)	# The name of the output file

# Parse the arguments
args = parser.parse_args()

# Grab the arguments
key = args.key.encode()	# The encryption key converted to bytes
encdec = args.encdec		# Whether to encrypt 
noncefile = args.noncefile	# The name of the nonce file
tagfile = args.tagfile		# The name of the tag file
outFileName = args.outfile	# The name of the output file


nfile = open(noncefile, "rb")
INnonce = nfile.read()
nfile.close()

# Open the input file
with open(args.infile, "rb") as inFile:

	# TODO create an instance of the AES in GCM mode class
	cipher = AES.new(key,AES.MODE_GCM,nonce=INnonce)

	# TODO: Implement the encryption logic
	if encdec == 0:
		read_data = inFile.read()
		inFile.close()
		encryptedData, tag = cipher.encrypt_and_digest(read_data)
		with open(args.outfile, "wb") as outFile:
			outFile.write(encryptedData)
		outFile.close()
		tfile = open(tagfile, "wb")
		tfile.write(tag);
		tfile.close()
    	
	# TODO: Implement the decryption logic
	elif encdec == 1:
		read_data = inFile.read()
		inFile.close()
		decryptedData = cipher.decrypt(read_data)
		with open(args.outfile, "wb") as outFile:
			outFile.write(decryptedData)
		outFile.close()
		tfile = open(tagfile, "rb")
		tag = tfile.read()
		tfile.close()
		try:
			cipher.verify(tag)
			print("The plaintext is authentic")
		except:
			print("Wrong key or the integrity was compromised")
			
#sample input for encryption: python3 gcm.py -key 1234567890abcdef -noncefile gcmnonce.txt -tagfile gcmtag.txt -infile webcomic.jpg -outfile webcomic.enc -encdec 0
#sample input for decryption: python3 gcm.py -key 1234567890abcdef -noncefile gcmnonce.txt -tagfile gcmtag.txt -infile webcomic.enc -outfile decrypted_webcomic.jpg -encdec 1
