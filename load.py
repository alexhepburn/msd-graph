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
from bokeh.io import show, output_file
from bokeh.plotting import figure
from bokeh.models.graphs import from_networkx
from bokeh.models import Plot, MultiLine, Circle
from bokeh.palettes import Spectral4 


n= 40000
G=nx.Graph()
edges=[]

with open("./train_triplets.txt") as f:
    lst = [next(f).strip('\n').split('\t') for x in range(n)]

df = pd.DataFrame(data=lst, columns=['User', 'Song', 'Play Count'])

print("Unique Users: " + str(len(df['User'].unique())))
print("Unique Songs: " + str(len(df['Song'].unique())))

scores_dict = {}
sd = df.groupby('Song').sum().reset_index()
# Calculate how many listens each song has and put it into a dictionary
# in order to normalise the scores with respect to how popular the song is
for user in tqdm(df['User'].unique()):
	user_entires = df.loc[df['User'] == user]
	song_list = list(user_entires['Song'])
	scores_dict.clear()
	for song in song_list:
		user_score = int(user_entires.loc[user_entires['Song'] == song]['Play Count'])
		song_listens = df.loc[df['Song'] == song]
		user_list = list(song_listens['User'])
		if user in user_list:
			user_list.remove(user)
		for match in user_list:
			match_score = list(song_listens.loc[song_listens['User'] == match]['Play Count'])
			for s in match_score:
				# If users already have a song in common from before
				lst = float(sd.loc[sd['Song'] == song]['Play Count'])
				if match in scores_dict:
					scores_dict[match] = [scores_dict[match][0] + 1, scores_dict[match][1] + float(s)/lst]
				else:
					scores_dict[match] = [1, float(s)/lst]
	for key in scores_dict:
		s = 1./float(scores_dict[key][1])
		G.add_edge(user, key, score=s, capacity=scores_dict[key][0])
		edges.append([user, key, s])

nx.write_gml(G, './MSDgraph.gml')
