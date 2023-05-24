# -*- coding: utf-8 -*-
"""
Desc: nationwide microclimate mapping
Created on 23.06.22 09:30
@author: malle
"""

import pandas as pd
import numpy as np
import datetime
import time
import statsmodels.formula.api as smf
from pathlib import Path
import math
import rasterio
import concurrent.futures
import rioxarray
from time import strftime
import os
import sys
import glob
import netCDF4

if len(sys.argv) != 3:
    print("Usage ", sys.argv[0], " <p> <N>")
    sys.exit()
else:
    p = int(sys.argv[1])
    N = int(sys.argv[2])


def compute(infile_asp, infile_slope, infile_topo, infile_wet, infile_vegh, infile_temp, infile_svf,
            mod_temp, lme_temp, month_in, window):
    # print(f"Processing data: window={window}")

    with rasterio.open(infile_svf, cache=False) as src1:
        transm = src1.read(window=window)
        transm1 = np.expand_dims(transm[month_in, :, :], axis=0)

    if np.sum(np.isnan(transm1)) < transm1.shape[1] * transm1.shape[2]:

        with rasterio.open(infile_slope, cache=False) as src1:
            slope = src1.read(window=window)
        with rasterio.open(infile_topo, cache=False) as src1:
            topo_index = src1.read(window=window)
        with rasterio.open(infile_wet, cache=False) as src1:
            topo_wetness = src1.read(window=window)
        with rasterio.open(infile_asp, cache=False) as src1:
            aspect_n = src1.read(window=window)
        with rasterio.open(infile_vegh, cache=False) as src1:
            vegh = src1.read(window=window)
        with rasterio.open(infile_temp, cache=False) as src1:
            temp_used = src1.read(window=window)
            temp_used[temp_used == 0] = -32768
            temp_used[transm1 == -32768] = -32768

        stack_temp = np.vstack((temp_used, transm1, topo_index, topo_wetness, vegh, aspect_n, slope))
        del temp_used, topo_index, topo_wetness, vegh, aspect_n, slope
        id_array_temp = np.transpose(np.array
                                     (np.meshgrid(range(stack_temp.shape[1]), range(stack_temp.shape[2])))
                                     .T.reshape(-1, 2), (1, 0))
        combo_all_temp = np.zeros((stack_temp.shape[0] + id_array_temp.shape[0], id_array_temp.shape[1]),
                                  dtype=np.int16)
        combo_all_temp[:2, :] = id_array_temp
        combo_all_temp[2:, :] = stack_temp[:, id_array_temp[0, :], id_array_temp[1, :]]
        del stack_temp, id_array_temp
        combo_all_temp[combo_all_temp > 100000] = -32768

        df_temp_all = pd.DataFrame(np.transpose(combo_all_temp),
                                   columns=['idx1', 'idx2', 'Tmax_meteo', 'trans_Tmax', 'topo_index',
                                            'topo_wetness', 'vegh', 'aspect_n', 'slope'])
        del combo_all_temp
        df_temp_all["Intercept"] = np.ones(np.shape(df_temp_all["vegh"]))
        df_temp_all["Tmax_meteo:trans_Tmax"] = np.ones(np.shape(df_temp_all["vegh"]))

        micro_map_pred = (mod_temp.predict(lme_temp.fe_params,
                                           exog=df_temp_all[["Intercept", "Tmax_meteo", "trans_Tmax",
                                                             "Tmax_meteo:trans_Tmax", "topo_index", "topo_wetness",
                                                             "vegh", "aspect_n", "slope"]])).astype(np.int16)
        del df_temp_all
        micro_map_pred[micro_map_pred < -10000] = -32768
        micro_map_pred[np.isnan(micro_map_pred)] = -32768
        micro_map_pred[micro_map_pred > 5000] = -32768

    else:
        micro_map_pred = np.zeros([transm1.shape[1] * transm1.shape[2]])
        micro_map_pred[micro_map_pred == 0] = -32768

    micro_map_pred = np.reshape(micro_map_pred, (window.height, window.width))

    return window, micro_map_pred


def main(infile_asp, infile_slope, infile_topo, infile_wet,
         infile_vegh, infile_temp, infile_svf, outfile_micro, mod_tmin1,
         lme_tmin1, num_work, month_in):
    """Process infiles block-by-block and write to a new file
    """
    with concurrent.futures.ProcessPoolExecutor(max_workers=num_work) as executor:

        with rasterio.open(infile_asp) as src:
            profile1 = src.profile
            profile1['tiled'] = True
            profile1['blockxsize'] = 2560  # 4000 must be multiple of 16
            profile1['blockysize'] = 2560  # 4000 must be multiple of 16
            profile1['compress'] = 'DEFLATE'  # 'LZW'
            profile1['predictor'] = 2
            profile1['dtype'] = rasterio.int16
            profile1['nodata'] = -32768

            with rasterio.open(outfile_micro, "w+", **profile1) as dst:
                windows = (window for ij, window in dst.block_windows())
                futures = {executor.submit(compute, infile_asp, infile_slope, infile_topo, infile_wet, infile_vegh,
                                           infile_temp, infile_svf, mod_tmin1, lme_tmin1, month_in, window) for window
                           in windows}

                while futures:
                    done, futures = concurrent.futures.wait(futures, return_when=concurrent.futures.FIRST_COMPLETED)

                    for future in done:
                        window, data = future.result()
                        dst.write(data.astype(np.int16), indexes=1, window=window)
                        del future
                    for window in windows:
                        futures.add(executor.submit(compute, infile_asp, infile_slope, infile_topo, infile_wet,
                                                    infile_vegh, infile_temp, infile_svf, mod_tmin1, lme_tmin1,
                                                    month_in, window))


if __name__ == '__main__':
    TSTART = datetime.datetime.now()
    model_int = ["low", "high", "soil"]
    num_workers = p

    for model in model_int:
        start_model = time.time()
        dfs_model = pd.read_csv('/home/malle/micromap_nationwide/master_mods_in/master_mod_dfs_' + model + '.csv')
        mod_tmax = smf.mixedlm('Tmax ~ Tmax_meteo * trans_Tmax + topo_index + topo_wetness + vegh + aspect_n + '
                               'slope', dfs_model, groups=dfs_model['region'])
        lme_tmax = mod_tmax.fit()

        print("Model = " + model)

        wrk_dir = '/home/malle/slfhome/Postdoc2/experiment_sites_select'

        rasters_bf = Path('/home/malle/micromap_nationwide/PredRasters')
        topo_index_file = rasters_bf / 'TPI.tif'
        topo_wetness_file = rasters_bf / 'TWI.tif'
        aspect_n_file = rasters_bf / 'aspect_n.tif'
        slope_file = rasters_bf / 'slope.tif'
        transm_file = rasters_bf / 'transmissivity.tif'  # make sure right month is loaded here
        vegh_file = rasters_bf / 'VHM.tif'

        temp_loc_overall = Path('/home/sulmonie/T_past/cor_tasmax')
        out_folder_tmin = Path('/home/malle/micromap_nationwide/micromaps_out_present/' + model + '/tmax')
        out_folder_tmin.mkdir(parents=True, exist_ok=True)

        for date_num in range(1530, 3060, 1):
            TSTART_timestep = datetime.datetime.now()
            yr_id_frac, yr_id_whole = math.modf(date_num / 153)
            real_date = datetime.date(2002 + math.floor(yr_id_whole), 6, 1) + \
                        datetime.timedelta(days=153 * yr_id_frac)

            out_micromap_map_temp_rast = out_folder_tmin / Path('microtemp_' + real_date.strftime('%-Y-%m-%d') + '.tif')

            out_micromap_map_temp_nc = out_folder_tmin / Path('microtemp_' + real_date.strftime('%-Y-%m-%d') + '.nc')

            if out_micromap_map_temp_rast.is_file():
                os.remove(out_micromap_map_temp_rast)

            if out_micromap_map_temp_nc.is_file():
                if out_micromap_map_temp_nc.stat().st_size < 200000000:
                    os.remove(out_micromap_map_temp_nc)

            if out_micromap_map_temp_nc.is_file():
                pass
            else:
                date_int = '-' + f"{real_date.month:02d}" + '-' + f"{real_date.day:02d}"
                searchstring = '_corrected_' + str(date_num + 1) + '.tif'

                temp_int_files = glob.glob(str(temp_loc_overall) + '/*' + searchstring)
                month_in = int(real_date.strftime("%m"))

                # ----------------------------------------------------------------------------
                # RUN ACTUAL PREDICTION FUNCTION
                # ---------------------------------------------------------------------------
                main(str(aspect_n_file), str(slope_file), str(topo_index_file),
                     str(topo_wetness_file), str(vegh_file), temp_int_files[0], str(transm_file),
                     out_micromap_map_temp_rast, mod_tmax, lme_tmax, num_workers, month_in)

                # ----------------------------------------------------------------------------
                # Write Netcdf:
                # ----------------------------------------------------------------------------
                raster = rioxarray.open_rasterio(str(out_micromap_map_temp_rast))
                raster.coords["band"] = (
                        raster.coords["band"] + int((real_date - datetime.date(1900, 1, 1)).days - 1)).astype(
                    'int32')
                raster.coords["x"] = (raster.coords["x"]).astype(np.int32)
                raster.coords["y"] = (raster.coords["y"]).astype(np.int32)
                raster = raster.rename({'y': 'northing', 'x': 'easting', 'band': 'time'})

                ds = raster.to_dataset(name='data')
                del raster
                ds.time.attrs['units'] = 'days since 1900-01-01 00:00:00'

                ds.data.attrs['units'] = 'degree C'

                ds.data.attrs['_FillValue'] = int(-32768)
                ds.data.attrs['missing_value'] = int(-32768)
                ds.data.attrs['scale_factor'] = 0.01

                ds.northing.attrs['standard_name'] = 'projection y coordinate'
                ds.northing.attrs['long_name'] = 'swiss northing (lv95)'
                ds.northing.attrs['units'] = 'meters_north'
                ds.easting.attrs['standard_name'] = 'projection x coordinate'
                ds.easting.attrs['long_name'] = 'swiss easting (lv95)'
                ds.easting.attrs['units'] = 'meters_east'

                # del ds.spatial_ref.attrs['spatial_ref']
                ds.attrs['Instiution'] = 'Swiss Federal Institute for Forest, Snow and Landscape Research WSL'
                ds.attrs['history'] = 'created on ' + strftime("%d/%m/%Y %H:%M:%S")
                ds.attrs['title'] = 'Microclimate Past Temperatures Switzerland based on CH2018 data'
                ds.attrs[
                    'comment'] = 'NOTE: based on LME modelling, including transmissivity ' \
                                 '(daily averages between 8h and 14h UTC)'
                ds.attrs['version'] = '1.0'
                ds.attrs['hostname'] = os.uname().nodename
                ds.attrs['username'] = 'malle'  # os.getlogin()
                ds['data'].encoding['dtype'] = 'int16'

                # rename data variables to be consistent with R implementation
                if model == 'soil':
                    data_name = 'soiltmax'
                    long_name = 'daily maximum soil temperature 5cm below the surface'
                elif model == 'high':
                    data_name = 'tasmax'
                    long_name = 'daily maximum air temperature at 1m above ground'
                elif model == 'low':
                    data_name = 'tasmax'
                    long_name = 'daily maximum air temperature at 5cm above ground'
                else:
                    data_name = 'None'
                    long_name = 'None'

                ds.data.attrs['long_name'] = long_name
                ds[data_name] = ds['data']
                ds = ds.drop(['data'])

                encoding = {}
                encoding_keys = ("_FillValue", "dtype", "scale_factor", "add_offset", "grid_mapping")
                for data_var in ds.data_vars:
                    encoding[data_var] = {key: value for key, value in ds[data_var].encoding.items() if
                                          key in encoding_keys}
                    encoding[data_var].update(zlib=True, complevel=5)

                ds.to_netcdf(str(out_micromap_map_temp_nc), engine="netcdf4", encoding=encoding)
                del ds
                os.remove(str(out_micromap_map_temp_rast))

                TEND3a = datetime.datetime.now()
                print(
                    f'Done with pred. for {model}, timestep: {real_date}, took: {TEND3a - TSTART_timestep} [HH:MM:SS]')

    TEND4 = datetime.datetime.now()
    print(f'Total processing time: {TEND4 - TSTART} [HH:MM:SS]')