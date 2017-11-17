'''
Community detection using python-louvain, results plotted using Bokeh
'''
import networkx as nx 
import community
import numpy as np

from bokeh.io import show, output_file
from bokeh.plotting import figure
from bokeh.models.graphs import from_networkx
from bokeh.models.sources import ColumnDataSource
from bokeh.models import Plot, MultiLine, Circle
from bokeh.models import GraphRenderer, Oval
from bokeh.palettes import Category20c

eval_par = 'score'

G = nx.read_gml("./MSDgraph.gml")
partition = community.best_partition(G, weight=eval_par)
num_comm = len(np.unique(list(partition.values())))
plot = figure(title="MSD User Listens in Common", x_range=(-1.1,1.1), y_range=(-1.1,1.1), 
	plot_width=800, plot_height=800)
graph_renderer = from_networkx(G, nx.spring_layout, scale=2, center=(0,0), weight=eval_par)
ids_dat = graph_renderer.node_renderer.data_source.data["index"]

# -1 so it will throw out an error and not just colour all the nodes as 
# belonging to community 0
c = [-1] * len(partition.keys())
for i in range(num_comm):
	ids_comm = [key for key, value in partition.items() if value == i]
	ind = [j for j, item in enumerate(ids_dat) if item in ids_comm]
	for indx in ind:
		c[indx] = Category20c[20][i]
graph_renderer.node_renderer.glyph = Circle(size=7, fill_color="fill_color")
graph_renderer.node_renderer.data_source.add(c, "fill_color")
plot.renderers.append(graph_renderer)
output_file("community_det.html")
show(plot)
