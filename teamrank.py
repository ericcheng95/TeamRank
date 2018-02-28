import numpy
import operator
import sys

teamsdict = {}
teamsdictreverse = {}
teamsmatrix = None
resultsdict = {}

def print_results(b):
  teamnumber = 0
  for i in b:
    resultsdict[teamsdictreverse[teamnumber]] = i
    teamnumber += 1
  sortedresultsdict = sorted(resultsdict.items(), key=operator.itemgetter(1), reverse = True)
  place = 1
  for sortedresult in sortedresultsdict:
    print(place, sortedresult)
    place += 1

def power_iteration(A, numsimulations):
  b_k = numpy.random.rand(A.shape[0])

  for _ in range(numsimulations):
    b_k1 = numpy.dot(A, b_k)

    b_k1_norm = numpy.linalg.norm(b_k1)

    b_k = b_k1 / b_k1_norm

  return b_k

def add_match_data(data):
  team1 = data[0]
  team2 = data[1]

  if (team1 == "BYE" or team2 == "BYE"):
    return

  if (team1 not in teamsdict):
    print("Invalid Team Name 1:", team1)
    return
  if (team2 not in teamsdict):
    print("Invalid Team Name 2:", team2)
    return

  team1number = teamsdict[team1]
  team2number = teamsdict[team2]
  team1score = int(data[2])
  team2score = int(data[3])

  global teamsmatrix
  teamsmatrix[team1number, team2number] += team1score
  teamsmatrix[team2number, team2number] += team2score

# Opens the match file that is specified, and adds the data to the teamsmatrix
def initialize_match(matchnumber):
  matchstring = str(matchnumber).zfill(2)
  matchfilename = "Rounds/Round" + matchstring
  with open (matchfilename, "r") as matchesfile:
    matches = matchesfile.readlines()
    matchnumber = 0
    for match in matches:
      match = match.rstrip()
      data = match.split(":")
      add_match_data(data)

# Initializes each match that is specified
def initialize_matches(startindex, endindex):
  for i in range(startindex, endindex + 1):
    initialize_match(i)

# Opens Teams file and initiates the dict and matrix
def initialize_teams_dict():
  with open ("Teams/Teams", "r") as teamsfile:
    teams = teamsfile.readlines()
    teamnumber = 0
    for team in teams:
      team = team.rstrip()
      teamsdict[team] = teamnumber
      teamsdictreverse[teamnumber] = team
      teamnumber = teamnumber + 1
    global teamsmatrix
    teamsmatrix = numpy.zeros((teamnumber, teamnumber))

# Calls the Functions
def main():
  # Converts arguments to ints (breaks if invalid)
  startindex = int(sys.argv[1])
  endindex = int(sys.argv[2])
  # Insures Start Index is less than End Index
  if (startindex > endindex):
    print("StartIndex cannot be greater than EndIndex")
    return

  # Creates the Teams Dict from the Teams file
  initialize_teams_dict()
  # Creates the Teams and Matches Matrix
  initialize_matches(startindex, endindex)

  # Calculates Eigenvectors
  global teamsmatrix
  b = power_iteration(teamsmatrix, 1)
  print_results(b)

main()
