import numpy as np
import matplotlib.pyplot as plt
from dbClass import Database
import argparse
import os
parser = argparse.ArgumentParser()
parser.add_argument("--dbaddress", help="db address from local tunnel", default = 27017)
parser.add_argument("--odir", help="output directory", default = './plots')
args = parser.parse_args()
odir = args.odir + '/pllCapbank1D'
if not os.path.isdir(odir):
    os.makedirs(odir)
#A function to plot the capbank width
def plot_pllCapbankWidth(array,voltage,ECON_type,odir):
    plt.hist(array, 
             bins= np.arange(10,18,1)-0.5,
             color='b',
             alpha=0.5,
             label=f"Capbank width \u03BC:{np.mean(array):.3f} \u03C3:{np.std(array):.3f}")

    underflow = np.sum(array < 10)
    overflow = np.sum(array > 18)
    legend_text = f'Underflow: {underflow}, Overflow: {overflow}'

    plt.title(f"{ECON_type} Capbank Width [{voltage}]")
    plt.axvline(x=14,
                color='black', 
                alpha=0.5, 
                label="Thresold = 14", 
                linestyle='--')

    plt.grid(color='black', linestyle='--', linewidth=.05)
    plt.gca().xaxis.set_minor_locator(plt.NullLocator())
    plt.legend([f"Capbank width \u03BC:{np.mean(array):.3f} \u03C3:{np.std(array):.3f}",
                "Thresold = 14",
               legend_text],
               loc="best",fontsize='15')

    plt.ylabel('Count')
    plt.xlabel('Capbank Width')

    plt.savefig(f'{odir}/{ECON_type}_Capbank_Width [{voltage}].png', dpi=300, facecolor = "w")
    plt.clf()
    return plt

mongo = Database(args.dbaddress)

temp = [['1p08', '1p2', '1p32'], [1.08, 1.2, 1.32]]
for i in range(3):
    plot_pllCapbankWidth(mongo.pllCapbankWidthPlot(voltage=temp[0][i], econType = 'ECOND'), voltage = temp[1][i], ECON_type='ECON-D', odir=odir)
    plot_pllCapbankWidth(mongo.pllCapbankWidthPlot(voltage=temp[0][i], econType = 'ECONT'), voltage = temp[1][i], ECON_type='ECON-T', odir=odir)
