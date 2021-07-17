
import pya

# create a layout
layout = pya.Layout()

# set database unit to um
layout.dbu = 1

# create layers
l255 = layout.layer(255,0)
l1 = layout.layer(1,0)

# create the top cell
top_cell = layout.create_cell("top")

# definition of dimensions
lines_w = [1, 2, 3, 4, 5, 10, 15] # list of lines width (um)
lines_l = 2500 # line length (um)
lines_n = 5 # number of lines in an array of lines
array_g = 10 # gap between arrays of lines

x = 0 # abcisse of the array of lines
for w in lines_w: # for each line width
  lines_g = w # gap between lines
  line_cell_name =  f"{w}um_line" # name of the cell containing one line
  line_cell =  layout.create_cell(line_cell_name) # create the cell containing one line
  line = line_cell.shapes(l1).insert(pya.Box(0, 0, w, lines_l)) # create line in a line cell
  # create an array of line cell's instances
  line_array = pya.CellInstArray(line_cell.cell_index(), pya.Trans(pya.Point(x,0)), pya.Vector(w+lines_g, 0), pya.Vector(0, 0), 5, 0)
  top_cell.insert(line_array)
  x += 5*(w+lines_g)+array_g
  lines_g = 3*w
  line_array = pya.CellInstArray(line_cell.cell_index(), pya.Trans(pya.Point(x,0)), pya.Vector(w+lines_g, 0), pya.Vector(0, 0), 5, 0)
  top_cell.insert(line_array)
  x += 5*(w+lines_g)+array_g
  
# export gds file
layout.write("C:\\Users\\Eric\\gdrive\\it-app\\klayout\\python\\test.gds")