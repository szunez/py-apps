import numpy as np
def intToNum(i) :
    global number
    if i == '0' :
        number = 'zero'
    elif i == '1' :
        number = 'one'
    elif i == '2' :
        number = 'two'
    elif i == '3' :
        number = 'three'
    elif i == '4' :
        number = 'four'
    elif i == '5' :
        number = 'five'
    elif i == '6' :
        number = 'six'
    elif i == '7' :
        number = 'seven'
    elif i == '8' :
        number = 'eight'
    elif i == '9' :
        number = 'nine'
    else :
        number = '.'

n = input('How many decimal places of pi would you like to see? (0-15): ')
strOut = str(np.pi)[0:2+int(n):]
print('\n'+strOut+'\n')
q0 = input('Would you like to see the digits of pi in words? (yes/no): ')
if q0[0] == 'y' or q0[0] == 'Y':
    arrPi = list(strOut)
    print('\n')
    for i in arrPi :
        intToNum(i)
        print(number)
    print('\n')