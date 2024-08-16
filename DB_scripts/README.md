# HGCAL ECON Testing local DB
Scripts to create, parse and plot the local DB informations from Fermilab Robot testing for ECON. 

# Setting up the environment

See (hgcal-mongodb)[https://github.com/mstamenk/hgcal-mongodb] to get the MongoDB environment. 

To start the mongo DB locally:
```
mongod --dbpath /usr/local/var/mongodb --logpath /usr/local/var/log/mongodb/mongo.log --fork
```

This command is also included in an alias in the setup.sh script

```
source setup.sh
startdb
```

# Creating a DB

All the main functions for parsing the database are defined in the `json_uploaded.py`

An example to create a database from scratch is shown in `create_db.py`. 

Summary plots production can be found in `summary.py`.

