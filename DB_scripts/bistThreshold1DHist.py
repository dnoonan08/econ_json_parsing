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

    
def plot_bistThreshold(array,ECON_type,odir, tray_number='all'):
    
    #To plot all the D chips that failed the bist threshold test
    counts, bins, patches = plt.hist(array, bins= np.arange(0.8,1.34,0.02),color='b',alpha=0.5,label=f"Failing Voltage \u03BC:{np.mean(array):.3f} \u03C3:{np.std(array):.3f}")
    plt.title(f"{ECON_type} Bist Threshold")

    underflow_bist = np.sum(array < 0.8)
    overflow_bist = np.sum(array > 1.3)
    legend_text_bist = f'Underflow: {underflow_bist}, Overflow: {overflow_bist}'


    max_failing_voltage = np.max(array)
    q25, q50, q75 = np.percentile(array, [25, 50, 75])


    total_chips = len(array)


    plt.axvline(x=max_failing_voltage, color='black', alpha=0.5, label=f"Max Failing Voltage = {max_failing_voltage:.2f}", linestyle='--')

    plt.axvline(x=q25, color='red', alpha=0.5, label=f"25% Quantile = {q25:.2f}", linestyle='--')
    plt.axvline(x=q50, color='green', alpha=0.5, label=f"50% Quantile = {q50:.2f}", linestyle='--')
    plt.axvline(x=q75, color='blue', alpha=0.5, label=f"75% Quantile = {q75:.2f}", linestyle='--')
    plt.grid(color='black', linestyle='--', linewidth=.05)
    plt.gca().xaxis.set_minor_locator(plt.NullLocator())
    plt.legend([f"Failing Voltage \u03BC:{np.mean(array):.3f} \u03C3:{np.std(array):.3f}", 
                f"Max Failing Voltage = {max_failing_voltage:.2f}",
                f"25% Quantile = {q25:.2f}",
                f"50% Quantile = {q50:.2f}",
                f"75% Quantile = {q75:.2f}", 
                legend_text_bist], loc="best", fontsize='12')



    #plt.legend(loc="best",fontsize='15')
    max_count = max(counts)
    plt.ylim(0, 2.0* max_count)


    plt.ylabel('Count')
    plt.xlabel('Failing Voltage')
    plt.text(0.9, 1.8 * max_count, f'Total Chips: {total_chips}', fontsize=8, ha='center')

    plt.savefig(f'{odir}/Bist_Threshold_{ECON_type}_{tray_number}.png', dpi=300, facecolor = "w")
    plt.clf()


mongo = Database(args.dbaddress, client = 'econdDB')

tray_numbers = mongo.getTrayNumbers()

first_failure, bist_result = mongo.getBISTInfo()
plot_bistThreshold(first_failure, ECON_type='ECON-D', odir=odir)


for tray_number in tray_numbers:
    if tray_number in [10,11,12,13,70,71]: continue
    try:
        first_failure, bist_result = mongo.getBISTInfo(tray_number = tray_number)
        plot_bistThreshold(first_failure, ECON_type='ECON-D', odir=odir, tray_number=str(tray_number))
    except: continue

