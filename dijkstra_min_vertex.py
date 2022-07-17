import csv
import timeit
import networkx as nx
from matplotlib import pyplot as plt

G = nx.DiGraph()

def Dijkstra(Graph, from_vertex, to_vertex):
	row = len(Graph)
	col = len(Graph[0])
	dist = [float("Inf")] * row
	blackened_vertex = [0] * row
	path_length = [0] * row
	parent = [-1] * row
	dist[from_vertex] = 0

	for count in range(row - 1):
		u = MinDistance(dist, blackened_vertex)

		if u == float("Inf"):
			break
		else:
			blackened_vertex[u] = 1
		for v in range(row):
			if blackened_vertex[v] == 0 and Graph[u][v] and dist[u] + Graph[u][v] < dist[v]:
				parent[v] = u
				path_length[v] = path_length[parent[v]] + 1
				dist[v] = dist[u] + Graph[u][v]
			elif blackened_vertex[v] == 0 and Graph[u][v] and dist[u] + Graph[u][v] == dist[v] and path_length[u] + 1 < path_length[v]:
				parent[v] = u
				path_length[v] = path_length[u] + 1

	if dist[to_vertex] != float("Inf"):
		PrintPath(parent, to_vertex)
	else:
		print("There is no path between ", from_airport, "to ",to_airport)

def PrintPath(parent_vertex, last_vertex):
	if parent_vertex[last_vertex] == -1:
		print(dict_airport_id_name[str(last_vertex)]+'('+str(last_vertex)+')',end='')
		arr_total_disc.append(last_vertex)
		return
	PrintPath(parent_vertex, parent_vertex[last_vertex])
	print(" -> "+dict_airport_id_name[str(last_vertex)]+'('+str(last_vertex)+')', end='')
	arr_total_disc.append(last_vertex)

def MinDistance(dist, Blackened):
	min = float("Inf")
	for v in range(len(dist)):
		if not Blackened[v] and dist[v] < min:
			min = dist[v]
			Min_index = v
	return float("Inf") if min == float("Inf") else Min_index

node_num=3266
Graph=[[float("Inf") for i in range(node_num)] for j in range(node_num)]
graph_disc=[[float("Inf") for i in range(node_num)] for j in range(node_num)]
graph_cost=[[float("Inf") for i in range(node_num)] for j in range(node_num)]
for i in range(node_num):
	Graph[i][i]=0

dict_airport_id_name={}
dict_airport_name_id={}
total_disc=0
total_cost=0
arr_total_disc=[]
with open('Airports-last.csv') as csv_file:
	csv_reader = csv.reader(csv_file, delimiter=',')
	line_count = 0
	for column in csv_reader:
		if line_count==0:
			line_count += 1
		else:
			line_count += 1
			dict_airport_name_id[column[0]]=column[1]
			dict_airport_id_name[column[1]] = column[0]
			Graph[int(column[1])][int(column[2])] = 1
			graph_disc[int(column[1])][int(column[2])] = int(column[3])
			graph_cost[int(column[1])][int(column[2])] = int(column[4])

from_airport = input("\nEnter from airport name: ")
to_airport = input("Enter to airport name: ")

start = timeit.default_timer()
Dijkstra(Graph, int(dict_airport_name_id[from_airport]), int(dict_airport_name_id[to_airport]))

for i in range(len(arr_total_disc)):
	with open('Airports-last.csv') as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')

		for column in csv_reader:
			if column[1] == str(arr_total_disc[i]):
				G.add_edge(column[1], column[2], color='b')

			if column[2] == str(arr_total_disc[i]):
				G.add_edge(column[2], column[1], color='b')
	if i!=0:
		total_disc=total_disc+graph_disc[arr_total_disc[i]][arr_total_disc[i-1]]
		total_cost = total_cost + graph_cost[arr_total_disc[i]][arr_total_disc[i - 1]]
		G.add_edge(arr_total_disc[i], arr_total_disc[i-1], color='r')

edges = G.edges()
colors = [G[u][v]['color'] for u, v in edges]
nx.draw(G, with_labels=True, edge_color=colors, font_color='white', node_color='black', node_size=1000)

plt.savefig("graph-min-vertex.png", format="PNG")
plt.show()

print('\nTotal distance -> '+str(total_disc)+' km')
print('Total cost -> '+str(total_cost)+' $')
stop = timeit.default_timer()

print('Time: ', stop - start, ' seconds')