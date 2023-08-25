lows=['mi','bi','tri','quadri','quinti','sexti','septi','octi','noni']
prefs=['','un','duo','tre','quattuor','quin','ses','septen','octo','noven']
ordsx=['deci','viginti','triginti','quadraginti','quinquaginti','sexaginti','septuaginti','octoginti','nonaginti','centi',]
ordsc=['','decicenti',\
    'viginticenti',\
    'trigintacenti',\
    'quadra­gintacent­i',\
    'quinqua­gintacent­i',\
    'sexagintacenti',\
    'septuagintacenti',\
    'octogintacenti',\
    'nonagintacenti',\
    'ducenti',\
    'trecenti',\
    'quadringenti',\
    'quingenti',\
    'sescenti',\
    'septingenti',\
    'octingenti',\
    'nongenti',\
    'millini']
n=int(input('enter the number of ordenals to output [1-19]: '))
for x in range(9) :
    print(str(lows[x])+'llion')
for k in range(n) :
    for j in range(len(ordsx)) :
        for i in range(len(prefs)) :
            print(str(prefs[i])+str(ordsx[j])+str(ordsc[k])+'llion')