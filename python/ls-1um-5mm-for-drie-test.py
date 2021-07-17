import pya # import python module

def adjustOriginCenter(layout,topcell):
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
layout.dbu = 0.001 # set database unit to um
l255 =  pya.LayerInfo(255,0) # create LayerInfo for layer 255 (used for frames etc...)
l1_info = pya.LayerInfo(1,0) # create LayerInfo for layer 1
l1 = layout.insert_layer(l1_info) # layer 1 index

# definition of dimensions
lines_w = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096] # list of lines width (um)
for idx, val in enumerate(lines_w) : lines_w[idx] *= 1e3 # change lines widths unit to nm
lines_l = 4000*1e3 # line length (um)
array_g = 10*1e3 # gap between arrays of lines

x = 0 # abcisse of the array of lines
for w in lines_w: # for each line width
  if w  < 100*1e3: # number of lines and gap between lines depends on the line width
    n = 5
    g = w
  elif w > 100*1e3 and w < 1000*1e3:
    n = 3
    g = 100*1e3
  else:
    n =1
    g = 100*1e3
  line_cell_name =  f"{int(w/1000)}um_line" # name of the cell containing one line
  line_cell =  layout.create_cell(line_cell_name) # create the cell containing one line
  line = line_cell.shapes(l1).insert(pya.Box(0, 0, w, lines_l)) # create line in a line cell
  # create an array of line cell's instances
  line_array = pya.CellInstArray(line_cell.cell_index(), pya.Trans(pya.Point(x,0)), pya.Vector(w+g, 0), pya.Vector(0, 0), n, 0)
  top_cell.insert(line_array)
  text_pcell =  layout.create_cell("TEXT", "Basic", {"text":f"{int(w/1000)}", "layer": l1_info, "mag": 10, "font": 1})
  t = pya.Trans(x, -10000)
  top_cell.insert(pya.CellInstArray(text_pcell.cell_index(), t))
  x += n*(w+g)+array_g
  #g = 3*w
  #line_array = pya.CellInstArray(line_cell.cell_index(), pya.Trans(pya.Point(x,0)), pya.Vector(w+g, 0), pya.Vector(0, 0), n, 0)
  #top_cell.insert(line_array)
  #x += n*(w+g)+array_g
  
adjustOriginCenter(layout,top_cell)

# export gds file
layout.write("C:\\Users\\Eric\\gdrive\\it-app\\klayout\\python\\test.gds")