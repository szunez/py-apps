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

number = input('Please enter a number: ')
getNth(number)
print(number+nth)