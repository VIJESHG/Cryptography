from AES256 import *
import argparse
from argparse import RawTextHelpFormatter


parser = argparse.ArgumentParser(description='AES 256-bit Encrypt and Decrypt', formatter_class = RawTextHelpFormatter)
parser.add_argument('mode',help="encrypt or decrypt")
args = parser.parse_args()

mode = str(args.mode).lower()

def getDecryptBlock(block):
	file = open(block, 'r')
	byte = file.read()
	blockarray = []
	block = []
	for i in range(0,len(byte),2):
		blockarray.append(int(byte[i:i+2],16))

	for i in range(0,len(blockarray),16):
		block.append(blockarray[i:i+16])
	return block

def getEncryptBlock(block):
	file = open(block,'rb')
	byte = file.read().encode("hex")				#plaintext in the form of bytes 
	blockarray = []
	arr = []
	for i in range(0,len(byte),2):
		arr.append(int(byte[i:i+2], 16))
	
	while len(arr) >= 16:
		blockarray.append(arr[0:16])
		arr = arr[16:]
		if len(arr) < 16:
			temparray = [0]*16
			for k in range(0,len(arr)):
				temparray[k] = arr[k]
			blockarray.append(temparray)				#plaintext in block of 16
	return blockarray

def getKey(filename):
	len_key = 64
	keyfile = open(filename, 'r')
	hexadecimalkey = keyfile.read()
	keyarray = []
	for i in range(0, len_key, 2):
		keyarray.append(int(hexadecimalkey[i:i+2], 16))
	return keyarray

def fileEncrypt():
	block = getEncryptBlock("testBlock")
	#print len(block)
	key = getKey("testKey")
	outfile = open("encrypted_file","wb")
	strangen = ""
	cryptLargeblock = []
	for i in range(len(block)):
		cryptLargeblock.append(encrypt(block[i],key))

	while i < len(cryptLargeblock):
		for row in cryptLargeblock:
			for item in row:
				strangen += hex(item)[2:].zfill(2)
		i += 1
	outfile.write(strangen)
	outfile.close()
	#print len(cryptLargeblock)

def fileDecrypt():
	key = getKey("testKey")
	file = open("decrypted_file","wb")
	decryptBlock = []
	decString = ""
	eblock = getDecryptBlock("encrypted_file")
	#print len(eblock)

	for i in range(len(eblock)):
		decryptBlock.append(decrypt(eblock[i],key))

	for row in decryptBlock:
		for item in row:
			decString += chr(item)

	file.write(decString)
	file.close()

if mode == "encrypt" or mode == "e":
	fileEncrypt()
elif mode == "decrypt" or mode == "d":
	fileDecrypt()
