from sol_class import *
from os import path

numberOfRaces = 8


reglist = []
racelist = []
for i in range(1, numberOfRaces + 1):
    reglist.append('./Registracije/registracije{0}.csv'.format(i))
    racelist.append({'resultloc': './Rezultati/SOL{0}.csv'.format(i), 'name': 'SOL {0}'.format(i)})

registrations = Registrations(reglist=reglist)

races = Races('SOL',
              raceslist= racelist,
              runners = registrations.runners,
              clubs = registrations.clubs,
              categories= registrations.categories)
races.scoreRaces()
races.saveResults('sol_2017.csv')