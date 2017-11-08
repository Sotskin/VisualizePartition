import json
from graph_tool.all import *
from gi.repository import Gtk, Gdk

from pprint import pprint

data = open('alexnet_good_params.json','r')
nodes = json.load(data)["nodes"]

g = Graph()
g.add_vertex(len(nodes))

# indice dictionary to keep track of index for each vertex
indice = {}

shapes = ['circle','triangle']

# Variables defined for color
alpha = 0.9
base = [0, 15, 0, alpha]
ceil = [40, 20, 0]
rgb = {'R':0, 'r':1, 'C':2}
t = []
for i in range(0,3):
    t.append( (255-base[i]-ceil[i])/len(nodes[0]['partitions']) )
print(t)

# vertex and edge properties
cost = g.new_vertex_property("int")
name = g.new_vertex_property("string")

size = g.new_vertex_property("float")
shape = g.new_vertex_property("string")
color = g.new_vertex_property("vector<double>")

#g.edge_properties["cost"]=cost
#g.vertex_properties["name"]=name
#g.vertex_properties["shape"]=shape
#g.vertex_properties["color"]=color

for i in range(0,len(nodes)):
    node = nodes[i]
    indice[node['name']] = i
    
    name[i] = node['name']
    cost[i] = node['cost']
    
    shape[i] = shapes[(int)(node['op']=='null')]
    color[i] = base
    for part in node['partitions']:
        color[i][rgb[part]] += t[rgb[part]]
    for j in range(0,3):
        color[i][j] = color[i][j]/255

    # Add edges
    for source in node["inputs"]:
        if source in indice:
            g.add_edge(indice[source],i)
            
        else:
            print(source, "is not in indices")

graph_draw(g,
        vertex_halo = False, #True,
        vertex_halo_size = prop_to_size(cost, mi = 1.3, ma = 1.1),
        
        vertex_text = name,
        vertex_shape = shape,
        vertex_size = prop_to_size(cost,mi = 12, ma = 25),
        vertex_font_size = 14,
        vertex_text_position = 0,
        vertex_fill_color = color,
        
        edge_pen_width = 1
        # output_size = (1920,1080),
        # output = "output.png"
        )
