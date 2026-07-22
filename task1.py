# task 1 phase `1`
# kol country 3ndha `played, won, drawn, lost, goals for, goals against, goals diff, points`

teams = ["KSA","POL", "MEX", "ARG"]
standings = {}
for team in teams:
    standings[team]= {"P":0, "W":0, "D":0, "L":0, "GF":0, "GA":0,"GD":0 ,"Pts":0}


# function to update the dictionary
# GD = GF - GA
def process_match(standings, team1, team2,team1_goals, team2_goals):
    standings[team1]["P"]+=1
    standings[team2]["P"]+=1

    standings[team1]["GF"] +=  team1_goals
    standings[team2]["GA"] +=  team1_goals
    
    standings[team2]["GF"] +=  team2_goals
    standings[team1]["GA"] +=  team2_goals

    if team1_goals == team2_goals:
        standings[team1]["D"]+=1
        standings[team2]["D"]+=1
    elif team1_goals > team2_goals:
        standings[team1]["W"]+=1
        standings[team2]["L"]+=1
    else:
        standings[team1]["L"]+=1
        standings[team2]["W"]+=1

    # Update goal difference
    standings[team1]["GD"] = standings[team1]["GF"] - standings[team1]["GA"]
    standings[team2]["GD"] = standings[team2]["GF"] - standings[team2]["GA"]

    # Update points
    standings[team1]["Pts"] = standings[team1]["W"] * 3 + standings[team1]["D"]
    standings[team2]["Pts"] = standings[team2]["W"] * 3 + standings[team2]["D"]


# a function to sort the standings based on points, goal difference, and goals for , formating in a table
def sort_standings(standings):
    return sorted(standings.items(), key=lambda x: (x[1]["Pts"], x[1]["GD"], x[1]["GF"]), reverse=True)

def display_standings(standings):
    print(f"{'Team':<5} {'P':<3} {'W':<3} {'D':<3} {'L':<3} {'GF':<4} {'GA':<4} {'GD':<4} {'Pts':<4}")
    sorted_teams = sort_standings(standings)
    print("-" * 40)
    for team, stats in sorted_teams:
        gd_display = f"{stats['GD']:+}"  # Display GD with a sign
        if stats['GD'] == 0:
            gd_display = "0"  # Display GD as 0 without a sign if it's zero 
        print(f"{team:<5} {stats['P']:<3} {stats['W']:<3} {stats['D']:<3} {stats['L']:<3} {stats['GF']:<4} {stats['GA']:<4} {gd_display:<4} {stats['Pts']:<4}")
   

matchups = [("ARG", "MEX"), ("ARG", "POL"), ("ARG", "KSA"),
            ("MEX", "POL"), ("MEX", "KSA"), ("POL", "KSA")]


for team1, team2 in matchups:
  # bouns : add input validation to ensure the user enters a valid score in the format "X-Y" where X and Y are integers
  while True:
      try:
          score = input(f"Enter score for {team1} vs {team2} (format: 2-0): ")
          team1_goals, team2_goals = map(int, score.split("-"))
          process_match(standings, team1, team2, team1_goals, team2_goals)
          break
      except ValueError:
          print("Invalid input format. Please enter the score in the format 'X-Y' where X and Y are integers.")
          continue

display_standings(standings)
