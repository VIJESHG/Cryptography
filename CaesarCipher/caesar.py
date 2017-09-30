import string
def encrypt(str1, k, l):
    for i in str1:
        if ord(i) in range(97, 123):
            l.append(((ord(i) -97 + k) % 26) + 97)
        if ord(i) in range(65, 91):
            l.append(((ord(i) -65 + k) % 26) + 65)

def decrypt(str1, k, l):
    k = -k;
    for i in str1:
        if ord(i) in range(97, 123):
            l.append(((ord(i) -97 + k) % 26) + 97)
        if ord(i) in range(65, 91):
            l.append(((ord(i) -65 + k) % 26) + 65)

def convertintostring(l):
    res = []
    for i in range(0, len(l)):
        if(i != 0 and i % 5 == 0):
            res.append(' ')
        if(i != 0 and i % 50 == 0):
            res.append('\n')
        res.append(l[i])
    return ''.join(res)

file1 = open("testfile.txt", "r") 
file2 = open("encoded.txt", "w") 
file3 = open("decoded.txt", "w") 
str1 = file1.read()

k = input("Enter value of k\n")
print str1
#Remove punctuation marks
for i in string.punctuation:
    str1 = str1.replace(i, "")
#Remove digits
for i in string.digits:
    str1 = str1.replace(i, "")
#Remove whitespaces
for i in string.whitespace:
    str1 = str1.replace(i, "")

#encryption
l2 = []
encrypt(str1, k, l2)

#convert in ASCII
l3 = [chr(i) for i in l2]

#print in specific format
str4 = convertintostring(l3)
print('\n')
print "ENCRYPTED TEXT"
print str4
file2.write(str4)
for i in string.whitespace:
    str4 = str4.replace(i, "")

#decryption
l4 = []
decrypt(str4, k, l4)

l5 = [chr(i) for i in l4]

str5 = convertintostring(l5)
print('\n')
print "DECRYPTED TEXT"
print str5
file3.write(str5)

