# Python program to print prime factors
# This code is contributed by Harshit Agrawal, made to work with Python 3.x by Stephanos Zunez
import math
import sys
def primeFactors(n) :                          # A function to print all prime factors of a given number n
    while n % 2 == 0 :                         # Print the number of two's that divide n
        #print(n)
        n = n / 2
    for i in range(3,int(math.sqrt(n))+1,2) : # n must be odd at this point, so a skip of 2 ( i = i + 2) can be used
        while n % i == 0:                      # while i divides n , print i ad divide n
            print(int(i))
            n = n / i         
    if n > 2 :                                # Condition if n is a prime number greater than 2
        print(int(n))
n = int(sys.argv[1])                          # this allows for a commandline argument to used as n
primeFactors(n)