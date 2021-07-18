# klayout scripting tutorial
# rb-01-box.rb
# Eric Lebrasseur 201123

# create a layout
layout = RBA::Layout::new()

# set database unit to um (default is nm)
layout.dbu = 1

# create a layer (return the layer index)
layer_1 = layout.layer(1,0)

# create a cell object
top = layout.create_cell("top")

# draw a box (rectangle) of size 10x20um
box = top.shapes(layer_1).insert(RBA::Box::new(0, 0, 10, 20))

# export gds file into the directory where the script is (__dir__)
layout.write(__dir__+"/tuto-box.gds")