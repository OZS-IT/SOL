from main_classes import *
from os import path

numberOfRaces = 8


reglist = []
racelist = []
for i in range(1, numberOfRaces + 1):
    reglist.append('./registrations/registrations{0}.csv'.format(i))
    racelist.append({'resultloc': './results/seeoc{0}.csv'.format(i), 'name': 'seeoc{0}'.format(i)})

registrations = Registrations(reglist=reglist)

races = Races('seeoc',
              raceslist= racelist,
              runners = registrations.runners,
              clubs = registrations.clubs,
              categories= registrations.categories)
races.scoreRaces()
races.saveResults('seeoc_2018.csv')