# World Cup Theme 🏆

A collection of Python exercises built around a World Cup theme, covering 3 different tasks: managing a group standings table, encoding/decoding tickets, and a full football match simulation with an AI that makes real-time tactical decisions.

## Repo Contents

| File | Description |
|---|---|
| `task1.py` | Calculates and sorts a World Cup group standings table |
| `task2.py` | Encodes and decodes entry tickets (Ticket Codec) with validity checking |
| `task3.py` | A full football match simulation (players, teams, events, penalty shootout) |
| `task3 with the AI bouns.py` | Same match simulation + a `MatchAI` class that controls in-game tactical decisions via a language model (LLM) hosted on Kaggle |
| `ngrok-kaggle.ipynb` | A notebook that runs the LLM server (Flask) on Kaggle and exposes it to the internet via ngrok, so `task3 with the AI bouns.py` can reach it |

---

## Task 1 — World Cup Group Standings

**Idea:** Calculate a standings table for a group of 4 teams (KSA, POL, MEX, ARG), just like any World Cup group.

**How it works:**
- Each team has a dictionary tracking: `Played, Won, Drawn, Lost, Goals For, Goals Against, Goal Diff, Points`.
- `process_match()` takes a match result between two teams and updates both teams' stats (win = 3 points, draw = 1 point).
- `sort_standings()` ranks teams by **Points → Goal Difference → Goals For**, matching the official FIFA tiebreaker order.
- `display_standings()` prints the table neatly formatted into columns.
- The script loops through every possible matchup between the four teams (6 matches total), taking each result from the user via input in `X-Y` format.
- **Bonus:** input validation — if the user enters an invalid format, the script shows an error message and asks them to re-enter instead of crashing.

**Run it:**
```bash
python task1.py
```
It will prompt you to enter the result of each match, then print the final sorted table.
<img width="230" height="79" alt="image" src="https://github.com/user-attachments/assets/7956d31f-6268-44d6-a856-a899fc544470" />

---

## Task 2 — Ticket Codec (Ticket Encoding/Decoding)

**Idea:** A simple system to generate a text "barcode" for each entry ticket, with a checksum that guarantees the ticket hasn't been tampered with.

**`TicketCodec` class:**
- `calculate_checksum(ticket_id)`: calculates a checksum by summing `ord(character) * (index + 1)` for every character in the ticket code, taking the remainder mod 256.
- `encode(ticket_id)`: returns the ticket code plus the checksum in hexadecimal format (two digits, e.g. `a3`).
- `decode(barcode)`: separates the ticket from the checksum, recalculates the checksum from the ticket, and compares it against the attached checksum. If they match, it returns the original ticket; if not, it returns a **"CORRUPTED TICKET"** message.

**Tests included in the file:**
- Encoding and decoding a normal ticket (`TICKET123`).
- Attempting to decode a ticket after manually altering the checksum (should come out corrupted).
- Attempting to decode a ticket after changing its first character (same result).
- Additional examples with different ticket codes (`GATE2026A`, `ticket2026B`).

**Run it:**
```bash
python task2.py
```

---

## Task 3 — Match Simulation (Full Football Match Simulation)

This is the largest task in the repo, and it comes in two versions: `task3.py` (the base simulation) and `task3 with the AI bouns.py` (the same simulation plus the AI layer).

### Core Classes

**`Player`**
- Each player has: a name, base attack (`base_attack`), base defense (`base_defense`), a position (`position`), a count of disciplinary incidents (`incidents`), and stamina (`stamina`) starting at 100.
- `deplete_stamina()`: reduces stamina each minute, with a floor of 10.0 (formula: `Stamina(t) = max(10.0, Stamina(t-1) - decay)`).
- `get_effective_attack()` / `get_effective_defense()`: the actual attack/defense value is scaled by the remaining stamina percentage (`base_value * stamina/100`).
- `is_eligible()` / `add_incident()` **(bonus)**: if a player accumulates more than 3 incidents, they become ineligible to continue in the match.

**`Team`**
- Contains a `roster` (all players, 26 total), an `active_lineup` (starting 11), and `substitutions_remaining` (allowed substitutions, defaulting to 5).
- `bench` (property): all players not in the starting lineup.
- `get_aggregate_attack()` / `get_aggregate_defense()`: average attack strength across forwards/midfielders, and average defense strength across defenders/goalkeepers.
- `execute_substitution()`: performs a substitution between a starting player and a bench player, checking that substitutions remain available.
- `enforce_discipline()` **(bonus)**: automatically removes any player who has lost eligibility (`is_eligible() == False`) from the starting lineup.
- `swipe_players_from_the_bench()`: a smart auto-substitution — finds the lowest-stamina player in the starting lineup and swaps them with the best available bench player in the same position (if that bench player has higher stamina).

**`MatchEvent`**
- Represents any event in the match (goal, penalty, etc.) with an ID, type, minute, team, and optional player.

**`Match`**
- Controls the entire match: both teams, the score, the current minute, the event timeline (`timeline`), and the match phase (`REGULATION`, `FINISHED`, `PENALTIES`).
- `run_minute_tick()`: simulates one minute of the match — depletes every player's stamina, gives each player a 1% chance of picking up a disciplinary incident, attempts a goal for each team, enforces discipline rules, and performs auto-substitutions if needed.
- `process_goal_attempt()`: each minute has a 10% chance that a team attempts to score, with the outcome decided by a randomized formula:
  `Goal = (Aggregate_Attack × random(0.75, 1.25)) > (Aggregate_Defense × 1.3 × random(0.80, 1.20))`.
- `run_penalty_shootout()`: if the match ends in a draw, runs a penalty shootout (5 kicks per team, 75% scoring chance per kick) and determines the winner.

### Demo Section (`if __name__ == "__main__"`)
- Creates two teams (KSA and ARG) with 26 players each (3 forwards, 3 midfielders, 3 defenders, a goalkeeper, etc. based on the position distribution).
- Runs a full 90-minute simulation, then prints the final score and winner (or runs a penalty shootout if it's a draw).
- Finally runs a second test with teams that have very strong attack stats (`base_attack=95`) to confirm the simulation responds correctly to differences in team strength.

---

## Task 3 Bonus — MatchAI 🤖 (An AI-Driven Coach)

The `task3 with the AI bouns.py` version adds a **`MatchAI`** class on top of everything above. It represents a "virtual coach" that observes the match and makes tactical changes during play using a **real LLM** (not fixed rule-based logic).

### How the AI Works

1. **`observe_state(match)`** — gathers a full snapshot of the current match state: the minute, the score, each team's average attack/defense, remaining substitutions, and the stamina level of every player in the lineup.

2. **`decide_action(match)`** — sends this state as a prompt to a language model hosted on **Kaggle** (a simple Flask server), exposed to the internet via **ngrok** (the `ngrok-kaggle.ipynb` notebook is what runs this server). The AI responds with a single word chosen from four options:
   - `SUBSTITUTE` — make a substitution
   - `CHANGE_FORMATION` — change the formation
   - `HOLD` — settle the game down / play more defensively
   - `PUSH_ATTACK` — push forward offensively

   If the response isn't one of these four (or if the connection fails), it defaults safely to `HOLD`.

3. **`apply_decision(action)`** — actually executes the decision on the team:
   - **`SUBSTITUTE`** → uses `swipe_players_from_the_bench()` to swap out the lowest-stamina player for the best available replacement in the same position.
   - **`HOLD`** → decreases `risk_tolerance` by 0.2 (floor of 0.0) — the team plays more cautiously.
   - **`PUSH_ATTACK`** → increases `risk_tolerance` by 0.2 (cap of 1.0) — the team plays more aggressively.
   - **`CHANGE_FORMATION`** → randomly picks one of 3 formations (Defensive 5-3-2 / Balanced 4-4-2 / Attacking 3-4-3), and actually redistributes the 11 starting players across the four positions (`FORWARD`, `MIDFIELDER`, `DEFENDER`, `GOALKEEPER`) according to the chosen formation — which directly affects subsequent attack/defense calculations.

Every decision is logged in `decision_log`, keeping a full record of each team's coaching decisions throughout the match.

### Integration with the Simulation

In the demo section, one `MatchAI` instance is created per team (once, before the loop starts — not recreated every iteration), and every 20 minutes of match time the AI is asked to decide and execute an action:

```python
ai_home = MatchAI(controlled_team=team1, risk_tolerance=0.5)
ai_away = MatchAI(controlled_team=team2, risk_tolerance=0.5)

for _ in range(90):
    match.run_minute_tick()
    if match.current_minute % 20 == 0:
        action_home = ai_home.decide_action(match)
        ai_home.apply_decision(action_home)
        action_away = ai_away.decide_action(match)
        ai_away.apply_decision(action_away)
```

### Running It

⚠️ **Important:** this part requires an actual internet connection and a running LLM server, so you need to:

1. Run the `ngrok-kaggle.ipynb` notebook on Kaggle first, which will give you a live ngrok URL (something like `https://xxxx.ngrok-free.dev/generate`).
2. Make sure that same URL is set in the `URL` variable inside `decide_action()`.
3. Then run:
```bash
python "task3 with the AI bouns.py"
```

Every call to `decide_action()` sends a real request over the internet to the server, so the full 90-minute simulation can take noticeably longer than usual, depending on the server's response time and how often the AI is consulted.

### Requirements
```bash
pip install requests
```
(`random` and `os` are built into Python, no installation needed.)

---

## General Notes

- Code comments are written in Franco-Arabic (Arabic transliterated in Latin letters) to document the logic during development.
- The word "bouns" in function and file names is a documentation note marking additional (bonus) work on top of each task's core requirements.
- No API keys or secrets are exposed in the code — the ngrok URL in `task3 with the AI bouns.py` is temporary and changes every time the Kaggle server is restarted.
