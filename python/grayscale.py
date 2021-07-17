import pya
import os

app = pya.Application.instance
mw = app.main_window

# create a new layout
mw.create_layout(0)
view = mw.current_view()
cv = view.cellview(0)

# create a new layer in that layout
layout = cv.layout
layer_ids = []

