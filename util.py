from unidecode import unidecode

def despace(niz):
    a=''
    for i in niz:
        if i!=' ':
            a+=i
    return a

def identifier(string):
    return despace(unidecode(string)).lower()

def pointsSOL(place):
    t=[25,20,15,12,10,8,7,6,5,4,3,2,1]
    if place > len(t)-1:
        return 1
    return t[place]