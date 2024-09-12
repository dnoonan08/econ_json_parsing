import numpy as np
import matplotlib.pyplot as plt
from dbClass import Database
import argparse
import os
parser = argparse.ArgumentParser()
parser.add_argument("--dbaddress", help="db address from local tunnel", default = 27017)
parser.add_argument("--odir", help="output directory", default = './plots')
args = parser.parse_args()
odir = args.odir + '/eTxDelayWidth1DHist'
if not os.path.isdir(odir):
    os.makedirs(odir)
def plot_eTxWidth(array,voltage,ECON_type,odir):
    plt.hist(array.flatten(), 
             bins= np.arange(13,28,1)-0.5,
             color='b',
             alpha=0.5,
             label=f"Max width \u03BC:{np.mean(array):.3f} \u03C3:{np.std(array):.3f}")

    underflow = np.sum(array < 13)
    overflow = np.sum(array > 27.5)
    legend_text = f'Underflow: {underflow}, Overflow: {overflow}'

    plt.title(f"{ECON_type} eTx width [{voltage}]")
    plt.axvline(x=15,
                color='black', 
                alpha=0.5, 
                label="Max Thresold = 15", 
                linestyle='--')

    plt.grid(color='black', linestyle='--', linewidth=.05)
    plt.gca().xaxis.set_minor_locator(plt.NullLocator())
    plt.legend([f"Max width \u03BC:{np.mean(array):.3f} \u03C3:{np.std(array):.3f}",
                "Max Threshold = 15",
                legend_text],
                loc='best',fontsize=15)

    plt.ylabel('Number of eTx')
    plt.xlabel('Phase width')

    plt.savefig(f'{odir}/Phase_width__of_all_eTx_{ECON_type} [{voltage}].png', dpi=300, facecolor = "w")

    plt.clf()
    return plt

mongo = Database(args.dbaddress)

temp = [['1p08', '1p2', '1p32'], [1.08, 1.2, 1.32]]
for i in range(3):
    plot_eTxWidth(mongo.etxMaxWidthPlot(voltage=temp[0][i], econType = 'ECOND'), voltage = temp[1][i], ECON_type='ECON-D', odir=odir)
    plot_eTxWidth(mongo.etxMaxWidthPlot(voltage=temp[0][i], econType = 'ECONT'), voltage = temp[1][i], ECON_type='ECON-T', odir=odir)

