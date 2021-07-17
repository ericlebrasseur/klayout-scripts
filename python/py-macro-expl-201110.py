import pya

# The Application class #
##################

# Instance of the application object (unique)
app = pya.Application.instance()
print("Instance of the application object: ", app)

# user local storage path
print("User local storage path: ",app.application_data_path())

# names of the configuration parameters sorted
# inside the configuration database 
app_config_names = app.get_config_names()
print("Configuration parameters names: ",app_config_names)

# read the configuration database
# put in comment because there are too many
# print("Configuration parameters names and values:")
#for name in app_config_names:
# app_config = app.get_config(name)
#  print(f"  {name}: {app_config}")

# write the configuration database
# example with background-color parameter
app.set_config('background-color', '#402000')

# activate the setting that have been made with "set_config"
app.commit_config()
background_color = app.get_config('background-color')
print(f'background-color: {background_color}')
# set back the blue background color
app.set_config('background-color', '#002040')
app.commit_config()
background_color = app.get_config('background-color')
print(f'background-color: {background_color}')
# it seems that commit is not necessary in this case...

# returns the installation path (were the executable is located)
print("Installation path :", app.inst_path())

# returns true if klayout runs in editable mode
print("klayout runs in editable mode: ", app.is_editable())

# returns the KLAYOUT_PATH value. This is the search path
# were klayout looks for library files or macros.
print("KLAYOUT_PATH value: ", app.klayout_path())

# returns the MainWindow object (see below)
mw = app.main_window()
print("MainWindow object: ",mw)

# process pending events (enable to stop long operations)
print("Process pending events: ", app.process_events())

# reads the configuration database from a file
# does nothing if the config file does not exist as here
# and return false
print("Reads the configuration database from a file: ",
app.read_config('not_existing_config_file.txt'),
"(false because file does not exist)")

# sets a configuration parameter with the given name
# to a given value
# app.set_config(string name, string value)

# delivers klayout's version string
print("klayout's version: ", app.version())

# The MainWindow class #
###################

# cancel any pending operation and resets the mode
# to the default mode
mw.cancel()

# close the current tab
mw.close_current_view()

#close all tab
mw.close_all()

# methods bound to the menu items
# used to trigger a menu function from a script
# there are plenty of them!
# mw.cm_*

# create a new layout and load it into a layout view
# 0 → replace the current layout
# 1 → in a new view
# 2 → to the current view
layout = mw.create_layout(1)
print("Cell view of the created layout: ", layout)
# with a given technology
# mw.create(string tech, int mode)

# create a new empty tab (= view = LayoutView)
# return the index of the created view
view = mw.create_view()
print("Index of the created view: ", view)

# returns a LayoutView object (see below)
# which represent the current tab
cv = mw.current_view()
print("Reference to the current view's object: ", cv)
print("LayoutView.current: ", cv.current())

# returns the index of the current tab
print("Current view's index: ", mw.current_view_index)

# returns the LayoutView object from a view index
# the view index is the number of the tab (0 is the leftmost one)
print(mw.view(0))

# selects the view with the index given in this call
mw.current_view_index=(0)

# gets the global grid in micrometer units
print('Global grid unit: ', mw.grid_micron())

print(cv.box())