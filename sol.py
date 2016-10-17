from sol_class import *
from os import path

registrations = Registrations(reglist=['./Registracije/registracije1.csv'])

races = Races('SOL',
              raceslist= [{'resultloc': './Rezultati/SOL1.csv', 'name': 'SOL 1'}],
              runners = registrations.runners,
              clubs = registrations.clubs,
              categories= registrations.categories)
races.scoreRaces()
races.saveResults('sol_2017.csv')