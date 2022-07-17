import csv
import timeit
from collections import defaultdict
import networkx as nx
import matplotlib.pyplot as plt

G = nx.DiGraph()

class Graph():

    def __init__(self):
        self.edges = defaultdict(list)
        self.weights = {}

    def add_edge(self, from_vertex, to_vertex, distance):
        self.edges[from_vertex].append(to_vertex)
        self.edges[to_vertex].append(from_vertex)
        self.weights[(from_vertex, to_vertex)] = distance
        self.weights[(to_vertex, from_vertex)] = distance

graph = Graph()
dict_airport_id_name={}
dict_airport_name_id={}
edges = []

with open('Airports-last.csv') as csv_file:

    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0

    for column in csv_reader:
        if line_count == 0:
            line_count += 1
        else:
            data=list((str(column[1]),str(column[2]),int(column[3])))
            edges.append(data)
            dict_airport_name_id[column[0]]=column[1]
            dict_airport_id_name[column[1]]=column[0]

for edge in edges:
    graph.add_edge(*edge)

def dijsktra(graph_airport, fisrt_node, last_node):
    shortest_paths = {dict_airport_name_id[fisrt_node]: (None, 0)}
    current_node = dict_airport_name_id[fisrt_node]
    visited = set()

    while current_node != dict_airport_name_id[last_node]:
        visited.add(current_node)

        for next_node in graph_airport.edges[current_node]:
            weight = graph_airport.weights[(current_node, next_node)] + shortest_paths[current_node][1]
            if next_node not in shortest_paths:
                shortest_paths[next_node] = (current_node, weight)
            else:
                current_shortest_weight = shortest_paths[next_node][1]
                if current_shortest_weight > weight:
                    shortest_paths[next_node] = (current_node, weight)

        next_destinations = {node: shortest_paths[node] for node in shortest_paths if node not in visited}
        if not next_destinations:
            return "There is no path between ", from_airport, "to "+to_airport
        current_node = min(next_destinations, key=lambda k: next_destinations[k][1])

    path = []
    total_distance=0
    start=""

    while current_node is not None:
        airpoty_id_name=dict_airport_id_name[current_node]+'('+current_node+')'

        path.append(airpoty_id_name)

        with open('Airports-last.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')

            for column in csv_reader:
                if column[1]==current_node:
                    G.add_edge(column[1], column[2], color='b')

                if column[2]==current_node:
                    G.add_edge(column[2], column[1], color='b')

        if current_node!=dict_airport_name_id[last_node]:
            G.add_edge(current_node,start,color='r')
            start=current_node
        else:
            start=current_node

        next_node = shortest_paths[current_node][0]
        if total_distance==0:
            total_distance=int(shortest_paths[current_node][1])
        current_node = next_node

    path = path[::-1]

    edges = G.edges()
    colors = [G[u][v]['color'] for u, v in edges]
    nx.draw(G, with_labels=True, edge_color=colors, font_color='white', node_color='black', node_size=1000)

    plt.savefig("graph-min-dist.png", format="PNG")
    plt.show()

    print(" -> ".join(path)+'\nTotal distance -> '+str(total_distance)+" km")

from_airport = input("\nEnter from airport name: ")
to_airport = input("Enter to airport name: ")

start = timeit.default_timer()
dijsktra(graph, str(from_airport), str(to_airport))
stop = timeit.default_timer()
print('Time: ', stop - start, ' seconds')