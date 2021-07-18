# klayout scripting tutorial
# create a box and save it to a gds file

import os
import pya # import python API (Application Programming Interface)

# create a layout
layout = pya.Layout()

# set database unit to um (default is nm)
layout.dbu = 1

# create a layer (return the layer index)
layer_1 = layout.layer(1,0)

# create a cell object
top = layout.create_cell("top")

# draw a box (rectangle) of size 10x20um
box = top.shapes(layer_1).insert(pya.Box(0, 0, 10, 20))

# export gds file
layout.write(os.path.dirname(__file__)+"/tuto-box.gds")