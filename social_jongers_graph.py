from pyvis.network import Network
from itertools import combinations
import pickle

# load in social golfers solution
pickle_name = f"output/answer_112_6_1.pkl"
with open(pickle_name, 'rb') as file:
    SOLUTION = pickle.load(file)



# Create empty Pyvis network
graph = Network(width="100%",height="750px", select_menu=True, directed=False)


player_names = list(range(0,100))
players = set()

for day, groups in SOLUTION.items():
    for i,group in groups.items():
        tablePlayers = []
        for seatIndex,playerIndex in group.items():
            pIndex = playerIndex[0]
            if pIndex not in players:
                players.add(pIndex)
                graph.add_node(pIndex, title=f"Player {player_names[pIndex]+1}")
            tablePlayers.append(pIndex)

        relations = combinations(tablePlayers, 2)
        for rel in relations:
            graph.add_edge(rel[0], rel[1])


# Show the graph
graph.barnes_hut()
graph.show_buttons(filter_=['physics'])
graph.save_graph("graph.html")