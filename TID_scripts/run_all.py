# Script to run all the tests

import os, glob

import argparse
parser = argparse.ArgumentParser(description='Args')
parser.add_argument('--path', type = str) # repo name on github json repo
args = parser.parse_args()

python_scripts = glob.glob('./*.py')
python_scripts = [os.path.basename(s) for s in python_scripts if 'common' not in s and 'run_all' not in s and 'check_reports' not in s]

print(python_scripts)

path = args.path

cmd = 'python3 %s --path %s'

for s in python_scripts:
    new_cmd = cmd%(s,path)
    print(new_cmd)
    os.system(new_cmd)