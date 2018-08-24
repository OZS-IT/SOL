from main_classes import *
from os import path
from util import *

numberOfRaces = 4


reglist = []
racelist = []
for i in range(1, numberOfRaces + 1):
    if i == 3 or i == 4:
        continue

    registrationsFromResults(infile = './results/seeoc{0}.csv'.format(i), outfile = './registrations/registrations{0}.csv'.format(i), filterSEEOC = True)
    reglist.append('./registrations/registrations{0}.csv'.format(i))
    racelist.append({'resultloc': './results/seeoc{0}.csv'.format(i), 'name': 'seeoc{0}'.format(i)})
    if i == 4:
        racelist[-1]['type'] = 'relay'

registrations = Registrations(reglist=reglist)

races = Races('seeoc',
              raceslist= racelist,
              runners = registrations.runners,
              clubs = registrations.clubs,
              categories= registrations.categories,
              maxScoredRunners=2,
              maxScoredTeamsRelay=1,
              scoreFunction=pointsSEEOC,
              scoreFunctionRelay=pointsSEEOCRelay)

races.scoreRaces()

for name,club in races.clubs.clubs.items():
    print(name, club.getClubScore())

clubScoresToCSV(races, file = 'seeoc_2018.csv')
clubScoresToHTML(races, file = 'seeoc_2018.html')

#races.saveResults('seeoc_2018.csv')