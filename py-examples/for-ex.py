def getNth(i) :
    global nth
    strIntr = str(i)
    intIntr = int(i)
    if  strIntr == '1' :
        nth = 'st'
    elif  strIntr == '2' :
        nth = 'nd'
    elif  strIntr == '3' :
        nth = 'rd'
    elif strIntr[len(strIntr)-1] == '1' and intIntr >= 21 :
        nth = 'st'
    elif strIntr[len(strIntr)-1] == '2' and intIntr >= 22 :
        nth = 'nd'
    elif strIntr[len(strIntr)-1] == '3' and intIntr >= 23 :
        nth = 'rd'
    else :
        nth = 'th'

def runFor (n) :
    print('--------------------------------------------------------------------------------')
    for i in range(n) :
        getNth(i)
        print(str(i)+nth+' of '+str(n))
        i = i + 1
    getNth(i)
    print(str(i)+nth+' of '+str(n))
    print('\n'+str(n)+' interations completed\nGoodbye!\n--------------------------------------------------------------------------------')

print('--------------------------------------------------------------------------------')
runFor(int(input('Enter the number of interations: ')))