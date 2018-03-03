import numpy
import operator
import sys

teamsdict = {}
teamsdictreverse = {}
resultsdict = {}

teamssetwins = {}
teamssetlosses = {}
teamsmatchwins = {}
teamsmatchlosses = {}

def print_results(b):
  teamnumber = 0
  for i in b:
    resultsdict[teamsdictreverse[teamnumber]] = i
    teamnumber += 1
  sortedresultsdict = sorted(resultsdict.items(), key=operator.itemgetter(1), reverse = True)
  place = 1
  for sortedresult in sortedresultsdict:
    teamname = sortedresult[0]
    value = sortedresult[1]
    setwins = str(teamssetwins[teamname])
    setlosses = str(teamssetlosses[teamname])
    matchwins = str(teamsmatchwins[teamname])
    matchlosses = str(teamsmatchlosses[teamname])

    placestring = str(place)
    placestring = "{:3}".format(placestring)
    teamname = "{:30}".format(teamname)
    valuestring = str(value)
    valuestring = "{:30}".format(valuestring)
    setwins = "{:3}".format(setwins)
    setlosses = "{:3}".format(setlosses)
    matchwins = "{:3}".format(matchwins)
    matchlosses = "{:3}".format(matchlosses)

    print(placestring, teamname, valuestring, "Set", setwins, ":", setlosses, "Match", matchwins, ":", matchlosses)
    place += 1

def power_iteration(A, numsimulations):
  #b_k = numpy.random.rand(A.shape[0])
  b_k = numpy.ones(A.shape[0])
  #b_k = numpy.linalg.norm(b_k)

  for _ in range(numsimulations):
    b_k1 = numpy.dot(A, b_k)

    b_k1_norm = numpy.linalg.norm(b_k1)

    b_k = b_k1 / b_k1_norm

  return b_k

def power_iteration2(A):
  eig = numpy.linalg.eig(A)
  eigenvalues = eig[0]
  eigenvectors = eig[1]
  largesteigenvalue = 0
  largesteigenvalueindex = 0
  index = 0
  for eigenvalue in eigenvalues:
    if (abs(eigenvalue) > largesteigenvalue):
      largesteigenvalue = eigenvalue
      largesteigenvalueindex = index
    index += 1
  print(largesteigenvalue)
  print(eigenvectors[largesteigenvalueindex])

def normalize_matrix(teamsmatrix):
  teamsmatrix /= numpy.sum(teamsmatrix, axis=0)
  return teamsmatrix

def add_match_score(dictionary, teamname, value):
  if (teamname in dictionary):
    dictionary[teamname] += value
  else:
    dictionary[teamname] = value

def add_match_data(teamsmatrix, data):
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
  numgames = team1score + team2score

  teamsmatrix[team1number, team2number] = team1score  * 1.0/ numgames
  teamsmatrix[team2number, team1number] = team2score * 1.0 / numgames
  
  add_match_score(teamsmatchwins, team1, team1score)
  add_match_score(teamsmatchwins, team2, team2score)
  add_match_score(teamsmatchlosses, team1, team2score)
  add_match_score(teamsmatchlosses, team2, team1score)

  add_match_score(teamssetwins, team1, int(team1score > team2score))
  add_match_score(teamssetlosses, team1, int(team2score > team1score))
  add_match_score(teamssetwins, team2, int(team2score > team1score))
  add_match_score(teamssetlosses, team2, int(team1score > team2score))
  

# Opens the match file that is specified, and adds the data to the teamsmatrix
def initialize_match(teamsmatrix, matchnumber):
  matchstring = str(matchnumber).zfill(2)
  matchfilename = "Rounds/Round" + matchstring
  with open (matchfilename, "r") as matchesfile:
    matches = matchesfile.readlines()
    matchnumber = 0
    for match in matches:
      match = match.rstrip()
      data = match.split(":")
      add_match_data(teamsmatrix, data)

# Initializes each match that is specified
def initialize_matches(teamsmatrix, startindex, endindex):
  for i in range(startindex, endindex + 1):
    initialize_match(teamsmatrix, i)

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
    return teamnumber
 
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
  teamnumber = initialize_teams_dict()
  teamsmatrix = numpy.eye(teamnumber)

  # Creates the Teams and Matches Matrix
  initialize_matches(teamsmatrix, startindex, endindex)

  # Calculates Eigenvectors
  teamsmatrix = normalize_matrix(teamsmatrix)
  b = power_iteration(teamsmatrix, 10000)
  print_results(b)
  #power_iteration2(teamsmatrix)

main()
