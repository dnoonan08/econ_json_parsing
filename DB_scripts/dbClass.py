import pymongo
import numpy as np
import pandas as pd

class Database:
    def __init__(self, ip):
        ## this connects to the database
        self.client = pymongo.MongoClient(ip)
        self.session = self.client.start_session()
        self.db = self.client['jsonDB'] ## this name will probably change when we decide on an official name

    def pllCapbankWidthPlot(self, lowerLim=None, upperLim=None, voltage = '1p2', econType = 'ECOND'):
        #This function makes a plot of the PLL Capbank Width
        #if the user provides a range it will plot only over that range
        #if not it plots the capbank width over the whole dataset 
        #for different voltages use the name argument and please provide a string
        #1p08 for 1.08V, 1p2 for 1.2V, 1p32 for 1.32V
        #Also use the ECON type argument to make request info for ECOND vs ECONT 
        if econType == 'ECOND':
            if voltage == '1p2':
                if lowerLim and upperLim:
                    x = list(self.db['testPLLInfo'].find({'chip_number': {"$lt": upperLim, "$gt": lowerLim}, 'ECON_type': econType}, 
                                                         {'width':'$test_info.test_pll_capbank_width_1_2.metadata.pll_capbank_width', '_id':0}))
                    capbankwidth = np.array([y['width'] for y in x if y != {}])
                    return capbankwidth
                else:
                    x = list(self.db['testPLLInfo'].find({'ECON_type': econType}, {'width':'$test_info.test_pll_capbank_width_1_2.metadata.pll_capbank_width', '_id':0}))
                    capbankwidth = np.array([y['width'] for y in x if y != {}])
                    return capbankwidth
            if voltage == '1p08':
                if lowerLim and upperLim:
                    x = list(self.db['testPLLInfo'].find({'chip_number': {"$lt": upperLim, "$gt": lowerLim}, 'ECON_type': econType}, 
                                                         {'width':'$test_info.test_pll_capbank_width_1_08.metadata.pll_capbank_width', '_id':0}))
                    capbankwidth = np.array([y['width'] for y in x if y != {}])
                    return capbankwidth
                else:
                    x = list(self.db['testPLLInfo'].find({'ECON_type': econType}, {'width':'$test_info.test_pll_capbank_width_1_08.metadata.pll_capbank_width', '_id':0}))
                    capbankwidth = np.array([y['width'] for y in x if y != {}])
                    return capbankwidth
            if voltage == '1p32':
                if lowerLim and upperLim:
                    x = list(self.db['testPLLInfo'].find({'chip_number': {"$lt": upperLim, "$gt": lowerLim}, 'ECON_type': econType}, 
                                                         {'width':'$test_info.test_pll_capbank_width_1_32.metadata.pll_capbank_width', '_id':0}))
                    capbankwidth = np.array([y['width'] for y in x if y != {}])
                    return capbankwidth
                else:
                    x = list(self.db['testPLLInfo'].find({'ECON_type': econType}, {'width':'$test_info.test_pll_capbank_width_1_32.metadata.pll_capbank_width', '_id':0}))
                    capbankwidth = np.array([y['width'] for y in x if y != {}])
                    return capbankwidth
        
        if econType == 'ECONT':
            if voltage == '1p2':
                if lowerLim and upperLim:
                    x = list(self.db['testPLLInfo'].find({'chip_number': {"$lt": upperLim, "$gt": lowerLim}, 'ECON_type': econType}, 
                                                         {'width':'$test_info.test_pll_capbank_width_1_2.metadata.pll_capbank_width', '_id':0}))
                    capbankwidth = np.array([y['width'] for y in x if y != {}])
                    return capbankwidth
                else:
                    x = list(self.db['testPLLInfo'].find({'ECON_type': econType}, {'width':'$test_info.test_pll_capbank_width_1_2.metadata.pll_capbank_width', '_id':0}))
                    capbankwidth = np.array([y['width'] for y in x if y != {}])
                    return capbankwidth
            if voltage == '1p08':
                if lowerLim and upperLim:
                    x = list(self.db['testPLLInfo'].find({'chip_number': {"$lt": upperLim, "$gt": lowerLim}, 'ECON_type': econType}, 
                                                         {'width':'$test_info.test_pll_capbank_width_1_08.metadata.pll_capbank_width', '_id':0}))
                    capbankwidth = np.array([y['width'] for y in x if y != {}])
                    return capbankwidth
                else:
                    x = list(self.db['testPLLInfo'].find({'ECON_type': econType}, {'width':'$test_info.test_pll_capbank_width_1_08.metadata.pll_capbank_width', '_id':0}))
                    capbankwidth = np.array([y['width'] for y in x if y != {}])
                    return capbankwidth
            if voltage == '1p32':
                if lowerLim and upperLim:
                    x = list(self.db['testPLLInfo'].find({'chip_number': {"$lt": upperLim, "$gt": lowerLim}, 'ECON_type': econType}, 
                                                         {'width':'$test_info.test_pll_capbank_width_1_32.metadata.pll_capbank_width', '_id':0}))
                    capbankwidth = np.array([y['width'] for y in x if y != {}])
                    return capbankwidth
                else:
                    x = list(self.db['testPLLInfo'].find({'ECON_type': econType}, {'width':'$test_info.test_pll_capbank_width_1_32.metadata.pll_capbank_width', '_id':0}))
                    capbankwidth = np.array([y['width'] for y in x if y != {}])
                    return capbankwidth
                    
    def prbsMaxWidthPlot(self, lowerLim=None, upperLim=None, voltage = '1p2', econType = 'ECOND'):
        #This function makes a plot of the PRBS Max Width
        #if the user provides a range it will plot only over that range
        #if not it plots the capbank width over the whole dataset 
        #for different voltages use the name argument and please provide a string
        #1p08 for 1.08V, 1p2 for 1.2V, 1p32 for 1.32V
        #Also use the ECON type argument to make request info for ECOND vs ECONT 
        if econType == 'ECOND':
            if voltage == '1p2':
                if lowerLim and upperLim:
                    x = list(self.db['testIOInfo'].find({'chip_number': {"$lt": upperLim, "$gt": lowerLim}, 'ECON_type': econType}, 
                                                        {'maxwidth':'$test_info.test_ePortRXPRBS_1_2.metadata.maxwidth', '_id':0}))
                    maxwidth =np.array([y['maxwidth'] for y in x if y != {}])
                    return maxwidth
                else:
                    x = list(self.db['testIOInfo'].find({'ECON_type': econType}, {'maxwidth':'$test_info.test_ePortRXPRBS_1_2.metadata.maxwidth', '_id':0}))
                    maxwidth =np.array([y['maxwidth'] for y in x if y != {}])
                    return maxwidth
            if voltage == '1p08':
                if lowerLim and upperLim:
                    x = list(self.db['testIOInfo'].find({'chip_number': {"$lt": upperLim, "$gt": lowerLim}, 'ECON_type': econType}, 
                                                        {'maxwidth':'$test_info.test_ePortRXPRBS_1_08.metadata.maxwidth', '_id':0}))
                    maxwidth = np.array([y['maxwidth'] for y in x if y != {}])
                    return maxwidth
                else:
                    x = list(self.db['testIOInfo'].find({'ECON_type': econType}, {'maxwidth':'$test_info.test_ePortRXPRBS_1_08.metadata.maxwidth', '_id':0}))
                    maxwidth =np.array([y['maxwidth'] for y in x if y != {}])
                    return maxwidth
            if voltage == '1p32':
                if lowerLim and upperLim:
                    x = list(self.db['testIOInfo'].find({'chip_number': {"$lt": upperLim, "$gt": lowerLim}, 'ECON_type': econType}, 
                                                        {'maxwidth':'$test_info.test_ePortRXPRBS_1_32.metadata.maxwidth', '_id':0}))
                    maxwidth =np.array([y['maxwidth'] for y in x if y != {}])
                    return maxwidth
                else:
                    x = list(self.db['testIOInfo'].find({'ECON_type': econType}, {'maxwidth':'$test_info.test_ePortRXPRBS_1_32.metadata.maxwidth', '_id':0}))
                    maxwidth =np.array([y['maxwidth'] for y in x if y != {}])
                    return maxwidth
                    
        if econType == 'ECONT':
            if voltage == '1p2':
                if lowerLim and upperLim:
                    x = list(self.db['testIOInfo'].find({'chip_number': {"$lt": upperLim, "$gt": lowerLim}, 'ECON_type': econType}, 
                                                        {'maxwidth':'$test_info.test_ePortRXPRBS_1_2.metadata.maxwidth', '_id':0}))
                    maxwidth =np.array([y['maxwidth'] for y in x if y != {}])
                    return maxwidth
                else:
                    x = list(self.db['testIOInfo'].find({'ECON_type': econType}, {'maxwidth':'$test_info.test_ePortRXPRBS_1_2.metadata.maxwidth', '_id':0}))
                    maxwidth =np.array([y['maxwidth'] for y in x if y != {}])
                    return maxwidth
            if voltage == '1p08':
                if lowerLim and upperLim:
                    x = list(self.db['testIOInfo'].find({'chip_number': {"$lt": upperLim, "$gt": lowerLim}, 'ECON_type': econType}, 
                                                        {'maxwidth':'$test_info.test_ePortRXPRBS_1_08.metadata.maxwidth', '_id':0}))
                    maxwidth = np.array([y['maxwidth'] for y in x if y != {}])
                    return maxwidth
                else:
                    x = list(self.db['testIOInfo'].find({'ECON_type': econType}, {'maxwidth':'$test_info.test_ePortRXPRBS_1_08.metadata.maxwidth', '_id':0}))
                    maxwidth =np.array([y['maxwidth'] for y in x if y != {}])
                    return maxwidth
            if voltage == '1p32':
                if lowerLim and upperLim:
                    x = list(self.db['testIOInfo'].find({'chip_number': {"$lt": upperLim, "$gt": lowerLim}, 'ECON_type': econType}, 
                                                        {'maxwidth':'$test_info.test_ePortRXPRBS_1_32.metadata.maxwidth', '_id':0}))
                    maxwidth =np.array([y['maxwidth'] for y in x if y != {}])
                    return maxwidth
                else:
                    x = list(self.db['testIOInfo'].find({'ECON_type': econType}, {'maxwidth':'$test_info.test_ePortRXPRBS_1_32.metadata.maxwidth', '_id':0}))
                    maxwidth =np.array([y['maxwidth'] for y in x if y != {}])
                    return maxwidth
                    
    def etxMaxWidthPlot(self, lowerLim=None, upperLim=None, voltage = '1p2', econType = 'ECOND'):
        #This function makes a plot of the eTX Delay scan Max Width
        #if the user provides a range it will plot only over that range
        #if not it plots the capbank width over the whole dataset 
        #for different voltages use the name argument and please provide a string
        #1p08 for 1.08V, 1p2 for 1.2V, 1p32 for 1.32V
        #Also use the ECON type argument to make request info for ECOND vs ECONT 
        if econType == 'ECOND':
            if voltage == '1p2':
                if lowerLim and upperLim:
                    x = list(self.db['testIOInfo'].find({'chip_number': {"$lt": upperLim, "$gt": lowerLim}, 'ECON_type': econType}, 
                                                        {'maxwidth':'$test_info.test_eTX_delayscan_1_2.metadata.max_width', '_id':0}))
                    maxwidth =np.array([y['maxwidth'] for y in x if y != {}])
                    return maxwidth
                else:
                    x = list(self.db['testIOInfo'].find({'ECON_type': econType}, {'maxwidth':'$test_info.test_eTX_delayscan_1_2.metadata.max_width', '_id':0}))
                    maxwidth =np.array([y['maxwidth'] for y in x if y != {}])
                    return maxwidth
            if voltage == '1p08':
                if lowerLim and upperLim:
                    x = list(self.db['testIOInfo'].find({'chip_number': {"$lt": upperLim, "$gt": lowerLim}, 'ECON_type': econType}, 
                                                        {'maxwidth':'$test_info.test_eTX_delayscan_1_08.metadata.max_width', '_id':0}))
                    maxwidth = np.array([y['maxwidth'] for y in x if y != {}])
                    return maxwidth
                else:
                    x = list(self.db['testIOInfo'].find({'ECON_type': econType}, {'maxwidth':'$test_info.test_eTX_delayscan_1_08.metadata.max_width', '_id':0}))
                    maxwidth =np.array([y['maxwidth'] for y in x if y != {}])
                    return maxwidth
            if voltage == '1p32':
                if lowerLim and upperLim:
                    x = list(self.db['testIOInfo'].find({'chip_number': {"$lt": upperLim, "$gt": lowerLim}, 'ECON_type': econType}, 
                                                        {'maxwidth':'$test_info.test_eTX_delayscan_1_32.metadata.max_width', '_id':0}))
                    maxwidth =np.array([y['maxwidth'] for y in x if y != {}])
                    return maxwidth
                else:
                    x = list(self.db['testIOInfo'].find({'ECON_type': econType}, {'maxwidth':'$test_info.test_eTX_delayscan_1_32.metadata.max_width', '_id':0}))
                    maxwidth =np.array([y['maxwidth'] for y in x if y != {}])
                    return maxwidth

        if econType == 'ECONT':
            if voltage == '1p2':
                if lowerLim and upperLim:
                    x = list(self.db['testIOInfo'].find({'chip_number': {"$lt": upperLim, "$gt": lowerLim}, 'ECON_type': econType}, 
                                                        {'maxwidth':'$test_info.test_eTX_delayscan_1_2.metadata.max_width', '_id':0}))
                    maxwidth =np.array([y['maxwidth'] for y in x if y != {}])
                    return maxwidth
                else:
                    x = list(self.db['testIOInfo'].find({'ECON_type': econType}, {'maxwidth':'$test_info.test_eTX_delayscan_1_2.metadata.max_width', '_id':0}))
                    maxwidth =np.array([y['maxwidth'] for y in x if y != {}])
                    return maxwidth
            if voltage == '1p08':
                if lowerLim and upperLim:
                    x = list(self.db['testIOInfo'].find({'chip_number': {"$lt": upperLim, "$gt": lowerLim}, 'ECON_type': econType}, 
                                                        {'maxwidth':'$test_info.test_eTX_delayscan_1_08.metadata.max_width', '_id':0}))
                    maxwidth = np.array([y['maxwidth'] for y in x if y != {}])
                    return maxwidth
                else:
                    x = list(self.db['testIOInfo'].find({'ECON_type': econType}, {'maxwidth':'$test_info.test_eTX_delayscan_1_08.metadata.max_width', '_id':0}))
                    maxwidth =np.array([y['maxwidth'] for y in x if y != {}])
                    return maxwidth
            if voltage == '1p32':
                if lowerLim and upperLim:
                    x = list(self.db['testIOInfo'].find({'chip_number': {"$lt": upperLim, "$gt": lowerLim}, 'ECON_type': econType}, 
                                                        {'maxwidth':'$test_info.test_eTX_delayscan_1_32.metadata.max_width', '_id':0}))
                    maxwidth =np.array([y['maxwidth'] for y in x if y != {}])
                    return maxwidth
                else:
                    x = list(self.db['testIOInfo'].find({'ECON_type': econType}, {'maxwidth':'$test_info.test_eTX_delayscan_1_32.metadata.max_width', '_id':0}))
                    maxwidth =np.array([y['maxwidth'] for y in x if y != {}])
                    return maxwidth
    def getVoltageAndCurrent(self, lowerLim=None, upperLim=None, econType = 'ECOND'):
        #This function makes a plot of the PLL Capbank Width
        #if the user provides a range it will plot only over that range
        #if not it plots the capbank width over the whole dataset 
        #for different voltages use the name argument and please provide a string
        # 1p08 for 1.08V, 1p2 for 1.2V, 1p32 for 1.32V
        #Also use the ECON type argument to make request info for ECOND vs ECONT 
        if econType == 'ECOND':
            if lowerLim and upperLim:
                x = list(self.db['testPowerInfo'].find({'chip_number': {"$lt": upperLim, "$gt": lowerLim}, 'ECON_type': econType}, {'_id':0, 'voltage': 
                                                                                                                                    '$test_info.test_currentdraw_1p2V.metadata.voltage', 'current':'$test_info.test_currentdraw_1p2V.metadata.current'}))
                current = np.array([y['current'] for y in x if y != {}])
                voltage = np.array([y['voltage'] for y in x if y != {}])
                return current, voltage
            else:
                x = (list(self.db['testPowerInfo'].find({'ECON_type': econType},{'_id':0, 'voltage': '$test_info.test_currentdraw_1p2V.metadata.voltage', 
                                                                                 'current':'$test_info.test_currentdraw_1p2V.metadata.current'})))
                current = np.array([y['current'] for y in x if y != {}])
                voltage = np.array([y['voltage'] for y in x if y != {}])
                return current, voltage
        if econType == 'ECONT':
            if lowerLim and upperLim:
                x = list(self.db['testPowerInfo'].find({'chip_number': {"$lt": upperLim, "$gt": lowerLim}, 'ECON_type': econType}, {'_id':0, 'voltage': 
                                                                                                                                    '$test_info.test_currentdraw_1p2V.metadata.voltage', 'current':'$test_info.test_currentdraw_1p2V.metadata.current'}))
                current = np.array([y['current'] for y in x if y != {}])
                voltage = np.array([y['voltage'] for y in x if y != {}])
                return current, voltage
            else:
                x = (list(self.db['testPowerInfo'].find({'ECON_type': econType},{'_id':0, 'voltage': '$test_info.test_currentdraw_1p2V.metadata.voltage', 
                                                                                 'current':'$test_info.test_currentdraw_1p2V.metadata.current'})))
                current = np.array([y['current'] for y in x if y != {}])
                voltage = np.array([y['voltage'] for y in x if y != {}])
                return current, voltage
    def getBISTInfo(self, lowerLim=None, upperLim=None):
        #This function makes a plot of the PLL Capbank Width
        #if the user provides a range it will plot only over that range
        #if not it plots the capbank width over the whole dataset 
        #for different voltages use the name argument and please provide a string
        # 1p08 for 1.08V, 1p2 for 1.2V, 1p32 for 1.32V
        #Also use the ECON type argument to make request info for ECOND vs ECONT 
        if lowerLim and upperLim:
            x = list(self.db['testBistInfo'].find({'chip_number': {"$lt": upperLim, "$gt": lowerLim}, 'ECON_type': 'ECOND'}, 
                                                  {'first_failure':'$test_info.test_bist.metadata.first_failure', 'bist_result':'$test_info.test_bist.metadata.bist_results', '_id':0}))
            first_failure = np.array([y['first_failure'] for y in x if y != {}])
            bist_result = ([y['bist_result'] for y in x if y != {}])
            return first_failure, bist_result
        else:
            x = list(mydatabase['testBistInfo'].find({'ECON_type':'ECOND'},{'first_failure':'$test_info.test_bist.metadata.first_failure', 
                                                                            'bist_result':'$test_info.test_bist.metadata.bist_results', '_id':0}))
            first_failure = np.array([y['first_failure'] for y in x if y != {}])
            bist_result = ([y['bist_result'] for y in x if y != {}])
            return first_failure, bist_result
            
    def phaseScan2DPlot(self, chipNum, econType = 'ECOND', voltage = '1p2'):
        #returns the information needed to make the phase scan 2d plot
        #for a given chip number
        #for different voltages use the name argument and please provide a string
        # 1p08 for 1.08V, 1p2 for 1.2V, 1p32 for 1.32V
        #Also use the ECON type argument to make request info for ECOND vs ECONT 
        if econType == 'ECOND':
            if voltage == '1p2':
                x = np.array(list(self.db['testIOInfo'].find({'chip_number':chipNum, 
                                                              'ECON_type':econType},{'eRX_errcounts':'$test_info.test_ePortRXPRBS_1_2.metadata.eRX_errcounts', '_id':0})))
                return np.array(x[0]['eRX_errcounts'])
            if voltage == '1p08':
                x = np.array(list(self.db['testIOInfo'].find({'chip_number':chipNum, 
                                                              'ECON_type':econType},{'eRX_errcounts':'$test_info.test_ePortRXPRBS_1_08.metadata.eRX_errcounts', '_id':0})))
                return np.array(x[0]['eRX_errcounts'])
            if voltage == '1p32':
                x = np.array(list(self.db['testIOInfo'].find({'chip_number':chipNum, 
                                                              'ECON_type':econType},{'eRX_errcounts':'$test_info.test_ePortRXPRBS_1_32.metadata.eRX_errcounts', '_id':0})))
                return np.array(x[0]['eRX_errcounts'])
        if econType == 'ECONT':
            if voltage == '1p2':
                x = np.array(list(self.db['testIOInfo'].find({'chip_number':chipNum, 
                                                              'ECON_type':econType},{'eRX_errcounts':'$test_info.test_ePortRXPRBS_1_2.metadata.eRX_errcounts', '_id':0})))
                return np.array(x[0]['eRX_errcounts'])
            if voltage == '1p08':
                x = np.array(list(self.db['testIOInfo'].find({'chip_number':chipNum, 
                                                              'ECON_type':econType},{'eRX_errcounts':'$test_info.test_ePortRXPRBS_1_08.metadata.eRX_errcounts', '_id':0})))
                return np.array(x[0]['eRX_errcounts'])
            if voltage == '1p32':
                x = np.array(list(self.db['testIOInfo'].find({'chip_number':chipNum, 
                                                              'ECON_type':econType},{'eRX_errcounts':'$test_info.test_ePortRXPRBS_1_32.metadata.eRX_errcounts', '_id':0})))
                return np.array(x[0]['eRX_errcounts'])
                
    def delayScan2DPlot(self, chipNum, econType = 'ECOND', voltage = '1p2'):
        #returns the information needed to make the delay scan 2d plot
        #for a given chip number
        #for different voltages use the name argument and please provide a string
        # 1p08 for 1.08V, 1p2 for 1.2V, 1p32 for 1.32V
        #Also use the ECON type argument to make request info for ECOND vs ECONT 
        if econType == 'ECOND':
            if voltage == '1p2':
                x = list(self.db['testIOInfo'].find({'chip_number':chipNum, 
                                                     'ECON_type':econType},{'eTX_bitcounts':'$test_info.test_eTX_delayscan_1_2.metadata.eTX_bitcounts','eTX_errcounts':'$test_info.test_eTX_delayscan_1_2.metadata.eTX_errcounts', '_id':0}))
                bitcounts = np.array(x[0]['eTX_bitcounts'])
                errcounts = np.array(x[0]['eTX_errcounts'])
                return bitcounts, errcounts
            if voltage == '1p08':
                x = list(self.db['testIOInfo'].find({'chip_number':chipNum, 
                                                     'ECON_type':econType},{'eTX_bitcounts':'$test_info.test_eTX_delayscan_1_08.metadata.eTX_bitcounts','eTX_errcounts':'$test_info.test_eTX_delayscan_1_08.metadata.eTX_errcounts', '_id':0}))
                bitcounts = np.array(x[0]['eTX_bitcounts'])
                errcounts = np.array(x[0]['eTX_errcounts'])
                return bitcounts, errcounts
            if voltage == '1p2':
                x = list(self.db['testIOInfo'].find({'chip_number':chipNum, 
                                                     'ECON_type':econType},{'eTX_bitcounts':'$test_info.test_eTX_delayscan_1_32.metadata.eTX_bitcounts','eTX_errcounts':'$test_info.test_eTX_delayscan_1_32.metadata.eTX_errcounts', '_id':0}))
                bitcounts = np.array(x[0]['eTX_bitcounts'])
                errcounts = np.array(x[0]['eTX_errcounts'])
                return bitcounts, errcounts
        if econType == 'ECONT':
            if voltage == '1p2':
                x = list(self.db['testIOInfo'].find({'chip_number':chipNum, 
                                                     'ECON_type':econType},{'eTX_bitcounts':'$test_info.test_eTX_delayscan_1_2.metadata.eTX_bitcounts','eTX_errcounts':'$test_info.test_eTX_delayscan_1_2.metadata.eTX_errcounts', '_id':0}))
                bitcounts = np.array(x[0]['eTX_bitcounts'])
                errcounts = np.array(x[0]['eTX_errcounts'])
                return bitcounts, errcounts
            if voltage == '1p08':
                x = list(self.db['testIOInfo'].find({'chip_number':chipNum, 
                                                     'ECON_type':econType},{'eTX_bitcounts':'$test_info.test_eTX_delayscan_1_08.metadata.eTX_bitcounts','eTX_errcounts':'$test_info.test_eTX_delayscan_1_08.metadata.eTX_errcounts', '_id':0}))
                bitcounts = np.array(x[0]['eTX_bitcounts'])
                errcounts = np.array(x[0]['eTX_errcounts'])
                return bitcounts, errcounts
            if voltage == '1p2':
                x = list(self.db['testIOInfo'].find({'chip_number':chipNum, 
                                                     'ECON_type':econType},{'eTX_bitcounts':'$test_info.test_eTX_delayscan_1_32.metadata.eTX_bitcounts','eTX_errcounts':'$test_info.test_eTX_delayscan_1_32.metadata.eTX_errcounts', '_id':0}))
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
        if econType == 'ECOND':
            x = list(mydatabase['TestSummary'].find({'ECON_type':econType},{'outcome':'$individual_test_outcomes', 'passed':'$summary.passed', 'total': '$summary.total', '_id':0}))
            frac_passed = []
            for y in x:
                outcomes = y['outcome']
                passed = y['passed']
                total = y['total']
                tot_econd = []
                for key in outcomes:
                    if outcomes[key]== -2:
                        tot_econd.append(key)
                denominator = total - len(tot_econd)
                frac = passed/denominator
                frac_passed.append(frac)
            return np.array(frac_passed)
        if econType == 'ECONT':
            x = list(mydatabase['TestSummary'].find({'ECON_type':econType},{'outcome':'$individual_test_outcomes', 'passed':'$summary.passed', 'total': '$summary.total', '_id':0}))
            frac_passed = []
            for y in x:
                outcomes = y['outcome']
                passed = y['passed']
                total = y['total']
                tot_econd = []
                for key in outcomes:
                    if outcomes[key]== -2:
                        tot_econd.append(key)
                denominator = total - len(tot_econd)
                frac = passed/denominator
                frac_passed.append(frac)
            return np.array(frac_passed)
    def getTestingSummaries(self, econType = 'ECOND'):
        #This function returns a dataframe for the testing summary plots prepared by Marko
        #Please use the econType argument to specify ECOND or ECONT and the function expects a string for this argument
        if econType == 'ECOND':
            maps = ['passed', 'failed','error','skipped']
            counters = {}
            total = 0
            for obj in mydatabase['TestSummary'].find({'ECON_type':econType},{'individual_test_outcomes':1, '_id':0}):
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
        if econType == 'ECONT':
            maps = ['passed', 'failed','error','skipped']
            counters = {}
            total = 0
            for obj in mydatabase['TestSummary'].find({'ECON_type':econType},{'individual_test_outcomes':1, '_id':0}):
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
        
