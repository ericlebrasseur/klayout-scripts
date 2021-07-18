import pya

# create a unique representation of the application (klayout program)
app = pya.Application.instance()

# create the main window of the program
# (that include the menus, the tool panels, the layout views...)
mw = app.main_window()

# create a layout view, which is a representation of a layout tab
# can be multiple layout view. Here we select the current tab.
lv = mw.current_view()
print(lv)

print(get_menu_symbols)

