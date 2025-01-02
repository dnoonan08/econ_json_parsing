from http import client
import numpy as np
import matplotlib.pyplot as plt
from dbClass import Database
import argparse
from matplotlib import colors
import matplotlib.colors as mcolors
import matplotlib.patches as mpatches


from slack_sdk import WebClient

from matplotlib.ticker import PercentFormatter
import os
import pandas as pd
parser = argparse.ArgumentParser()
parser.add_argument("--dbaddress", help="db address from local tunnel", default = 27017)
parser.add_argument("--odir", help="output directory", default = './plots')
parser.add_argument("--tray", help="tray to run on", default = 26)
parser.add_argument("--econType", help="ECOND or ECONT", default = 'ECOND')
args = parser.parse_args()

odir = args.odir + '/summary'
if not os.path.isdir(odir):
    os.makedirs(odir)

def send_slack(message):
    client = WebClient(token="xoxb-6330326503621-6564241964674-WW41OQd73lgPCM8eGgFgJBLI")

    result = client.chat_postMessage(
            channel = "cms-econ-asic", 
            text = message,
            username = "Bot User")

    return result

def send_slack_image(image_path):
    client = WebClient(token="xoxb-6330326503621-6564241964674-WW41OQd73lgPCM8eGgFgJBLI")

    with open(image_path, "rb") as file_content:
        result = client.files_upload(
        channels="cms-econ-asic",
        file=file_content,
        filename="image.png",
        title="PNG Image"
        )

def trayChipPlot(chip_numbers, results, econType, odir,tray_number):
    """
    Generates a 2D plot representing a tray of 6x15 chips with colors indicating test pass fractions.

    Parameters:
        chip_numbers: list of chip numbers (1 to 90)
        results: list of fractions of tests passed (values between 0 and 1)
        econType: string representing the ECON chip type
        odir: output directory to save the plot
    """
    # Define tray dimensions
    rows, cols = 15, 6
    tray = np.full((rows, cols), -1,dtype=float)

    text_labels = np.full((rows, cols), '', dtype=object)
    chip_labels = np.full((rows, cols), '', dtype=object)

    
    # Fill the tray with results based on chip numbers
    for chip, fraction in zip(chip_numbers, results):
        row = ( 89 - (chip - 1)) // cols
        col = (89 - (chip - 1)) % cols

        tray[row, col] = fraction
        text_labels[row, col] = f"{fraction:.0%}"  # Convert fraction to percentage
        chip_labels[row,col] = f"{chip}"
    
    # Create the figure
    fig, ax = plt.subplots(figsize=(6, 15))  # Adjust figsize for better visualization
    #cmap = plt.get_cmap("RdYlGn")  # Red to Green colormap
    #norm = mcolors.Normalize(vmin=0, vmax=1)  # Normalize values between 0 and 1


    #cmap_colors = [
    #    (1, 0, 0),  # Red for 0
    #    (1, 1, 0),  # Yellow for 0.99
    #    (0, 1, 0)   # Green for 1
    #]
    #cmap = mcolors.LinearSegmentedColormap.from_list("custom", cmap_colors, N=256)
    
    # Define normalization: linear scaling up to 0.99, then distinct for 1.0
    #norm = mcolors.Normalize(vmin=0, vmax=1)
    # Plot heatmap

        # Define the colormap with distinct green for 1 and a gradient from red to yellow for <1
    cmap_color = [(1, 1, 1), (1, 0, 0), (1, 0.5, 0), (0, 1, 0)]  # White, Red, Orange, Green
    thresholds = [-1, 0, 0.5, 0.99, 1.0]  # White for -1, Red for 0-0.5, Orange for 0.5-0.99, Green for 1.0

    # Create the colormap and normalization
    cmap = mcolors.LinearSegmentedColormap.from_list("custom", cmap_color, N=256)
    norm = mcolors.BoundaryNorm(thresholds, cmap.N)

    cax = ax.imshow(tray, cmap=cmap, norm=norm, aspect="auto")
    
    # Add text labels
    for i in range(rows):
        for j in range(cols):
            ax.text(j, i, text_labels[i, j], ha='center', va='center', fontsize=8, color='black')
            ax.text(j+0.1, i+ 0.1, chip_labels[i, j], ha='center', va='center', fontsize=4, color='black')

    
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)


    ax.set_title(f"Tray {tray_number} Chip Summary for ECON Type {econType}")
    
    # Add colorbar
    #cbar = fig.colorbar(cax, ax=ax)
    #cbar.set_label("Fraction of Tests Passed")
    # Create custom legend
    legend_patches = [
    mpatches.Patch(color='white', label='No test'),
    mpatches.Patch(color='red', label='Hard fail'),
    mpatches.Patch(color='orange', label='Fail'),
    mpatches.Patch(color='green', label='Pass')
    ]
    ax.legend(handles=legend_patches, loc='upper left', bbox_to_anchor=(1, 1), title='Categories')

    # Save the plot
    image_path = f"{odir}/tray_{tray_number}_chip_summary_{econType}.png"
    fig.savefig(image_path, dpi=300, bbox_inches="tight")
    plt.close(fig)
    return image_path
   
if args.econType == 'ECOND':
    mongo = Database(args.dbaddress, client='econdDB')
elif args.econType == 'ECONT':
    mongo = Database(args.dbaddress, client='econtDB')


tray = args.tray
econdFracPassed, econd_chip_numbers = mongo.getFractionOfTestsPassed(econType=args.econType, tray_number=tray)
econd_chip_numbers = econd_chip_numbers-int(tray)*100

daq_asic,daq_emu, daq_counter, word_count = mongo.testOBErrorInfo(econType=args.econType, voltage = '0p99', tray_number=tray)
print(len(daq_asic), len(daq_emu), len(word_count))


#print(econd_chip_numbers,econdFracPassed)
image_path = trayChipPlot(econd_chip_numbers,econdFracPassed, econType = 'ECOND', odir = odir, tray_number=tray)

#send_slack_image(image_path)

