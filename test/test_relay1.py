import sys
sys.path.insert(0, '../')

from main_classes import *
from os import path
from util import *

reglist = []
racelist = []
i = 1

registrationsFromResults(infile = './results/test_relay{0}.csv'.format(i), outfile = './registrations/registrations_test_relay{0}.csv'.format(i))
reglist.append('./registrations/registrations_test_relay{0}.csv'.format(i))
racelist.append({'resultloc': './results/test_relay{0}.csv'.format(i), 'name': 'test_relay{0}'.format(i)})
if i == 1:
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

assert races.clubs.clubs['okazimut'].getClubScore() == 158
assert races.clubs.clubs['okpolaris'].getClubScore() == 168
assert races.clubs.clubs['okkomenda'].getClubScore() == 146
assert races.clubs.clubs['oksg'].getClubScore() == 0

for name,club in races.clubs.clubs.items():
    print(name, club.getClubScore())


#races.saveResults('seeoc_2018.csv')