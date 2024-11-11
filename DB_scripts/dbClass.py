import pymongo
import numpy as np
import pandas as pd

def constructQueryPipeline(query_map, econType='ECOND', lowerLim = None, upperLim=None, chipNum=None):
    match_stage = {
        "$match": {
            "ECON_type": econType
        }
    }
    if lowerLim is not None and upperLim is not None:
        match_stage["$match"]["chip_number"] = {"$lt": upperLim, "$gt": lowerLim}
    if chipNum is not None:
         match_stage["$match"]["chip_number"] = chipNum
    pipeline = [
            match_stage,
            {
                "$project": {
                    "chip_number": 1,
                    "Timestamp": 1,
                    "data": {field: f"${query_map[field]}" for field in query_map} 
                }
            },
            {
                "$match": {
                    "data": {"$ne": None}  # Filter out documents with None width
                }
            },
            {
                "$sort": {
                    "Timestamp": -1  # Sort by Timestamp in descending order
                }
            },
            {
                "$group": {
                    "_id": "$chip_number",  # Group by chip_number
                    "latest_data": {"$first": "$data"},  # Get the latest width
                    "latest_timestamp": {"$first": "$Timestamp"}  # Get the latest timestamp
                }
            }
        ]
    return pipeline

class Database:
    def __init__(self, ip, client):
        ## this connects to the database
        self.client = pymongo.MongoClient('localhost',ip)
        self.session = self.client.start_session()
        self.db = self.client[client] ## this name will probably change when we decide on an official name

    def pllCapbankWidthPlot(self, lowerLim=None, upperLim=None, voltage = '1p2', econType = 'ECOND'):
        #This function makes a plot of the PLL Capbank Width
        #if the user provides a range it will plot only over that range
        #if not it plots the capbank width over the whole dataset 
        #for different voltages use the name argument and please provide a string
        #1p08 for 1.08V, 1p2 for 1.2V, 1p32 for 1.32V
        #Also use the ECON type argument to make request info for ECOND vs ECONT 
        voltage_field_map = {
        '1p08': {'capbankwidth':'test_info.test_pll_capbank_width_1_08.metadata.pll_capbank_width'},
        '1p2': {'capbankwidth':'test_info.test_pll_capbank_width_1_2.metadata.pll_capbank_width'},
        '1p32': {'capbankwidth':'test_info.test_pll_capbank_width_1_32.metadata.pll_capbank_width'},
        }
        if voltage not in voltage_field_map:
            raise ValueError("Invalid voltage specified. Choose from '1p08', '1p2', '1p32'.")
        query_map = voltage_field_map[voltage]
        pipeline = constructQueryPipeline(query_map, econType=econType, lowerLim = lowerLim, upperLim=upperLim)
        cursor = self.db['testPLLInfo'].aggregate(pipeline)
        capbankwidth = np.array([doc['latest_data']['capbankwidth'] for doc in cursor if doc.get('latest_data') is not None and 'capbankwidth' in doc['latest_data'].keys()])
        return capbankwidth
        
                    
    def prbsMaxWidthPlot(self, lowerLim=None, upperLim=None, voltage = '1p2', econType = 'ECOND'):
        #This function makes a plot of the PRBS Max Width
        #if the user provides a range it will plot only over that range
        #if not it plots the capbank width over the whole dataset 
        #for different voltages use the name argument and please provide a string
        #1p08 for 1.08V, 1p2 for 1.2V, 1p32 for 1.32V
        #Also use the ECON type argument to make request info for ECOND vs ECONT 
        voltage_field_map = {
        '1p08': {'maxwidth':'test_info.test_ePortRXPRBS_1_08.metadata.maxwidth'},
        '1p2': {'maxwidth':'test_info.test_ePortRXPRBS_1_2.metadata.maxwidth'},
        '1p32': {'maxwidth':'test_info.test_ePortRXPRBS_1_32.metadata.maxwidth'}
        }
        if voltage not in voltage_field_map:
            raise ValueError("Invalid voltage specified. Choose from '1p08', '1p2', '1p32'.")
        query_map = voltage_field_map[voltage]
        pipeline = constructQueryPipeline(query_map, econType=econType, lowerLim = lowerLim, upperLim=upperLim)
        cursor = self.db['testIOInfo'].aggregate(pipeline)
        maxwidth = np.array([doc['latest_data']['maxwidth'] for doc in cursor if doc.get('latest_data') is not None and 'maxwidth' in doc['latest_data'].keys()])
        return maxwidth
                    
                    
    def etxMaxWidthPlot(self, lowerLim=None, upperLim=None, voltage = '1p2', econType = 'ECOND'):
        #This function makes a plot of the eTX Delay scan Max Width
        #if the user provides a range it will plot only over that range
        #if not it plots the capbank width over the whole dataset 
        #for different voltages use the name argument and please provide a string
        #1p08 for 1.08V, 1p2 for 1.2V, 1p32 for 1.32V
        #Also use the ECON type argument to make request info for ECOND vs ECONT 
        voltage_field_map = {
        '1p08': {'maxwidth':'test_info.test_eTX_delayscan_1_08.metadata.max_width'},
        '1p2': {'maxwidth':'test_info.test_eTX_delayscan_1_2.metadata.max_width'},
        '1p32': {'maxwidth':'test_info.test_eTX_delayscan_1_32.metadata.max_width'}
        }
        if voltage not in voltage_field_map:
            raise ValueError("Invalid voltage specified. Choose from '1p08', '1p2', '1p32'.")
        query_map = voltage_field_map[voltage]
        pipeline = constructQueryPipeline(query_map, econType=econType, lowerLim = lowerLim, upperLim=upperLim)
        cursor = self.db['testIOInfo'].aggregate(pipeline)
        maxwidth = np.array([doc['latest_data']['maxwidth'] for doc in cursor if doc.get('latest_data') is not None and 'maxwidth' in doc['latest_data'].keys()])
        return maxwidth

    def getVoltageAndCurrent(self, lowerLim=None, upperLim=None, econType = 'ECOND'):
        #This function makes a plot of the PLL Capbank Width
        #if the user provides a range it will plot only over that range
        #if not it plots the capbank width over the whole dataset 
        #for different voltages use the name argument and please provide a string
        # 1p08 for 1.08V, 1p2 for 1.2V, 1p32 for 1.32V
        #Also use the ECON type argument to make request info for ECOND vs ECONT 

        #note this test does not run at different voltages but I wanted to just have something there so the format of all the functions are uniform
        voltage_field_map = {
            'None': {
                    'current':'test_info.test_currentdraw_1p2V.metadata.current',
                    'voltage':'test_info.test_currentdraw_1p2V.metadata.voltage',
                    },
        }
        
        query_map = voltage_field_map['None']
        pipeline = constructQueryPipeline(query_map, econType=econType, lowerLim = lowerLim, upperLim=upperLim)
        cursor = self.db['testPowerInfo'].aggregate(pipeline)
        documents = list(cursor)

        current = np.array([
            doc['latest_data']['current'] for doc in documents 
            if doc.get('latest_data') is not None and 'current' in doc['latest_data'].keys()
        ])
        
        voltage = np.array([
            doc['latest_data']['voltage'] for doc in documents 
            if doc.get('latest_data') is not None and 'voltage' in doc['latest_data'].keys()
        ])
        return current, voltage

    def getBISTInfo(self, lowerLim=None, upperLim=None, econType='ECOND'):
        #This function makes a plot of the PLL Capbank Width
        #if the user provides a range it will plot only over that range
        #if not it plots the capbank width over the whole dataset 
        #for different voltages use the name argument and please provide a string
        # 1p08 for 1.08V, 1p2 for 1.2V, 1p32 for 1.32V
        #Also use the ECON type argument to make request info for ECOND vs ECONT 
        
        voltage_field_map = {
            'None': {
                    'first_failure':'test_info.test_bist.metadata.first_failure',
                    'bist_result':'test_info.test_bist.metadata.bist_results',
                    },
        }
        
        query_map = voltage_field_map['None']
        pipeline = constructQueryPipeline(query_map, econType=econType, lowerLim = lowerLim, upperLim=upperLim)
        cursor = self.db['testBistInfo'].aggregate(pipeline)
        documents = list(cursor)
        first_failure = np.array([
            doc['latest_data']['first_failure'] for doc in documents 
            if doc.get('latest_data') is not None and 'first_failure' in doc['latest_data'].keys()
        ])
        
        bist_result = [
            doc['latest_data']['bist_result'] for doc in documents 
            if doc.get('latest_data') is not None and 'bist_result' in doc['latest_data'].keys()
        ]
        return first_failure, bist_result
            
    def phaseScan2DPlot(self, chipNum, econType = 'ECOND', voltage = '1p2'):
        #returns the information needed to make the phase scan 2d plot
        #for a given chip number
        #for different voltages use the name argument and please provide a string
        # 1p08 for 1.08V, 1p2 for 1.2V, 1p32 for 1.32V
        #Also use the ECON type argument to make request info for ECOND vs ECONT 

        voltage_field_map = {
        '1p08': {'eRX_errcounts':'test_info.test_ePortRXPRBS_1_08.metadata.eRX_errcounts'},
        '1p2': {'eRX_errcounts':'test_info.test_ePortRXPRBS_1_2.metadata.eRX_errcounts'},
        '1p32': {'eRX_errcounts':'test_info.test_ePortRXPRBS_1_32.metadata.eRX_errcounts'}
        }
        if voltage not in voltage_field_map:
            raise ValueError("Invalid voltage specified. Choose from '1p08', '1p2', '1p32'.")
        query_map = voltage_field_map[voltage]
        pipeline = constructQueryPipeline(query_map, econType=econType, chipNum=chipNum)
        cursor = self.db['testIOInfo'].aggregate(pipeline)
        eRX_errcounts = np.array([doc['latest_data']['eRX_errcounts'] for doc in cursor if doc.get('latest_data') is not None and 'eRX_errcounts' in doc['latest_data'].keys()])
        return eRX_errcounts
        
                
    def delayScan2DPlot(self, chipNum, econType = 'ECOND', voltage = '1p2'):
        #returns the information needed to make the delay scan 2d plot
        #for a given chip number
        #for different voltages use the name argument and please provide a string
        # 1p08 for 1.08V, 1p2 for 1.2V, 1p32 for 1.32V
        #Also use the ECON type argument to make request info for ECOND vs ECONT 
        voltage_field_map = {
        '1p08': {
                'eTX_bitcounts':'test_info.test_eTX_delayscan_1_08.metadata.eTX_bitcounts',
                'eTX_errcounts':'test_info.test_eTX_delayscan_1_08.metadata.eTX_errcounts',
                },
        '1p2': {
                'eTX_bitcounts':'test_info.test_eTX_delayscan_1_08.metadata.eTX_bitcounts',
                'eTX_errcounts':'test_info.test_eTX_delayscan_1_08.metadata.eTX_errcounts',
                },
        '1p32': {
               'eTX_bitcounts':'test_info.test_eTX_delayscan_1_08.metadata.eTX_bitcounts',
                'eTX_errcounts':'test_info.test_eTX_delayscan_1_08.metadata.eTX_errcounts',
                }
        }
        if voltage not in voltage_field_map:
            raise ValueError("Invalid voltage specified. Choose from '1p08', '1p2', '1p32'.")
        query_map = voltage_field_map[voltage]
        pipeline = constructQueryPipeline(query_map, econType=econType, chipNum=chipNum)
        cursor = self.db['testIOInfo'].aggregate(pipeline)
        documents = list(cursor)
        print(documents)
        eTX_bitcounts = np.array([
            doc['latest_data']['eTX_bitcounts'] for doc in documents 
            if doc.get('latest_data') is not None and 'eTX_bitcounts' in doc['latest_data'].keys()
        ])
        
        eTX_errcounts = [
            doc['latest_data']['eTX_errcounts'] for doc in documents 
            if doc.get('latest_data') is not None and 'eTX_errcounts' in doc['latest_data'].keys()
        ]
        return eTX_bitcounts, eTX_errcounts
        

    def getFractionOfTestsPassed(self, econType = 'ECOND'):
        #This function grabs the fraction of tests that passed
        #So what this does is first count the number of tests that got skipped
        #And subtracts this from the total number of tests that were collected
        #This should give the total number of tests performed for either ECOND or ECONT
        #Then it just returns the total fraction of tests that pass for a given chip by
        #Dividing the total number of tests passed over the total number of tests performed
        #please use the econType argument to specify ECOND or ECONT and it expects a string input
        voltage_field_map = {
            'None': {
                    'outcome':'individual_test_outcomes',
                    'passed':'summary.passed',
                    'total': 'summary.total'
                    },
        }
        query_map = voltage_field_map['None']
        pipeline = constructQueryPipeline(query_map, econType=econType)
        cursor = self.db['TestSummary'].aggregate(pipeline)
        x = list(cursor)
        frac_passed = []
        # Extract outcomes, passed, and total
        outcomes = np.array([doc['latest_data']['outcome'] for doc in x])
        passed = np.array([doc['latest_data']['passed'] for doc in x])
        total = np.array([doc['latest_data']['total'] for doc in x])
        
        # Iterate over each outcome to compute fractions
        for i in range(len(outcomes)):
            tot_econt = np.array([key for key in outcomes[i] if outcomes[i][key] == -2])
            denominator = total[i] - len(tot_econt)
            
            # Handle division by zero
            if denominator > 0:
                frac = passed[i] / denominator
            else:
                frac = 0  # or np.nan, depending on how you want to handle it
            
            frac_passed.append(frac)
        
        # Convert to NumPy array
        return np.array(frac_passed)
        
    def getTestingSummaries(self, econType = 'ECOND'):
        #This function returns a dataframe for the testing summary plots prepared by Marko
        #Please use the econType argument to specify ECOND or ECONT and the function expects a string for this argument
        voltage_field_map = {
            'None': {
                    'individual_test_outcomes':'individual_test_outcomes',
                    },
        }
        query_map = voltage_field_map['None']
        pipeline = constructQueryPipeline(query_map, econType=econType)
        cursor = self.db['TestSummary'].aggregate(pipeline)
        outcomes = list(cursor)
        # Prepare a counter array for 'passed', 'failed', 'error', 'skipped'
        maps = ['passed', 'failed','error','skipped']
        counters = {}
        total = 0
        for obj in outcomes:
            for key, value in obj['latest_data']['individual_test_outcomes'].items():
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
        
        
