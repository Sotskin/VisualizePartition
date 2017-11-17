import json
from graph_tool.all import *
from gi.repository import Gtk, Gdk
import sys
from math import pi
from pprint import pprint

if len(sys.argv) <= 1:
    print("Please input file name")
    exit()

try:
    data = open(sys.argv[1],'r')
    nodes = json.load(data)["nodes"]
except OSError:
    print("Json Not found")
    exit()

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
    t.append( (255-base[i]-ceil[i])/len(nodes[0]['partition']) )

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

text_pos = g.new_vertex_property("float")

pos = g.new_vertex_property("vector<double>")
init_x = 200
init_y = 300
x_h = init_x + 100
y_h = init_y - 100
x_m = init_x + 100
y_m = init_y + 0
x_l = init_x + 100
y_l = init_y + 100
dif = 230
flag = True
c = 0
#pi = math.pi

for i in range(0,len(nodes)):
    node = nodes[i]
    indice[node['name']] = i
    
    name[i] = node['name'] + "\x0c test"
    cost[i] = node['cost']
    
    shape[i] = shapes[(int)(node['op']=='null')]
    color[i] = base
    for part in node['partition']:
        color[i][rgb[part]] += t[rgb[part]]
    for j in range(0,3):
        color[i][j] = color[i][j]/255

    x = 0
    y = 0
    if "backward" in name[i]:
        if flag:
            x_l = x_h - dif
            flag = False
        x = x_l
        y = y_l
        x_l -= dif
        c += 1
        text_pos[i] = pi/2
    elif "weight" in name[i]:
        x = x_m
        y = y_m
        #x_m += 2*dif
    elif "data" == name[i]:
        x = init_x
        y = init_y
        text_pos[i] = 0
    elif "label" in name[i]:
        #x = x_m + (g.num_vertices()-4)/5*2*dif
        y = y_m
        text_pos[i] = 0
    else:
        x = x_h
        y = y_h
        x_h += dif
        x_m += dif
        text_pos[i] = 3*pi/2
    pos[i].append(x)
    pos[i].append(y)
    x+=dif
    y+=dif
    # Add edges
    for source in node["inputs"]:
        if source in indice:
            g.add_edge(indice[source],i)
            
        else:
            print(source, "is not in indices")

pos[0][0] = init_x + 100 + c*dif

A = graph_draw(g, pos = pos,
        fit_view = False,
        vertex_halo = False, #True,
        vertex_halo_size = prop_to_size(cost, mi = 1.3, ma = 1.1),
        
        vertex_text = name,
        vertex_shape = shape,
        vertex_size = prop_to_size(cost,mi = 12, ma = 25),
        vertex_font_size = 14,
        vertex_text_position = text_pos,
        vertex_fill_color = color,
        

        edge_pen_width = 1,
        bg_color = [1,1,1,1],
        output_size = (init_x*2 + 100 + c*dif, init_y * 2),
        output = "output.png"
        )

for a in A[0]:
    print(a)
