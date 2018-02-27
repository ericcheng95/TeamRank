import numpy

teamsdict = {}

def initialize_teams_dict():
  with open ("Teams/Teams", "r") as teamsfile:
    teams = teamsfile.readlines()
    teamnumber = 0
    for team in teams:
      teamsdict[team.rstrip()] = teamnumber
      teamnumber = teamnumber + 1

def main():
  initialize_teams_dict()

main()
