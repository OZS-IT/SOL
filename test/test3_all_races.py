import sys
sys.path.insert(0, '../')

from main_classes import *
from os import path
from util import *

reglist = []
racelist = []

numberOfRaces = 3

for i in range(1, numberOfRaces + 1):
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

assert races.clubs.clubs['seeocokazimut'].getClubScore() == 45 + 45 + 79
assert races.clubs.clubs['seeocokpolaris'].getClubScore() == 39 + 66 + 138
assert races.clubs.clubs['seeocokkomenda'].getClubScore() == 64 + 64 + 133
assert races.clubs.clubs['seeocoksg'].getClubScore() == 0

for name,club in races.clubs.clubs.items():
    print(name, club.getClubScore())


#races.saveResults('seeoc_2018.csv')