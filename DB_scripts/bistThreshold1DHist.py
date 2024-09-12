import numpy as np
import matplotlib.pyplot as plt
from dbClass import Database
import argparse
import os
parser = argparse.ArgumentParser()
parser.add_argument("--dbaddress", help="db address from local tunnel", default = 27017)
parser.add_argument("--odir", help="output directory", default = './plots')
args = parser.parse_args()

odir = args.odir + '/bistThreshold'
if not os.path.isdir(odir):
    os.makedirs(odir)

    
def plot_bistThreshold(array,ECON_type,odir):
    
    #To plot all the D chips that failed the bist threshold test
    plt.hist(array, bins= np.arange(0.8,1.3,0.01),color='b',alpha=0.5,label=f"Failing Voltage \u03BC:{np.mean(array):.3f} \u03C3:{np.std(array):.3f}")
    plt.title(f"{ECON_type} Bist Threshold")

    underflow_bist = np.sum(array < 0.8)
    overflow_bist = np.sum(array > 1.3)
    legend_text_bist = f'Underflow: {underflow_bist}, Overflow: {overflow_bist}'

    plt.axvline(x=1.01, color='black', alpha=0.5, label="Max Failing Voltage = 1.01", linestyle='--')
    plt.grid(color='black', linestyle='--', linewidth=.05)
    plt.gca().xaxis.set_minor_locator(plt.NullLocator())
    plt.legend([f"Failing Voltage \u03BC:{np.mean(array):.3f} \u03C3:{np.std(array):.3f}", 
                "Max Failing Voltage = 1.01", 
                legend_text_bist], loc="best", fontsize='15')


    #plt.legend(loc="best",fontsize='15')

    plt.ylabel('Count')
    plt.xlabel('Failing Voltage')

    plt.savefig(f'{odir}/Bist_Threshold_{ECON_type}.png', dpi=300, facecolor = "w")


mongo = Database(args.dbaddress)

first_failure, bist_result = mongo.getBISTInfo()
plot_bistThreshold(first_failure, ECON_type='ECON-D', odir=odir)


