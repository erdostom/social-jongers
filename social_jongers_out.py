import pickle
from color import color
from random import shuffle
import csv 


def printSolution(ans):
    # load in player list
    with open("players.csv", 'r', newline='') as file:
        data = csv.DictReader(file, delimiter=';')
        player_dicts = [row for row in data]

    # shuffle player list to add variation (despite using same SAT solution)
    shuffle(player_dicts)
    player_names = [p["name"] for p in player_dicts]
    player_clubs = [p["club"] for p in player_dicts]

    # print player list
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


if __name__=="__main__":
    # load in social golfers solution
    pickle_name = f"output/answer_100_8.pkl"
    with open(pickle_name, 'rb') as file:
        ans = pickle.load(file)
    printSolution(ans)