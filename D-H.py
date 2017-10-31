from random import randint
sharedPrimeValue = 23    									# p value
sharedBaseValue = 5      									# g value
								
alicePrivateKey = randint(1,100)								#Alice's Private Key
bobPrivateKey = randint(1,100)									#Bob's Private Key


print "Publicly Shared Variables:"
print "p value: " , sharedPrimeValue 
print "g value: " , sharedBaseValue 

print "\nPrivate Keys:"
print "AlicePrivateKey: ",alicePrivateKey
print "BobPrivateKey  : ",bobPrivateKey

A = (sharedBaseValue ** alicePrivateKey) % sharedPrimeValue     # Alice Sends Bob A = g^a mod p
print	"\nValue send by Alice to Bob through public channel: " , int(A) 
 
B = (sharedBaseValue ** bobPrivateKey) % sharedPrimeValue		# Bob Sends Alice B = g^b mod p
print	"\nValue send by Bob to Alice through public channel: ", int(B)
 
print "\nPrivately Calculated Keys After Exchange:" 
aliceKeyAfterExg = (B ** alicePrivateKey) % sharedPrimeValue	# Alice Computes Shared Secret: s = B^a mod p
print "Alice Shared Secret: ", int(aliceKeyAfterExg) 
 
bobKeyAfterExg = (A ** bobPrivateKey) % sharedPrimeValue			# Bob Computes Shared Secret: s = A^b mod p
print "Bob Shared Secret  : ", int(bobKeyAfterExg) 
