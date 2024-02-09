from ortools.sat.python import cp_model
from itertools import groupby, product, combinations
import pickle
import math
import csv

# load in player list
with open("players.csv", 'r', newline='') as file:
    data = csv.DictReader(file, delimiter=';')
    player_dicts = [row for row in data]
player_names = [p["name"] for p in player_dicts]
player_clubs = [p["club"] for p in player_dicts]


n_players = 100        # player count
n_days = 8             # hanchan count
players_per_group = 4  # four player game
crossover_ratio = 0.3  # threshold of intra-club play

# This is a convenience function to help iterate over groups
def groupby_keys(input_list, keylist):
    keyfunc = lambda x: tuple(x[k] for k in keylist)
    yield from groupby(sorted(input_list, key=keyfunc), key=keyfunc)


# these will come in handy
n_groups = n_players // players_per_group
n_games_per_seat = math.ceil(n_days / players_per_group)
players = list(range(n_players))
days = list(range(n_days))
groups = list(range(n_groups))
seats = list(range(players_per_group))
club_matrix = [[player_clubs[i] == player_clubs[j] for i in range(n_players)] for j in range(n_players)]


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

    model.Add(sum(players_together) <= 1)



# [1] Minimizing intra-club play (VERY SLOW)
model.Minimize(sum(penalties))

# [2] Threshold intra-club play (FASTER)
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
pickle_name = f"answer_{n_players}_{n_days}_intra_club.pkl"
with open(pickle_name, 'wb') as file:
    pickle.dump(ans, file)

print(f"Solution dumped --> {pickle_name}")