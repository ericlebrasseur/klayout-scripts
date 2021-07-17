
# import python API (Application Programming Interface)
import pya

# create a layout
layout = pya.Layout()

# set database unit to nm
layout.dbu = 0.001

# create layers (return the layers index)
l255 = layout.layer(255,0)
l1 = layout.layer(1,0)

# create cells
cell_top = layout.create_cell("top")
cell_cp = layout.create_cell("SqSiPHA45W100nm")

# draw the cp
S = 0.0707
P = 70.7
pts = [pya.DPoint(-S, 0), pya.DPoint(0, -S), pya.DPoint(S, 0), pya.DPoint(0, S)]
cp = pya.DPolygon(pts)
cell_cp.shapes(l1).insert(cp)
array_cell_cp = pya.CellInstArray(
  cell_cp.cell_index(),
  pya.DCplxTrans(1, 0, False, -50*1e3, -50*1e3),
  pya.DVector(0, 0),
  pya.DVector(P, P),
  1, 20)
cell_top.insert(array_cell_cp)

# export gds file
layout.write("C:\\Users\\Eric\\gdrive\\it-app\\klayout\\python\\slanted-array-test.gds")