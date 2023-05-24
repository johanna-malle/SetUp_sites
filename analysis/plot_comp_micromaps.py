# -*- coding: utf-8 -*-
"""
Desc: generate plots that show differences in climate & forest change scenarios
Created on 06.05.22 08:32
@author: malle
"""

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from src.help_functions import raster2array


if __name__ == '__main__':

    bf = Path('/home/malle/slfhome/Postdoc2/experiment_sites_select/BDM_1/MicroMaps/incl_transm')
    bf_plot = Path('/home/malle/johanna_micromap')
    bf_temp = Path('/home/malle/slfhome/Postdoc2/experiment_sites_select/BDM_1/PredRasters')
    date = '2046-06-06'

    temp_today = bf_temp / 'temp_20210605.tif'
    temp_rcp26 = bf_temp / 'CH2018_corrected_tasmax_DMI-HIRHAM_ECEARTH_EUR11_RCP26_QMgrid_summer10yrs5_2046_06_06.tif'
    temp_rcp85 = bf_temp / 'CH2018_corrected_tasmax_DMI-HIRHAM_ECEARTH_EUR11_RCP85_QMgrid_summer10yrs5_2046_06_06.tif'

    summer_today = bf / 'temp_2046-06-06_transm1_today_summer.tif'
    summer_rcp26 = bf / 'temp_2046-06-06_transm1_RCP26_summer.tif'
    summer_rcp85 = bf / 'temp_2046-06-06_transm1_RCP85_summer.tif'

    winter_rcp26 = bf / 'temp_2046-06-06_transm1_RCP26_winter.tif'
    winter_rcp85 = bf / 'temp_2046-06-06_transm1_RCP85_winter.tif'

    summer_cut025_today = bf / 'temp_2046-06-06_transm1_today_summer_025_fm1_0mbuffer.tif'
    summer_cut025_rcp26 = bf / 'temp_2046-06-06_transm1_RCP26_summer_025_fm1_0mbuffer.tif'
    summer_cut025_rcp85 = bf / 'temp_2046-06-06_transm1_RCP85_summer_025_fm1_0mbuffer.tif'

    summer_cut075_today = bf / 'temp_2046-06-06_transm1_today_summer_075_fm1_0mbuffer.tif'
    summer_cut075_rcp26 = bf / 'temp_2046-06-06_transm1_RCP26_summer_075_fm1_0mbuffer.tif'
    summer_cut075_rcp85 = bf / 'temp_2046-06-06_transm1_RCP85_summer_075_fm1_0mbuffer.tif'

    summer_cut050_today = bf / 'temp_2046-06-06_transm1_today_summer_050_fm1_0mbuffer.tif'
    summer_cut050_rcp26 = bf / 'temp_2046-06-06_transm1_RCP26_summer_050_fm1_0mbuffer.tif'
    summer_cut050_rcp85 = bf / 'temp_2046-06-06_transm1_RCP85_summer_050_fm1_0mbuffer.tif'

    summer_rcp26_array, summer_rcp26_metadata = raster2array(str(summer_rcp26))
    summer_rcp85_array, summer_rcp85_metadata = raster2array(str(summer_rcp85))
    summer_today_array, summer_today_metadata = raster2array(str(summer_today))

    summer_cut025_rcp26_array, summer_cut025_rcp26_metadata = raster2array(str(summer_cut025_rcp26))
    summer_cut025_rcp85_array, summer_cut025_rcp85_metadata = raster2array(str(summer_cut025_rcp85))
    summer_cut025_today_array, summer_cut025_today_metadata = raster2array(str(summer_cut025_today))

    summer_cut075_rcp26_array, summer_cut075_rcp26_metadata = raster2array(str(summer_cut075_rcp26))
    summer_cut075_rcp85_array, summer_cut075_rcp85_metadata = raster2array(str(summer_cut075_rcp85))
    summer_cut075_today_array, summer_cut075_today_metadata = raster2array(str(summer_cut075_today))

    summer_cut050_rcp26_array, summer_cut050_rcp26_metadata = raster2array(str(summer_cut050_rcp26))
    summer_cut050_rcp85_array, summer_cut050_rcp85_metadata = raster2array(str(summer_cut050_rcp85))
    summer_cut050_today_array, summer_cut050_today_metadata = raster2array(str(summer_cut050_today))

    temp_today_array, temp_today_metadata = raster2array(str(temp_today))
    temp_rcp26_array, temp_rcp26_metadata = raster2array(str(temp_rcp26))
    temp_rcp85_array, temp_rcp85_metadata = raster2array(str(temp_rcp85))

    tt_min=np.min([np.min(summer_cut050_rcp26_array), np.min(summer_cut050_rcp85_array), np.min(temp_rcp26_array), np.min(temp_rcp85_array),
            np.min(summer_cut025_rcp26_array), np.min(summer_cut025_rcp85_array), np.min(summer_rcp26_array), np.min(summer_rcp85_array)])/100
    tt_max=np.max([np.max(summer_cut050_rcp26_array), np.max(summer_cut050_rcp85_array), np.max(temp_rcp26_array), np.max(temp_rcp85_array),
            np.max(summer_cut025_rcp26_array), np.max(summer_cut025_rcp85_array), np.max(summer_rcp26_array), np.max(summer_rcp85_array)])/100

    fig = plt.figure(figsize=(18, 7.5))

    ax1 = fig.add_subplot(241)
    plt.imshow(temp_rcp26_array/100, extent=temp_rcp26_metadata['extent'], alpha=1.0)
    plt.clim(tt_min, tt_max)
    plt.xticks(color='w',fontsize=2)
    plt.yticks(fontsize=8)
    plt.ylabel('RCP 2.6 $\longrightarrow$',rotation=0,fontsize=10,labelpad=35)
  #  ax1.ticklabel_format(style='plain')

    ax2 = fig.add_subplot(242)
    plt.imshow(summer_rcp26_array/100, extent=summer_rcp26_metadata['extent'], alpha=1.0)
    plt.xticks(color='w',fontsize=2)
    plt.clim(tt_min, tt_max)
    plt.yticks(color='w',fontsize=3)
  #  ax2.ticklabel_format(style='plain')

    ax3 = fig.add_subplot(243)
    pl34=plt.imshow(summer_cut025_rcp26_array/100, extent=summer_cut025_rcp26_metadata['extent'], alpha=1.0)
    plt.xticks(color='w',fontsize=2)
    plt.yticks(fontsize=8)
    plt.clim(tt_min, tt_max)
    plt.yticks(color='w',fontsize=3)
  #  ax3.ticklabel_format(style='plain')

    ax4 = fig.add_subplot(244)
    pl34=plt.imshow(summer_cut050_rcp26_array/100, extent=summer_cut050_rcp26_metadata['extent'], alpha=1.0)
    plt.xticks(color='w',fontsize=2)
    plt.yticks(fontsize=8)
    plt.clim(tt_min, tt_max)
    plt.yticks(color='w',fontsize=3)
 #   ax3.ticklabel_format(style='plain')

    ax5 = fig.add_subplot(245)
    plt.imshow(temp_rcp85_array/100, extent=temp_rcp85_metadata['extent'], alpha=1.0)
    plt.xticks(fontsize=8)
    plt.yticks(fontsize=8)
    plt.clim(tt_min, tt_max)
    plt.ylabel('RCP 8.5 $\longrightarrow$',rotation=0,fontsize=10,labelpad=35)
  #  ax1.ticklabel_format(style='plain')

    ax6 = fig.add_subplot(246)
    plt.imshow(summer_rcp85_array/100, extent=summer_rcp85_metadata['extent'], alpha=1.0)
    plt.xticks(fontsize=8)
    plt.yticks(color='w',fontsize=3)
    plt.clim(tt_min, tt_max)
    #ax2.ticklabel_format(style='plain')

    ax7 = fig.add_subplot(247)
    pl34=plt.imshow(summer_cut025_rcp85_array/100, extent=summer_cut025_rcp26_metadata['extent'], alpha=1.0)
    plt.xticks(fontsize=8)
    plt.yticks(fontsize=8)
    plt.clim(tt_min, tt_max)
    plt.yticks(color='w',fontsize=3)
    #ax3.ticklabel_format(style='plain')

    ax8 = fig.add_subplot(248)
    pl34=plt.imshow(summer_cut050_rcp85_array/100, extent=summer_cut050_rcp26_metadata['extent'], alpha=1.0)
    plt.xticks(fontsize=8)
    plt.clim(tt_min, tt_max)
    plt.yticks(fontsize=8)
    plt.yticks(color='w',fontsize=3)
    #ax3.ticklabel_format(style='plain')

    fig.subplots_adjust(right=0.8)
    cbar_ax = fig.add_axes([0.825, 0.26, 0.009, 0.47])
    cbar=fig.colorbar(pl34, cax=cbar_ax)

    #cbar = plt.colorbar(fraction=0.046, pad=0.04)
    cbar.set_label('Temperatur [\N{DEGREE SIGN}C]', rotation=270, labelpad=20)

    ax1.set_title('CH2018', fontsize=10)
    ax2.set_title('Ist-Zustand', fontsize=10)
    ax3.set_title('25% Ausdünnung', fontsize=10)
    ax4.set_title('50% Ausdünnung', fontsize=10)
    fig.suptitle('06. Juni 2046', fontsize=12)
    fig.subplots_adjust(top=0.9)
    fig_comp1 = bf_plot / "temp2046_comp_rcp85_rcp26.png"
    fig.savefig(fig_comp1, dpi=450, bbox_inches='tight')
    plt.close()

    tt_min=np.min([np.min(summer_cut050_rcp26_array[10:-60,30:-40]),np.min(summer_cut050_rcp85_array[10:-60,30:-40]),np.min(temp_rcp26_array[10:-60,30:-40]),np.min(temp_rcp85_array[10:-60,30:-40]),
            np.min(summer_cut025_rcp26_array[10:-60,30:-40]),np.min(summer_cut025_rcp85_array[10:-60,30:-40]),np.min(summer_rcp26_array[10:-60,30:-40]),np.min(summer_rcp85_array[10:-60,30:-40])])/100
    tt_max=np.max([np.max(summer_cut050_rcp26_array[10:-60,30:-40]),np.max(summer_cut050_rcp85_array[10:-60,30:-40]),np.max(temp_rcp26_array[10:-60,30:-40]),np.max(temp_rcp85_array[10:-60,30:-40]),
            np.max(summer_cut025_rcp26_array[10:-60,30:-40]),np.max(summer_cut025_rcp85_array[10:-60,30:-40]),np.max(summer_rcp26_array[10:-60,30:-40]),np.max(summer_rcp85_array[10:-60,30:-40])])/100


    fig = plt.figure(figsize=(18, 7.5))

    ax1 = fig.add_subplot(241)
    ext = temp_rcp26_metadata['extent']
    plt.imshow(temp_rcp26_array[10:-60,30:-40]/100, extent=[ext[0]+300,ext[1]-400,ext[2]+600,ext[3]-100], alpha=1.0)
    plt.clim(tt_min, tt_max)
    plt.xticks([2653300,2653400,2653500,2653600],['0', '10', '20', '30m'],color='w',fontsize=2)
    plt.yticks([1182600,1182700,1182800,1182900],['0', '10', '20', '30m'],fontsize=8)
    plt.ylabel('RCP 2.6 $\longrightarrow$',rotation=0,fontsize=10,labelpad=35)
  #  ax1.ticklabel_format(style='plain')

    ax2 = fig.add_subplot(242)
    plt.imshow(summer_rcp26_array[10:-60,30:-40]/100, extent=[ext[0]+300,ext[1]-400,ext[2]+600,ext[3]-100], alpha=1.0)
    plt.xticks(color='w',fontsize=2)
    plt.clim(tt_min, tt_max)
    plt.yticks(color='w',fontsize=3)
    plt.xticks([2653300, 2653400, 2653500, 2653600],['0', '10', '20', '30m'],color='w',fontsize=2)
    plt.yticks([1182600, 1182700, 1182800, 1182900],['0', '10', '20', '30m'],color='w',fontsize=2)
  #  ax2.ticklabel_format(style='plain')

    ax3 = fig.add_subplot(243)
    pl34=plt.imshow(summer_cut025_rcp26_array[10:-60,30:-40]/100,extent=[ext[0]+300,ext[1]-400,ext[2]+600,ext[3]-100], alpha=1.0)
    plt.clim(tt_min, tt_max)
    plt.xticks([2653300,2653400,2653500,2653600],['0', '10', '20', '30m'],color='w',fontsize=2)
    plt.yticks([1182600,1182700,1182800,1182900],['0', '10', '20', '30m'],color='w',fontsize=2)
    #ax3.ticklabel_format(style='plain')

    ax4 = fig.add_subplot(244)
    pl34=plt.imshow(summer_cut050_rcp26_array[10:-60,30:-40]/100,extent=[ext[0]+300,ext[1]-400,ext[2]+600,ext[3]-100], alpha=1.0)
    plt.clim(tt_min, tt_max)
    plt.xticks([2653300,2653400,2653500,2653600],['0', '10', '20', '30m'],color='w',fontsize=2)
    plt.yticks([1182600,1182700,1182800,1182900],['0', '10', '20', '30m'],color='w',fontsize=2)
    #   ax3.ticklabel_format(style='plain')

    ax5 = fig.add_subplot(245)
    plt.imshow(temp_rcp85_array[10:-60,30:-40]/100,extent=[ext[0]+300,ext[1]-400,ext[2]+600,ext[3]-100], alpha=1.0)
    plt.xticks([2653300,2653400,2653500,2653600],['0', '10', '20', '30m'],fontsize=8)
    plt.yticks([1182600,1182700,1182800,1182900],['0', '10', '20', '30m'],fontsize=8)
    plt.clim(tt_min, tt_max)
    plt.ylabel('RCP 8.5 $\longrightarrow$',rotation=0,fontsize=10,labelpad=35)
 #   ax5.ticklabel_format(style='plain')

    ax6 = fig.add_subplot(246)
    plt.imshow(summer_rcp85_array[10:-60,30:-40]/100,extent=[ext[0]+300,ext[1]-400,ext[2]+600,ext[3]-100], alpha=1.0)
    plt.xticks([2653300,2653400,2653500,2653600],['0', '10', '20', '30m'],fontsize=8)
    plt.yticks([1182600,1182700,1182800,1182900],['0', '10', '20', '30m'],color='w',fontsize=3)
    plt.clim(tt_min, tt_max)
    #ax2.ticklabel_format(style='plain')

    ax7 = fig.add_subplot(247)
    pl34=plt.imshow(summer_cut025_rcp85_array[10:-60,30:-40]/100,extent=[ext[0]+300,ext[1]-400,ext[2]+600,ext[3]-100], alpha=1.0)
    plt.xticks([2653300,2653400,2653500,2653600],['0', '10', '20', '30m'],fontsize=8)
    plt.yticks([1182600,1182700,1182800,1182900],['0', '10', '20', '30m'],color='w',fontsize=3)
    plt.clim(tt_min, tt_max)
    #ax3.ticklabel_format(style='plain')

    ax8 = fig.add_subplot(248)
    pl34=plt.imshow(summer_cut050_rcp85_array[10:-60,30:-40]/100,extent=[ext[0]+300,ext[1]-400,ext[2]+600,ext[3]-100], alpha=1.0)
    plt.clim(tt_min, tt_max)
    plt.xticks([2653300,2653400,2653500,2653600],['0', '10', '20', '30m'],fontsize=8)
    plt.yticks([1182600,1182700,1182800,1182900],['0', '10', '20', '30m'],color='w',fontsize=3)
    #ax3.ticklabel_format(style='plain')

    fig.subplots_adjust(right=0.8)
    cbar_ax = fig.add_axes([0.825, 0.26, 0.009, 0.47])
    cbar=fig.colorbar(pl34, cax=cbar_ax)

    #cbar = plt.colorbar(fraction=0.046, pad=0.04)
    cbar.set_label('Temperatur [\N{DEGREE SIGN}C]', rotation=270, labelpad=20)

    ax1.set_title('CH2018', fontsize=10)
    ax2.set_title('Ist-Zustand', fontsize=10)
    ax3.set_title('25% Ausdünnung', fontsize=10)
    ax4.set_title('50% Ausdünnung', fontsize=10)
    fig.suptitle('06. Juni 2046', fontsize=12)
    fig.subplots_adjust(top=0.9)
    fig_comp1 = bf_plot / "temp2046_comp_rcp85_rcp26_zoom.png"
    fig.savefig(fig_comp1, dpi=450, bbox_inches='tight')
    plt.close()

    tt_min = np.min([np.min(summer_cut050_today_array), np.min(summer_cut050_rcp85_array), np.min(temp_today_array),
                     np.min(temp_rcp85_array),
                     np.min(summer_cut025_today_array), np.min(summer_cut025_rcp85_array), np.min(summer_today_array),
                     np.min(summer_rcp85_array)]) / 100
    tt_max = np.max([np.max(summer_cut050_today_array), np.max(summer_cut050_rcp85_array), np.max(temp_today_array),
                     np.max(temp_rcp85_array),
                     np.max(summer_cut025_today_array), np.max(summer_cut025_rcp85_array), np.max(summer_today_array),
                     np.max(summer_rcp85_array)]) / 100

    fig = plt.figure(figsize=(18, 7.5))

    ax1 = fig.add_subplot(241)
    plt.imshow(temp_today_array / 100, extent=temp_today_metadata['extent'], alpha=1.0)
    plt.clim(tt_min, tt_max)
    plt.xticks(color='w', fontsize=2)
    plt.yticks(fontsize=8)
    plt.ylabel('"Today" $\longrightarrow$ \n 5.6.2021', rotation=0, fontsize=10, labelpad=35)
    #  ax1.ticklabel_format(style='plain')

    ax2 = fig.add_subplot(242)
    plt.imshow(summer_today_array / 100, extent=summer_today_metadata['extent'], alpha=1.0)
    plt.xticks(color='w', fontsize=2)
    plt.clim(tt_min, tt_max)
    plt.yticks(color='w', fontsize=3)
    #  ax2.ticklabel_format(style='plain')

    ax3 = fig.add_subplot(243)
    pl34 = plt.imshow(summer_cut025_today_array / 100, extent=summer_cut025_today_metadata['extent'], alpha=1.0)
    plt.xticks(color='w', fontsize=2)
    plt.yticks(fontsize=8)
    plt.clim(tt_min, tt_max)
    plt.yticks(color='w', fontsize=3)
    #  ax3.ticklabel_format(style='plain')

    ax4 = fig.add_subplot(244)
    pl34 = plt.imshow(summer_cut050_today_array / 100, extent=summer_cut050_today_metadata['extent'], alpha=1.0)
    plt.xticks(color='w', fontsize=2)
    plt.yticks(fontsize=8)
    plt.clim(tt_min, tt_max)
    plt.yticks(color='w', fontsize=3)
    #   ax3.ticklabel_format(style='plain')

    ax5 = fig.add_subplot(245)
    plt.imshow(temp_rcp85_array / 100, extent=temp_rcp85_metadata['extent'], alpha=1.0)
    plt.xticks(fontsize=8)
    plt.yticks(fontsize=8)
    plt.clim(tt_min, tt_max)
    plt.ylabel('RCP 8.5 $\longrightarrow$ \n 6.6.2046', rotation=0, fontsize=10, labelpad=35)
    #  ax1.ticklabel_format(style='plain')

    ax6 = fig.add_subplot(246)
    plt.imshow(summer_rcp85_array / 100, extent=summer_rcp85_metadata['extent'], alpha=1.0)
    plt.xticks(fontsize=8)
    plt.yticks(color='w', fontsize=3)
    plt.clim(tt_min, tt_max)
    # ax2.ticklabel_format(style='plain')

    ax7 = fig.add_subplot(247)
    pl34 = plt.imshow(summer_cut025_rcp85_array / 100, extent=summer_cut025_rcp26_metadata['extent'], alpha=1.0)
    plt.xticks(fontsize=8)
    plt.yticks(fontsize=8)
    plt.clim(tt_min, tt_max)
    plt.yticks(color='w', fontsize=3)
    # ax3.ticklabel_format(style='plain')

    ax8 = fig.add_subplot(248)
    pl34 = plt.imshow(summer_cut050_rcp85_array / 100, extent=summer_cut050_rcp26_metadata['extent'], alpha=1.0)
    plt.xticks(fontsize=8)
    plt.clim(tt_min, tt_max)
    plt.yticks(fontsize=8)
    plt.yticks(color='w', fontsize=3)
    # ax3.ticklabel_format(style='plain')

    fig.subplots_adjust(right=0.8)
    cbar_ax = fig.add_axes([0.825, 0.26, 0.009, 0.47])
    cbar = fig.colorbar(pl34, cax=cbar_ax)

    # cbar = plt.colorbar(fraction=0.046, pad=0.04)
    cbar.set_label('Temperatur [\N{DEGREE SIGN}C]', rotation=270, labelpad=20)

    ax1.set_title('CH2018', fontsize=10)
    ax2.set_title('Ist-Zustand', fontsize=10)
    ax3.set_title('25% Ausdünnung', fontsize=10)
    ax4.set_title('50% Ausdünnung', fontsize=10)
  #  fig.suptitle('06. Juni 2046', fontsize=12)
    fig.subplots_adjust(top=0.9)
    fig_comp1 = bf_plot / "temp2046_comp_today_rcp85.png"
    fig.savefig(fig_comp1, dpi=450, bbox_inches='tight')
    plt.close()

    tt_min = np.min(
        [np.min(summer_cut050_today_array[10:-60, 30:-40]), np.min(summer_cut050_rcp85_array[10:-60, 30:-40]),
         np.min(temp_today_array[10:-60, 30:-40]), np.min(temp_rcp85_array[10:-60, 30:-40]),
         np.min(summer_cut025_today_array[10:-60, 30:-40]), np.min(summer_cut025_rcp85_array[10:-60, 30:-40]),
         np.min(summer_today_array[10:-60, 30:-40]), np.min(summer_rcp85_array[10:-60, 30:-40])]) / 100
    tt_max = np.max(
        [np.max(summer_cut050_today_array[10:-60, 30:-40]), np.max(summer_cut050_rcp85_array[10:-60, 30:-40]),
         np.max(temp_today_array[10:-60, 30:-40]), np.max(temp_rcp85_array[10:-60, 30:-40]),
         np.max(summer_cut025_today_array[10:-60, 30:-40]), np.max(summer_cut025_rcp85_array[10:-60, 30:-40]),
         np.max(summer_today_array[10:-60, 30:-40]), np.max(summer_rcp85_array[10:-60, 30:-40])]) / 100

    fig = plt.figure(figsize=(18, 7.5))

    ax1 = fig.add_subplot(241)
    ext = temp_rcp26_metadata['extent']
    plt.imshow(temp_today_array[10:-60, 30:-40] / 100, extent=[ext[0] + 300, ext[1] - 400, ext[2] + 600, ext[3] - 100],
               alpha=1.0)
    plt.clim(tt_min, tt_max)
    plt.xticks([2653300, 2653400, 2653500, 2653600], ['0', '10', '20', '30m'], color='w', fontsize=2)
    plt.yticks([1182600, 1182700, 1182800, 1182900], ['0', '10', '20', '30m'], fontsize=8)
    plt.ylabel('"Today" $\longrightarrow$ \n 5.6.2021', rotation=0, fontsize=10, labelpad=35)
    #  ax1.ticklabel_format(style='plain')

    ax2 = fig.add_subplot(242)
    plt.imshow(summer_today_array[10:-60, 30:-40] / 100,
               extent=[ext[0] + 300, ext[1] - 400, ext[2] + 600, ext[3] - 100], alpha=1.0)
    plt.xticks(color='w', fontsize=2)
    plt.clim(tt_min, tt_max)
    plt.yticks(color='w', fontsize=3)
    plt.xticks([2653300, 2653400, 2653500, 2653600], ['0', '10', '20', '30m'], color='w', fontsize=2)
    plt.yticks([1182600, 1182700, 1182800, 1182900], ['0', '10', '20', '30m'], color='w', fontsize=2)
    #  ax2.ticklabel_format(style='plain')

    ax3 = fig.add_subplot(243)
    pl34 = plt.imshow(summer_cut025_today_array[10:-60, 30:-40] / 100,
                      extent=[ext[0] + 300, ext[1] - 400, ext[2] + 600, ext[3] - 100], alpha=1.0)
    plt.clim(tt_min, tt_max)
    plt.xticks([2653300, 2653400, 2653500, 2653600], ['0', '10', '20', '30m'], color='w', fontsize=2)
    plt.yticks([1182600, 1182700, 1182800, 1182900], ['0', '10', '20', '30m'], color='w', fontsize=2)
    # ax3.ticklabel_format(style='plain')

    ax4 = fig.add_subplot(244)
    pl34 = plt.imshow(summer_cut050_today_array[10:-60, 30:-40] / 100,
                      extent=[ext[0] + 300, ext[1] - 400, ext[2] + 600, ext[3] - 100], alpha=1.0)
    plt.clim(tt_min, tt_max)
    plt.xticks([2653300, 2653400, 2653500, 2653600], ['0', '10', '20', '30m'], color='w', fontsize=2)
    plt.yticks([1182600, 1182700, 1182800, 1182900], ['0', '10', '20', '30m'], color='w', fontsize=2)
    #   ax3.ticklabel_format(style='plain')

    ax5 = fig.add_subplot(245)
    plt.imshow(temp_rcp85_array[10:-60, 30:-40] / 100, extent=[ext[0] + 300, ext[1] - 400, ext[2] + 600, ext[3] - 100],
               alpha=1.0)
    plt.xticks([2653300, 2653400, 2653500, 2653600], ['0', '10', '20', '30m'], fontsize=8)
    plt.yticks([1182600, 1182700, 1182800, 1182900], ['0', '10', '20', '30m'], fontsize=8)
    plt.clim(tt_min, tt_max)
    plt.ylabel('RCP 8.5 $\longrightarrow$ \n 6.6.2046', rotation=0, fontsize=10, labelpad=35)
    #   ax5.ticklabel_format(style='plain')

    ax6 = fig.add_subplot(246)
    plt.imshow(summer_rcp85_array[10:-60, 30:-40] / 100,
               extent=[ext[0] + 300, ext[1] - 400, ext[2] + 600, ext[3] - 100], alpha=1.0)
    plt.xticks([2653300, 2653400, 2653500, 2653600], ['0', '10', '20', '30m'], fontsize=8)
    plt.yticks([1182600, 1182700, 1182800, 1182900], ['0', '10', '20', '30m'], color='w', fontsize=3)
    plt.clim(tt_min, tt_max)
    # ax2.ticklabel_format(style='plain')

    ax7 = fig.add_subplot(247)
    pl34 = plt.imshow(summer_cut025_rcp85_array[10:-60, 30:-40] / 100,
                      extent=[ext[0] + 300, ext[1] - 400, ext[2] + 600, ext[3] - 100], alpha=1.0)
    plt.xticks([2653300, 2653400, 2653500, 2653600], ['0', '10', '20', '30m'], fontsize=8)
    plt.yticks([1182600, 1182700, 1182800, 1182900], ['0', '10', '20', '30m'], color='w', fontsize=3)
    plt.clim(tt_min, tt_max)
    # ax3.ticklabel_format(style='plain')

    ax8 = fig.add_subplot(248)
    pl34 = plt.imshow(summer_cut050_rcp85_array[10:-60, 30:-40] / 100,
                      extent=[ext[0] + 300, ext[1] - 400, ext[2] + 600, ext[3] - 100], alpha=1.0)
    plt.clim(tt_min, tt_max)
    plt.xticks([2653300, 2653400, 2653500, 2653600], ['0', '10', '20', '30m'], fontsize=8)
    plt.yticks([1182600, 1182700, 1182800, 1182900], ['0', '10', '20', '30m'], color='w', fontsize=3)
    # ax3.ticklabel_format(style='plain')

    fig.subplots_adjust(right=0.8)
    cbar_ax = fig.add_axes([0.825, 0.26, 0.009, 0.47])
    cbar = fig.colorbar(pl34, cax=cbar_ax)

    # cbar = plt.colorbar(fraction=0.046, pad=0.04)
    cbar.set_label('Temperatur [\N{DEGREE SIGN}C]', rotation=270, labelpad=20)

    ax1.set_title('CH2018', fontsize=10)
    ax2.set_title('Ist-Zustand', fontsize=10)
    ax3.set_title('25% Ausdünnung', fontsize=10)
    ax4.set_title('50% Ausdünnung', fontsize=10)
 #   fig.suptitle('06. Juni 2046', fontsize=12)
    fig.subplots_adjust(top=0.9)
    fig_comp1 = bf_plot / "temp2046_comp_today_rcp85_zoom.png"
    fig.savefig(fig_comp1, dpi=450, bbox_inches='tight')
    plt.close()
