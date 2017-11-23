'''
Community detection using python-louvain, results plotted using Bokeh
'''
import networkx as nx 
import community
import numpy as np
import pandas as pd

from bokeh.io import show, output_file
from bokeh.plotting import figure
from bokeh.models.graphs import from_networkx
from bokeh.models.sources import ColumnDataSource
from bokeh.models import Plot, MultiLine, Circle
from bokeh.models import GraphRenderer, Oval
from bokeh.palettes import Set3

# Number of triplets used to construct the graph
n = 20000

# Which parameter you want to evaluate when doing community detection
eval_par = 'capacity'

# Read in csv of song ids -> song names to see which songs certain 
# communities listen to
track_df = pd.read_csv('unique_tracks.txt', delimiter='<SEP>', names=['TrackID', 'Song', 
	'Artist Name', 'Song Title'], engine='python')

# Read in triplets to dataframe for searching for popular songs in communities
with open("./train_triplets.txt") as f:
    lst = [next(f).strip('\n').split('\t') for x in range(n)]
df = pd.DataFrame(data=lst, columns=['User', 'Song', 'Play Count'])
df['Play Count'] = df['Play Count'].astype(int)
G = nx.read_gml("./MSDgraph.gml")
print(len(G.nodes()))
partition = community.best_partition(G, weight=eval_par)
num_comm = len(np.unique(list(partition.values())))
print(str(num_comm) + ' communities found.')
# -1 so it will throw out an error and not just colour all the nodes as 
# belonging to community 0
song_dict = []
for i in range(0, 5):
	d = {}
	song_dict.append(d)

c = {}
comm_songs = pd.DataFrame(columns=['User', 'Community Song 1', 'Community Song 2', 'Community Song 3',
	'Community Song 4', 'Community Song 5'], dtype='object')
save_df = pd.DataFrame(columns=['TrackID', 'Song', 'Artist Name', 'Song Title', 'Community'])
for i in range(0, num_comm):
	print("Sorting through community " + str(i))
	# Match indices from ids_comm to indices in graph and set colour for each node
	# so that nodes in a community are the same colour
	ids_comm = [key for key, value in partition.items() if value == i]
	for ids in ids_comm:
		c[ids] = Set3[12][i]
	# Search for popular songs inside communities
	comm = df[df['User'].isin(ids_comm)].groupby('Song').sum().reset_index().sort_values('Play Count',
		ascending=False)
	songs = track_df[track_df['Song'].isin(list(comm['Song'])[0:5])]
	songs['Community'] = [i] * songs.shape[0]
	plays = comm[comm['Song'].isin(list(songs['Song']))]
	plays.columns.values[0] = 'Song'
	songs = pd.merge(songs, plays, how='left', on='Song')
	songs = songs.sort_values('Play Count', ascending=False)
	save_df = save_df.append(songs, ignore_index=True)
	for user in ids_comm:
		song_str = ""
		for i in range(5):
			song_str = songs['Artist Name'][i] + ', ' + songs['Song Title'][i] + ', ' + str(songs['Play Count'][i])
			song_dict[i][user] = song_str

save_df.to_csv('./community_songs.csv', sep=',')
nx.set_node_attributes(G, name='fillcolor', values=c)
plot = figure(title="MSD User Listens in Common", x_range=(-1.1,1.1), y_range=(-1.1,1.1), 
	plot_width=800, plot_height=800)
graph_renderer = from_networkx(G, nx.spring_layout, scale=2, center=(0,0), weight=eval_par)
graph_renderer.node_renderer.data_source.add(list(c.values()), 'fillcolor')
graph_renderer.node_renderer.glyph = Circle(size=7, fill_color='fillcolor')
plot.renderers.append(graph_renderer)
output_file("community_det.html")
show(plot)

# Save which community each node is in
nx.set_node_attributes(G, name='community', values=partition)
for i in range(5):
	nx.set_node_attributes(G, name='communitySong' + str(i), values=song_dict[i])
nx.write_gml(G, './MSDgraph_comm.gml')