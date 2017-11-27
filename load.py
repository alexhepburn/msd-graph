'''
Contructs a GML file in the current directory storing various attributed from the
Million Song Dataset - The Echo Nest Taste Profile Subset
attributes stored in the graph are:
'score' = the sum of songs that users have in common divided by the total number of 
		  listens for that song
'capacity' = number of songs users have in common
'''

import pandas as pd
import networkx as nx 
import numpy as np
from tqdm import *
import copy

n= 20000
G=nx.Graph()
edges=[]

with open("./train_triplets.txt") as f:
    lst = [next(f).strip('\n').split('\t') for x in range(n)]

df = pd.DataFrame(data=lst, columns=['User', 'Song', 'Play Count'])
df['Play Count'] = df['Play Count'].astype(int)
print("Unique Users: " + str(len(df['User'].unique())))
print("Unique Songs: " + str(len(df['Song'].unique())))
scores_dict = {}
songs = df.groupby('Song')
sd = songs.sum().reset_index()

for name, group in tqdm(songs):
	userlst = list(group['User'])
	while len(userlst) > 1:
		user = userlst[0]
		userlst.remove(user)
		for u in userlst:
			if (user, u) in scores_dict:
				scores_dict[(user, u)] += 1.
			elif (u, user) in scores_dict:
				scores_dict[(u, user)] += 1.
			else:
				scores_dict[(user, u)] = 1.
for key in scores_dict:
	G.add_edge(key[0], key[1], capacity=1/scores_dict[key])
print('Number of nodes: ' + str(len(G.nodes())))
print('Number of edges: ' + str(len(G.edges())))
nx.write_gml(G, './MSDgraph2.gml')