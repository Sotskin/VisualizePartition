import random
import sys
import json
from math import pi
from graph_tool.all import *
from gi.repository import Gtk, Gdk

# Read json file.
if len(sys.argv) <= 1:
    print("Please input file name")
    exit()

try:
    data = open(sys.argv[1],'r')
    nodes = json.load(data)["nodes"]
except OSError:
    print("Json Not found")
    exit()

if len(sys.argv) > 2:
    outputname = sys.argv[2] + ".png"
else:
    outputname = "output.png"

# Initialize Graph
g = Graph()
g.add_vertex(len(nodes))

# indice dictionary to keep track of index for each vertex
indice = {}

shapes = ['circle','triangle']

# Variables defined for color. The color for the cut is generated randomly with a fixed seed.
alpha = 0.9
ptypes = len(nodes[0]['partition'])
psize = pow(3, ptypes)
rand_range = 100
random.seed(66666)
r_ran = random.sample(range(0, rand_range), psize)
b_ran = random.sample(range(0, rand_range), psize)
g_ran = random.sample(range(0, rand_range), psize)
rgb = {'R':0, 'r':1, 'C':2}
partname = ['R', 'r', 'C']
# vertex and edge properties
cost = g.new_vertex_property("int")
name = g.new_vertex_property("string")
shape = g.new_vertex_property("string")
color = g.new_vertex_property("vector<double>")
stroke_color = g.new_vertex_property("vector<double>")

text_pos = g.new_vertex_property("float")
text_offset = g.new_vertex_property("vector<double>")
pos = g.new_vertex_property("vector<double>")

# Add label nodes
px = 50
py = 50
pdifx = 150
pdify = 20
for i in range(0, psize):
    ln = g.add_vertex();
    pos[ln] = [px + (i//3)*pdifx, py + (i%3)*pdify]
    text_pos[ln] = 0
    shape[ln] = "square"
    color[ln] = [r_ran[i]/rand_range , g_ran[i]/rand_range , b_ran[i]/rand_range , alpha]
    label = ""
    tmp = i
    for j in range(0, ptypes):
        label = partname[tmp%3] + label
        tmp //= 3
    name[ln] = label

# pre-positions for each node
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
c = 0 # counter used for label tensor position
offset = 17 # text offset (vertical)


# Add nodes and edges to the graph
for i in range(0,len(nodes)):
    node = nodes[i]
    indice[node['name']] = i
    
    name[i] = node['name']
    cost[i] = node['cost']
    
    shape[i] = shapes[(int)(node['op']=='null')]
    stroke_color[i] = [0, 0, 0, .5]

    #Color
    ci = 0
    for part in node['partition']:
        ci *= 3
        ci += rgb[part]
    color[i] = [r_ran[ci]/rand_range , g_ran[ci]/rand_range , b_ran[ci]/rand_range , alpha]
    
    # Replica hidden node to print cost
    hidv = g.add_vertex()
    name[hidv] = "Cost = " + str(cost[i])
    
    # Calculate the position for each node
    # A series of assumptions is made about json file for this to work
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
        text_offset[hidv] = [0, offset]
    elif "weight" in name[i]:
        x = x_m
        y = y_m
        #x_m += 2*dif
        #text_offset[hidv] = [0, -offset]
        name[hidv] = ""
    elif "data" == name[i]:
        x = init_x
        y = init_y
        text_pos[i] = 0
        #text_offset[hidv] = [0, -offset]
        name[hidv] = ""
    elif "label" in name[i]:
        #x = x_m + (g.num_vertices()-4)/5*2*dif
        y = y_m
        text_pos[i] = 0
        #text_offset[hidv] = [0, -offset]
        name[hidv] = ""
    else:
        x = x_h
        y = y_h
        x_h += dif
        x_m += dif
        text_pos[i] = 3*pi/2
        text_offset[hidv] = [0, -offset]
    pos[i].append(x)
    pos[i].append(y)

    # Replica edge properties
    pos[hidv].append(x)
    pos[hidv].append(y)
    shape[hidv] = shape[i]
    color[hidv] = [0,0,0,0]
    stroke_color[hidv] = [0,0,0,0]
    text_pos[hidv] = text_pos[i]
    cost[hidv] = cost[i]
    

    # Add edges
    for source in node["inputs"]:
        if source in indice:
            g.add_edge(indice[source],i)
            
        else:
            print(source, "is not in indices")
    
# Set x position for "label" node
pos[0][0] = init_x + 50 + c*dif

graph_draw(g, pos = pos,
        fit_view = False,
        vertex_halo = False, #True,
        vertex_halo_size = prop_to_size(cost, mi = 1.3, ma = 1.1),
        

        vertex_text = name,
        vertex_shape = shape,
        vertex_size = prop_to_size(cost,mi = 22, ma = 35),
        vertex_font_size = 15,
        vertex_text_position = text_pos,
        vertex_text_offset = text_offset,
        vertex_color = stroke_color,
        vertex_fill_color = color,
        

        edge_pen_width = 3,
        bg_color = [1,1,1,1],
        output_size = (init_x*2 + 100 + c*dif, init_y * 2),
        output = outputname
        )


#graphviz_draw(g, pos = pos, 
#        size = (100, 100),
#        vprops = {
#            "label":name
#            
#            },
#        
#
#        output = "visoutput.png")
