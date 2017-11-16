import pandas as pd
import networkx as nx 
import numpy as np
import matplotlib.pyplot as plt 

from bokeh.io import show, output_file
from bokeh.plotting import figure
from bokeh.models.graphs import from_networkx
from bokeh.models import Plot, MultiLine, Circle
from bokeh.palettes import Spectral4 


n= 1000
G=nx.Graph()
edges=[]

with open("./train_triplets.txt") as f:
    lst = [next(f).strip('\n').split('\t') for x in range(n)]

df = pd.DataFrame(data=lst, columns=['User', 'Song', 'Play Count'])

print("Unique Users: " + str(len(df['User'].unique())))
print("Unique Songs: " + str(len(df['Song'].unique())))

scores_dict = {}
song_listens_dict = {}

# Calculate how many listens each song has and put it into a dictionary
# in order to normalise the scores with respect to how popular the song is
for song in df['Song'].unique():
	listens_arr = np.array(df.loc[df['Song'] == song]['Play Count'], dtype=int)
	song_listens_dict[song] = sum(listens_arr)

for user in df['User'].unique():
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
				if match in scores_dict:
					scores_dict[match] = scores_dict[match] + float(s)/float(song_listens_dict[song])
				else:
					scores_dict[match] = float(s)/float(song_listens_dict[song])
	for key in scores_dict:
		s = 1./float(scores_dict[key])
		G.add_edge(user, key, weight=s)
		edges.append([user, key, s])

print("Total number of edges: " + str(G.number_of_edges()))
plot = figure(title="MSD User Listens in Common", x_range=(-1.1,1.1), y_range=(-1.1,1.1), plot_width=800, plot_height=800)
graph_renderer = from_networkx(G, nx.spring_layout, scale=2, center=(0,0))
graph_renderer.node_renderer.glyph = Circle(size=7, fill_color=Spectral4[0])
graph_renderer.edge_renderer
plot.renderers.append(graph_renderer)
output_file("msd2.html")
show(plot)

elarge=[(u,v) for (u,v,d) in G.edges(data=True) if d['weight'] >0.5]
esmall=[(u,v) for (u,v,d) in G.edges(data=True) if d['weight'] <=0.5]
