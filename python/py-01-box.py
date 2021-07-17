# klayout scripting tutorial
# py-01-box.py
# Eric Lebrasseur 201123

# import python API (Application Programming Interface)
import pya

# create a layout
layout = pya.Layout()

# set database unit to nm
layout.dbu = 0.001

# create a layer (return the layer index)
layer_1 = layout.layer(1,0)

# create a cell object
top = layout.create_cell("top")

# draw a box (rectangle) of size 10x20um
box = cell.shapes(layer_1).insert(pya.Box(0, 0, 10*1e3, 20*1e3))

# export gds file
layout.write("C:\\Users\\ericl\\gdrive\\it-app\\klayout\\python\\py-test.gds")