# -*- coding: utf-8 -*-
"""
Desc: Script to manipulate shapefiles (canopy height models) for land use change experiments
3 Options implemented to remove trees: 'manual' , 'auto', 'random'
'manual' allows user to select area of interest to remove all trees within selected perimeter (e.g. wind-throw events)
'auto' allows user to specify a number, based on which every xth tree will be removed
'random ' allows user to specify fraction of forest which will be randomly removed

Created on 20.01.22 09:28
@author: malle
"""

from src.forest_change_functions import *


USE_CLI_ARGS = False  # set to True if running from the command line, set to False if running from PyCharm

@click.command()
@click.option('--cut_trees_method', help='auto or random or manual [str]')
@click.option('--amount_trees_cut', default=None, type=float, help='only needs to be set if auto - '
                                                                   'every xth tree to be cut [float]')
@click.option('--random_fraction_cut', default=None, type=float, help='only needs to be set if random - '
                                                                      'fraction of dataset to be cut [float]')
@click.option('--path_in', help='input path [str]')
def cli(cut_trees_method, amount_trees_cut, random_fraction_cut, path_in, buffer, forest_mask, buffer_peri):
    main(cut_trees_method, amount_trees_cut, random_fraction_cut, path_in, buffer, forest_mask, buffer_peri)


if __name__ == '__main__':

    if USE_CLI_ARGS:
        cli()
    else:
        cut_trees_method = 'manual'  # options: 'manual' , 'auto', 'random'-
        amount_trees_cut = 3  # if using auto setting - every xth tree to cut (if random/manual - ignore)
        random_fraction_cut = 0.25  # if using random setting - which fraction of all trees should be cut? (if auto/manual - ignore)
        buffer = 0  # if wanting to add buffer around each individual tree crown [if pycrown delination is done well this should not be necessary]
        buffer_peri = 200  # meters added to perimeter of BDM site (not to be incorporated into this analysis, but for transmissivity calculations)
        forest_mask = 1  # set to 0 or 1 => select x percent of forest within forest mask only [default: 1]

        path_in = '/home/malle/pycrown/experiment_sites_select/BDM_3/result/' \
                  'dalponteCIRC_numba_12mrad_ws3_chm3_thseed01_thcrown01/'  # path to pycrown output
        main(cut_trees_method, amount_trees_cut, random_fraction_cut, path_in, buffer, forest_mask, buffer_peri)
