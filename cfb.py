from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
import sys
import argparse

# Create an instance of the argument parser
parser=argparse.ArgumentParser(description="Argument parser")

# Define the valid arguments
parser.add_argument("-key", type=str)		# The key
parser.add_argument("-encdec", type=int)	# Whether to encrypt or decrypt (0 = encrypt; 1 = decrypt)
parser.add_argument("-iv", type=str)		# The initialization vector
parser.add_argument("-infile", type=str)	# The name of the input file
parser.add_argument("-outfile", type=str)	# The name of the output file
parser.add_argument("-blocksize", type=int)	# The size of the block (in bits!)

# Parse the arguments
args = parser.parse_args()

# Grab the arguments
key = args.key.encode()	# The encryption key converted to bytes
encdec = args.encdec		# Whether to encrypt 
iv = args.iv.encode()		# The IV in bytes
blockSize = args.blocksize	# The size of the block
outFileName = args.outfile	# The name of the output file

# Open the input file
with open(args.infile, "rb") as inFile:

	# TODO create an instance of the AES in CFB mode class
	cipher = AES.new(key,AES.MODE_CFB,iv,segment_size=128)

	# TODO: Implement the encryption logic
	if encdec == 0:
		read_data = inFile.read(blockSize)
		while read_data:
			encryptedData = cipher.encrypt(read_data)
			with open(args.outfile, "ab") as outFile:
				outFile.write(encryptedData)
			outFile.close()
			read_data = inFile.read(blockSize)
		inFile.close()
    	
	# TODO: Implement the decryption logic
	elif encdec == 1:
    		read_data = inFile.read(blockSize)
	    	while read_data:
    			decryptedData = cipher.decrypt(read_data)
    			with open(args.outfile, "ab") as outFile:
    				outFile.write(decryptedData)
    			outFile.close()
    			read_data = inFile.read(blockSize)
	    	inFile.close()

#sample input for encryption: python3 cfb.py -key 1234567890abcdef -iv 534567890abcdeds -blocksize 16 -infile webcomic.jpg -outfile webcomic.enc -encdec 0
#sample input for decryption: python3 cfb.py -key 1234567890abcdef -iv 534567890abcdeds -blocksize 16 -infile webcomic.enc -outfile decrypted_webcomic.jpg -encdec 1
