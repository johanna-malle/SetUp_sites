# Forest-change scenarios at Biodiversity Monitoring (BDM) sites in Switzerland

Author: Dr Johanna Malle (<mailto:johanna.malle@wsl.ch>)

Set of scripts needed to a) prep for forest change scenarios b) run forest change scenarios and c) compute microclimate for these scenarios (past/present/future) at 1x1km biodiversity sites in Switzerland. 

Use **raster_prep.py** to cut national CHM/DTM and create DSM for spatial extent of interest. 

Use **run_pycrown.py** to delineate trees and create shapefiles for all tree crowns. Before running the script you need to install pycrown (create seperate environment), details on how to do this as well as the method used by pycrown can be found here:
https://github.com/manaakiwhenua/pycrown

Use **adapt_chm.py** to create a modified CHM based on user input (manual tree cutting, automated tree cutting or random tree cutting)
If wanting to run from command line, set USE_CLI_ARGS=TRUE in top of script, otherwise edit settings on bottom of the script.

Use **micromap_BDM.py** to calculate microclimate at the selected BDM sites. Select which forest change scenario to run for, which model (soil, high, low) and which climate scenario to run.

In the **analysis** folder there are a set of scripts for post-processing results, merging transmissivity, and calculating temperature tolerances. 

## Main outputs
raster_prep.py:
* **CHM, DTM, DSM** for extent of interest (stored as .tif-file)
* **Forest mask** for extent of interest (stored as .tif-file)
* **Plots** for cut CHM, DTM, DSM, forest mask

adapt_chm.py:
* **adapted CHM** (stored as .tif-file)
* **comparative plots** (before/after forest-change scenario, stored as .tif-file)

run_pycrown.py:
* **tree-delinated CHM** (stored as .tif-file)
* **crown locations** (stored as .shp-file)

## Requirements


### Installation and environment set-up for forest-change scenarios:
Python 3.7 is required.
Only tested on Ubuntu 20.04

#### Environment set-up (with Conda package manager)
Create the environment and install all required packages

`conda env create -f environment.yml`

##### Activate the environment

Windows: `activate forest_change_env`

Linux: `source activate forest_change_env`

Once this is set up you are technically able to run all scripts in this repository except the pycrown delineation. Before running this script you need to install pycrown (create seperate environment), details on how to do this and how it works can be found here:
https://github.com/manaakiwhenua/pycrown


## Known problems/caveats

Paths etc. still need to mostly be updated in the scripts. Large amounts of input data required.

