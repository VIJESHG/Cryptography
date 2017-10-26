import sys

additive_inv = {'0000':'0000', '0001':'1111', '0010':'1110', '0011':'1101', '0100':'1100', '0101':'1011', '0110':'1010' , '0111':'1001',
			'1000':'1000', '1001':'0111', '1010':'0110', '1011':'0101', '1100':'0100', '1101':'0011', '1110':'0010', '1111':'0001' }

multiplicative_inv = {'0000':'0000', '0001':'0001', '0010':'1001', '0011':'0110', '0100':'1101', '0101':'0111', '0110':'0011' , '0111':'0101',
			'1000':'1111', '1001':'0010', '1010':'1100', '1011':'1110', '1100':'1010', '1101':'0100', '1110':'1011', '1111':'1000' }
			
def mult_mod17(num1, num2):
	if num1 == 0:
		num1 = 16
	num3 = (num1 * num2) % 17
	if num3 == 16:
		num3 = 0
	return num3

def gen_enc_keys(key):
	key_list = []
	last_round = []
	shift_1 = key[6:] + key[:6]
	shift_2 = shift_1[6:] + shift_1[:6]
	shift_3 = shift_2[6:] + shift_2[:6]
	final_key_set = key + shift_1 + shift_2 + shift_3[:16]
	
	for i in range(4):
		rounds = []
		for j in range(6):
			rounds.append(final_key_set[:4])
			final_key_set = final_key_set[4:]
		key_list.append(rounds)
	
	for k in range(4):
		last_round.append(final_key_set[:4])
		final_key_set = final_key_set[4:]
	
	key_list.append(last_round)
	
	return key_list

def gen_dec_keys(key):
	keys = gen_enc_keys(key)
	print multiplicative_inv[keys[4][0]]
	round_1, round_2, round_3, round_4, round_5 = [], [], [], [], []
	final_decr_keys = []
	round_1.append(multiplicative_inv[keys[4][0]])
	round_1.append(additive_inv[keys[4][1]])
	round_1.append(additive_inv[keys[4][2]])
	round_1.append(multiplicative_inv[keys[4][3]])
	round_1.append(keys[3][4])
	round_1.append(keys[3][5])
	final_decr_keys.append(round_1)
	
	round_2.append(multiplicative_inv[keys[3][0]])
	round_2.append(additive_inv[keys[3][1]])
	round_2.append(additive_inv[keys[3][2]])
	round_2.append(multiplicative_inv[keys[3][3]])
	round_2.append(keys[2][4])
	round_2.append(keys[2][5])
	final_decr_keys.append(round_2)
	
	round_3.append(multiplicative_inv[keys[2][0]])
	round_3.append(additive_inv[keys[2][1]])
	round_3.append(additive_inv[keys[2][2]])
	round_3.append(multiplicative_inv[keys[2][3]])
	round_3.append(keys[1][4])
	round_3.append(keys[1][5])
	final_decr_keys.append(round_3)
	
	round_4.append(multiplicative_inv[keys[1][0]])
	round_4.append(additive_inv[keys[1][1]])
	round_4.append(additive_inv[keys[1][2]])
	round_4.append(multiplicative_inv[keys[1][3]])
	round_4.append(keys[0][4])
	round_4.append(keys[0][5])
	final_decr_keys.append(round_4)
	
	round_5.append(multiplicative_inv[keys[0][0]])
	round_5.append(additive_inv[keys[0][1]])
	round_5.append(additive_inv[keys[0][2]])
	round_5.append(multiplicative_inv[keys[0][3]])
	final_decr_keys.append(round_5)
	
	return final_decr_keys

	
	

def round_operations(s, rounds):
	keys = []
	for i in range(6):
		keys.append(int(rounds[i],2))
	
	block = []
	for i in range(4):
		block.append(int(s[i],2))
	
	a1 = mult_mod17(block[0], keys[0])
	a2 = (block[1] + keys[1]) % 16
	a3 = (block[2] + keys[2]) % 16
	a4 = mult_mod17(block[3], keys[3])
	a5 = a1 ^ a3
	a6 = a2 ^ a4
	a7 = mult_mod17(a5, keys[4])
	a8 = (a6 + a7) % 16
	a9 = mult_mod17(a8, keys[5])
	a10 = (a7 + a9) % 16
	a11 = a1 ^ a9
	a12 = a3 ^ a9
	a13 = a2 ^ a10
	a14 = a4 ^ a10
	
	block[0] = ("{0:04b}".format(a11))
	block[1] = ("{0:04b}".format(a13))
	block[2] = ("{0:04b}".format(a12))
	block[3] = ("{0:04b}".format(a14))
	return block

def half_round(s, last_round):
	keys = []
	for i in range(4):
		keys.append(int(last_round[i],2))
	
	block = []
	for i in range(4):
		block.append(int(s[i],2))
	
	v1 = mult_mod17(block[0], keys[0])
	v2 = (block[1] + keys[1]) % 16
	v3 = (block[2] + keys[2]) % 16
	v4 = mult_mod17(block[3], keys[3])
	
	block[0] = ("{0:04b}".format(v1))
	block[1] = ("{0:04b}".format(v2))
	block[2] = ("{0:04b}".format(v3))
	block[3] = ("{0:04b}".format(v4))
	
	return block

def encrypt(text, keys):
	s1, s2, s3, s4 = text[:4], text[4:8], text[8:12], text[12:16]
	s = [s1] + [s2] + [s3] + [s4]
	for r in range(len(keys)-1):
		s = round_operations(s, keys[r])
	last_round = keys[len(keys)-1]
	ctext = half_round(s, last_round)
	return ctext

def decrypt(ctext,keys):
	s1, s2, s3, s4 = ctext[:4], ctext[4:8], ctext[8:12], ctext[12:16]
	s = [s1] + [s2] + [s3] + [s4]
	
	for i in range(len(keys)-1):
		s = round_operations(s, keys[i])
	last_round = keys[len(keys)-1]
	ptext = half_round(s, last_round)
	return ptext


def main():
	print "Simplified IDEA With Encryption and Decryption:"
	key  = raw_input("Enter the 32 bit key: ")
	plaintext = raw_input("Enter 16 bit plaintext: ")	
	
	enc_keys = gen_enc_keys(key)
	print "Encryption Subkeys:" + str(enc_keys)
	
	Ciphertext = encrypt(plaintext, enc_keys)
	print "Encrypted Plaintext: ", Ciphertext
	
	ctext = ""
	for i in range(len(Ciphertext)):
		ctext = ctext + Ciphertext[i]
	dec_keys = gen_dec_keys(key)
	print "Decryption Subkeys:" + str(dec_keys)
	Plaintext = decrypt(ctext,dec_keys)
	
	print "Decrypted Ciphertext: ", Plaintext
	
	
if __name__ == '__main__':
	main()
