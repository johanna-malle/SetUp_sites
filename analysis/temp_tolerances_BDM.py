# -*- coding: utf-8 -*-
"""
Desc: create temperature tolerance plots of plant, bird and butterfly communities at BDM sites
Created on 23.02.22 08:59
@author: malle
"""
import os
import csv
from pathlib import Path
import pyreadr
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

bf_coord = Path('/home/malle/slfhome/Postdoc2/experiment_sites_select')
sites = ["BDM_1","BDM_2","BDM_3"]   # os.listdir(bf_coord)

path_plots = "/home/malle/slfhome/Postdoc2/BD_sites/temp_tolerances/"

file_dir = Path("/home/malle/slfhome/Postdoc2/BD_sites/temp_tolerances/copy_data")
file_plants = file_dir / "plants_bdm.RData"
file_birds = file_dir / "birds_bdm.RData"
file_butter = file_dir / "butter_bdm.RData"

bdm_load = pyreadr.read_r(file_plants) # also works for Rds
bdm_plants = bdm_load[None]

bdm_load = pyreadr.read_r(file_birds) # also works for Rds
bdm_birds = bdm_load[None]

bdm_load = pyreadr.read_r(file_butter) # also works for Rds
bdm_butter = bdm_load[None]


coord_spec = bf_coord / "BD1" / "coord.csv"
# all BD sites:
for site in sites:
    site = os.path.basename(site)
    file_plot = os.path.join(path_plots,"STIs_"+str(site)+".png")
    file_plot1 = os.path.join(path_plots,"STIs_"+str(site)+"_just1.png")

    coord_spec = bf_coord / site / "coord.csv"
    # get coords
    xys = []
    with open(coord_spec) as fp:
        reader = csv.reader(fp)
        next(reader)
        for row in reader:
            xys.append([float(n) for n in row[:2]])

    upper_left, lower_right = xys[0], xys[1]
    mid_x , mid_y = upper_left[0]+500, lower_right[1]+500

    cut_BDsite = bdm_plants.loc[(pd.to_numeric(bdm_plants["XKoord_LV95"], errors='coerce') == mid_x) & (pd.to_numeric(bdm_plants["YKoord_LV95"], errors='coerce') == mid_y)]
    period_1_plants = cut_BDsite.loc[(bdm_plants["year_Pl"] > 2004) & (bdm_plants["year_Pl"] < 2010)]
    period_2_plants = cut_BDsite.loc[(bdm_plants["year_Pl"] > 2016) & (bdm_plants["year_Pl"] < 2022)]
    period_all_plants = cut_BDsite.loc[(bdm_plants["year_Pl"] > 2010) & (bdm_plants["year_Pl"] < 2022)]

    cut_BDsite = bdm_birds.loc[(pd.to_numeric(bdm_birds["XKoord_LV95"], errors='coerce') == mid_x) & (pd.to_numeric(bdm_birds["YKoord_LV95"], errors='coerce') == mid_y)]
    period_1_birds = cut_BDsite.loc[(pd.to_numeric(bdm_birds["year_Bi"], errors='coerce') > 2004) & (pd.to_numeric(bdm_birds["year_Bi"], errors='coerce') < 2010)]
    period_2_birds = cut_BDsite.loc[(pd.to_numeric(bdm_birds["year_Bi"], errors='coerce') > 2016) & (pd.to_numeric(bdm_birds["year_Bi"], errors='coerce') < 2022)]
    period_all_birds = cut_BDsite.loc[(pd.to_numeric(bdm_birds["year_Bi"], errors='coerce') > 2010) & (pd.to_numeric(bdm_birds["year_Bi"], errors='coerce') < 2022)]

    cut_BDsite = bdm_butter.loc[(pd.to_numeric(bdm_butter["XKoord_LV95"], errors='coerce') == mid_x) & (pd.to_numeric(bdm_butter["YKoord_LV95"], errors='coerce') == mid_y)]
    period_1_butter = cut_BDsite.loc[(pd.to_numeric(bdm_butter["year_Bu"], errors='coerce') > 2004) & (pd.to_numeric(bdm_butter["year_Bu"], errors='coerce') < 2010)]
    period_2_butter = cut_BDsite.loc[(pd.to_numeric(bdm_butter["year_Bu"], errors='coerce') > 2016) & (pd.to_numeric(bdm_butter["year_Bu"], errors='coerce') < 2022)]
    period_all_butter = cut_BDsite.loc[(pd.to_numeric(bdm_butter["year_Bu"], errors='coerce') > 2010) & (pd.to_numeric(bdm_butter["year_Bu"], errors='coerce') < 2022)]


    fig = plt.figure(figsize=(13, 5))
    plant_ax = fig.add_subplot(131)
    plt.hist(period_1_plants.overall_niche, alpha=0.4, bins=20, color='teal', edgecolor ='k', label="2005-2009",density=True)  # density=False would make counts
    plt.axvline(period_1_plants.overall_niche.mean(), color='teal', linestyle='dashed', linewidth=1.5)
    plt.hist(period_2_plants.overall_niche, alpha=0.4, bins=20, color='orangered', edgecolor ='k', label="2017-2021",density=True)  # density=False would make counts
    plt.axvline(period_2_plants.overall_niche.mean(), color='orangered', linestyle='dashed', linewidth=1.5)
    plt.xlabel("Temperature ["+u"\u2103"+"]")
    # plt.ylabel("Count")
    plt.legend(loc='upper right')
    plt.title("Plants @ "+site)
    plt.text(0.8, 0.7, '\u0394'+'$T_{avg}$ = '+str(round(period_2_plants.overall_niche.mean() - period_1_plants.overall_niche.mean(),2))+u"\u2103",
             fontsize = 10, color = 'k',  horizontalalignment='center', verticalalignment='center', transform=plant_ax.transAxes)

    bird_ax = fig.add_subplot(132)
    plt.hist(period_1_birds.overall_niche, alpha=0.4, bins=20, color='teal', edgecolor ='k', label="2005-2009",density=True)
    plt.axvline(period_1_birds.overall_niche.mean(), color='teal', linestyle='dashed', linewidth=1.5)
    plt.hist(period_2_birds.overall_niche, alpha=0.4, bins=20, color='orangered', edgecolor ='k', label="2017-2021",density=True)
    plt.axvline(period_2_birds.overall_niche.mean(), color='orangered', linestyle='dashed', linewidth=1.5)
    plt.xlabel("Temperature ["+u"\u2103"+"]")
    plt.legend(loc='upper right')
    plt.title("Birds @ "+site)
    plt.text(0.8, 0.7, '\u0394'+'$T_{avg}$ = '+
             str(round(period_2_birds.overall_niche.mean() - period_1_birds.overall_niche.mean(),2))+u"\u2103",
             fontsize = 10, color = 'k',  horizontalalignment='center', verticalalignment='center',
             transform=bird_ax.transAxes)

    butter_ax = fig.add_subplot(133)
    plt.hist(period_1_butter.overall_niche, alpha=0.4, bins=20, color='teal', edgecolor='k', label="2005-2009",density=True)
    plt.axvline(period_1_butter.overall_niche.mean(), color='teal', linestyle='dashed', linewidth=1.5)
    plt.hist(period_2_butter.overall_niche, alpha=0.4, bins=20, color='orangered', edgecolor='k', label="2017-2021",density=True)
    plt.axvline(period_2_butter.overall_niche.mean(), color='orangered', linestyle='dashed', linewidth=1.5)
    plt.xlabel("Temperature ["+u"\u2103"+"]")
    plt.legend(loc='upper right')
    plt.title("Butterflies @ "+site)
    plt.text(0.8, 0.7, '\u0394'+'$T_{avg}$ = ' +
             str(round(period_2_butter.overall_niche.mean() - period_1_butter.overall_niche.mean(), 2))+u"\u2103",
             fontsize=10, color='k', horizontalalignment='center', verticalalignment='center',
             transform=butter_ax.transAxes)
    fig.savefig(file_plot, dpi=600, bbox_inches='tight')
    plt.close()

    fig = plt.figure(figsize=(7, 6))
    sns.kdeplot(period_all_plants.overall_niche, shade=True, color='teal', alpha=0.4, label="Plants")
    plt.axvline(period_all_plants.overall_niche.mean(), color='teal', linestyle='dashed', linewidth=1.5)
    sns.kdeplot(period_all_birds.overall_niche, shade=True, color='orangered', alpha=0.4, label="Birds")
    plt.axvline(period_all_birds.overall_niche.mean(), color='orangered', linestyle='dashed', linewidth=1.5)
    sns.kdeplot(period_all_butter.overall_niche, shade=True, color='purple', alpha=0.4, label="Butterflies")
    plt.axvline(period_all_butter.overall_niche.mean(), color='purple', linestyle='dashed', linewidth=1.5)

    plt.xlabel("Temperature Indices of species communities ["+u"\u2103"+"]")
    plt.legend(loc='upper right')
    plt.title("2011-2021 @ "+site)


    fig.savefig(file_plot1, dpi=600, bbox_inches='tight')
    plt.close()

