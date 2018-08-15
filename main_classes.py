from util import *
from re import sub
import csv


## Categories

class Category:
    def __init__(self, kat):
        self.category = self.parseCat(kat)
    def __eq__(self, other):
        assert isinstance(other, Category)
        return self.category == other.category
    def __lt__(self, other):
        assert isinstance(other, Category)
        return self.category <= other.category
    def __repr__(self):
        return str(self.category)

    @staticmethod
    def parseCat(kat):
        kat = identifier(kat)
        kat = sub(r'[hm]', 'M', kat)
        kat = sub(r'[wdz]', 'Ž', kat)
        return kat

class Categories:
    def __init__(self, catlist = []):
        self.categories = dict()
        for cat in catlist:
            self.add(Category(cat))

    def __repr__(self):
        return str(self.categories)

    def add(self, cat):
        if isinstance(cat, Category):
            self.categories[cat.category] = cat
        else:
            raise ValueError("The added cat is not an instance of Category!")

    def getCat(self, catname, add = False):
        if not self.categories.get(Category.parseCat(catname)) and add:
            self.add(Category(catname))
        return self.categories.get(Category.parseCat(catname))


## Clubs

class Club:
    def __init__(self, name):
        self.name = identifier(name)
        self.realname = name
        self.scores = []
    def __eq__(self, other):
        return self.name == other.name
    def __repr__(self):
        return str(self.realname)

    @staticmethod
    def parseClub(club):
        club = identifier(club)
        return club

    def addScore(self, score):
        self.scores.append(score)

    def getClubScore(self):
        return sum([score['points'] for score in self.scores])

class Clubs:
    def __init__(self, clublist = []):
        self.clubs = dict()
        for club in clublist:
            self.add(Club(club))
    def add(self, club):
        if isinstance(club, Club):
            self.clubs[club.name] = club
        else:
            raise ValueError("The added club is not an instance of Club!")
    def getClub(self, clubname, add = False):
        if not self.clubs.get(Club.parseClub(clubname)) and add:
            self.add(Club(clubname))
        return self.clubs.get(Club.parseClub(clubname))


## Runners

class Runner:
    def __init__(self, name, surname, club, category):
        self.name = name
        self.surname = surname
        self.title = self.parseRunner(name+surname)
        self.club = club
        self.category = category
        self.results = []
        self.scores = []
        self.lastscore = None
        self.sumscore = 0
        self.avgscore = 0
        self.registered_at = dict()

    def __repr__(self):
        return "[{0} {1}, {2}, {3}]".format(self.surname, self.name, self.club, self.category)

    def addResult(self, result):
        self.results.append(result)

    def addScore(self, score):
        self.scores.append(score)
        self.club.addScore(score)
        self.lastscore = score

    def computeScore(self, noCountingRaces):
        if not self.scores:
            return
        scores = [score['points'] for score in self.scores]
        scores.sort(key = lambda x: -x)
        n = min(len(scores), noCountingRaces)
        self.sumscore = sum(scores[:n])
        self.avgscore = round(self.sumscore / n)

    def addRegistration(self, id):
        self.registered_at[id] = True # todo test if this changes object

    @staticmethod
    def parseRunner(fullname):
        return identifier(fullname)

class Runners:
    def __init__(self, runnerlist = []):
        self.runners = dict()
        self.__newRunnerId = 0
        for runner in runnerlist:
            self.addRunner(Runner(runner.name, runner.surname, runner.club, runner.category))

    def __repr__(self):
        return str(self.runners)

    def addRunner(self, runner):
        if isinstance(runner, Runner):
            runner.id = self.getNewId()
            self.runners[runner.id] = runner
        else:
            raise ValueError("The added runner is not an instance of Runner!")
    def getNewId(self):
        self.__newRunnerId += 1
        return self.__newRunnerId
    def getRunner(self, runnerdata, add = False):
        myrunner = None
        ## check if any existing runners match. if no create a new one.
        ## todo when registration numbers are used in competitions use them here instead for
        ## fast searching
        for _, runner in self.runners.items():
            if (runner.title == Runner.parseRunner(runnerdata['name']+runnerdata['surname']) and
                        runner.club == runnerdata['club']):
                if myrunner:
                    raise ValueError("Found multiple instances for runner {0}!".format(runner.title))
                myrunner = runner
        if not myrunner and add:
            myrunner = Runner(runnerdata['name'], runnerdata['surname'], runnerdata['club'], runnerdata['category'])
            self.addRunner(myrunner)
        return myrunner


class Registration:
    def __init__(self, fileloc):
        self.fileloc = fileloc
        self.id = 1

    def getDataFromRegistration(self, runners, clubs, categories):
        f = open(self.fileloc, 'r', encoding='utf-8')
        reader = csv.reader(f, delimiter=';', quotechar='"')
        for row in reader:
            if not row:
                continue
            if row[0][0] == '\ufeff':
                row[0] = row[0][1:]
            siteId = row[0]
            name = row[1]
            surname = row[2]
            club = row[3]
            category = row[4]

            runnerclub = clubs.getClub(club, add = True)
            runnercategory = categories.getCat(category, add = True)
            runner = runners.getRunner({
                'name': name,
                'surname': surname,
                'club': runnerclub,
                'category': runnercategory
            })
            if not runner:
                runner = Runner(name, surname, runnerclub, runnercategory)
                runner.siteId = siteId
                runners.addRunner(runner)
            runner.addRegistration(self.id)
        f.close()

class Registrations:
    def __init__(self, reglist = [], runners = Runners(), categories = Categories(), clubs = Clubs()):
        self.registrations = []
        self.__newRegId = 0
        self.runners = runners
        self.categories = categories
        self.clubs = clubs
        for reg in reglist:
            newreg = Registration(reg)
            self.addReg(newreg)
            newreg.getDataFromRegistration(self.runners, self.clubs, self.categories)


    def addReg(self, reg):
        if isinstance(reg, Registration):
            reg.id = self.getNewId()
            self.registrations.append(reg)
        else:
            raise ValueError("The added reg is not an instance of Registration!")

    def getNewId(self):
        self.__newRegId += 1
        return self.__newRegId

    def getDataFromRegistrations(self):
        for reg in self.registrations:
            reg.getDataFromRegistration(self.runners, self.clubs, self.categories)



## Races

class Race:
    def __init__(self, name, runners, clubs, categories, resultloc, joinedkats = [], racenum = 0, maxScoredRunners = float('inf'), scoreFunction = lambda x: -x, clubType='club'):
        self.name = name
        self.runners = runners
        self.clubs = clubs
        self.categories = categories
        self.altkats = dict()
        self.__racenum = racenum
        self.maxScoredRunners = maxScoredRunners
        self.scoreFunction = scoreFunction
        self.clubType = clubType
        for lis in joinedkats:
            for kat in lis:
                self.altkats[kat] = lis
        self.clubCounterByCategory = dict()
        for category in categories.categories.keys():
            self.clubCounterByCategory[category] = dict()
        self.results = self.parseRace(resultloc)

    def parseRace(self, resultloc):
        results = []

        f = open(resultloc, 'r', encoding = 'utf-8')
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
        classifierI = header.index('Classifier')
        timeI = header.index('Time')

        for row in reader:
            if self.clubType == 'club':
                club = row[clubI]
                if not club:
                    club = row[cityI]
                if not club:
                    club = 'ind.'
            elif self.clubType == 'country':
                club = row[countryI]
            else:
                raise ValueError('Provided clubType not supported: ' + self.clubType)
            club = self.clubs.getClub(club)
            if not club:
                if self.clubType == 'country':
                    print('No club')
                continue

            category = row[catI]
            category1 = self.categories.getCat(category)

            runner = self.runners.getRunner({
                'name': row[nameI],
                'surname': row[surnameI],
                'club': club,
                'category': category1
            }) ## category is used only to create a new runner, not to check for equality
            if not runner:
                continue ## runner not registered

            if runner.category.category in self.altkats.get(category, []):
                category = runner.category
            else:
                category = category1
            if not category:
                continue ## category not existant and not merged with existing category

            time = row[timeI]
            classifiers = {"mp": 3, "dns": 1, "dnf": 2, "disq": 4}

            classifier = int(row[classifierI])
            if classifiers.get(time.lower()):
                classifier = classifiers[time.lower()]

            if not time or classifier != 0:
                time = 0 ## todo make custom class for time and differentiate 0 from None
            else:
                time1 = time.split(':')[::-1]
                time = 0
                for i in range(len(time1)):
                    time +=  int(time1[i]) * (60**i)
                if not classifier:
                    classifier = 0

            if not time:
                time = float('inf')
            results.append({
                'runner': runner,
                'category': category,
                'classifier': classifier,
                'time': time,
                'club': club
            })
            runner.addResult({
                'name': self.name,
                'racenum': self.__racenum,
                'time': time,
                'category': category,
            })
        f.close()
        return results

    def scoreResults(self):
        ## todo create a subclass, that includes this function and leave the instance clean
        self.results.sort(key=lambda x: (x['category'], x['time']))
        prevCat = Category('')
        place = 1
        for result in self.results:
            runner = result['runner']
            if prevCat != result['category']:
                prevCat = result['category']
                place = 1
            else:
                place += 1
            if result['category'] != runner.category:
                runner.addScore({
                    'racenum': self.__racenum,
                    'place': '',
                    'points': 0,
                    'show': '*',
                    'time': result['time']
                })
                place -= 1 ## this person does not count for scores
            elif not runner.registered_at.get(self.__racenum, False):
                place -= 1 ## not counting for scores
                continue
            elif self.clubCounterByCategory[result['category'].category].get(result['club'].name, 0) >= self.maxScoredRunners:
                place -= 1 ## club already scored the maximum number of runners
                continue
            elif result['classifier'] == 0:
                points = self.scoreFunction(place)
                runner.addScore({
                    'racenum': self.__racenum,
                    'place': str(place),
                    'points': points,
                    'show': str(points),
                    'time': result['time']
                })
            else:
                runner.addScore({
                    'racenum': self.__racenum,
                    'place': '',
                    'points': 0,
                    'show': '-',
                    'time': result['time']
                })
            self.clubCounterByCategory[result['category'].category][result['club'].name] = self.clubCounterByCategory[result['category'].category].get(result['club'].name, 0) + 1
            runner.computeScore(noCountingRaces = (self.__racenum // 2) + 1)

class Races:
    def __init__(self, name, runners = Runners(), clubs = Clubs(), categories = Categories(), raceslist = [], maxScoredRunners = float('inf'), scoreFunction = lambda x: -x, clubType = 'club', scoreFunctionRelay = lambda x: -x, maxScoredTeamsRelay = float('inf')):
        self.races = []
        self.name = name
        self.runners = runners
        self.clubs = clubs
        self.categories = categories
        self.maxScoredRunners = maxScoredRunners
        self.maxScoredTeamsRelay = maxScoredTeamsRelay
        self.scoreFunction = scoreFunction
        self.scoreFunctionRelay = scoreFunctionRelay
        self.clubType = clubType
        self.__racenum = 0
        for race in raceslist:
            self.addRace(race)
        # self.scoreRaces()

    def getNewRaceNum(self):
        self.__racenum += 1
        return self.__racenum

    def addRace(self, race):
        if not race.get('joinedkats'):
            race['joinedkats'] = []

        if race.get('type') == 'relay':
            scoreFunc = self.scoreFunctionRelay
            maxScoredRunners = self.maxScoredTeamsRelay
        else:
            scoreFunc = self.scoreFunction
            maxScoredRunners = self.maxScoredRunners
        self.races.append(Race(race['name'],
                               self.runners,
                               self.clubs,
                               self.categories,
                               race['resultloc'],
                               race['joinedkats'],
                               self.getNewRaceNum(),
                               maxScoredRunners = maxScoredRunners,
                               scoreFunction = scoreFunc,
                               clubType = self.clubType))

    def scoreRaces(self):
        for race in self.races:
            race.scoreResults()

    def saveResults(self, outfile):
        f = open(outfile, 'w', encoding = 'utf-8')

        racenames = [race.name for race in self.races]
        header = "Surname;First name;City;Class;Time;Pl;Points;" + ';'.join(racenames) + ";Sum;Average;ID\n";
        f.write(header)

        for runner in sortSOL(self.runners.runners):
            last = runner.lastscore
            if not last:
                last = {
                    'place': '',
                    'show': '',
                    'time': ''
                }
                time = ''
            else:
                time = last['time']
                timeH = time // 3600
                time = (time % 3600)
                timeM = time // 60
                timeS = time % 60
                time = "{0}:{1}:{2}".format(timeH, timeM, timeS)

            line = [runner.surname, runner.name, str(runner.club), str(runner.category), time, last['place'], last['show']]

            prevRaceNum = 0
            raceNum = 0
            for score in runner.scores:
                raceNum = score['racenum']
                line += [''] * (raceNum - prevRaceNum) ## add missing races
                prevRaceNum = raceNum + 1
                line.append(score['show'])

            line += [''] * (self.__racenum - raceNum) ## add remaining races to the end
            line.append(str(runner.sumscore))
            line.append(str(runner.avgscore))
            siteId = ''
            if hasattr(runner, 'siteId'):
                siteId = runner.siteId
            line.append(siteId)
            line = ';'.join(line)

            f.write(line)
            f.write('\n')
        f.close()