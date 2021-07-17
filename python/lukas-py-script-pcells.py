# Python script

# Script to test KLayout's "Basic" PCell library components
# by Lukas Chrostowski, 2015/11

import pya

import numpy as n


def PCell_get_parameter_list ( cell_name, library_name ):
  # function to list all the parameters & defaults for a PCell
  # example usage:
  # PCell_get_parameter_list("CIRCLE", "Basic")

  print("* def PCell_get_parameter_list ( %s, %s): " % ( cell_name, library_name ))

  lib = pya.Library.library_by_name(library_name)
  if lib == None:
    raise Exception("Unknown lib '%s'" % library_name)

  pcell_decl = lib.layout().pcell_declaration(cell_name);
  if pcell_decl == None:
     raise Exception("Unknown PCell '%s'" % cell_name)

  type2s = ['TypeBoolean', 'TypeDouble', 'TypeInt', 'TypeLayer', 'TypeList', 'TypeNone', 'TypeShape', 'TypeString']

  for p in pcell_decl.get_parameters():
    if ~p.readonly:
      print("Name: %s, %s, unit: %s, default: %s, description: %s%s" % \
        (p.name, type2s[p.type], p.unit, p.default, p.description, ", hidden" if p.hidden else "."))

def PCell_get_parameters ( pcell ):
  # function to list the values for all parameters for an intantiated PCell
  # example usage:
  # ly = pya.Application.instance().main_window().current_view().active_cellview().layout() 
  # pcell = ly.create_cell("CIRCLE", "Basic", { "radius": 10, "layer": pya.LayerInfo(1, 0) } )
  # PCell_get_parameters( pcell )

  print("* def PCell_get_parameters ( %s ):" % pcell )
  print(pcell.pcell_parameters())

  params = pcell.pcell_parameters_by_name()

  for param in params.keys():
    print("Parameter: %s, Value: %s" % (param, params[param]))



cell = pya.Application.instance().main_window().current_view().active_cellview().cell
ly = pya.Application.instance().main_window().current_view().active_cellview().layout() 

# clean all cells within "cell"
ly.prune_subcells(cell.cell_index(), 10)

layer = pya.LayerInfo(1, 0)

PCell_get_parameter_list("CIRCLE", "Basic")
pcell = ly.create_cell("CIRCLE", "Basic", { "radius": 10.1, "layer": layer } )
t = pya.Trans(0, 0)
cell.insert(pya.CellInstArray(pcell.cell_index(), t))
PCell_get_parameters ( pcell )


PCell_get_parameter_list("DONUT", "Basic")
pcell = ly.create_cell("DONUT", "Basic", { "radius1": 9.75, "radius1": 10.25, "layer": layer } )
cell.insert(pya.CellInstArray(pcell.cell_index(), t))
PCell_get_parameters ( pcell )


PCell_get_parameter_list("TEXT", "Basic")
pcell = ly.create_cell("TEXT", "Basic", { "text": "KLayout + Python = fun!", "layer": layer } )
cell.insert(pya.CellInstArray(pcell.cell_index(), t))
PCell_get_parameters ( pcell )


"""
PCell_get_parameter_list("ROUND_PATH", "Basic")
points=n.array([ [0,0], [10,0], [10,10] ])
a1 = []
for p in points:
  a1.append (pya.DPoint(p[0], p[1]))
wg_path = pya.DPath(a1, w)
param = { "npoints": 100, "radius": 4, "path": wg_path, "layer": layer }
pcell = ly.create_cell("ROUND_PATH", "Basic", param )
cell.insert(pya.CellInstArray(pcell.cell_index(), t))
PCell_get_parameters ( pcell )
"""