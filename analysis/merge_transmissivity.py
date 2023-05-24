# -*- coding: utf-8 -*-
"""
Desc: Script to analyse and merge Transmissivity output
Created on 17.03.22 14:42
@author: malle
"""

import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point
import pandas as pd
from osgeo import gdal, osr
from pathlib import Path
import os
import xarray as xr
from scipy import interpolate
import datetime
import imageio
import rioxarray
import re
from src.help_functions import raster2array, search_in_file


if __name__ == '__main__':


    TSTART = datetime.datetime.now()
    # folder where all tiles of CanRad are stored
    site_all = ['BDM_1']  #,'BDM_2','BDM_3'] #,'BDM_2','BDM_3']
    num_all = ['050']#,'025','075']

    for site in site_all:
        for num in num_all:
            basefolder = Path('/home/malle/transm_calcs/'+site+'/Output_CR_10m_summer_'+num+'_fm1_0mbuffer')

            # what resolution [m]?
            nums_file = [int(s) for s in re.findall(r'\d+', str(basefolder))]

            resolution = nums_file[1]  # 10
            print('Site = '+site+', Resolution = '+str(resolution)+'m')
            print(basefolder)
            if ~resolution % 5 == 0:
                print('Double check resolution obtained from filename... it does not seem to be divisible by 5, '
                      'instead it is: '+str(resolution)+'m')

            # deal with forest mask
            if resolution == 20:  # still use 10m forest mask
                resolution1 = 10
            else:
                resolution1 = resolution

            forest_mask_file = '/home/malle/slfhome/Postdoc2/experiment_sites_select/' + site + '/Forest_mask_'\
                               + str(resolution1)+'m.tif'
            fi = gdal.Open(forest_mask_file)
            gt = fi.GetGeoTransform()
            proj = fi.GetProjection()

            if resolution != resolution1:
                gt1 = list(gt)
                gt1[1] = resolution
                gt1[5] = -resolution
                gt = tuple(gt1)

            xds_fm = rioxarray.open_rasterio(forest_mask_file)
            a45 = np.where(xds_fm.values == 128, np.nan, xds_fm.values)
            xds_fm.values = a45
            fm_df = xds_fm.to_dataframe(name="mask_value").reset_index()
            to_mask = fm_df[np.isnan(fm_df['mask_value'])]
            fm_array, fm_array_metadata = raster2array(forest_mask_file)

            plot_dir = basefolder / 'Plots'
            isExist = os.path.exists(plot_dir)
            if not isExist:
                os.makedirs(plot_dir)
                print("Plot directory is created!")

            tif_dir = basefolder / 'OutTifs'
            isExist = os.path.exists(tif_dir)
            if not isExist:
                os.makedirs(tif_dir)
                print("tif directory is created!")

            tif_dir_month = basefolder / 'OutTifs_monthly'
            isExist = os.path.exists(tif_dir_month)
            if not isExist:
                os.makedirs(tif_dir_month)
                print("tif directory is created!")

            # load forest mask
            fig1 = plt.figure(figsize=(13, 4))
            ax_old = fig1.add_subplot(111)
            ax_old.set_title('Forest mask ch', fontsize=9)
            plt.imshow(fm_array, cmap=plt.get_cmap('plasma'), extent=fm_array_metadata['extent'])
            cbar1 = plt.colorbar(fraction=0.046, pad=0.04)
            cbar1.set_label('Canopy height [m]', rotation=270, labelpad=20)
            fm_plot = plot_dir / "forest_mask.png"
            fig1.savefig(fm_plot, dpi=350, bbox_inches='tight')
            plt.close()

            # get all tile names
            ignored = {"Plots","OutTifs", "OutTifs_monthly"}
            calc_locs = [x for x in os.listdir(basefolder) if x not in ignored]

            all_calcs = []
            for calc_loc in calc_locs:
                loc_path = basefolder / calc_loc
                ds = xr.open_dataset(loc_path / Path("Output_" + calc_loc + ".nc"))
                df = ds.to_dataframe()
                df = df.reset_index(level=[0, 1])
                df = df.set_index(pd.DatetimeIndex(df['datetime']))
                df = df.between_time('9:00', '15:00')   # this should be changed to 9-15 CET, but for the time being I leave it
                df1 = df.groupby('Coordinates').resample('1D').mean()
                all_calcs.append(df1)
                # f = netCDF4.Dataset(loc_path / Path("Output_" + calc_loc + ".nc"))
                # time_all = f.variables['datetime']
                # dtime = netCDF4.num2date(time_all[:], time_all.units)

            # combine list
            df_all = pd.concat(all_calcs)
            df_all_new = df_all.reset_index(level=[1])



            df_all_new.to_pickle(plot_dir / "combined_frame.pkl")  # later do: df = pd.read_pickle(file_name)

            TEND1 = datetime.datetime.now()
            print(f'Processing time to combine all sub-tiles into dataframe: {TEND1-TSTART} [HH:MM:SS]')

            df_all_forest = df_all_new.copy()
            df_all_forest.insert(0, 'index', np.arange(len(df_all_forest)), True)
            df_all_forest = df_all_forest.set_index('index')

            # set all values that lay outside of forests to nan for analysis:
            if resolution == 20:
                coords_cut2 = list(zip(to_mask['x']-5, to_mask['y']-5))
            else:
                coords_cut2 = list(zip(to_mask['x'], to_mask['y']))

            df_all_forest.loc[df_all_forest[["easting", "northing"]].apply(tuple, 1).isin(coords_cut2),
                              ['Forest_Transmissivity', 'Vf_hemi', 'Vf_planar', 'SWR_total', 'SWR_direct']] = np.nan


            # this was quite a bit slower:
            # coords_cut = np.array(to_mask[['x','y']])

            # def check_cut(easting,northing):
            #       if  any( (easting == coords_cut[:,0]) & (northing == (coords_cut[:,1]))):
            #          return true
            #      else:
            #         return false

            # df_all_forest['test2']=df_all_forest.apply(lambda x: check_cut(x['easting'],x['northing']),axis=1)
            # df_all_forest.loc[df_all_forest['test2'],
            # ['forest_transmissivity','vf_hemi','vf_planar','swr_total','swr_direct']] = np.nan

            # ...and this was the slowest: >3min
            # coords_cut = np.array(to_mask[['x','y']])
            # for coord in coords_cut:
            #     df_all_forest.loc[(df_all_forest.easting == coord[0] ) & (df_all_forest.northing == coord[1] ),
            #     ['Forest_Transmissivity','Vf_hemi','Vf_planar','SWR_total','SWR_direct']] = np.nan

            # df_all_forest = df_all_forest.set_index('Coordinates')

            TEND2 = datetime.datetime.now()
            print(f'Processing time to mask out non-forested areas: {TEND2-TEND1} [HH:MM:SS]')

            df_all_forest.to_pickle(plot_dir / "combined_frame_forest.pkl")  # later do: df = pd.read_pickle(file_name)

            t3 = df_all_new[['Forest_Transmissivity', 'Vf_hemi', 'datetime']].groupby('datetime').describe()
            t3_forest = df_all_forest[['Forest_Transmissivity', 'Vf_hemi', 'datetime']].groupby('datetime').describe()

            fig = plt.figure(figsize=(10, 5))
            ax = fig.add_subplot(111)
            plt.plot(t3.index, t3['Forest_Transmissivity']['mean'], label="Mean")
            plt.plot(t3_forest.index, t3_forest['Forest_Transmissivity']['mean'], label="Mean forest")
            plt.plot(t3.index, t3['Forest_Transmissivity']['25%'], label="25th percentile")
            plt.plot(t3_forest.index, t3_forest['Forest_Transmissivity']['25%'], label="25th percentile forest")
            plt.plot(t3.index, t3['Forest_Transmissivity']['75%'], label="75th percentile")
            plt.plot(t3_forest.index, t3_forest['Forest_Transmissivity']['75%'], label="75th percentile forest")
            plt.legend(loc='upper right')
            plt.title('BD 1')
            plt.xlabel('Time')
            plt.ylabel('Forest Transmissivity [%]')
            fig_save = plot_dir / Path("mean_transm.png")
            fig.savefig(fig_save, dpi=350, bbox_inches='tight')
            plt.close()

            # The size of each step in days
            day_delta = datetime.timedelta(days=1)
            start_date_copy = datetime.date(2020, 6, 1)

            df_all_forest.set_index('datetime', inplace=True)

            for switch in [0,1]:

                if switch == 1:
                    start_date = datetime.date(2019, 10, 1)
                    end_date = datetime.date(2019, 10, 31)
                    print('just october...')
                else:
                    start_date = datetime.date(2020, 6, 1)
                    end_date = datetime.date(2020, 9, 30)
                    print('june-september...')


                # loop through from May to September, 1 plot per week
                while start_date <= end_date:
                    #print(start_date)
                    out_transm_tif =  tif_dir / Path('transm' + pd.Timestamp(start_date).strftime('%Y-%m-%d') + '.tif')
                    #print(out_transm_tif)
                    if out_transm_tif.is_file():
                        pass
                        # print('not re-generating file...')
                    else:
                        # print('making file...')
                        # cut out calculated transmissivity for this day
                        df_cut = df_all[df_all.index.isin(np.array([pd.Timestamp(start_date)]).astype('datetime64[ns]'), level=1)]
                        df_cut_forest = df_all_forest[df_all_forest.index.isin
                                                      (np.array([pd.Timestamp(start_date)]).astype('datetime64[ns]'), level=0)]

                        geometry = [Point(xy) for xy in zip(df_cut.easting, df_cut.northing)]
                        df_t = df_cut.drop(['easting', 'northing'], axis=1)
                        gdf = gpd.GeoDataFrame(df_t, crs="EPSG:2056", geometry=geometry)
                        df_t_for = df_cut_forest.drop(['easting', 'northing'], axis=1)
                        gdf_for = gpd.GeoDataFrame(df_t_for, crs="EPSG:2056", geometry=geometry)

                        lon, lat = df_cut['easting'], df_cut['northing']
                        xmin, ymin, xmax, ymax = [lon.min() - (resolution / 2), lat.min() - (resolution / 2), lon.max() + (resolution / 2),
                                                  lat.max() + (resolution / 2)]
                        lon_list = np.arange(xmin, xmax, (xmax - xmin) / (1000 / resolution))
                        lat_list = np.arange(ymin, ymax, (ymax - ymin) / (1000 / resolution))

                        lon_2d, lat_2d = np.meshgrid(lon_list, lat_list)
                        r = interpolate.griddata(points=(lon-resolution/2, lat-resolution/2), values=gdf['Forest_Transmissivity'].values, xi=(lon_2d, lat_2d))
                        r = np.flip(r, axis=0)

                        r_for = interpolate.griddata(points=(lon-resolution/2, lat-resolution/2), values=gdf_for['Forest_Transmissivity'].values, xi=(lon_2d, lat_2d))
                        r_for = np.flip(r_for, axis=0)

                        result = np.where(r < 0, np.nan, r)
                        result_for = np.where(r_for < 0, np.nan, r_for)

                        extent = [xmin, xmax, ymin, ymax]


                        if start_date == start_date_copy:
                            v_for = interpolate.griddata(points=(lon, lat), values=gdf_for['Vf_hemi'].values, xi=(lon_2d, lat_2d))
                            v_for = np.flip(v_for, axis=0)
                            v_result_for = np.where(v_for < 0, np.nan, v_for)

                            fig_save = plot_dir / Path("VF_hemi_for.png")
                            fig = plt.figure(figsize=(10, 10))
                            ax = fig.add_subplot(111)
                            ax.set_title('SVF mean/median = '+str(round(np.nanmean(v_result_for), 1)) + '/' +
                                         str(round(np.nanmedian(v_result_for), 1)))
                            ax.grid(False)
                            plt.imshow(v_result_for, cmap=plt.get_cmap('plasma'), vmin=0, vmax=100, extent=extent)
                            cbar1 = plt.colorbar(fraction=0.046, pad=0.04)
                            cbar1.set_label('VF_hemi [%]', rotation=270, labelpad=20, fontsize=10)
                            fig.savefig(fig_save, dpi=350, bbox_inches='tight')
                            plt.close()

                            v_for = interpolate.griddata(points=(lon, lat), values=gdf['Vf_hemi'].values, xi=(lon_2d, lat_2d))
                            v_for = np.flip(v_for, axis=0)
                            v_result = np.where(v_for < 0, np.nan, v_for)

                            fig_save = plot_dir / Path("VF_hemi.png")
                            fig = plt.figure(figsize=(10, 10))
                            ax = fig.add_subplot(111)
                            ax.set_title('SVF mean/median = '+str(round(np.nanmean(v_result), 1))+'/'+str(round(np.nanmedian(v_result), 1)))
                            ax.grid(False)
                            plt.imshow(v_result, cmap=plt.get_cmap('plasma'), vmin=0, vmax=100, extent=extent)
                            cbar1 = plt.colorbar(fraction=0.046, pad=0.04)
                            cbar1.set_label('VF_hemi [%]', rotation=270, labelpad=20, fontsize=10)
                            fig.savefig(fig_save, dpi=350, bbox_inches='tight')
                            plt.close()

                            # write out SVF tifs for further analysis
                            out_transm_tif = plot_dir / Path('SVF.tif')

                            srs = osr.SpatialReference()
                            srs.ImportFromEPSG(2056)

                            driver = gdal.GetDriverByName('GTiff')
                            # create new clipped temp file:
                            out_ds = driver.Create(str(out_transm_tif), v_result.shape[1], v_result.shape[0], 1, gdal.GDT_Int16,
                                                   options=['COMPRESS=ZSTD', 'PREDICTOR=2', 'ZSTD_LEVEL=1'])
                            out_ds.SetGeoTransform(gt)
                            out_ds.SetProjection(srs.ExportToWkt())
                            outband = out_ds.GetRasterBand(1)
                            outband.SetNoDataValue(np.nan)
                            outband.WriteArray(v_result * 100)
                            outband.FlushCache()
                            outband = None  # close properly! (important!!)
                            out_ds = None  # close properly! (important!!)

                        # write out transmissivity tifs for further analysis
                        srs = osr.SpatialReference()
                        srs.ImportFromEPSG(2056)

                        driver = gdal.GetDriverByName('GTiff')
                        # create new clipped temp file:
                        out_ds = driver.Create(str(out_transm_tif), result.shape[1], result.shape[0], 1, gdal.GDT_Int16,
                                               options = ['COMPRESS=ZSTD', 'PREDICTOR=2', 'ZSTD_LEVEL=1'])
                        out_ds.SetGeoTransform(gt)
                        out_ds.SetProjection(srs.ExportToWkt())
                        outband = out_ds.GetRasterBand(1)
                        outband.SetNoDataValue(np.nan)
                        outband.WriteArray(result*100)
                        outband.FlushCache()
                        outband = None  # close properly! (important!!)
                        out_ds = None  # close properly! (important!!)


                        fig_save = plot_dir / "Transm_summer_png" / Path("transm_"+pd.Timestamp(start_date).strftime('%Y-%m-%d')+".png")
                        Path(plot_dir / "Transm_summer_png").mkdir(parents=True, exist_ok=True)
                        fig = plt.figure(figsize=(10, 10))
                        ax = fig.add_subplot(111)
                        ax.grid(False)
                        ax.set_title('Time-stamp: ' + pd.Timestamp(start_date).strftime('%Y-%m-%d') + ', mean/median = ' +
                                     str(round(np.nanmean(result), 1))+'/'+str(round(np.nanmedian(result), 1)), fontsize=12)
                        plt.imshow(result, cmap=plt.get_cmap('plasma'), vmin=0, vmax=100, extent=extent)
                        cbar1 = plt.colorbar(fraction=0.046, pad=0.04)
                        cbar1.set_label('Forest Transmissivity [%]', rotation=270, labelpad=20, fontsize=10)
                        fig.savefig(fig_save, dpi=350, bbox_inches='tight')
                        plt.close()

                        fig_save = plot_dir / "Transm_summer_forest_png" / Path("transm_" +
                                                                                pd.Timestamp(start_date).strftime('%Y-%m-%d') + ".png")
                        Path(plot_dir / "Transm_summer_forest_png").mkdir(parents=True, exist_ok=True)
                        fig = plt.figure(figsize=(10, 10))
                        ax = fig.add_subplot(111)
                        ax.grid(False)
                        ax.set_title('Time-stamp: ' + pd.Timestamp(start_date).strftime('%Y-%m-%d') + ', mean/median = ' +
                                     str(round(np.nanmean(result_for), 1))+'/'+str(round(np.nanmedian(result_for), 1)), fontsize=12)
                        plt.imshow(result_for, cmap=plt.get_cmap('plasma'), vmin=0, vmax=100, extent=extent)
                        cbar1 = plt.colorbar(fraction=0.046, pad=0.04)
                        cbar1.set_label('Forest Transmissivity [%]', rotation=270, labelpad=20, fontsize=10)
                        fig.savefig(fig_save, dpi=350, bbox_inches='tight')
                        plt.close()

                    start_date += day_delta

                TEND3 = datetime.datetime.now()
                print(f'Processing time to plot transmissivity map every {day_delta} days: {TEND3-TEND2} [HH:MM:SS]')

                if switch == 1:
                    mon_range = range(10,11,1)
                else:
                    mon_range = range(6,10,1)

                for mon_id in mon_range:
                    if switch == 1:
                        searchstring = '-' + str(mon_id) + '-'
                    else:
                        searchstring = '-0' + str(mon_id) + '-'

                    dir_content = sorted(tif_dir.iterdir())
                    filelist = []
                    for path in dir_content:
                        if not path.is_dir():
                            search_in_file(path, searchstring, filelist)

                    trans_all_stack = []
                    for trans_rast_num in filelist:
                        if trans_rast_num[-3:] == 'tif':
                            trans_rast = tif_dir / trans_rast_num
                            fi = gdal.Open(str(trans_rast))
                            gt = fi.GetGeoTransform()
                            proj = fi.GetProjection()
                            band = fi.GetRasterBand(1)
                            trans1 = band.ReadAsArray()
                            trans_all = trans1.reshape(1, trans1.shape[0], trans1.shape[1])
                            trans_all_stack.append(trans_all)

                    AS = np.stack(trans_all_stack, axis=0)
                    transm_avg_month = np.mean(np.squeeze(AS), axis=0)

                    out_transm_tif_mo = tif_dir_month / Path('transm_'+str(mon_id)+'.tif')

                    srs = osr.SpatialReference()
                    srs.ImportFromEPSG(2056)

                    driver = gdal.GetDriverByName('GTiff')
                    out_ds = driver.Create(str(out_transm_tif_mo), transm_avg_month.shape[1], transm_avg_month.shape[0], 1, gdal.GDT_Int16,
                                           options=['COMPRESS=ZSTD', 'PREDICTOR=2', 'ZSTD_LEVEL=1'])
                    out_ds.SetGeoTransform(gt)
                    out_ds.SetProjection(srs.ExportToWkt())
                    outband = out_ds.GetRasterBand(1)
                    outband.SetNoDataValue(np.nan)
                    outband.WriteArray(transm_avg_month )
                    outband.FlushCache()
                    outband = None  # close properly! (important!!)
                    out_ds = None  # close properly! (important!!)

                # make gif:
                ignored = {"test"}
                pics_filenames = sorted([x for x in os.listdir(plot_dir / "Transm_summer_png") if x not in ignored])
                with imageio.get_writer(plot_dir / "summer_originalCHM.gif", mode='I', duration=0.3) as writer:
                    for pics_filename in pics_filenames:
                        image = imageio.imread(plot_dir / "Transm_summer_png" / pics_filename)
                        writer.append_data(image)

                TEND4 = datetime.datetime.now()
                print(f'Processing time to make gif + write monthly tifs: {TEND4-TEND3} [HH:MM:SS]')


    print(f'Total processing time: {TEND4-TSTART} [HH:MM:SS]')
