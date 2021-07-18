include RBA

# create a new view (mode 1) with an empty layout
main_window = RBA::Application::instance.main_window
layout = main_window.create_layout(1).layout
layout_view = main_window.current_view

# set the database unit (shown as an example, the default is 0.001)
layout.dbu = 0.001

# create a cell
cell = layout.create_cell("TOP")

# create a layer
layer_index = layout.insert_layer(RBA::LayerInfo::new(10, 0))

# add a shape
cell.shapes(layer_index).insert(RBA::Box::new(0, 0, 1000, 2000))

# select the top cell in the view, set up the view's layer list and
# fit the viewport to the extensions of our layout
layout_view.select_cell(cell.cell_index, 0)
layout_view.add_missing_layers
layout_view.zoom_fit