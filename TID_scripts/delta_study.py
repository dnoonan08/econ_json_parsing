import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import argparse
import os

parser = argparse.ArgumentParser(description='Args')
parser.add_argument('--path', default='../../', type=str)  # repo name on github json repo
parser.add_argument('--chip', default='chip005-econd')  # repo name on github
parser.add_argument('--type', default='pp')  # repo name on github
parser.add_argument('--test', default='1')  # repo name on github

args = parser.parse_args()

# Read the CSV file
df = pd.read_csv('../../bist-study-averages/bist-csv/%s_%s_test%s.csv' % (args.chip, args.type, args.test))

# Convert TIMESTAMPS to datetime
df['TIMESTAMPS'] = pd.to_datetime(df['TIMESTAMPS'])

# Calculate the time in hours since the first timestamp
df['Time (hours)'] = (df['TIMESTAMPS'] - df['TIMESTAMPS'].iloc[0]).dt.total_seconds() / 3600

first_xrayon_time = df.loc[df['XRAYON'] == True, 'Time (hours)'].iloc[0]
first_tid_10_time = df.loc[df['TID'] >= 10, 'Time (hours)'].iloc[0]

midpoint = len(df) // 2

def find_max_min_sram_values(df, sram_col, window=3):
# Find the maximum value that occurs more than twice
    value_counts = df[sram_col].value_counts()
    max_value = value_counts[value_counts > 25].index.max()
    max_index = df[df[sram_col] == max_value].index[0]
    max_tid = df.loc[max_index, 'TID']

    rolling_min = df[sram_col][max_index:].rolling(window=window, center=True).min()
    min_index_after_max = rolling_min.idxmin()
    min_value_after_max = df.loc[min_index_after_max, sram_col]
    min_tid_after_max = df.loc[min_index_after_max, 'TID']

    if min_index_after_max > max_index and          min_value_after_max < max_value:
        return max_value, max_tid, min_value_after_max, min_tid_after_max
    else:
        return max_value, max_tid, None, None

def find_min(df, sram_col):
# Find the maximum value that occurs more than twice
    value_counts = df[sram_col].value_counts()
    min_value = value_counts[value_counts > 10].index.min()
    min_index = df[df[sram_col] == min_value].index[0]
    min_tid = df.loc[min_index, 'TID']
    return min_value, min_tid

# Function to save interesting results to CSV
def save_interesting_results(chip, type, test ,sram_number, first_sram_value, max_value, max_tid, min_value_after_max, min_tid_after_max, xray_on_voltage, tid_10_voltage, min_temp_sram_value):
    results_file = '../../bist-study-averages/results-csv/results_%s_%s.csv'%(type,test)
    new_entry = {
    'chip': chip.replace('chip00','').replace('-econd-sw',''),
    'sram_number': sram_number,
    'first_sram_value': first_sram_value,
    'min_temp_sram_value': min_temp_sram_value,
    #'max_tid': max_tid,
    #'min_tid_after_max': min_tid_after_max,
    'xray_on_voltage': xray_on_voltage,
    'tid_10_voltage': tid_10_voltage,
    'max_value': max_value,
    'delta_min_start' : min_temp_sram_value-first_sram_value,
    'delta_xray_on_min' : xray_on_voltage-min_temp_sram_value,
    'delta_tid10_xray' : tid_10_voltage-xray_on_voltage,
    'delta_tid10_min' : tid_10_voltage-min_temp_sram_value,
    'delta_tidmax_tid10' : max_value - tid_10_voltage,
    'min_value_after_max': min_value_after_max,
    
    }

    if os.path.exists(results_file):
        results_df = pd.read_csv(results_file)
        if not ((results_df['chip'] == chip) & (results_df['sram_number'] == sram_number)).any():
            results_df = results_df._append(new_entry, ignore_index=True)
            results_df.to_csv(results_file, index=False)
    else:
        results_df = pd.DataFrame([new_entry])
        results_df.to_csv(results_file, index=False)


def save_all_results(chip, type, test ,sram_number, first_sram_value, max_value, max_tid,min_value, min_value_after_max, min_tid_after_max, xray_on_voltage, tid_10_voltage, min_temp_sram_value):

    if min_value_after_max:
        min_value_after_max = round(min_value_after_max,3)
    results_file = '../../bist-study-averages/results-csv/results_all.csv'
    new_entry = {
    'chip': chip.replace('chip00','').replace('-econd',''),
    'type' : type,
    'test' : test,
    'sram_number': sram_number,
    'Vstart': round(first_sram_value,3),
    'Vmin_temperature': round(min_temp_sram_value,3),
    #'max_tid': max_tid,
    #'min_tid_after_max': min_tid_after_max,
    'VTID0': round(xray_on_voltage,3),
    'VTID10': round(tid_10_voltage,3),
    'Vmin': round(min_value,3),
    'Vmax': round(max_value,3),
    'Vmin_after_max': min_value_after_max,
    'Δ(Vmin_temperature-Vstart)' : round(min_temp_sram_value-first_sram_value,3),
    'Δ(VTID0-Vmin_temperature)' : round(xray_on_voltage-min_temp_sram_value,3),
    'Δ(VTID10-VTID0)' : round(tid_10_voltage-xray_on_voltage,3),
    'Δ(VTID10-Vstart)' : round(tid_10_voltage-min_temp_sram_value,3),
    'Δ(Vmax-Vstart)' : round(max_value - tid_10_voltage,3),
    
    }

    if os.path.exists(results_file):
        results_df = pd.read_csv(results_file)
        if not ((results_df['chip'] == chip) & (results_df['sram_number'] == sram_number)).any():
            results_df = results_df._append(new_entry, ignore_index=True)
            results_df.to_csv(results_file, index=False)
    else:
        results_df = pd.DataFrame([new_entry])
        results_df.to_csv(results_file, index=False)




# Function to detect significant changes
def detect_significant_changes(series, initial_threshold=0.95, change_threshold=0.05):
    significant_changes = []
    initial_value = None
    for i in range(len(series)):
        if initial_value is None and series[i] > initial_threshold:
            initial_value = series[i]
            significant_changes.append((i, series[i]))
        elif initial_value is not None and abs(series[i] - initial_value) >     change_threshold:
            initial_value = series[i]
            significant_changes.append((i, series[i]))
    return significant_changes

# Plot each SRAM as a function of time in individual figures
for i in range(1, 13):
    sram_col = f'SRAM {i}'
    fig, ax1 = plt.subplots(figsize=(10, 6))
    ax1.plot(df['Time (hours)'], df[sram_col], label=sram_col)

    xray_on_voltage = df[sram_col].loc[df['Time (hours)'] == first_xrayon_time].values[0]
    tid_10_voltage = df[sram_col].loc[df['Time (hours)'] == first_tid_10_time].values[0]

    ax1.axvline(x=first_xrayon_time, color='green', linestyle='--', label='XRAYON True')
    ax1.axhline(y=xray_on_voltage, color='green', linestyle='--', label='voltage > %.2f'%(xray_on_voltage))

    ax1.axvline(x=first_tid_10_time, color='blue', linestyle='--', label='TID >= 10 MRad')
    ax1.axhline(y=tid_10_voltage, color='blue', linestyle='--', label='voltage > %.2f'%tid_10_voltage)

    # Detect significant changes
    #significant_changes = detect_significant_changes(df[sram_col], initial_threshold=0.95)
    #for idx, value in significant_changes:
    #    ax1.axhline(y=value, linestyle='--', color='orange', label=f'Significant Change > {value:.2f}')

    # Add horizontal line at the SRAM value for which the TEMPERATURE is the lowest
    first_half_df = df.iloc[:midpoint]
    min_temp_index = first_half_df[first_half_df['XRAYON'] == False]['TEMPERATURE'].idxmin()
    min_temp_sram_value = first_half_df.loc[min_temp_index, sram_col]
    ax1.axhline(y=min_temp_sram_value, color='purple', linestyle='--', label='Min Temp (XRAYON False) = %.2f' % min_temp_sram_value)


    # Add horizontal lines for max and min SRAM values and corresponding TID values
    max_value, max_tid, min_value_after_max, min_tid_after_max = find_max_min_sram_values(df, sram_col)

    if max_value < tid_10_voltage:
        max_value = tid_10_voltage

    ax1.axhline(y=max_value, color='cyan', linestyle='--', label='Max (TID=%.2f), voltage = %.2f'%(max_tid,max_value))
    if min_value_after_max is not None:
        ax1.axhline(y=min_value_after_max, color='magenta', linestyle='--', label='Min aftermax (TID=%.2f), voltage = %.2f'%(min_tid_after_max,min_value_after_max))


    min_value, min_tid = find_min(df, sram_col)
    ax1.axhline(y=min_value, color='skyblue', linestyle='--', label='Min (TID=%.2f), voltage = %.2f'%(min_tid,min_value))


    # Add horizontal line with the first value of the SRAM
    first_sram_value = df[sram_col].iloc[0]
    ax1.axhline(y=first_sram_value, color='brown', linestyle='--', label='Start = %.2f'%first_sram_value)


    ax1.set_ylabel(sram_col)
    ax1.set_xlabel('Time (hours)')
    ax1.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    ax1.grid(True)

    # Overlay the temperature (TID) as a function of time
    ax2 = ax1.twinx()
    ax2.plot(df['Time (hours)'], df['TEMPERATURE'], color='red', label='TEMPERATURE')
    ax2.set_ylabel('TEMPERATURE', color='red')
    ax2.legend(loc='upper left')

    plt.tight_layout()
    plt.savefig(f'../../bist-study-averages/delta-plots/voltage_{args.chip}_{args.type}_test{args.test}_SRAM{i}.png')
    plt.close()

    # Save interesting results
    if (max_value - first_sram_value) > 0.03:
        save_interesting_results(args.chip, args.type, args.test ,i, first_sram_value, max_value, max_tid, min_value_after_max, min_tid_after_max, xray_on_voltage, tid_10_voltage, min_temp_sram_value)
    
    save_all_results(args.chip, args.type, args.test ,i, first_sram_value, max_value, max_tid, min_value,min_value_after_max, min_tid_after_max, xray_on_voltage, tid_10_voltage, min_temp_sram_value)


    

# Summary plot with all 12 SRAMs in the same canvas
fig, axs = plt.subplots(12, 1, figsize=(10, 30), sharex=True)

for i in range(1, 13):
    sram_col = f'SRAM {i}'
    axs[i-1].plot(df['Time (hours)'], df[sram_col], label=sram_col)
    axs[i-1].axvline(x=first_xrayon_time, color='green', linestyle='--', label='XRAYON True')
    axs[i-1].axhline(y=df[sram_col].loc[df['Time (hours)'] == first_xrayon_time].values[0], color='green', linestyle='--', label='voltage > %.2f'%df[sram_col].loc[df['Time (hours)'] == first_xrayon_time].values[0])

    axs[i-1].axvline(x=first_tid_10_time, color='blue', linestyle='--', label='TID >= 10 MRad')
    axs[i-1].axhline(y=df[sram_col].loc[df['Time (hours)'] == first_tid_10_time].values[0], color='blue', linestyle='--', label='voltage > %.2f'%df[sram_col].loc[df['Time (hours)'] == first_tid_10_time].values[0])

    # Detect significant changes
    #significant_changes = detect_significant_changes(df[sram_col], initial_threshold=0.95)
    #for idx, value in significant_changes:
    #    axs[i-1].axhline(y=value, linestyle='--', color='orange', label=f'Significant Change > {value:.2f}')
    
    # Add horizontal line at the SRAM value for which the TEMPERATURE is the lowest
    first_half_df = df.iloc[:midpoint]
    min_temp_index = first_half_df[first_half_df['XRAYON'] == False]['TEMPERATURE'].idxmin()
    min_temp_sram_value = first_half_df.loc[min_temp_index, sram_col]
    axs[i-1].axhline(y=min_temp_sram_value, color='purple', linestyle='--', label='Min Temp (XRAYON False) = %.2f' % min_temp_sram_value)

    # Add horizontal lines for max and min SRAM values and corresponding TID values
    max_value, max_tid, min_value_after_max, min_tid_after_max = find_max_min_sram_values(df, sram_col)
    axs[i-1].axhline(y=max_value, color='cyan', linestyle='--', label='Max (TID=%.2f), voltage = %.2f'%(max_tid,max_value))
    if min_value_after_max is not None:
        axs[i-1].axhline(y=min_value_after_max, color='magenta', linestyle='--', label='Min after Max (TID=%.2f), voltage = %.2f'%(min_tid_after_max,min_value_after_max))


    min_value, min_tid = find_min(df, sram_col)
    axs[i-1].axhline(y=min_value, color='skyblue', linestyle='--', label='Min (TID=%.2f), voltage = %.2f'%(min_tid,min_value))

    # Add horizontal line with the first value of the SRAM
    first_sram_value = df[sram_col].iloc[0]
    axs[i-1].axhline(y=first_sram_value, color='brown', linestyle='--', label='Start = %.2f'%first_sram_value)

    #print("SRAM %d"%i)
    #print(first_sram_value, )

    axs[i-1].set_ylabel(sram_col)
    axs[i-1].set_ylim(0.9,1.3)
    axs[i-1].legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    axs[i-1].grid(True)

# Overlay the temperature (TID) as a function of time
for ax in axs:
    ax2 = ax.twinx()
    ax2.plot(df['Time (hours)'], df['TEMPERATURE'], color='red', label='TEMPERATURE')
    ax2.set_ylabel('TEMPERATURE', color='red')
    ax2.legend(loc='upper left')

# Set common labels
axs[-1].set_xlabel('Time (hours)')

plt.tight_layout()
fig.savefig(f'../../bist-study-averages/delta-plots/voltage_{args.chip}_{args.type}_test{args.test}_summary.png')
plt.close()
