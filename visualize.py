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
shapes = ['circle','pentagon']


# vertex and edge properties
cost = g.new_vertex_property("int")
name = g.new_vertex_property("string")

size = g.new_vertex_property("float")
shape = g.new_vertex_property("string")
color = g.new_vertex_property("string")

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

    for source in node["inputs"]:
        if source in indice:
            g.add_edge(indice[source],i)
            
        else:
            print(source, "is not in indices")

    if node['cost'] != 0:
        color[i] = 'green'
    else:
        color[i] = 'yellow'


graph_draw(g,
        vertex_halo = True,        
        vertex_halo_size = prop_to_size(cost, mi = 1.5, ma = 1.1),
        
        vertex_text = name,
        vertex_shape = shape,
        vertex_size = prop_to_size(cost,mi = 12, ma = 25),
        vertex_font_size = 14,
        vertex_text_position = 0,
        vertex_fill_color = color,
        
        edge_pen_width = 0.6
        # output_size = (1920,1080),
        # output = "output.png"
        )

'''
graph_draw(g,
        vertex_text = cost,
        vertex_shape = shape,
        vertex_font_size = 15,
        #vertex_text_position = 0,
        vertex_fill_color = color,
        # output_size = (1920,1080),
        # output = "output.png"
        )

'''

'''
pos = g.vp["pos"]
win = GraphWindow(g, pos, geometry=(500,400),
        vertex_text = name,
        vertex_shape = shape,
        vertex_font_size = 15,
        vertex_text_position = 0,
        vertex_fill_color = color,
        # output_size = (1920,1080),
        # output = "output.png"
        )

win.connect("delete_event", Gtk.main_quit)

win.show_all()
Gtk.main()
'''
