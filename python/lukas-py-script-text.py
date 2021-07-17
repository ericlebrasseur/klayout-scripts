# how to write text with python script

import pya
import numpy as n

cell = pya.Application.instance().main_window().current_view().active_cellview().cell
ly = pya.Application.instance().main_window().current_view().active_cellview().layout() 

# clean all cells within "cell"
# ly.prune_subcells(cell.cell_index(), 10)

layer = pya.LayerInfo(1, 0)

pcell = ly.create_cell("TEXT", "Basic", { "text": "HELLO", "layer": layer, "mag": 15 } )
t = pya.Trans(0, 0)
cell.insert(pya.CellInstArray(pcell.cell_index(), t))
