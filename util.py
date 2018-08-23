from unidecode import unidecode
import csv
import pandas as pd

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

def sortedResultsByClubs(races):
    results = []
    for name,club in races.clubs.clubs.items():
        results.append({
            'name': name,
            'score': club.getClubScore()
            })
    results.sort(key = lambda x: -x['score'])
    return results

def clubScoresToCSV(races, file):
    f = open(file, 'w', encoding = 'utf-8')
    f.write('club;score\n')

    results = sortedResultsByClubs(races)
    for result in results:
        f.write('{0};{1}'.format(result['name'], result['score']))
        f.write('\n')

    f.close()
    return

def clubScoresToHTML(races, file):
    f = open(file, 'w', encoding = 'utf-8')
    results = sortedResultsByClubs(races)
    
    df = pd.DataFrame(results)

    f.write(df.to_html())
    f.close()
    return

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

        seemocCountriesList = ['BUL', 'CRO', 'CYP', 'GRE', 'ITA', 'MKD', 'MDA', 'BIH', 'ROU', 'SRB', 'SLO', 'TUR', 'BiH']
        seemocCategoriesList = ['W35 SEEMOC', 'M35 SEEMOC', 'W40 SEEMOC', 'M40 SEEMOC', 'W45 SEEMOC', 'M45 SEEMOC', 'W50 SEEMOC', 'M50 SEEMOC', 'W55 SEEMOC', 'M55 SEEMOC', 'W60 SEEMOC', 'M60 SEEMOC', 'W65 SEEMOC', 'M65 SEEMOC', 'W70 SEEMOC', 'M70 SEEMOC', 'MW35 SEEMOC', 'MW45 SEEMOC', 'MW55 SEEMOC']
        seeocCategoriesList = ['W16 SEEOC', 'M16 SEEOC', 'M18 SEEOC', 'W18 SEEOC', 'W20 SEEOC', 'M20 SEEOC', 'W21E SEEOC', 'M21E SEEOC']

        if (filterSEEOC and len(club) > 5 and club[0:4] == 'Team' and category in seeocCategoriesList) or ( filterSEEMOC and len(club) == 3 and club in seemocCountriesList and category in seemocCategoriesList ) or (not filterSEEOC and not filterSEEMOC):
            g.write(';'.join([siteId, name, surname, club, category]))        
            g.write('\n')        

    g.close()
    f.close()



