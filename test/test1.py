import sys
sys.path.insert(0, '../')

from main_classes import *
from os import path
from util import *

numberOfRaces = 1


reglist = []
racelist = []
for i in range(1, numberOfRaces + 1):
    if i == 2 or i == 3:
        continue

    registrationsFromResults(infile = './results/test{0}.csv'.format(i), outfile = './registrations/registrations_test{0}.csv'.format(i))
    reglist.append('./registrations/registrations_test{0}.csv'.format(i))
    racelist.append({'resultloc': './results/test{0}.csv'.format(i), 'name': 'test{0}'.format(i)})
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


#races.saveResults('seeoc_2018.csv')