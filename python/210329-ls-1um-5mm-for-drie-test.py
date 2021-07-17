import pya # import python module
import os

def adjustOriginCenter(layout, topcell):
  """
  adjust the cell origin to the center of the design
  """
  bbox= topcell.bbox()
  trans = pya.Trans.new(-bbox.center())
  for inst in layout.top_cell().each_inst():
    layout.top_cell().transform(inst,trans)
    
  for li in layout.layer_indices():
    for shape in layout.top_cell().each_shape(li):
      layout.top_cell().shapes(li).transform(shape,trans)
      layout.update()
  return(layout)

layout = pya.Layout() # create a layout
top_cell = layout.create_cell("top") # create the top cell
lines_cell = layout.create_cell("lines") # create the lines cell
layout.dbu = 0.001 # set database unit to nm
l255 =  pya.LayerInfo(255,0) # create LayerInfo for layer 255 (used for frames etc...)
l1_info = pya.LayerInfo(1,0) # create LayerInfo for layer 1
l1 = layout.insert_layer(l1_info) # layer 1 index

# definition of dimensions
lines_w = [0.5, 1, 2, 4, 8, 16, 32, 64, 128, 256, 512] # list of lines width (um)
for idx, val in enumerate(lines_w) : lines_w[idx] *= 1e3 # change lines widths unit to nm (=dbu)
lines_l = 4000*1e3 # line length (nm)
array_g = 10*1e3 # gap between arrays of lines (nm)
x = 0 # abcisse of the array of lines
n = 1 # number of lines in an array of lines
g = 10*1e3 # gap between each lines (nm)
    
for w in lines_w: # for each line width
  if w < 1000:
    formated_w = round(w/1000,1)
  else:
    formated_w = int(w/1000)
  line_cell_name =  f"{formated_w}um_line" # name of the cell containing one line
  line_cell =  layout.create_cell(line_cell_name) # create the cell containing one line
  line = line_cell.shapes(l1).insert(pya.Box(0, 0, w, lines_l)) # create line in a line cell
  # create an array of line cell's instances
  line_array = pya.CellInstArray(line_cell.cell_index(), pya.Trans(pya.Point(x, 0)), pya.Vector(w+g, 0), pya.Vector(0, 0), n, 0)
  lines_cell.insert(line_array)
  text_pcell =  layout.create_cell("TEXT", "Basic", {"text":f"{formated_w}", "layer": l1_info, "mag": 10, "font": 1})
  t = pya.Trans(x, -10000)
  lines_cell.insert(pya.CellInstArray(text_pcell.cell_index(), t))
  x += n*(w+g)+array_g

# repeat lines cell lines_n times
lines_n = 3 # number of lines_cell instances
lines_inst = pya.CellInstArray(lines_cell.cell_index(), pya.Trans(pya.Point(0, 0)), pya.Vector(x, 0), pya.Vector(0, 0), lines_n, 0)
top_cell.insert(lines_inst)

# add a larger area directly in top cell
large_area = top_cell.shapes(l1).insert(pya.Box(lines_n*x, 0, lines_n*x+1024000, lines_l))

adjustOriginCenter(layout, top_cell) # doesn't work with only an array of instances. Works if I add the large area.

# export gds file
cwd_path = (os.path.dirname(os.path.realpath(__file__))) # path of the directory where this script is
layout.write(cwd_path+"\\test.gds")