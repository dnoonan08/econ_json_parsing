import numpy as np
import matplotlib.pyplot as plt
from dbClass import Database
import argparse
import os
import pandas as pd
from collections import defaultdict
parser = argparse.ArgumentParser()
parser.add_argument("--dbaddress", help="db address from local tunnel", default = 27017)
parser.add_argument("--odir", help="output directory", default = './CSV')
args = parser.parse_args()

odir = args.odir + '/econdCSV'
if not os.path.isdir(odir):
    os.makedirs(odir)

db = Database(args.dbaddress, client = 'econdDB')
chip_results = defaultdict(lambda: defaultdict(float))
##TO DO: if there are multiple assert statements remove from the list and query the metadata from the table 
keysForPassFail = [
    'test_common_mode_erx_route',
    'test_errBit_roc_errin_1',
    'test_errBit_roc_errin_0',
    'test_fc_lock',
    'test_rw_allregisters_0',
    'test_rw_allregisters_255',
    'test_hard_reset_i2c_allregisters',
    'test_hold_hard_reset',
    'test_soft_reset_i2c_allregisters',
    'test_hold_soft_reset',
    'test_wrong_reg_address',
    'test_wrong_i2c_address',
    'test_alladdresses_0',
    'test_alladdresses_1',
    'test_alladdresses_2',
    'test_alladdresses_3',
    'test_alladdresses_4',
    'test_alladdresses_5',
    'test_alladdresses_6',
    'test_alladdresses_7',
    'test_alladdresses_8',
    'test_alladdresses_9',
    'test_alladdresses_10',
    'test_alladdresses_11',
    'test_alladdresses_12',
    'test_alladdresses_13',
    'test_alladdresses_14',
    'test_alladdresses_15',
    'test_chip_sync',
    'test_input_aligner_shift_shift0',
    'test_alignment_erx',
    'test_alignment_etx',
    'test_pll_lock_1_08',
    'test_pll_lock_1_32',
    'test_pll_lock_1_2',
    'test_reset_requests_setup',
    'test_reset_requests_watchdogs',
    'test_reset_requests_alert_limits',
    'test_reset_requests_bits',
    'test_clearing_fc',
    'test_serializer',
    
]
def stringReplace(word):
    if "[" in word:
        word = word.replace("[","_")
    if ".." in word:
        word = word.replace("..","_")
    if "/" in word:
        word = word.replace("/","_")
    if "]" in word:
        word = word.replace("]", "")
    if "." in word:
        word = word.replace(".","p")
    return word

print('Gathering all data')
## Get bist results
voltages, bist_results, chipNumBIST = db.getBISTInfoFull()
goodIdx = 0
for i, volt in enumerate(voltages):
    if volt != None:
        goodIdx = i
        break
## Get Pass/fail results
outcomes, chipNums, Timestamp, IP = db.getPassFailResults()
socket = replaced_arr = ['B' if x == '46' else 'A' for x in IP]
updatedTimestamp = [
    date.replace(year=2025) if date.year == 1970 else date for date in Timestamp
]

## get streamCompare results
word_err_count_0p99, word_err_count_1p03, word_err_count_1p08, word_err_count_1p20, chipNumSC = db.testStreamComparison()

## get current reading and temperature results
current, voltage, current_during_hardreset, current_after_hardreset, current_during_softreset, current_after_softreset, current_runbit_set, temperature, chipNumCurrent = db.getVoltageAndCurrentCSV()

## get results from teat_packets
results = db.retrieveTestPacketInfo()
chipNumsPacket = results['chipNum']
results = {key: value for key, value in results.items() if key != 'chipNum'}

## get results from I2C read/write errors
chipNumI2C, n_read_errors_asic, n_read_errors_emulator, n_write_errors_asic, n_write_errors_emulator= db.retrieveI2Cerrcnts()


print('writing data to csv')
## write results to a dictionary
## Add in pass/fail results and the timestamp
for i, chipNum in enumerate(chipNums):
    # arr = np.array(list(outcomes[i].values()))
    # if (np.isin(-1, arr) == True):
    #     continue
    for key in keysForPassFail:
        chip_results[chipNum][key] = outcomes[i][key]
    chip_results[chipNum]['Timestamp'] = updatedTimestamp[i]
    chip_results[chipNum]['Socket'] = socket[i]
    chip_results[chipNum]['Tray'] = str(chipNum)[:2]
    ## initializing these because some chips were not run on the streamCompare test
    chip_results[chipNum]['SCTestWordCount0p99V'] = None
    chip_results[chipNum]['SCTestErrCount0p99V'] = None
    chip_results[chipNum]['SCTestWordCount1p03V'] = None
    chip_results[chipNum]['SCTestErrCount1p03V'] = None
    chip_results[chipNum]['SCTestWordCount1p08V'] = None
    chip_results[chipNum]['SCTestErrCount1p08V'] = None
    chip_results[chipNum]['SCTestWordCount1p20V'] = None
    chip_results[chipNum]['SCTestErrCount1p20V'] = None
    

## add in results from current draw plus the temperature
for i, chipNum in enumerate(chipNumCurrent):
    chip_results[chipNum]['current'] = current[i]
    chip_results[chipNum]['current_during_hardreset'] = current_during_hardreset[i]
    chip_results[chipNum]['current_after_hardreset'] = current_after_hardreset[i]
    chip_results[chipNum]['current_during_softreset'] = current_during_softreset[i]
    chip_results[chipNum]['current_after_softreset'] = current_after_softreset[i]
    chip_results[chipNum]['current_runbit_set'] = current_runbit_set[i]
    chip_results[chipNum]['temperature'] = temperature[i]
## add in results for read/write errors of I2C test
for i, chipNum in enumerate(chipNumI2C):
    chip_results[chipNum]['n_read_errors_asic'] = n_read_errors_asic[i]
    chip_results[chipNum]['n_read_errors_emulator'] = n_read_errors_emulator[i]
    chip_results[chipNum]['n_write_errors_asic'] = n_write_errors_asic[i]
    chip_results[chipNum]['n_write_errors_emulator'] = n_write_errors_emulator[i]
## add in results for test packets
for i, chipNum in enumerate(chipNumsPacket):
    for key in results.keys():
        chip_results[chipNum][key] = results[key][i]
## add in results for SC test
for i, chipNum in enumerate(chipNumSC):
    ## These if/else statements are necessary because if there was a read error the query will return None since metadata does not exist
    ## but the standard data format looks like [timestamp, word count, error count] which will throw an error if the query returns None
    if word_err_count_0p99[i] == None:
        chip_results[chipNum]['SCTestWordCount0p99V'] = None
        chip_results[chipNum]['SCTestErrCount0p99V'] = None
    else:
        chip_results[chipNum]['SCTestWordCount0p99V'] = word_err_count_0p99[i][-1][1]
        chip_results[chipNum]['SCTestErrCount0p99V'] = word_err_count_0p99[i][-1][-1]
    if word_err_count_1p03[i] == None:
        chip_results[chipNum]['SCTestWordCount1p03V'] = None
        chip_results[chipNum]['SCTestErrCount1p03V'] = None
    else:
        chip_results[chipNum]['SCTestWordCount1p03V'] = word_err_count_1p03[i][-1][1]
        chip_results[chipNum]['SCTestErrCount1p03V'] = word_err_count_1p03[i][-1][-1]
    if word_err_count_1p08[i] == None:
        chip_results[chipNum]['SCTestWordCount1p08V'] = None
        chip_results[chipNum]['SCTestErrCount1p08V'] = None
    else:
        chip_results[chipNum]['SCTestWordCount1p08V'] = word_err_count_1p08[i][-1][1]
        chip_results[chipNum]['SCTestErrCount1p08V'] = word_err_count_1p08[i][-1][-1]
    if word_err_count_1p20[i] == None:
        chip_results[chipNum]['SCTestWordCount1p20V'] = None
        chip_results[chipNum]['SCTestErrCount1p20V'] = None
    else:
        chip_results[chipNum]['SCTestWordCount1p20V'] = word_err_count_1p20[i][-1][1]
        chip_results[chipNum]['SCTestErrCount1p20V'] = word_err_count_1p20[i][-1][-1]
        
## add bist results
for i, chipNum in enumerate(chipNumBIST):
    for j, volt in enumerate(voltages[goodIdx]):
        ## The if/else statement logic is the same as above 
        if bist_results[i] == None:
             chip_results[chipNum][f'OBTest_1_Result_{stringReplace(str(volt))}V'] = None
             chip_results[chipNum][f'OBTest_2_Result_{stringReplace(str(volt))}V'] = None
             chip_results[chipNum][f'OBTest_3_Result_{stringReplace(str(volt))}V'] = None
             chip_results[chipNum][f'OBTest_4_Result_{stringReplace(str(volt))}V'] = None
             chip_results[chipNum][f'PPTest_1_Result_{stringReplace(str(volt))}V'] = None
             chip_results[chipNum][f'PPTest_2_Result_{stringReplace(str(volt))}V'] = None
             chip_results[chipNum][f'PPTest_3_Result_{stringReplace(str(volt))}V'] = None
             chip_results[chipNum][f'PPTest_4_Result_{stringReplace(str(volt))}V'] = None
        else:
            chip_results[chipNum][f'OBTest_1_Result_{stringReplace(str(volt))}V'] = bist_results[i][j][0]
            chip_results[chipNum][f'OBTest_2_Result_{stringReplace(str(volt))}V'] = bist_results[i][j][1]
            chip_results[chipNum][f'OBTest_3_Result_{stringReplace(str(volt))}V'] = bist_results[i][j][2]
            chip_results[chipNum][f'OBTest_4_Result_{stringReplace(str(volt))}V'] = bist_results[i][j][3]
            chip_results[chipNum][f'PPTest_1_Result_{stringReplace(str(volt))}V'] = bist_results[i][j][4]
            chip_results[chipNum][f'PPTest_2_Result_{stringReplace(str(volt))}V'] = bist_results[i][j][5]
            chip_results[chipNum][f'PPTest_3_Result_{stringReplace(str(volt))}V'] = bist_results[i][j][6]
            chip_results[chipNum][f'PPTest_4_Result_{stringReplace(str(volt))}V'] = bist_results[i][j][7]

# Now, convert the defaultdict into a pandas DataFrame
# The outer dictionary (chip names) becomes the columns, and the inner dictionary keys (test names) become rows
df = pd.DataFrame.from_dict(chip_results, orient='index')

# Save the DataFrame to a CSV file
df.to_csv(f'{odir}/chip_test_results.csv')

print('Done!')
