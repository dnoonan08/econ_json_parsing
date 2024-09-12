import pymongo
import numpy as np
import pandas as pd

def getLatestFiles(x):
    ## This function creates an True/False Array to select the latest files in the DB
    x = list(x) #first we have to convert the query to a list
    chip_numbers = np.array([y['chip_number'] for y in x]) #make an array of all the chip numbers
    TS= np.array([y['Timestamp'] for y in x]) #make an array of all the timestamps
    truth_array = np.array([True]*len(chip_numbers)) #initialize the true/false array
    #This finds all the duplicate chip numbers in the array
    u, c = np.unique(chip_numbers, return_counts=True)
    dup = u[c > 1]
    for d in dup:
        #looping through all the duplicate chip numbers
        #first we find the indexes where the duplicate chip numbers exist
        temp = (np.argwhere(chip_numbers == d))[:,0]
        maxIdx = temp[0]
        #Next in this loop we find the index that gives the latest file
        #we are sorting by Timestamp
        for t in temp:
            if TS[t] > TS[maxIdx]:
                maxIdx = t
        #Next we are looping through the indexes again and then assigning the
        #Indexes which are not the index of the latest file to false
        for t in temp:
            if t < maxIdx:
                truth_array[t] = False
    return truth_array

class Database:
    def __init__(self, ip):
        ## this connects to the database
        self.client = pymongo.MongoClient('localhost',ip)
        self.session = self.client.start_session()
        self.db = self.client['jsonDB'] ## this name will probably change when we decide on an official name

    def pllCapbankWidthPlot(self, lowerLim=None, upperLim=None, voltage = '1p2', econType = 'ECOND'):
            #This function makes a plot of the PLL Capbank Width
            #if the user provides a range it will plot only over that range
            #if not it plots the capbank width over the whole dataset 
            #for different voltages use the name argument and please provide a string
            #1p08 for 1.08V, 1p2 for 1.2V, 1p32 for 1.32V
            #Also use the ECON type argument to make request info for ECOND vs ECONT 
        latestFilesWChipLimits = getLatestFiles(self.db['testPLLInfo'].find({'chip_number': {"$lt": upperLim, "$gt": lowerLim}, 'ECON_type': econType},{'chip_number':'$chip_number', 'Timestamp':'$Timestamp'}))
        latestFiles = getLatestFiles(self.db['testPLLInfo'].find({'ECON_type': econType},{'chip_number':'$chip_number', 'Timestamp':'$Timestamp'}))
        if voltage == '1p2':
            if lowerLim and upperLim:
                x = np.array(list(self.db['testPLLInfo'].find({'chip_number': {"$lt": upperLim, "$gt": lowerLim}, 'ECON_type': econType}, {'width':'$test_info.test_pll_capbank_width_1_2.metadata.pll_capbank_width', '_id':0})))[latestFilesWChipLimits]
                capbankwidth = np.array([y['width'] for y in x if y != {}])
                return capbankwidth
            else:
                x = np.array(list(self.db['testPLLInfo'].find({'ECON_type': econType}, 
                                                                  {'width':'$test_info.test_pll_capbank_width_1_2.metadata.pll_capbank_width', '_id':0})))[latestFiles]
                capbankwidth = np.array([y['width'] for y in x if y != {}])
                return capbankwidth
        if voltage == '1p08':
            if lowerLim and upperLim:
                x = np.array(list(self.db['testPLLInfo'].find({'chip_number': {"$lt": upperLim, "$gt": lowerLim}, 'ECON_type': econType}, {'width':'$test_info.test_pll_capbank_width_1_08.metadata.pll_capbank_width', '_id':0})))[latestFilesWChipLimits]
                capbankwidth = np.array([y['width'] for y in x if y != {}])
                return capbankwidth
            else:
                x = np.array(list(self.db['testPLLInfo'].find({'ECON_type': econType}, {'width':'$test_info.test_pll_capbank_width_1_08.metadata.pll_capbank_width', '_id':0})))[latestFiles]
                capbankwidth = np.array([y['width'] for y in x if y != {}])
                return capbankwidth
        if voltage == '1p32':
            if lowerLim and upperLim:
                x = np.array(list(self.db['testPLLInfo'].find({'chip_number': {"$lt": upperLim, "$gt": lowerLim}, 'ECON_type': econType}, {'width':'$test_info.test_pll_capbank_width_1_32.metadata.pll_capbank_width', '_id':0})))[latestFilesWChipLimits]
                capbankwidth = np.array([y['width'] for y in x if y != {}])
                return capbankwidth
            else:
                x = np.array(list(self.db['testPLLInfo'].find({'ECON_type': econType}, {'width':'$test_info.test_pll_capbank_width_1_32.metadata.pll_capbank_width', '_id':0})))[latestFiles]
                capbankwidth = np.array([y['width'] for y in x if y != {}])
                return capbankwidth
        
                    
    def prbsMaxWidthPlot(self, lowerLim=None, upperLim=None, voltage = '1p2', econType = 'ECOND'):
        #This function makes a plot of the PRBS Max Width
        #if the user provides a range it will plot only over that range
        #if not it plots the capbank width over the whole dataset 
        #for different voltages use the name argument and please provide a string
        #1p08 for 1.08V, 1p2 for 1.2V, 1p32 for 1.32V
        #Also use the ECON type argument to make request info for ECOND vs ECONT 
        latestFilesWChipLimits = getLatestFiles(self.db['testIOInfo'].find({'chip_number': {"$lt": upperLim, "$gt": lowerLim}, 'ECON_type': econType},{'chip_number':'$chip_number', 'Timestamp':'$Timestamp'}))
        latestFiles = getLatestFiles(self.db['testIOInfo'].find({'ECON_type': econType},{'chip_number':'$chip_number', 'Timestamp':'$Timestamp'}))
        if voltage == '1p2':
            if lowerLim and upperLim:
                x = np.array(list(self.db['testIOInfo'].find({'chip_number': {"$lt": upperLim, "$gt": lowerLim}, 'ECON_type': econType},{'maxwidth':'$test_info.test_ePortRXPRBS_1_2.metadata.maxwidth', '_id':0})))[latestFilesWChipLimits]
                maxwidth =np.array([y['maxwidth'] for y in x if y != {}])
                return maxwidth
            else:
                x = np.array(list(self.db['testIOInfo'].find({'ECON_type': econType}, {'maxwidth':'$test_info.test_ePortRXPRBS_1_2.metadata.maxwidth', '_id':0})))[latestFiles]
                maxwidth =np.array([y['maxwidth'] for y in x if y != {}])
                return maxwidth
        if voltage == '1p08':
            if lowerLim and upperLim:
                x = np.array(list(self.db['testIOInfo'].find({'chip_number': {"$lt": upperLim, "$gt": lowerLim}, 'ECON_type': econType}, {'maxwidth':'$test_info.test_ePortRXPRBS_1_08.metadata.maxwidth', '_id':0})))[latestFilesWChipLimits]
                maxwidth = np.array([y['maxwidth'] for y in x if y != {}])
                return maxwidth
            else:
                x = np.array(list(self.db['testIOInfo'].find({'ECON_type': econType}, {'maxwidth':'$test_info.test_ePortRXPRBS_1_08.metadata.maxwidth', '_id':0})))[latestFiles]
                maxwidth =np.array([y['maxwidth'] for y in x if y != {}])
                return maxwidth
        if voltage == '1p32':
            if lowerLim and upperLim:
                x = np.array(list(self.db['testIOInfo'].find({'chip_number': {"$lt": upperLim, "$gt": lowerLim}, 'ECON_type': econType}, {'maxwidth':'$test_info.test_ePortRXPRBS_1_32.metadata.maxwidth', '_id':0})))[latestFilesWChipLimits]
                maxwidth =np.array([y['maxwidth'] for y in x if y != {}])
                return maxwidth
            else:
                x = np.array(list(self.db['testIOInfo'].find({'ECON_type': econType}, {'maxwidth':'$test_info.test_ePortRXPRBS_1_32.metadata.maxwidth', '_id':0})))[latestFiles]
                maxwidth =np.array([y['maxwidth'] for y in x if y != {}])
                return maxwidth
                    
                    
    def etxMaxWidthPlot(self, lowerLim=None, upperLim=None, voltage = '1p2', econType = 'ECOND'):
        #This function makes a plot of the eTX Delay scan Max Width
        #if the user provides a range it will plot only over that range
        #if not it plots the capbank width over the whole dataset 
        #for different voltages use the name argument and please provide a string
        #1p08 for 1.08V, 1p2 for 1.2V, 1p32 for 1.32V
        #Also use the ECON type argument to make request info for ECOND vs ECONT 
        latestFilesWChipLimits = getLatestFiles(self.db['testIOInfo'].find({'chip_number': {"$lt": upperLim, "$gt": lowerLim}, 'ECON_type': econType},{'chip_number':'$chip_number', 'Timestamp':'$Timestamp'}))
        latestFiles = getLatestFiles(self.db['testIOInfo'].find({'ECON_type': econType},{'chip_number':'$chip_number', 'Timestamp':'$Timestamp'}))
        if voltage == '1p2':
            if lowerLim and upperLim:
                x = np.array(list(self.db['testIOInfo'].find({'chip_number': {"$lt": upperLim, "$gt": lowerLim}, 'ECON_type': econType},{'maxwidth':'$test_info.test_eTX_delayscan_1_2.metadata.max_width', '_id':0})))[latestFilesWChipLimits]
                maxwidth =np.array([y['maxwidth'] for y in x if y != {}])
                return maxwidth
            else:
                x = np.array(list(self.db['testIOInfo'].find({'ECON_type': econType}, {'maxwidth':'$test_info.test_eTX_delayscan_1_2.metadata.max_width', '_id':0})))[latestFiles]
                maxwidth =np.array([y['maxwidth'] for y in x if y != {}])
                return maxwidth
        if voltage == '1p08':
            if lowerLim and upperLim:
                x = np.array(list(self.db['testIOInfo'].find({'chip_number': {"$lt": upperLim, "$gt": lowerLim}, 'ECON_type': econType}, {'maxwidth':'$test_info.test_eTX_delayscan_1_08.metadata.max_width', '_id':0})))[latestFilesWChipLimits]
                maxwidth = np.array([y['maxwidth'] for y in x if y != {}])
                return maxwidth
            else:
                x = np.array(list(self.db['testIOInfo'].find({'ECON_type': econType}, {'maxwidth':'$test_info.test_eTX_delayscan_1_08.metadata.max_width', '_id':0})))[latestFiles]
                maxwidth =np.array([y['maxwidth'] for y in x if y != {}])
                return maxwidth
        if voltage == '1p32':
            if lowerLim and upperLim:
                x = np.array(list(self.db['testIOInfo'].find({'chip_number': {"$lt": upperLim, "$gt": lowerLim}, 'ECON_type': econType}, {'maxwidth':'$test_info.test_eTX_delayscan_1_32.metadata.max_width', '_id':0})))[latestFilesWChipLimits]
                maxwidth =np.array([y['maxwidth'] for y in x if y != {}])
                return maxwidth
            else:
                x = np.array(list(self.db['testIOInfo'].find({'ECON_type': econType}, {'maxwidth':'$test_info.test_eTX_delayscan_1_32.metadata.max_width', '_id':0})))[latestFiles]
                maxwidth =np.array([y['maxwidth'] for y in x if y != {}])
                return maxwidth

    def getVoltageAndCurrent(self, lowerLim=None, upperLim=None, econType = 'ECOND'):
        #This function makes a plot of the PLL Capbank Width
        #if the user provides a range it will plot only over that range
        #if not it plots the capbank width over the whole dataset 
        #for different voltages use the name argument and please provide a string
        # 1p08 for 1.08V, 1p2 for 1.2V, 1p32 for 1.32V
        #Also use the ECON type argument to make request info for ECOND vs ECONT 
        latestFilesWChipLimits = getLatestFiles(self.db['testPowerInfo'].find({'chip_number': {"$lt": upperLim, "$gt": lowerLim}, 'ECON_type': econType},{'chip_number':'$chip_number', 'Timestamp':'$Timestamp'}))
        latestFiles = getLatestFiles(self.db['testPowerInfo'].find({'ECON_type': econType},{'chip_number':'$chip_number', 'Timestamp':'$Timestamp'}))
        if lowerLim and upperLim:
            x = np.array(list(self.db['testPowerInfo'].find({'chip_number': {"$lt": upperLim, "$gt": lowerLim}, 'ECON_type': econType}, {'_id':0, 'voltage': '$test_info.test_currentdraw_1p2V.metadata.voltage', 'current':'$test_info.test_currentdraw_1p2V.metadata.current'})))[latestFilesWChipLimits]
            current = np.array([y['current'] for y in x if y != {}])
            voltage = np.array([y['voltage'] for y in x if y != {}])
            return current, voltage
        else:
            x = np.array((list(self.db['testPowerInfo'].find({'ECON_type': econType},{'_id':0, 'voltage': '$test_info.test_currentdraw_1p2V.metadata.voltage', 'current':'$test_info.test_currentdraw_1p2V.metadata.current'}))))[latestFiles]
            current = np.array([y['current'] for y in x if y != {}])
            voltage = np.array([y['voltage'] for y in x if y != {}])
            return current, voltage

    def getBISTInfo(self, lowerLim=None, upperLim=None, econType='ECOND'):
        #This function makes a plot of the PLL Capbank Width
        #if the user provides a range it will plot only over that range
        #if not it plots the capbank width over the whole dataset 
        #for different voltages use the name argument and please provide a string
        # 1p08 for 1.08V, 1p2 for 1.2V, 1p32 for 1.32V
        #Also use the ECON type argument to make request info for ECOND vs ECONT 
        latestFilesWChipLimits = getLatestFiles(self.db['testBistInfo'].find({'chip_number': {"$lt": upperLim, "$gt": lowerLim}, 'ECON_type': econType},{'chip_number':'$chip_number', 'Timestamp':'$Timestamp'}))
        latestFiles = getLatestFiles(self.db['testBistInfo'].find({'ECON_type': econType},{'chip_number':'$chip_number', 'Timestamp':'$Timestamp'}))
        if lowerLim and upperLim:
            x = np.array(list(self.db['testBistInfo'].find({'chip_number': {"$lt": upperLim, "$gt": lowerLim}, 'ECON_type': 'ECOND'}, {'first_failure':'$test_info.test_bist.metadata.first_failure', 'bist_result':'$test_info.test_bist.metadata.bist_results', '_id':0})))[latestFilesWChipLimits]
            first_failure = np.array([y['first_failure'] for y in x if y != {}])
            bist_result = ([y['bist_result'] for y in x if y != {}])
            return first_failure, bist_result
        else:
            x = np.array(list(self.db['testBistInfo'].find({'ECON_type':'ECOND'},{'first_failure':'$test_info.test_bist.metadata.first_failure', 'bist_result':'$test_info.test_bist.metadata.bist_results', '_id':0})))[latestFiles]
            first_failure = np.array([y['first_failure'] for y in x if y != {}])
            bist_result = ([y['bist_result'] for y in x if y != {}])
            return first_failure, bist_result
            
    def phaseScan2DPlot(self, chipNum, econType = 'ECOND', voltage = '1p2'):
        #returns the information needed to make the phase scan 2d plot
        #for a given chip number
        #for different voltages use the name argument and please provide a string
        # 1p08 for 1.08V, 1p2 for 1.2V, 1p32 for 1.32V
        #Also use the ECON type argument to make request info for ECOND vs ECONT 
        latestFiles = getLatestFiles(self.db['testIOInfo'].find({'chip_number':chipNum, 'ECON_type': econType},{'chip_number':'$chip_number', 'Timestamp':'$Timestamp'}))
        if voltage == '1p2':
            x = np.array(list(self.db['testIOInfo'].find({'chip_number':chipNum, 'ECON_type':econType},{'eRX_errcounts':'$test_info.test_ePortRXPRBS_1_2.metadata.eRX_errcounts', '_id':0})))[latestFiles]
            return np.array(x[0]['eRX_errcounts'])
        if voltage == '1p08':
            x = np.array(list(self.db['testIOInfo'].find({'chip_number':chipNum, 'ECON_type':econType},{'eRX_errcounts':'$test_info.test_ePortRXPRBS_1_08.metadata.eRX_errcounts', '_id':0})))[latestFiles]
            return np.array(x[0]['eRX_errcounts'])
        if voltage == '1p32':
            x = np.array(list(self.db['testIOInfo'].find({'chip_number':chipNum, 'ECON_type':econType},{'eRX_errcounts':'$test_info.test_ePortRXPRBS_1_32.metadata.eRX_errcounts', '_id':0})))[latestFiles]
            return np.array(x[0]['eRX_errcounts'])
        
                
    def delayScan2DPlot(self, chipNum, econType = 'ECOND', voltage = '1p2'):
        #returns the information needed to make the delay scan 2d plot
        #for a given chip number
        #for different voltages use the name argument and please provide a string
        # 1p08 for 1.08V, 1p2 for 1.2V, 1p32 for 1.32V
        #Also use the ECON type argument to make request info for ECOND vs ECONT 
        latestFiles = getLatestFiles(self.db['testIOInfo'].find({'chip_number':chipNum, 'ECON_type': econType},{'chip_number':'$chip_number', 'Timestamp':'$Timestamp'}))
        if voltage == '1p2':
            x = np.array(list(self.db['testIOInfo'].find({'chip_number':chipNum, 'ECON_type':econType},{'eTX_bitcounts':'$test_info.test_eTX_delayscan_1_2.metadata.eTX_bitcounts','eTX_errcounts':'$test_info.test_eTX_delayscan_1_2.metadata.eTX_errcounts', '_id':0})))[latestFiles]
            bitcounts = np.array(x[0]['eTX_bitcounts'])
            errcounts = np.array(x[0]['eTX_errcounts'])
            return bitcounts, errcounts
        if voltage == '1p08':
            x = np.array(list(self.db['testIOInfo'].find({'chip_number':chipNum, 'ECON_type':econType},{'eTX_bitcounts':'$test_info.test_eTX_delayscan_1_08.metadata.eTX_bitcounts','eTX_errcounts':'$test_info.test_eTX_delayscan_1_08.metadata.eTX_errcounts', '_id':0})))[latestFiles]
            bitcounts = np.array(x[0]['eTX_bitcounts'])
            errcounts = np.array(x[0]['eTX_errcounts'])
            return bitcounts, errcounts
        if voltage == '1p2':
            x = np.array(list(self.db['testIOInfo'].find({'chip_number':chipNum, 'ECON_type':econType},{'eTX_bitcounts':'$test_info.test_eTX_delayscan_1_32.metadata.eTX_bitcounts','eTX_errcounts':'$test_info.test_eTX_delayscan_1_32.metadata.eTX_errcounts', '_id':0})))[latestFiles]
            bitcounts = np.array(x[0]['eTX_bitcounts'])
            errcounts = np.array(x[0]['eTX_errcounts'])
            return bitcounts, errcounts

    def getFractionOfTestsPassed(self, econType = 'ECOND'):
        #This function grabs the fraction of tests that passed
        #So what this does is first count the number of tests that got skipped
        #And subtracts this from the total number of tests that were collected
        #This should give the total number of tests performed for either ECOND or ECONT
        #Then it just returns the total fraction of tests that pass for a given chip by
        #Dividing the total number of tests passed over the total number of tests performed
        #please use the econType argument to specify ECOND or ECONT and it expects a string input
        latestFiles = getLatestFiles(self.db['TestSummary'].find({'ECON_type': econType},{'chip_number':'$chip_number', 'Timestamp':'$Timestamp'}))
        x = np.array(list(self.db['TestSummary'].find({'ECON_type':econType},{'outcome':'$individual_test_outcomes', 'passed':'$summary.passed', 'total': '$summary.total', '_id':0})))[latestFiles]
        frac_passed = []
        for y in x:
            outcomes = y['outcome']
            passed = y['passed']
            total = y['total']
            tot_econt = []
            for key in outcomes:
                if outcomes[key]== -2:
                    tot_econt.append(key)
            denominator = total - len(tot_econt)
            frac = passed/denominator
            frac_passed.append(frac)
        return np.array(frac_passed)
    def getTestingSummaries(self, econType = 'ECOND'):
        #This function returns a dataframe for the testing summary plots prepared by Marko
        #Please use the econType argument to specify ECOND or ECONT and the function expects a string for this argument
        latestFiles = getLatestFiles(self.db['TestSummary'].find({'ECON_type': econType},{'chip_number':'$chip_number', 'Timestamp':'$Timestamp'}))
        maps = ['passed', 'failed','error','skipped']
        counters = {}
        total = 0
        for obj in np.array(list(self.db['TestSummary'].find({'ECON_type':econType},{'individual_test_outcomes':1, '_id':0})))[latestFiles]:
            for key, value in obj['individual_test_outcomes'].items():
                if value == 1:
                    if key in counters.keys():
                        counters[key][0]+=1
                    else:
                        counters[key] = [1,0,0,0]
                elif value == 0:
                    if key in counters.keys():
                        counters[key][1]+=1
                    else:
                        counters[key] = [0,1,0,0]
                elif value == -1:
                    if key in counters.keys():
                        counters[key][2] += 1
                    else:
                        counters[key] = [0,0,1,0]
                elif value == -2:
                    if key in counters.keys():
                        counters[key][3] += 1
                    else:
                        counters[key] = [0,0,0,1]
        
            total += 1
        df = pd.DataFrame(counters, index=maps)
        df = df.T
        df = df/total
        return df
        
        
