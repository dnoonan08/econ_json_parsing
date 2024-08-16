# Functions to upload files in database


import pymongo
from pymongo import MongoClient, InsertOne
import numpy as np
import glob
import json

def selector(input):
    if input == 'passed':
        return 1
    elif input == 'failed':
        return 0
    ## This is for a test that was skipped
    else:
        return -1


def stringReplace(word):
    if "[" in word:
        word = word.replace("[","_")
    if ".." in word:
        word = word.replace("..","_")
    if "/" in word:
        word = word.replace("/","_")
    if "]" in word:
        word = word.replace("]", "")
    return word

def jsonFileUploader(fname,mycol):
    ## open the JSON File
    with open(fname) as jsonfile:
        data = json.load(jsonfile)
    ## preprocess the JSON file
    dict = {
            "summary": {'passed': data['summary']['passed'], 'total':data['summary']['total'], 'collected':data['summary']['collected']},
            "individual_test_outcomes": {
                f"{stringReplace(test['nodeid'].split('::')[1])}": selector(test['outcome']) for test in data['tests']
            },
            "tests":{
                f"{stringReplace(test['nodeid'].split('::')[1])}": {
                    "metadata": test['metadata'] if 'metadata' in test else None,
                    "failure_information":{
                        "failure_mode": test['call']['traceback'][0]['message'] if test['call']['traceback'][0]['message'] != '' else test['call']['crash']['message'],
                        "failure_cause": test['call']['crash']['message'],
                        "failure_code_line": test["call"]["crash"]["lineno"],
                    } if 'failed' in test['outcome'] else None,
                } for test in data['tests']
            },
            "identifier": data['chip_number'],
            "branch": data['branch'],
            'commit_hash': data['commit_hash'],
            'remote_url': data['remote_url'],
            'FPGA-hexa-IP': data['FPGA-hexa-IP'],
            'status': data['status'],
            'firmware_name': data['firmware_name'],
            'firmware_git_desc': data['firmware_git_desc'],
            'filename': fname,
            'ECON_type':(fname.split("report"))[1].split("_")[1],
            }
         ## Insert File into the DB 
    dict['tests']['test_alignment_erx']['metadata']['align_pattern'] = str(dict['tests']['test_alignment_erx']['metadata']['align_pattern'])
    
    x = mycol.insert_one(dict) # Write in DB