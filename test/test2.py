import sys
sys.path.insert(0, '../')

from main_classes import *
from os import path
from util import *

reglist = []
racelist = []
i = 2

registrationsFromResults(infile = './results/test{0}.csv'.format(i), outfile = './registrations/registrations_test{0}.csv'.format(i), filterSEEOC = True)
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

assert races.clubs.clubs['seeocokazimut'].getClubScore() == 45
assert races.clubs.clubs['seeocokpolaris'].getClubScore() == 66
assert races.clubs.clubs['seeocokkomenda'].getClubScore() == 64
assert races.clubs.clubs['seeocoksg'].getClubScore() == 0

for name,club in races.clubs.clubs.items():
    print(name, club.getClubScore())


#races.saveResults('seeoc_2018.csv')