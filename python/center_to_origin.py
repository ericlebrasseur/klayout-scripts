def adjustOriginLowerLeft(layout,topcell):
  """
  adjust the cell origin to the lower left corner of the design
  """
  bbox= topcell.bbox()
  trans = pya.Trans(pya.Point((-bbox.left), (-bbox.bottom)))
  # all instances 
  for inst in layout.top_cell().each_inst():
    layout.top_cell().transform(inst,trans)

  # all shapes
  for li in layout.layer_indices():
    for shape in layout.top_cell().each_shape(li):
      layout.top_cell().shapes(li).transform(shape,trans)
      layout.update()
    return(layout)

def adjustOriginCenter(layout,topcell):
  """
  adjust the cell origin to the center of the design
  """
  import pya
  bbox= topcell.bbox()
  trans = pya.Trans.new(-bbox.center())
  for inst in layout.top_cell().each_inst():
    layout.top_cell().transform(inst,trans)

  for li in layout.layer_indices():
    for shape in layout.top_cell().each_shape(li):
      layout.top_cell().shapes(li).transform(shape,trans)
      layout.update()
  return(layout)