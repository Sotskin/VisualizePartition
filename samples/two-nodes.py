from graph_tool.all import *

g = Graph()
g.add_vertex(2)
g.add_edge(0,1)

cost = g.new_edge_property("int")
name = g.new_vertex_property("string")
part = g.new_vertex_property("string")

name[0]="softmax/label"
name[1]="data"
part[0]="circle"
part[1]="square"

cost[g.edge(0,1)] = 100

g.edge_properties["cost"]=cost
g.vertex_properties["name"]=name
g.vertex_properties["part"]=part

graph_draw(g,
        vertex_text = name,
        vertex_shape = part,
        vertex_font_size = 20, 
        edge_text = cost,
        edge_font_size = 20,

        output_size = (600,600),
        output = "two-nodes.png"
        )
