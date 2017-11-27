import pandas as pd
import networkx as nx 
import numpy as np
from tqdm import *
from bokeh.io import show, output_file
from bokeh.plotting import figure
from bokeh.models.graphs import from_networkx
from bokeh.models import Plot, MultiLine, Circle
from bokeh.palettes import Spectral4

G = nx.read_gml("./MSDgraph_comm.gml")
fillcolor = nx.get_node_attributes(G, 'fillcolor')
T = nx.minimum_spanning_tree(G, weight='capacity', algorithm='prim')
betweeness = nx.betweenness_centrality(G, weight='capacity')
eig = nx.eigenvector_centrality(G, weight='capacity')
plot = figure(title="MSD User Listens in Common", x_range=(-1.1,1.1), y_range=(-1.1,1.1), 
	plot_width=800, plot_height=800)

nodes = T.nodes()
print('Number of nodes: ' + str(len(nodes)))
width = []
print(min(betweeness.values()))
print(max(betweeness.values()))

print(min(eig.values()))
print(max(eig.values()))
for n in nodes:
	width.append(betweeness[n])

graph_renderer = from_networkx(T, nx.spring_layout, scale=2, center=(0,0), weight='capacity')
graph_renderer.node_renderer.data_source.add(list(fillcolor.values()), 'fillcolor')
#graph_renderer.node_renderer.data_source.add(width, 'width')
graph_renderer.node_renderer.glyph = Circle(size=7, fill_color='fillcolor')
plot.renderers.append(graph_renderer)
output_file("min_span.html")
show(plot)