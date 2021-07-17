import pya # import python module
import os # needed to find the script directory (in the second last line)

def adjustOriginCenter(frame):
  """
  adjust the cell origin to the center of the design
  """
  trans = pya.Trans.new(-frame.center())
  for inst in layout.top_cell().each_inst():
    layout.top_cell().transform(inst,trans)
    
  for li in layout.layer_indices():
    for shape in layout.top_cell().each_shape(li):
      layout.top_cell().shapes(li).transform(shape,trans)
      layout.update()
  return(layout)


layout = pya.Layout() # create a layout
top_cell = layout.create_cell("top") # create the top cell

layout.dbu = 0.001 # set database unit to nm
l255 =  pya.LayerInfo(255,0) # create LayerInfo for layer 255 (used for frames etc...)
l1_info = pya.LayerInfo(1,0) # create LayerInfo for layer 1
l1 = layout.insert_layer(l1_info) # layer 1 index

# definition of dimensions
lines_w = [1, 3, 5, 7, 9, 11] # list of lines width (um)
lines_w_variation = [1, 1.2, 1.4, 1.6, 1.8, 2] # distance added to the line width in order to take into account
                                                                    # the resist width reduction + the under etching
for idx, val in enumerate(lines_w) : lines_w[idx] *= 1e3 # change lines widths unit to nm (=dbu)
for idx, val in enumerate(lines_w_variation) : lines_w_variation[idx] *= 1e3 # change lines widths unit to nm (=dbu)
pitch = 200*1e3 # line width + holes width (nm)
lines_l = 200*1e3 # line length (nm)
x = 0 # abcissa of the first line
y = 0 # ordinate of the 200um-lines cell instances

lines200um_cell = layout.create_cell("200um-lines") # create the 200um long lines cell
for w in lines_w: # for each line width
  for var in lines_w_variation: # for each line variation
    line = pya.Box(x, 0, x + pitch - w - var, lines_l) # create a line
    lines200um_cell.shapes(l1).insert(line) # put the line in the 200um-lines cell
    x += pitch
line = pya.Box(x, 0, x + pitch - w - var, lines_l) # create a line
lines200um_cell.shapes(l1).insert(line)

# copy n instances of 200um-lines cells in top cells
inst_n = 15 # number of cell instances
inst = pya.CellInstArray(lines200um_cell.cell_index(), pya.Trans(pya.Point(0, y)), pya.Vector(0, 0), pya.Vector(0, lines_l+10*1e3), 1, inst_n)
top_cell.insert(inst)

# same with lines length of 1000um
lines_l = 1000*1e3 # line length (nm)
x = 0 # abcissa of the first line
y = 4000*1e3 # ordinate of the 1000um-lines cell instances

lines1000um_cell = layout.create_cell("1000um-lines") # create the 1000um long lines cell
for w in lines_w: # for each line width
  for var in lines_w_variation: # for each line variation
    line = pya.Box(x, 0, x + pitch - w - var, lines_l) # create a line
    lines1000um_cell.shapes(l1).insert(line) # put the line in the 1000um-lines cell
    x += pitch
line = pya.Box(x, 0, x + pitch - w - var, lines_l) # create a line
lines1000um_cell.shapes(l1).insert(line)
x += pitch

# copy n instances of 200um-lines cells in top cells
inst_n = 3 # number of cell instances
inst = pya.CellInstArray(lines1000um_cell.cell_index(), pya.Trans(pya.Point(0, y)), pya.Vector(0, 0), pya.Vector(0, lines_l+10*1e3), 1, inst_n)
top_cell.insert(inst)

frame = pya.Box.new(0, 0, x, y+inst_n*lines_l) # this is the surrouding area of the complete design
adjustOriginCenter(frame) # shift everything in the top 

# export gds file
cwd_path = (os.path.dirname(os.path.realpath(__file__))) # path of the directory where this script is
layout.write(cwd_path+"\\210616-otomo.gds")

