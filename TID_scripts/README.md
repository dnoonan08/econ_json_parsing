# TID scripts from July 2024 TID test at CERN

Setup of the framework: relies on a JSON Github repository:

https://github.com/mstamenk/tid-july-2024

# Setting up

```
git clone git@github.com:dnoonan08/econ_json_parsing.git
git submodule add git@github.com:mstamenk/tid-july-2024.git
```

Setting up the environment

```
source setup.sh # sets MYROOT bash variable as well as PYTHONPATH
```

# Structure

```
- common.py # all script needed for all plotting scripts
- current_tid.py # plot current vs TID - creates repo with plots current_vs_tid
```

