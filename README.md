# VisualizePartition
Partition graph visualization for rltofu json output



Create a way of visualizing a dataflow graph, its partitions, and the communication cost incurred at each part of the graph.

Visualization library / program used: **graph-tool**. Version 2.24-1 for python3

Scheme for data input, including the level of granularity for the communication cost (per-node, per-edge and node): See **Json** folder for sample



**TO-DO**

Use Size & Color to represent the cost of node: The larger the bigger 

Use Shape to distinguish tensor and operator

Temp: Use Circle halo color to represent the partition type (Could use color instead)



GTK: 

Show detailed information when mouth selected a node

At somewhere, shows a label that shows correspondence between color/shape and meanings

