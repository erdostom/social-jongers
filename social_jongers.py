from ortools.sat.python import cp_model
from itertools import groupby, product, combinations
import pickle
import math
from color import color
import csv
from sys import argv


def load_players(player_file=None):
    if player_file==None and len(argv) <= 1:
        player_file = argv[1]

    with open(player_file, 'r', newline='') as file:
        data = csv.DictReader(file, delimiter=',')
        players = [row for row in data]
    return players

# This is a convenience function to help iterate over groups
def groupby_keys(input_list, keylist):
    keyfunc = lambda x: tuple(x[k] for k in keylist)
    yield from groupby(sorted(input_list, key=keyfunc), key=keyfunc)


player_dicts = load_players("players.csv")
player_names = [p["name"] for p in player_dicts]
player_clubs = [p["club"] for p in player_dicts]

n_players = 108
n_days = 6
players_per_group = 4
crossover_ratio = float(argv[1] if len(argv) > 1 else 1.0)

club_matrix = [[player_clubs[i] == player_clubs[j] and player_clubs[i] != '' for i in range(n_players)] for j in range(n_players)]

# these will come in handy
n_groups = n_players // players_per_group
n_games_per_seat = math.ceil(n_days / players_per_group)
players = list(range(n_players))
days = list(range(n_days))
groups = list(range(n_groups))
seats = list(range(players_per_group))

model = cp_model.CpModel()

variables = []
player_vars = {}
for player, day, group, seat in product(players, days, groups, seats):
    v_name = f"{player}_{day}_{group}_{seat}"
    the_var = model.NewBoolVar(v_name)
    variables.append({
        k: v
        for v, k in zip([v_name, player, day, group, seat, the_var],
                        ['Name', 'Player', 'Day', 'Group', 'Seat', 'CP_Var'])
    })
    player_vars[player, day, group, seat] = the_var

# each player must be in a single group on each day
for idx, grp in groupby_keys(variables, ['Player', 'Day']):
    model.Add(sum(x['CP_Var'] for x in grp) == 1)

# correct players per group (4 players at a table)
for idx, grp in groupby_keys(variables, ['Day', 'Group']):
    model.Add(sum(x['CP_Var'] for x in grp) == players_per_group)

# each game must have one member in each seat (east/south/west/north)
for idx, grp in groupby_keys(variables, ['Day', 'Group', 'Seat']):
    model.Add(sum(x['CP_Var'] for x in grp) == 1)

# players don't play in the same seat more often than necessary
for idx, grp in groupby_keys(variables, ['Player', 'Seat']):
    model.Add(sum(x['CP_Var'] for x in grp) <= n_games_per_seat)

penalties = []
for p1, p2 in combinations(players, r=2):
    players_together = []
    for day in days:
        for group in groups:
            together = model.NewBoolVar(f"M_{p1}_{p2}_{day}_{group}")
            players_together.append(together)
            p1g = sum(player_vars[p1, day, group, seat] for seat in seats)
            p2g = sum(player_vars[p2, day, group, seat] for seat in seats)
            model.Add(p1g + p2g - together <= 1)

            # objective: minimize games between players from same club
            if club_matrix[p1][p2]:
                penalties.append(together)

            # This section shows how to implement the implication version of the
            # multiplicative constraint
            # model.AddBoolOr([p1g.Not(), p2g.Not(), together])
            # model.AddImplication(together, p1g)
            # model.AddImplication(together, p2g)
    model.Add(sum(players_together) <= 1)

# [1] Minimizing intra-club play (minimize - VERY SLOW)
# model.Minimize(sum(penalties))

# [2] Minimize intra-club play (threshold - FASTER)
# model.Add(sum(penalties) <= int(crossover_ratio * n_players * n_days))

solver = cp_model.CpSolver()
solver.Solve(model)
print(solver.ResponseStats())



def parse_answer(variables):
    solution = {}
    for var in variables:
        player, day, group, seat = var['Player'], var['Day'], var[
            'Group'], var['Seat']
        solution[player, day, group, seat] = solver.Value(var['CP_Var'])

    days = sorted(set(x[1] for x in solution))
    groups = sorted(set(x[2] for x in solution))
    seats = sorted(set(x[3] for x in solution))
    answers = {}
    for day in days:
        answers[day] = {}
        for group in groups:
            answers[day][group] = {}
            for seat in seats:
                ans = [
                    k[0] for k, v in solution.items()
                    if k[1] == day and k[2] == group and k[3] == seat and v
                ]
                answers[day][group][seat] = sorted(ans)
    return answers


ans = parse_answer(variables)

# save answers
pickle_name = f"answer_{n_players}_{n_days}_{crossover_ratio}.pkl"

with open(pickle_name, 'wb') as file:
    pickle.dump(ans, file)


# print answers
compass = ["East", "South", "West", "North"]
colors = ["GREEN", "RED", "PURPLE", "BLUE"]
for day, groups in ans.items():
    color()
    color("BOLD")
    color("UNDERLINE")
    print(f"Round {day+1}:")
    for i,group in groups.items():
        color()
        print(f"Group {i+1}: ", end="")

        for seatIndex,playerIndex in group.items():
            color(colors[seatIndex])
            pIndex = playerIndex[0]
            print(f"{compass[seatIndex]} : {player_names[pIndex]}", end=" ")
            color("ITALIC")
            print(f"({player_clubs[pIndex]})", end=" ")
        print()
    print()
color()