from sol_class import *
from os import path

races = Races('SOL', raceslist= [{'resultloc': './Rezultati/SOL1.csv', 'name': 'SOL 1'}])
races.scoreRaces()
races.saveResults('sol_2017.csv')