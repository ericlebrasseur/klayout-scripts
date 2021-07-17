import os
# import argparse
import json
import numpy as np
import pandas as pd
# import plotly.graph_objects as go
from sys import argv
# from plotly.subplots import make_subplots
# from scipy.linalg.basic import det
# from scipy.signal import savgol_filter
# from scipy import signal
# from scipy.signal import find_peaks
# from scipy.interpolate import interp1d

# NOTE for confocal microscope: only supports OLS5000 at 50x magnification
# NOTE for profilometer: only supports Dektak

# parser = argparse.ArgumentParser(description="Extract contrast curve data from profilometer or confocal microscope csv data.")
# parser.add_argument("file", metavar="fp", type=str, nargs="+", help="file or list of files")
# parser.add_argument("--d")
# args = parser.parse_args()

# Comment lines starting with "(EXP)" shows an example of what happen if the data file is "dektak-data.csv"

def detect_step_center(dt, max): # Added by Eric on 210601
    """Detect center of step (approximately) Eric's way"""
    x1, x2 = 0, 0 # indexes of ordinate max/2 before and after step respectively
    for i in range(len(dt)):
        if dt[i][1] > max*0.5:
            x1 = i
            break
    for i in range(x1+10, len(dt)):
        if dt[i][1] < max*0.5:
            x2 = i-1
            break
    return int(x1 + (x2-x1)/2)

fp = argv[2] # point to the data file that we put as the second argument (after --d) when we run this file

if argv[1] == "--d":
    # extract step size and start of data
    # I guess d stands for dektak
    with open(fp) as dektak_file:
        dektak_lines = dektak_file.readlines()
        step_size = round(float(dektak_lines[6].split(",")[1].split(" ")[0]),3)
            # (EXP) Line No 6 is: ScanResolution,0.0999933 µm → step_size = 0.1
        for i, line in enumerate(dektak_lines):
            if line == "Data\n":
                data_start = i + 2
        meas_num = len(dektak_lines) - data_start # (EXP) len(dektak_lines)=30024 data_start=23 meas_num=30001
        # (EXP) there is a total of 30001 measurement points starting from line 23

    # read csv data using pandas and put in a numpy array
    CSV_DATA = pd.read_csv(
        fp,
        skiprows=data_start,
        usecols=(0, 1),
        dtype="float64",
        index_col=False,
        header=None).to_numpy()

if argv[1] == "--c":
    # I guess c stand for confocal
    # TODO step_size extraction
    # read csv data
    SHAPE_TEST = pd.read_csv(
        fp,
        skiprows=18,
        index_col=False,
        header=None).to_numpy()
    CSV_DATA = pd.read_csv(
        fp,
        skiprows=18,
        usecols=range(1, SHAPE_TEST.shape[1]),
        dtype="float64",
        index_col=False,
        header=None).to_numpy()
    CSV_DATA = np.delete(CSV_DATA, 0, 0)
    CSV_DATA = np.delete(CSV_DATA, 0, 1)
    CSV_DATA = np.flipud(CSV_DATA)

# detect center of step using find_peaks from scipy.signal package
max_removed = np.max(np.abs(CSV_DATA), axis=0)[1] # value of the highest peak. (EXP) 14.2818312162016
# step_len = int(100 / step_size) 
# peaks, properties = find_peaks(-CSV_DATA[::, 1], height=[max_removed*.4, max_removed*.8], width=step_len/2)
# peaks is the index of the center of the step (EXP) 6752    

peaks = detect_step_center(abs(CSV_DATA), max_removed)

# detect start of slope
slope_start = peaks + int(200 / step_size)

# smooth slope data
CSV_DATA_SMOOTH = savgol_filter(CSV_DATA[::, 1][slope_start:slope_start + int(1023/ step_size)], 701, 3)

# create dose LUT (Look-Up Table) → dictonary with 1023 data {index: depth (um)}
DOSE_DICT = {int(x/10)+1:-np.average(CSV_DATA_SMOOTH[x:x+int(1/step_size)]) for x in range(0, len(CSV_DATA_SMOOTH), int(1/step_size))}

# add dose 0 to LUT (now 1024 data but index 0 is at the end)
DOSE_DICT[0]= 0.0

# sort dict by key ascending (to put the index 0 at the begining of the dictionary)
DOSE_DICT = sorted(DOSE_DICT.items(), key=lambda x: int(x[0]))


# create json output file
json_data = dict()
json_data["System"] = "Tokyo University 66+"
json_data["Substrate"] = "SiO2"
json_data["Resist"] = "AZ4620"
json_data["Writehead"] = "20mm"
json_data["Laser Power (mW)"] = 300
json_data["Filter"] = 100
json_data["nover"] = 10
json_data["CI"] = True
json_data["Dose LUT"] = DOSE_DICT

# save json
with open(f"{fp}.json", "w") as json_file:
    json.dump(json_data, json_file, indent=4)

exit()
# Plotting
fig = make_subplots(rows=2, cols=1, subplot_titles=(f"Raw data from {fp}", "Contrast Curve"))
fig.update_xaxes(title_text="Scan position (mm)", row=1, col=1)
fig.update_yaxes(title_text="Height (um)", row=1, col=1)
fig.update_xaxes(title_text="Dose (percent)", row=2, col=1)
fig.update_yaxes(title_text="Resist removed (um)", row=2, col=1)
fig.add_trace(go.Scatter(
    mode="markers", x=CSV_DATA[::,0], y=CSV_DATA[::, 1],
    name="Raw Data", marker=dict(size=5, color="blue")), row=1, col=1)
fig.add_trace(go.Scatter(
    mode="markers", x=CSV_DATA[::,0] + CSV_DATA[::,0][slope_start], y=CSV_DATA_SMOOTH,
    name="Smoothed Data", marker=dict(size=3, color="red")), row=1, col=1)
fig.add_trace(go.Scatter(
    mode="markers", x=CSV_DATA[::,0] + CSV_DATA[::,0][slope_start],
    y=np.linspace(0, -max_removed, num = len(CSV_DATA_SMOOTH)),
    name="Ideal response", marker=dict(size=3, color="purple")), row=1, col=1)
fig.add_trace(go.Scatter(
    mode="markers", x=np.linspace(0, 1, num=len(CSV_DATA_SMOOTH)), y=-CSV_DATA_SMOOTH,
    name="Resist removed", marker=dict(size=5, color="black")), row=2, col=1)
# dose lut values plotted
# fig.add_trace(go.Scatter(
#     mode="markers", x=np.linspace(0, 1, num=len(DOSE_DICT)), y=list(DOSE_DICT.values()),
#     name="Dose LUT values", marker=dict(size=3, color="red")), row=2, col=1)
fig.add_trace(go.Scatter(
    mode="markers", x=[CSV_DATA[peaks][0]], y=[CSV_DATA[peaks][1]],
    name="Detected center of step", marker=dict(size=5,color="red")), row=1, col=1)
# fig.write_html(f"{fp}.html")
fig.write_image(f"{fp}.png", width = 1920, height = 1080)