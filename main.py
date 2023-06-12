import random

# For each 'skill' a team has (1-10) they will get that many chances to score, this chance indicates the liklihood of them scoring on that chance
scoringChance = 0.2
teams = []
groups = []

# Base class for any team that contains any value we use for this team
class Team:
    def __init__(self, name, shortname, skill):
        self.name = name
        self.shortname = shortname
        self.skill = skill

# Contains base functions for any match that takes place
class Match:
    # T1 is the home team, T2 the away team, T1 Goals stores how many goals T1 stored, T2 Goals self explanatory, result is U (unplayed), W, D or L depending on result
    def __init__(self, t1, t2):
        self.t1 = t1
        self.t2 = t2
        self.t1goals = 0
        self.t2goals = 0
        self.result = "U"

    # Simulates the match using our skill variable and outputs result that fits with parameters
    def simMatch(self):
        for x in range(self.t1.skill):
            doesScore = random.random()
            if doesScore < scoringChance:
                self.t1goals += 1
        
        for x in range(self.t2.skill):
            doesScore = random.random()
            if doesScore < scoringChance:
                self.t2goals += 1

        if self.t1goals > self.t2goals:
            self.result = "W"
        elif self.t1goals == self.t2goals:
            self.result = "D"
        else:
            self.result = "L"

class TwoLegMatch(Match):
    def __init__(self, t1, t2):
        super().__init__(t1, t2)
        self.gamesPlayed = 0

    def simMatch(self):
        for x in range(self.t1.skill):
            doesScore = random.random()
            if doesScore < scoringChance:
                self.t1goals += 1
        
        for x in range(self.t2.skill):
            doesScore = random.random()
            if doesScore < scoringChance:
                self.t2goals += 1

class KnockoutRoundHalf:
    pass

# Group class contains functions to simulate one group for the UCL
class Group:
    # Teams is a list of all teams in the group, table is a dictionary of the points table, fixtures is a 2D array of each week's fixtures, and weeksSimmed keeps track of how many
    # weeks have been played
    def __init__(self, t1, t2, t3, t4):
        self.teams = [t1, t2, t3, t4]
        self.table = {t1.shortname : {"mp" : 0, "w" : 0, "d" : 0, "l" : 0, "gf" : 0, "ga" : 0, "gd" : 0, "points" : 0}, t2.shortname : {"mp" : 0, "w" : 0, "d" : 0, "l" : 0, "gf" : 0, "ga" : 0, "gd" : 0, "points" : 0}, t3.shortname : {"mp" : 0, "w" : 0, "d" : 0, "l" : 0, "gf" : 0, "ga" : 0, "gd" : 0, "points" : 0}, t4.shortname : {"mp" : 0, "w" : 0, "d" : 0, "l" : 0, "gf" : 0, "ga" : 0, "gd" : 0, "points" : 0}}
        self.fixtures = [[], [], [], [], [], []]
        self.weeksSimmed = 0

    # Insertion sort based on points, no GD implementation yet
    def sortTable(self):
        sortedPoints = []
        sortedTeams = []
        sortedGD = []

        for team in self.teams:
            sortedPoints.append(self.table[team.shortname]["points"])
            sortedTeams.append(team)
            sortedGD.append(self.table[team.shortname]["gd"])

        for team in range(1, 4):
            tempPoints = sortedPoints[team]
            tempTeam = sortedTeams[team]
            tempGD = sortedGD[team]
            counter = team

            while counter > 0 and tempGD > sortedGD[counter - 1]:
                sortedPoints[counter] = sortedPoints[counter - 1]
                sortedTeams[counter] = sortedTeams[counter - 1]
                sortedGD[counter] = sortedGD[counter - 1]
                counter = counter - 1

            sortedPoints[counter] = tempPoints
            sortedTeams[counter] = tempTeam
            sortedGD[counter] = tempGD

        for team in range(1, 4):
            tempPoints = sortedPoints[team]
            tempTeam = sortedTeams[team]
            tempGD = sortedGD[team]
            counter = team

            while counter > 0 and tempPoints > sortedPoints[counter - 1]:
                sortedPoints[counter] = sortedPoints[counter - 1]
                sortedTeams[counter] = sortedTeams[counter - 1]
                sortedGD[counter] = sortedGD[counter - 1]
                counter = counter - 1

            sortedPoints[counter] = tempPoints
            sortedTeams[counter] = tempTeam
            sortedGD[counter] = tempGD

        self.teams = sortedTeams

    # "Randomly" generates order of play for the group
    def generateFixtures(self):
        hasPlayed = []
        for x in range (0, 3):
            opponent = random.randint(1, 3)
            while opponent in hasPlayed:
                opponent = random.randint(1, 3)

            hasPlayed.append(opponent)
            match1 = Match(self.teams[0], self.teams[opponent])
            match3 = Match(self.teams[opponent], self.teams[0])

            if opponent == 1:
                match2 = Match(self.teams[2], self.teams[3])
                match4 = Match(self.teams[3], self.teams[2])
            elif opponent == 2:
                match2 = Match(self.teams[1], self.teams[3])
                match4 = Match(self.teams[3], self.teams[1])
            else:
                match2 = Match(self.teams[1], self.teams[2])
                match4 = Match(self.teams[2], self.teams[1])

            self.fixtures[x].append(match1)
            self.fixtures[x].append(match2)
            self.fixtures[x + 3].append(match3)
            self.fixtures[x + 3].append(match4)

    # Debug function, prints fixtures to console
    def printFixtures(self):
        for week in range(6):
            print("-------------------")
            print(f"Week {week + 1}")
            print("-------------------")
            for game in range(2):
                print(f"{self.fixtures[week][game].t1.name} vs. {self.fixtures[week][game].t2.name}")

    # Neatly prints the points table
    def printTable(self):
        print("{:<22} | {:<8} | {:<8} | {:<8} | {:<8} | {:<8} | {:<8} | {:<8} | {:<8}".format("Club", "MP", "W", "D", "L", "GF", "GA", "GD", "Pts"))
        for team in self.teams:
            v = self.table[team.shortname]
            print("{:<22} | {:<8} | {:<8} | {:<8} | {:<8} | {:<8} | {:<8} | {:<8} | {:<8}".format(team.name, v["mp"], v["w"], v["d"], v["l"], v["gf"], v["ga"], v["gd"], v["points"]))
        print("------------------------------------------------------------------------------------------------------------------------------------------------------")

    # Simulates one week of the group stage's fixtures
    def simWeek(self):
        if self.weeksSimmed >= 6:
            print("Group stage has already been fully simmed.")
        else:
            for game in range(2):
                matchRunning = self.fixtures[self.weeksSimmed][game]
                matchRunning.simMatch()
                self.table[matchRunning.t1.shortname]["mp"] += 1
                self.table[matchRunning.t1.shortname]["gf"] += matchRunning.t1goals
                self.table[matchRunning.t1.shortname]["ga"] += matchRunning.t2goals
                self.table[matchRunning.t1.shortname]["gd"] += matchRunning.t1goals - matchRunning.t2goals

                self.table[matchRunning.t2.shortname]["mp"] += 1
                self.table[matchRunning.t2.shortname]["gf"] += matchRunning.t2goals
                self.table[matchRunning.t2.shortname]["ga"] += matchRunning.t1goals
                self.table[matchRunning.t2.shortname]["gd"] += matchRunning.t2goals - matchRunning.t1goals

                if matchRunning.result == "W":
                    self.table[matchRunning.t1.shortname]["w"] += 1
                    self.table[matchRunning.t1.shortname]["points"] += 3
                    self.table[matchRunning.t2.shortname]["l"] += 1
                elif matchRunning.result == "D":
                    self.table[matchRunning.t1.shortname]["d"] += 1
                    self.table[matchRunning.t1.shortname]["points"] += 1
                    self.table[matchRunning.t2.shortname]["d"] += 1
                    self.table[matchRunning.t2.shortname]["points"] += 1
                else:
                    self.table[matchRunning.t1.shortname]["l"] += 1
                    self.table[matchRunning.t2.shortname]["w"] += 1
                    self.table[matchRunning.t2.shortname]["points"] += 3
            
            self.weeksSimmed += 1

# Initialise teams from a file
def teamsFromFile(file):
    try:
        with open(file) as teamFile:
            nextTeam = teamFile.readline().strip()
            while nextTeam != "":
                nextTeamShortName = teamFile.readline().strip()
                nextTeamSkill = teamFile.readline().strip()
                teams.append(Team(nextTeam, nextTeamShortName, int(nextTeamSkill)))
                nextTeam = teamFile.readline().strip()
    except OSError:
        print("File not found.")
    except Exception as e:
        print(f"Unknown error occurred - {e}.")

def generateGroups():
    for team in teams:
        print(team.shortname)

    random.shuffle(teams)
    for x in range(0, 32, 4):
        print(x)
        group = Group(teams[x], teams[x + 1], teams[x + 2], teams[x + 3])
        groups.append(group)

def simulateGroupWeek():
    print("------------------------------------------------------------------------------------------------------------------------------------------------------")
    print("NEW WEEK")
    print("------------------------------------------------------------------------------------------------------------------------------------------------------")
    for group in groups:
        group.generateFixtures()
        group.simWeek()
        group.sortTable()
        group.printTable()

teamsFromFile("teams.txt")
generateGroups()
simulateGroupWeek()
simulateGroupWeek()
simulateGroupWeek()
simulateGroupWeek()
simulateGroupWeek()
simulateGroupWeek()

# Create group of teams consisting of two pots - the top from each group, and the second from each group
# Randomly pit those teams against each other, pot one vs pot two, no matches from the same group ideally
# Create path to final from there, so each opponent is decided beforehand...?