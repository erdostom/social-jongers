import pickle
from color import color
from random import shuffle
import csv 
COMPASS = ["East", "South", "West", "North"]
COLORS = ["GREEN", "RED", "PURPLE", "BLUE"]


# load in social golfers solution
pickle_name = f"output/answer_100_8.pkl"
with open(pickle_name, 'rb') as file:
    SOLUTION = pickle.load(file)


# print solution ("Player 1, Player 2...etc")
def genericSolution():
    player_names = list(range(0,100))
    shuffle(player_names)
    for day, groups in SOLUTION.items():
        print(f"Round {day+1}:")
        for i,group in groups.items():
            print(f"Group {i+1}: ", end="")
            for seatIndex,playerIndex in group.items():
                pIndex = playerIndex[0]
                print(f"[{COMPASS[seatIndex]}] Player {player_names[pIndex]+1}", end=" ")
            print()
        print()


# print (colored) solution, mapped to input CSV file
def printSolution(inputFile):
    # load in player list
    with open(inputFile, 'r', newline='') as file:
        data = csv.DictReader(file, delimiter=';')
        player_dicts = [row for row in data]

    # shuffle player list to add variation (despite using same SAT solution)
    shuffle(player_dicts)
    player_names = [p["name"] for p in player_dicts]
    player_clubs = [p["club"] for p in player_dicts]

    # print player list
    for day, groups in SOLUTION.items():
        color()
        color("BOLD")
        color("UNDERLINE")
        print(f"Round {day+1}:")
        for i,group in groups.items():
            color()
            print(f"Group {i+1}: ", end="")

            for seatIndex,playerIndex in group.items():
                color(COLORS[seatIndex])
                pIndex = playerIndex[0]
                print(f"{COMPASS[seatIndex]} : {player_names[pIndex]}", end=" ")
                color("ITALIC")
                print(f"({player_clubs[pIndex]})", end=" ")
            print()
        print()
    color()





# generate CSV ouput
def csvSolution(inputFile, outputFile):
    # load in player list
    with open(inputFile, 'r', newline='') as file:
        data = csv.DictReader(file, delimiter=';')
        player_dicts = [row for row in data]

    # shuffle player list to add variation (despite using same SAT solution)
    shuffle(player_dicts)
    player_names = [p["name"] for p in player_dicts]
    player_clubs = [p["club"] for p in player_dicts]


    with open(outputFile, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)

        # CSV header
        roundCount = 8
        roundNumbers = []
        for i in range(1,roundCount+1):
            roundNumbers.append("")
            roundNumbers.append(i)
        writer.writerow(["Player ID", "Name"] + roundNumbers)
        writer.writerow(["", ""]              + ["Table", "Seat"] * roundCount)


        # Generate assignments (playerID[day] : {table,seat})
        assignments = [[None for _ in range(roundCount)] for _ in range(len(player_names))]
        for day, groups in SOLUTION.items():
            for i,group in groups.items():
                for seatIndex,playerIndex in group.items():
                    pIndex = playerIndex[0]
                    table = i + 1
                    seat = COMPASS[seatIndex]
                    assignments[pIndex][day] = [table, seat]

        # write assignments
        for pIndex, allRounds in enumerate(assignments):
            playerName = player_names[pIndex]
            playerID = pIndex + 1
            row = [playerID, playerName]
            for r in allRounds: row += r
            writer.writerow(row)


if __name__=="__main__":
    # genericSolution()
    # printSolution("input/players.csv")
    csvSolution("input/players.csv", "input/Philly2024.csv")