import random

# Class representing a player in the game with "incidents"
class Player:
    def __init__(self, name, base_attack, base_defense, position, incidents = 0 ,stamina = 100.0 ):
        self.name = name
        self.base_attack = base_attack
        self.base_defense = base_defense
        self.incidents = incidents
        self.stamina = stamina
        self.position = position

    def __str__(self):
        return f"Player: {self.name}, Attack: {self.base_attack}, Defense: {self.base_defense}, Stamina: {self.stamina}, Position: {self.position}"
    
    # Deducts the designated rate from the stamina attribute... Stamina floor is capped firmly at 10.0."
    # Stamina(t) = Max(10.0, Stamina(t-1) - Base_Decay)
    def deplete_stamina(self, base_decay):
        self.stamina = max(10.0, self.stamina - base_decay)

    # Calculates the effective attack value based on the player's base attack and current stamina.
    # Effective_Attack = Base_Attack * (Stamina / 100.0)
    def get_effective_attack(self):
        return self.base_attack * (self.stamina / 100.0)
    
    def get_effective_defense(self):
        return self.base_defense * (self.stamina / 100.0)

    # bouns: b add function to add incidents to the player, w check if el incidents > 3, w if yes, el player ytl3 mn el match
    def is_eligible(self):
        return self.incidents <= 3
    
    def add_incident(self):
        self.incidents += 1
    

# Class representing a team in the game
class Team:
    def __init__(self, country_name, roster,active_lineup,substitutions_remaining = 5 ):
        self.country_name = country_name
        self.roster = roster
        self.active_lineup = active_lineup
        self.substitutions_remaining = substitutions_remaining  # Track the number of substitutions made

    @property
    def bench(self):
        return [player for player in self.roster if player not in self.active_lineup]

    def get_aggregate_attack(self):
        forward_and_midfielders = [player for player in self.active_lineup if player.position in ["FORWARD", "MIDFIELDER"]]
        return sum(player.get_effective_attack() for player in forward_and_midfielders) / len(forward_and_midfielders) if forward_and_midfielders else 0.0

    def get_aggregate_defense(self):
        defenders_and_goalkeepers = [player for player in self.active_lineup if player.position in ["DEFENDER", "GOALKEEPER"]]
        return sum(player.get_effective_defense() for player in defenders_and_goalkeepers) / len(defenders_and_goalkeepers) if defenders_and_goalkeepers else 0.0

   # el substitution function htb2a responsible 3n el substitution of players, w check if el player elly et5tar mn el bench w el player elly et5tar mn el active lineup, w check if el substitutions_remaining > 0
    def execute_substitution(self, player_out, player_in):
        if self.substitutions_remaining > 0:
            if player_out in self.active_lineup and player_in in self.bench:
                self.active_lineup.remove(player_out)
                self.active_lineup.append(player_in)
                self.substitutions_remaining -= 1
                print(f"Substitution made: {player_out.name} out, {player_in.name} in.")
            else:
                print("Invalid substitution. Check if the players are in the correct lineup/bench.")
        else:
            print("No substitutions remaining.")

    def remove_disciplined_player(self, player):
        if player in self.active_lineup:
            self.active_lineup.remove(player)
            print(f"{player.name} has been removed from the active lineup due to disciplinary action.")
        else:
            print(f"{player.name} is not in the active lineup.")
   
    # bouns: b add function to enforce discipline on the team, w check if el player is eligible, w if not, el player ytl3 mn el match
    def enforce_discipline(self):
        for player in self.active_lineup[:]:  # Iterate over a copy of the list to avoid modification issues
            if not player.is_eligible():
                self.remove_disciplined_player(player)

    def swipe_players_from_the_bench(self):
        lowest_stamina_player = min(self.active_lineup, key=lambda p: p.stamina)
        candidates = [p for p in self.bench if p.position == lowest_stamina_player.position]
        if candidates:
            highest_rating_bench_player = max(candidates, key=lambda p: p.get_effective_attack() if p.position in ["FORWARD", "MIDFIELDER"] else p.get_effective_defense())
            if highest_rating_bench_player.stamina > lowest_stamina_player.stamina:
                self.execute_substitution(lowest_stamina_player, highest_rating_bench_player)
                print(f"Substituted {lowest_stamina_player.name} with {highest_rating_bench_player.name} from the bench due to higher stamina.")


    def __str__(self):
        return f"Team: {self.country_name}, Players: {[str(player) for player in self.roster]}"
    

# Class representing an event in the match
class MatchEvent:
    def __init__(self, event_id, event_type, minute, team, outcome_text, player = None):
        self.event_id = event_id
        self.event_type = event_type
        self.minute = minute
        self.team = team
        self.player = player
        self.outcome_text = outcome_text

    def to_string(self):
        player_info = f", Player: {self.player.name}" if self.player else ""
        return f"Event ID: {self.event_id}, Type: {self.event_type}, Minute: {self.minute}, Team: {self.team.country_name}{player_info}, Outcome: {self.outcome_text}"
    
# class el match elly htb2a responsible 3n el match itself, el home team w el away team, el score, el minute, el timeline of events, w el phase of the match (REGULATION, FINISHED)
class Match:
    def __init__(self, home_team, away_team, home_score = 0, away_score = 0, current_minute = 0, timeline = None, phase = "REGULATION"):
        self.home_team = home_team
        self.away_team = away_team
        self.home_score = home_score
        self.away_score = away_score
        self.current_minute = current_minute
        self.timeline = timeline if timeline is not None else []
        self.phase = phase

# Runs a tick for the current minute of the match
    def run_minute_tick(self):
        self.current_minute += 1
        for player in self.home_team.active_lineup + self.away_team.active_lineup:
            player.deplete_stamina(base_decay=0.5)
            if random.random() < 0.01:  # 1% chance of adding an incident
                player.add_incident()
                print(f"Minute {self.current_minute}: Incident added to {player.name} of {self.home_team.country_name if player in self.home_team.active_lineup else self.away_team.country_name}. Total incidents: {player.incidents}")
        self.process_goal_attempt(self.home_team, self.away_team)
        self.process_goal_attempt(self.away_team, self.home_team)
        self.home_team.enforce_discipline()
        self.away_team.enforce_discipline()
        self.home_team.swipe_players_from_the_bench()
        self.away_team.swipe_players_from_the_bench()
        print(f"Minute {self.current_minute}: Match is ongoing.")


# attempt frequency: random.random() < 0.10
# Goal scored if: (Aggregate_Attack * Random(0.75, 1.25)) > (Aggregate_Defense * 1.3 * Random(0.80, 1.20))
    def process_goal_attempt(self, attacking_team, defending_team):
        if random.random() < 0.10:  # 10% chance of a goal attempt
            attack_strength = attacking_team.get_aggregate_attack() * random.uniform(0.85, 1.15) * random.uniform(0.75, 1.25) # bouns: n maltiply tany 3shan n3ml el random swing
            defense_strength = defending_team.get_aggregate_defense() * 1.3 * random.uniform(0.80, 1.20)
            if attack_strength > defense_strength:
                if attacking_team == self.home_team:
                    self.home_score += 1
                else:
                    self.away_score += 1
                event = MatchEvent(event_id=len(self.timeline)+1, event_type="GOAL", minute=self.current_minute, team=attacking_team, outcome_text="Goal scored!")
                self.timeline.append(event)
                print(f"Minute {self.current_minute}: Goal scored by {attacking_team.country_name}!")
       
    def run_penalty_shootout(self):
        self.phase = "PENALTIES"
        home_penalties = 0
        away_penalties = 0
        for i in range(5):
            if random.random() < 0.75:  # 75% chance of scoring a penalty
                home_penalties += 1
                event = MatchEvent(event_id=len(self.timeline)+1, event_type="PENALTY", minute=self.current_minute, team=self.home_team, outcome_text="Penalty scored!")
                self.timeline.append(event)
            else:
                event = MatchEvent(event_id=len(self.timeline)+1, event_type="PENALTY", minute=self.current_minute, team=self.home_team, outcome_text="Penalty missed!")
                self.timeline.append(event)

            if random.random() < 0.75:  # 75% chance of scoring a penalty
                away_penalties += 1
                event = MatchEvent(event_id=len(self.timeline)+1, event_type="PENALTY", minute=self.current_minute, team=self.away_team, outcome_text="Penalty scored!")
                self.timeline.append(event)
            else:
                event = MatchEvent(event_id=len(self.timeline)+1, event_type="PENALTY", minute=self.current_minute, team=self.away_team, outcome_text="Penalty missed!")
                self.timeline.append(event)
            print(f"Kick {i+1}: {self.home_team.country_name} {home_penalties} - {away_penalties} {self.away_team.country_name}")
        print(f"Penalty Shootout Result: {self.home_team.country_name} {home_penalties} - {away_penalties} {self.away_team.country_name}")
        if home_penalties > away_penalties:
            return f"{self.home_team.country_name} is the winner"
        elif away_penalties > home_penalties:
            return f"{self.away_team.country_name} is the winner"
        else:
            return "DRAW"


if __name__ == "__main__":
    # example usage: 3mlt el match between KSA and ARG , w 3mlt function to create team with 26 players, 11 active lineup, w 5 substitutions remaining
    def create_team(team_name):
        roster = [
            Player(name=f"{team_name}_Player{i+1}", base_attack=50 + i*5, base_defense=50 + i*5,
                   position="FORWARD" if i < 3 else "MIDFIELDER" if i < 6 else "DEFENDER" if i < 9 else "GOALKEEPER")
            for i in range(26)
        ]
        active_lineup = roster[:11]
        return Team(country_name=team_name, roster=roster, active_lineup=active_lineup)

    team1 = create_team("KSA")
    team2 = create_team("ARG")
    match = Match(home_team=team1, away_team=team2)
    for _ in range(90):
        match.run_minute_tick()

    # b3d el 90 minutes, el match phase tb2a FINISHED, w print el final score w el winner
    match.phase = "FINISHED"
    print(f"number of players in {match.home_team.country_name} active lineup: {len(match.home_team.active_lineup)}")
    print(f"number of players in {match.away_team.country_name} active lineup: {len(match.away_team.active_lineup)}")
    if match.home_score > match.away_score:
        print(f"Final Score: {match.home_team.country_name} {match.home_score} - {match.away_score} {match.away_team.country_name}. Winner: {match.home_team.country_name}")
    elif match.home_score < match.away_score:
        print(f"Final Score: {match.home_team.country_name} {match.home_score} - {match.away_score} {match.away_team.country_name}. Winner: {match.away_team.country_name}")
    else:
        print(f"Final Score: {match.home_team.country_name} {match.home_score} - {match.away_score} {match.away_team.country_name}. Winner: No one (Draw)")
        match.phase = "PENALTIES"
        match.run_penalty_shootout()
    
    for event in match.timeline: print(event.to_string())



####################################################################################


    # function to create team again with different base attack and same defense values for players to check if the match simulation is working correctly.
    def create_team_again(team_name):
        roster = [
            Player(name=f"{team_name}_Player{i+1}", base_attack=95, base_defense=50 + i*5,
                   position="FORWARD" if i < 3 else "MIDFIELDER" if i < 6 else "DEFENDER" if i < 9 else "GOALKEEPER")
            for i in range(26)
        ]
        active_lineup = roster[:11]
        return Team(country_name=team_name, roster=roster, active_lineup=active_lineup)


    team1Again = create_team_again("KSA")
    team2Again = create_team_again("ARG")
    match_again = Match(home_team=team1Again, away_team=team2Again)

    for _ in range(90):
        match_again.run_minute_tick()

    # b3d el 90 minutes, el match phase tb2a FINISHED, w print el final score w el winner, if draw
    match_again.phase = "FINISHED"
    print(f"number of players in {match_again.home_team.country_name} active lineup: {len(match_again.home_team.active_lineup)}")
    print(f"number of players in {match_again.away_team.country_name} active lineup: {len(match_again.away_team.active_lineup)}")
    if match_again.home_score > match_again.away_score:
        print(f"Final Score: {match_again.home_team.country_name} {match_again.home_score} - {match_again.away_score} {match_again.away_team.country_name}. Winner: {match_again.home_team.country_name}")
    elif match_again.home_score < match_again.away_score:
        print(f"Final Score: {match_again.home_team.country_name} {match_again.home_score} - {match_again.away_score} {match_again.away_team.country_name}. Winner: {match_again.away_team.country_name}")
    else:
        print(f"Final Score: {match_again.home_team.country_name} {match_again.home_score} - {match_again.away_score} {match_again.away_team.country_name}. Winner: No one (Draw)")
        match_again.phase = "PENALTIES"
        match_again.run_penalty_shootout()

    for event in match_again.timeline: print(event.to_string())

