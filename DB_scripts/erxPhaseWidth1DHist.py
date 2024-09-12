import numpy as np
import matplotlib.pyplot as plt
from dbClass import Database
import argparse
import os
parser = argparse.ArgumentParser()
parser.add_argument("--dbaddress", help="db address from local tunnel", default = 27017)
parser.add_argument("--odir", help="output directory", default = './plots')
args = parser.parse_args()
odir = args.odir + '/eRxPhaseWidth1DHist'
if not os.path.isdir(odir):
    os.makedirs(odir)
def plot_eRxPhaseWidth(array,voltage,ECON_type,odir):
    plt.hist(array.flatten(), 
             bins= np.arange(0,9,1)-0.5,
             color='b',
             alpha=0.5,
             label=f"eRx Phase width \u03BC:{np.mean(array):.3f} \u03C3:{np.std(array):.3f}")

    underflow = np.sum(array < 0)
    overflow = np.sum(array > 9)
    legend_text = f'Underflow: {underflow}, Overflow: {overflow}'

    plt.title(f"{ECON_type} eRx width [{voltage}]")
    plt.axvline(x=3,
                color='black', 
                alpha=0.5, 
                label="Thresold = 3", 
                linestyle='--')

    plt.grid(color='black', linestyle='--', linewidth=.05)
    plt.gca().xaxis.set_minor_locator(plt.NullLocator())
    plt.legend([f"eRx Phase width \u03BC:{np.mean(array):.3f} \u03C3:{np.std(array):.3f}",
                "Thresold = 3",
               legend_text],
               loc="upper left",fontsize='15')

    plt.ylabel('Number of eRx')
    plt.xlabel('Phase width')

    plt.savefig(f'{odir}/Phase_width__of_all_eRx_{ECON_type} [{voltage}].png', dpi=300, facecolor = "w")


    return plt

mongo = Database(args.dbaddress)

temp = [['1p08', '1p2', '1p32'], [1.08, 1.2, 1.32]]
for i in range(3):
    plot_eRxPhaseWidth(mongo.prbsMaxWidthPlot(voltage=temp[0][i], econType = 'ECOND'), voltage = temp[1][i], ECON_type='ECON-D', odir= odir)
    plot_eRxPhaseWidth(mongo.prbsMaxWidthPlot(voltage=temp[0][i], econType = 'ECONT'), voltage = temp[1][i], ECON_type='ECON-T', odir= odir)
