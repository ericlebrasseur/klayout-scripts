
import pya

# create a layout
layout = pya.Layout()

# set database unit to um
layout.dbu = 1

# create layers
l255 = layout.layer(255,0)
l1 = layout.layer(1,0)

# create a cell object
cell_line_1um = layout.create_cell("line_1um")

# draw a line (box)
line_1um = cell_line_1um.shapes(l1).insert(pya.Box(0, 0, 1, 2500))
cell_line_1um.shapes(l255).insert(pya.Box(-100, -100, 101, 2600))

# export gds file
layout.write("C:\\Users\\Eric\\gdrive\\it-app\\klayout\\python\\test.gds")