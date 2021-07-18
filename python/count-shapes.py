import pya

# create a unique representation of the application (klayout program)
app = pya.Application.instance()

# create the main window of the program
# (that include the menus, the tool panels, the layout views...)
mw = app.main_window()

# create a layout view, which is a representation of a layout tab
# can be multiple layout view. Here we select the current tab.
lv = mw.current_view()
# If there is no tab, a message is displayed and the program stop
if lv == None:
  pya.MessageBox.info("Shape Statistics",
    "No view selected.", pya.MessageBox.Ok)
  exit()

# Remark: the preparation step can be simplified  to:
# lv = pya.LayoutView.current()
# creation of app and mw was done for demonstration purpose

# set numbers of paths, polygons, boxes and texts to 0
paths = 0
polygons = 0
boxes = 0
texts = 0

# for each selected object, check the shape and add
# one to the number of corresponding shape
for sel in lv.each_object_selected():
  shape = sel.shape
  if shape.is_path():
    paths += 1
  elif shape.is_box():
    boxes += 1
  elif shape.is_polygon():
    polygons += 1
  elif shape.is_text():
    texts += 1

# Prepare the message reporting the number of shapes
s = f"Paths: {paths}\n"
s += f"Polygons: {polygons}\n"
s += f"Boxes: {boxes}\n"
s += f"Texts: {texts}\n"

# Report the number of shapes in a message box
pya.MessageBox.info("Shape Statistics", s, pya.MessageBox.Ok)