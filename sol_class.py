from util import *
from re import sub
from copy import deepcopy
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

    def getCat(self, catname):
        if not self.categories.get(Category.parseCat(catname)):
            self.add(Category(catname))
        return self.categories.get(Category.parseCat(catname))


## Clubs

class Club:
    def __init__(self, name):
        self.name = identifier(name)
        self.realname = name
    def __eq__(self, other):
        return self.name == other.name
    def __repr__(self):
        return str(self.realname)

    @staticmethod
    def parseClub(club):
        club = identifier(club)
        return club

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
    def getClub(self, clubname):
        if not self.clubs.get(Club.parseClub(clubname)):
            self.add(Club(clubname))
        return self.clubs[Club.parseClub(clubname)]


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

    def __repr__(self):
        return "[{0} {1}, {2}, {3}]".format(self.surname, self.name, self.club, self.category)

    def addResult(self, result):
        self.results.append(result)

    def addScore(self, score):
        self.scores.append(score)
        self.lastscore = score

    def computeScore(self, noCountingRaces):
        if not self.scores:
            return
        scores = [score['points'] for score in self.scores]
        scores.sort(key = lambda x: -x)
        n = min(len(scores), noCountingRaces)
        self.sumscore = sum(scores[:n])
        self.avgscore = round(self.sumscore / n)

    @staticmethod
    def parseRunner(fullname):
        return identifier(fullname)

class Runners:
    def __init__(self, runnerlist = []):
        self.runners = dict()
        self.__newRunnerId = 0
        for runner in runnerlist:
            self.add(Runner(runner.name, runner.surname, runner.club, runner.category))

    def __repr__(self):
        return str(self.runners)

    def add(self, runner):
        if isinstance(runner, Runner):
            runner.id = self.getNewId()
            self.runners[runner.id] = runner
        else:
            raise ValueError("The added runner is not an instance of Runner!")
    def getNewId(self):
        self.__newRunnerId += 1
        return self.__newRunnerId
    def getRunner(self, runnerdata):
        myrunner = None
        ## check if any existing runners match. if no create a new one.
        ## todo when registration numbers are used in competitions use them here instead for
        ## fast searching
        for _, runner in self.runners.items():
            if (runner.title == Runner.parseRunner(runnerdata['name']+runnerdata['surname']) and
                        runner.club == runnerdata.club):
                if myrunner:
                    raise ValueError("Found multiple instances for runner {0}!".format(runner.title))
                myrunner = runner
        ## For non registration based events todo remove for sol
        if not myrunner:
            myrunner = Runner(runnerdata['name'], runnerdata['surname'], runnerdata['club'], Category(runnerdata['category']))
            self.add(myrunner)
        return myrunner


## Races

class Race:
    def __init__(self, name, runners, clubs, categories, resultloc, joinedkats = [], racenum = 0):
        self.name = name
        self.runners = runners
        self.clubs = clubs
        self.categories = categories
        self.altkats = dict()
        self.__racenum = racenum
        for lis in joinedkats:
            for kat in lis:
                self.altkats[kat] = lis
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
        catI = header.index('Short')
        classifierI = header.index('Classifier')
        timeI = header.index('Time')

        for row in reader:
            club = row[clubI]
            if not club:
                club = row[cityI]
            if not club:
                club = 'ind.'
            club = self.clubs.getClub(club)

            category = row[catI]

            runner = self.runners.getRunner({
                'name': row[nameI],
                'surname': row[surnameI],
                'club': club,
                'category': category
            }) ## category is used only to create a new runner, not to check for equality
            if not runner:
                continue ## runner not registered

            if runner.category in self.altkats.get(category, []):
                category = runner.category

            category = self.categories.getCat(category)

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
                    time +=  int(time1[i]) * (60^i)
                if not classifier:
                    classifier = 0

            results.append({
                'runner': runner,
                'category': category,
                'classifier': classifier,
                'time': time
            })
            runner.addResult({
                'name': self.name,
                'racenum': self.__racenum,
                'time': time,
                'category': category
            })
        f.close()
        return results

    def scoreResults(self):
        ## todo create a subclass, that includes this function and leave the instance clean
        self.results.sort(key=lambda x: (x['category'], -x['time']))
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
            elif result['classifier'] == 0:
                points = pointsSOL(place)
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
            runner.computeScore(noCountingRaces = (self.__racenum // 2) + 1)

class Races:
    def __init__(self, name, runners = Runners(), clubs = Clubs(), categories = Categories(), raceslist = []):
        self.races = []
        self.name = name
        self.runners = runners
        self.clubs = clubs
        self.categories = categories
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
        self.races.append(Race(race['name'],
                               self.runners,
                               self.clubs,
                               self.categories,
                               race['resultloc'],
                               race['joinedkats'],
                               self.getNewRaceNum()))

    def scoreRaces(self):
        for race in self.races:
            race.scoreResults()

    def saveResults(self, outfile):
        f = open(outfile, 'w', encoding = 'utf-8')

        racenames = [race.name for race in self.races]
        header = "Surname;First name;City;Class;Time;Pl;Points;" + ';'.join(racenames) + ";Sum;Average\n";
        f.write(header)

        for _, runner in self.runners.runners.items():
            last = runner.lastscore
            if not last:
                last = {
                    'place': '',
                    'show': '',
                    'time': ''
                }

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
            line = ';'.join(line)

            f.write(line)
            f.write('\n')
        f.close()