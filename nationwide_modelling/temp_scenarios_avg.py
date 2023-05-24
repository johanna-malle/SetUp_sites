# -*- coding: utf-8 -*-
"""
Desc: nationwide microclimate mapping
Created on 23.06.22 09:30
@author: malle
"""

import numpy as np
import datetime
from pathlib import Path
import math
import rasterio
import os
import glob


def read_file(file):
    with rasterio.open(file) as src:
        return (src.read(1))


if __name__ == '__main__':
    TSTART = datetime.datetime.now()
    numbers_sc = [1, 0.5, 0]  # set to 1 if scenario is RCP8.5, 0.5 if RCP4.5 and 0 if scenario is RCP2.6
    case_temp = 'cortasmax'
    for scenario in numbers_sc:
        if scenario == 0:
            print("Climate Scenario: RCP2.6")
            sce = 'RCP26'
        elif scenario == 0.5:
            print("Climate Scenario: RCP4.5")
            sce = 'RCP45'
        elif scenario == 1:
            print("Climate Scenario: RCP8.5")
            sce = 'RCP85'
        elif scenario == 2:
            print("Climate Scenario: Today")
            sce = 'None'
        else:
            sce = 'None'

        out_dir = Path('/home/malle/micromap_nationwide/temp_rasters_avg/' + case_temp)

        temp_loc_overall = Path('/home/malle/micromap_nationwide/CH2018_' + case_temp)

        temp_loc = temp_loc_overall

        for date_num in range(0, 1530, 1):
            yr_id_frac, yr_id_whole = math.modf(date_num / 153)
            if date_num > 764:
                real_date = datetime.date(2046 + math.floor(yr_id_whole) + 44, 6, 1) + \
                            datetime.timedelta(days=153 * yr_id_frac)
            else:
                real_date = datetime.date(2046 + math.floor(yr_id_whole), 6, 1) + \
                            datetime.timedelta(days=153 * yr_id_frac)

            out_avg_temp = out_dir / Path('Temp_avg_' + sce + '_' + real_date.strftime('%-Y-%m-%d') + '.tif')
            searchstring = '_EUR11_' + sce + '_QMgrid_summer10yrs' + str(date_num + 1) + '.tif'
            if out_avg_temp.is_file():
                pass
            else:
                temp_int_files = glob.glob(str(temp_loc) + '/*' + searchstring)

                if len(temp_int_files) == 3:
                    array_list = [read_file(x) for x in temp_int_files]
                    array_out = np.mean(array_list, axis=0)

                    with rasterio.open(temp_int_files[0]) as src:
                        meta = src.meta
                        profile1 = src.profile
                        profile1['compress'] = 'deflate'
                        profile1['predictor'] = 2  # 'LZW'
                        profile1['dtype'] = rasterio.int16

                    with rasterio.open(out_avg_temp, 'w', **profile1) as dst:
                        dst.write(array_out.astype(rasterio.int16), 1)

                    os.remove(temp_int_files[0])
                    os.remove(temp_int_files[1])
                    os.remove(temp_int_files[2])

        TEND4 = datetime.datetime.now()
        print(f'Processing time for szenario: {TEND4 - TSTART} [HH:MM:SS]')

    TEND4 = datetime.datetime.now()
    print(f'Total processing time: {TEND4 - TSTART} [HH:MM:SS]')
    print(f'Total processing time: {TEND4 - TSTART} [HH:MM:SS]')