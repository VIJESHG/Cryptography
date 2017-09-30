# 15629177698EF862D42F77E8F862B7F8E87706CB8EC72F5A62C75A6215CBCB0DC7F8B762447706CB8E2FA9779DCB4C06   test string for brute force

import itertools
IP = [2, 6, 3, 1, 4, 8, 5, 7]    #permutation table for IP
EP = [4, 1, 2, 3, 2, 3, 4, 1]		#permutation table for E/P
IP_INVERSE = [4, 1, 3, 5, 7, 2, 8, 6]	#permutation table for inverse IP
P10 = [3, 5, 2, 7, 4, 10, 1, 9, 8, 6]  #P10 permutation
P8 = [6, 3, 7, 4, 8, 5, 10, 9]		#P8 permutation
P4 = [2, 4, 3, 1]						#P4 permutation

S0 = [[1, 0, 3, 2],
      [3, 2, 1, 0],
      [0, 2, 1, 3],
      [3, 1, 3, 2]]				#S0 box

S1 = [[0, 1, 2, 3],
      [2, 0, 1, 3],
      [3, 0, 1, 0],
      [2, 1, 0, 3]]				#S1 box



def permutate(original, fixed_key):
    new = ''
    for i in fixed_key:
        new += original[i - 1]
    return new


#splitting key into left part and right part
def left_part(bits):  	
    return bits[:len(bits)/2]


def right_part(bits):
    return bits[len(bits)/2:]


def shift(bits):
    rotated_left_part = left_part(bits)[1:] + left_part(bits)[0]
    rotated_right_part = right_part(bits)[1:] + right_part(bits)[0]
    return rotated_left_part + rotated_right_part


def key1(KEY):								#subkey K1 generation
    return permutate(shift(permutate(KEY, P10)), P8)


def key2(KEY):								#subkey K2 generation
    return permutate(shift(shift(shift(permutate(KEY, P10)))), P8)


def xor(bits, key):
    new = ''
    for bit, key_bit in zip(bits, key):
        new += str(((int(bit) + int(key_bit)) % 2))
    return new


def lookup_in_sbox(bits, sbox):
    row = int(bits[0] + bits[3], 2)
    col = int(bits[1] + bits[2], 2)
    return '{0:02b}'.format(sbox[row][col])


def f_k(bits, key):					#Fk function implementation
    L = left_part(bits)
    R = right_part(bits)
    bits = permutate(R, EP)
    bits = xor(bits, key)
    bits = lookup_in_sbox(left_part(bits), S0) + lookup_in_sbox(right_part(bits), S1)
    bits = permutate(bits, P4)
    return xor(bits, L)


def encrypt(plain_text,KEY):
    bits = permutate(plain_text, IP)
    temp = f_k(bits, key1(KEY))
    bits = right_part(bits) + temp
    bits = f_k(bits, key2(KEY))
    return permutate(bits + temp, IP_INVERSE)


def decrypt(cipher_text,KEY):
    bits = permutate(cipher_text, IP)
    temp = f_k(bits, key2(KEY))
    bits = right_part(bits) + temp
    bits = f_k(bits, key1(KEY))
    return chr(int(permutate(bits + temp, IP_INVERSE),2))

def case1(KEY):
	#KEY = '1010000010'
	st = raw_input("Enter the encryption string:")
	st1 = ' '.join(format(ord(x), '08b') for x in st)
	st2 = st1.split(' ')
	cipher = ''
	for each in st2:
		cipher = cipher + encrypt(each,KEY)
	print cipher
	
def case2(KEY):
	#KEY = '1010000010'
	print KEY
	st = raw_input("Enter the decryption string:")
	st1 = [st[i:i+8] for i in range(0,len(st), 8)]
	cipher = ''
	for each in st1:
		print decrypt(each,KEY)
	#print cipher
	
def case3(KEY):
	#st = raw_input("Enter the encryption string:")
	st = "15629177698EF862D42F77E8F862B7F8E87706CB8EC72F5A62C75A6215CBCB0DC7F8B762447706CB8E2FA9779DCB4C06"
	l = len(st)*4;
	st1 = "{0:8b}".format(int(st,16))
	st1 = st1.zfill(l)
	st2 = [st1[i:i+8] for i in range(0,len(st1), 8)]
	plain = ''
	for each in st2:
		plain = plain + decrypt(each,KEY)
	return plain

if __name__ == "__main__":
	print "Choose one of the following options:"
	print " 1: Case1() for encryption."
	print " 2: Case2() for decryption."
	print " 3: Case3() for brute-force decryption."
	
	option = input("Enter the option:")
	if(option == 1):
		KEY = raw_input("Enter the Encryption key:")
		case1(KEY)
	
	elif(option == 2):
		KEY = raw_input("Enter the Decryption key:");
		case2(KEY)
	
	elif(option == 3):
		KEY_SET =  ["".join(seq) for seq in itertools.product("01", repeat = 10)]
		for i in KEY_SET:
				print "Key:" + i		
				print "plaintext:"
				print case3(str(i))
				print "\n"	
	else:
		print "Invalid option..!!!"

