from unidecode import unidecode
import csv

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
    place = place - 1
    if place > len(t)-1:
        return 1
    return t[place]

def pointsSEEOC(place):
    t = [45,39,34,30,27,25,24,23,22,21,20,19,18,17,16,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1]
    place = place - 1
    if place > len(t)-1:
        return 0
    return t[place]

def pointsSEEOCRelay(place):
    t = [90,78,68,60,54,50,48,46,44,42,40,38,36,34,0]
    place = place - 1
    if place > len(t)-1:
        return 0
    return t[place]

def sortSOL(dict):
    ## todo expand
    return sorted(dict.values(), key = lambda x: (x.category, -x.sumscore))


def registrationsFromResults(infile, outfile, clubType = 'club', filterSEEOC = False, filterSEEMOC = False):
    f = open(infile, 'r', encoding = 'utf-8')
    g = open(outfile, 'w', encoding = 'utf-8')
    reader = csv.reader(f, delimiter = ';', quotechar = '"')

    header = next(reader)
    while len(header) < 6:
        header = next(reader)

    nameI = header.index('First name')
    surnameI = header.index('Surname')

    clubI = header.index('Cl.name')
    cityI = header.index('City')
    countryI = header.index('Nat')

    catI = header.index('Short')

    for row in reader:
        name = row[nameI]
        surname = row[surnameI]
        category = row[catI]
        siteId = '-1'

        if clubType == 'club':
            club = row[clubI]
            if not club:
                club = row[cityI]
        elif clubType == 'country':
            club = row[countryI]
        else:
            raise ValueError('Provided clubType not supported: ' + clubType)
        if not club:
            print('No country/club, even though it is needed for scoring: ' + name + ' ' + surname + ' ' + infile )

        seemocCountriesList = ['BUL', 'CRO', 'CYP', 'GRE', 'ITA', 'MAC', 'MOL', 'MNT', 'ROM', 'SRB', 'SLO', 'TUR'] # todo limit seemoc categories
        seemocCategoriesList = ['W35', 'M35', 'W40', 'M40', 'W45', 'M45', 'W50', 'M50', 'W55', 'M55', 'W60', 'M60', 'W65', 'M65', 'W70', 'M70', 'MW35', 'MW45', 'MW55']
        seeocCategoriesList = ['W16', 'M16', 'M18', 'W18', 'W20', 'M20', 'W21E', 'M21E']

        if (filterSEEOC and len(club) > 5 and club[0:5] == 'SEEOC' and category in seeocCategoriesList) or ( filterSEEMOC and len(club) == 3 and club in seemocCountriesList and category in seemocCategoriesList ) or (not filterSEEOC and not filterSEEMOC):
            g.write(';'.join([siteId, name, surname, club, category]))        
            g.write('\n')        

    g.close()
    f.close()



