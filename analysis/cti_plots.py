# -*- coding: utf-8 -*-
"""
Desc: create CTI plots of plant, bird and butterfly communities at BDM sites
Created on 23.02.22 12:20
@author: malle
"""

from pathlib import Path
import pyreadr
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

path_plots = '/home/malle/slfhome/Postdoc2/BD_sites/temp_tolerances/'

file_dir = Path('/home/malle/slfhome/Postdoc2/BD_sites/temp_tolerances/copy_data')
file_plants = file_dir / "CTI_plants.RData"
file_birds = file_dir / "CTI_birds.RData"
file_butter = file_dir / "CTI_butter.RData"

bdm_load = pyreadr.read_r(str(file_plants))
bdm_plants = bdm_load[None]

bdm_load = pyreadr.read_r(str(file_birds))
bdm_birds = bdm_load[None]

bdm_load = pyreadr.read_r(str(file_butter))
bdm_butter = bdm_load[None]

period_1_plants = bdm_plants.loc[(bdm_plants["year_Pl"] > 2004) & (bdm_plants["year_Pl"] < 2010)]
period_2_plants = bdm_plants.loc[(bdm_plants["year_Pl"] > 2014) & (bdm_plants["year_Pl"] < 2020)]
period_1_birds = bdm_birds.loc[(pd.to_numeric(bdm_birds["Year"], errors='coerce') > 2004) &
                               (pd.to_numeric(bdm_birds["Year"], errors='coerce') < 2010)]
period_2_birds = bdm_birds.loc[(pd.to_numeric(bdm_birds["Year"], errors='coerce') > 2014) &
                               (pd.to_numeric(bdm_birds["Year"], errors='coerce') < 2020)]
period_1_butter = bdm_butter.loc[(pd.to_numeric(bdm_butter["Year"], errors='coerce') > 2004) &
                                 (pd.to_numeric(bdm_butter["Year"], errors='coerce') < 2010)]
period_2_butter = bdm_butter.loc[(pd.to_numeric(bdm_butter["Year"], errors='coerce') > 2014) &
                                 (pd.to_numeric(bdm_butter["Year"], errors='coerce') < 2020)]

fig = plt.figure(figsize=(13, 5))
plant_ax = fig.add_subplot(131)
sns.kdeplot(period_1_plants.CTI, shade=True, color='teal', alpha=0.4, label="2005-2009")
sns.kdeplot(period_2_plants.CTI, shade=True, color='orangered', alpha=0.4, label="2015-2019")
plt.axvline(period_1_plants.CTI.mean(), color='teal', linestyle='dashed', linewidth=1.5)
plt.axvline(period_2_plants.CTI.mean(), color='orangered', linestyle='dashed', linewidth=1.5)
plt.legend(loc='upper left')
plt.title("Pflanzen")
plt.xlabel('')
plt.text(0.2, 0.7, '\u0394'+'$T_{avg}$ = ' +
         str(round(period_2_plants.CTI.mean() - period_1_plants.CTI.mean(), 2))+u"\u2103", fontsize=10,
         color='k',  horizontalalignment='center', verticalalignment='center', transform=plant_ax.transAxes)

bird_ax = fig.add_subplot(132)
sns.kdeplot(period_1_birds.CTI, shade=True, color='teal', alpha=0.4, label="2005-2009")
sns.kdeplot(period_2_birds.CTI, shade=True, color='orangered', alpha=0.4, label="2015-2019")
plt.xlabel('')
plt.axvline(period_1_birds.CTI.mean(), color='teal', linestyle='dashed', linewidth=1.5)
plt.axvline(period_2_birds.CTI.mean(), color='orangered', linestyle='dashed', linewidth=1.5)
plt.legend(loc='upper right')
plt.title("Vögel")
plt.text(0.2, 0.7, '\u0394'+'$T_{avg}$ = ' +
         str(round(period_2_birds.CTI.mean() - period_1_birds.CTI.mean(), 2))+u"\u2103",
         fontsize=10, color='k',  horizontalalignment='center', verticalalignment='center',
         transform=bird_ax.transAxes)
plt.ylabel('')

butter_ax = fig.add_subplot(133)
sns.kdeplot(period_1_butter.CTI, shade=True, color='teal', alpha=0.4, label="2005-2009")
sns.kdeplot(period_2_butter.CTI, shade=True, color='orangered', alpha=0.4, label="2015-2019")
plt.axvline(period_1_butter.CTI.mean(), color='teal', linestyle='dashed', linewidth=1.5)
plt.axvline(period_2_butter.CTI.mean(), color='orangered', linestyle='dashed', linewidth=1.5)
plt.legend(loc='upper left')
plt.title("Tagfalter")
plt.xlabel('')
plt.ylabel('')
plt.text(0.2, 0.7, '\u0394'+'$T_{avg}$ = ' +
         str(round(period_2_butter.CTI.mean() - period_1_butter.CTI.mean(), 2))+u"\u2103",
         fontsize=10, color='k', horizontalalignment='center', verticalalignment='center',
         transform=butter_ax.transAxes)
fig.supxlabel("Temperatur Index der Artengemeinschaften ["+u"\u2103"+"]")
fig.savefig(path_plots+"CTIs_plants_birds_butter.png", dpi=600, bbox_inches='tight')
plt.close()

fig = plt.figure(figsize=(13, 5))
plant_ax = fig.add_subplot(131)
plt.hist(period_1_plants.CTI, alpha=0.4, bins=20, color='teal', edgecolor='k', label="2005-2009", density=True)
plt.axvline(period_1_plants.CTI.mean(), color='teal', linestyle='dashed', linewidth=1.5)
plt.hist(period_2_plants.CTI, alpha=0.4, bins=10, color='orangered', edgecolor='k', label="2015-2019", density=True)
plt.axvline(period_2_plants.CTI.mean(), color='orangered', linestyle='dashed', linewidth=1.5)
plt.legend(loc='upper left')
plt.title("Pflanzen")
plt.xlabel('')
plt.text(0.2, 0.7, '\u0394'+'$T_{avg}$ = '+str(round(period_2_plants.CTI.mean() -
                                                     period_1_plants.CTI.mean(), 2))+u"\u2103", fontsize=10,
         color='k',  horizontalalignment='center', verticalalignment='center', transform=plant_ax.transAxes)

bird_ax = fig.add_subplot(132)
plt.xlabel('')
plt.hist(period_1_birds.CTI, alpha=0.4, bins=20, color='teal', edgecolor='k', label="2005-2009", density=True)
plt.axvline(period_1_birds.CTI.mean(), color='teal', linestyle='dashed', linewidth=1.5)
plt.hist(period_2_birds.CTI, alpha=0.4, bins=10, color='orangered', edgecolor='k', label="2015-2019", density=True)
plt.axvline(period_2_birds.CTI.mean(), color='orangered', linestyle='dashed', linewidth=1.5)
plt.legend(loc='upper right')
plt.title("Vögel")
plt.text(0.2, 0.7, '\u0394'+'$T_{avg}$ = ' +
         str(round(period_2_birds.CTI.mean() - period_1_birds.CTI.mean(), 2))+u"\u2103",
         fontsize=10, color='k',  horizontalalignment='center', verticalalignment='center',
         transform=bird_ax.transAxes)
plt.ylabel('')

butter_ax = fig.add_subplot(133)
plt.hist(period_1_butter.CTI, alpha=0.4, bins=20, color='teal', edgecolor='k', label="2005-2009", density=True)
plt.axvline(period_1_butter.CTI.mean(), color='teal', linestyle='dashed', linewidth=1.5)
plt.hist(period_2_butter.CTI, alpha=0.4, bins=10, color='orangered', edgecolor='k', label="2015-2019", density=True)
plt.axvline(period_2_butter.CTI.mean(), color='orangered', linestyle='dashed', linewidth=1.5)
plt.legend(loc='upper left')
plt.title("Tagfalter")
plt.xlabel('')
plt.ylabel('')
plt.text(0.2, 0.7, '\u0394'+'$T_{avg}$ = ' +
         str(round(period_2_butter.CTI.mean() - period_1_butter.CTI.mean(), 2))+u"\u2103",
         fontsize=10, color='k', horizontalalignment='center', verticalalignment='center',
         transform=butter_ax.transAxes)
fig.supxlabel("Temperatur Index der Artengemeinschaften ["+u"\u2103"+"]")
fig.savefig(path_plots+"CTIs_plants_birds_butter_bins.png", dpi=600, bbox_inches='tight')
plt.close()

fig = plt.figure(figsize=(13, 5))
plant_ax = fig.add_subplot(131)
sns.kdeplot(period_1_plants.CTI, shade=True, color='teal', alpha=0.4, label="2005-2009")
sns.kdeplot(period_2_plants.CTI, shade=True, color='orangered', alpha=0.4, label="2015-2019")
plt.axvline(period_1_plants.CTI.mean(), color='teal', linestyle='dashed', linewidth=1.5)
plt.axvline(period_2_plants.CTI.mean(), color='orangered', linestyle='dashed', linewidth=1.5)
plt.legend(loc='upper left')
plt.title("Plants")
plt.xlabel('')
plt.text(0.2, 0.7, '\u0394'+'$T_{avg}$ = ' +
         str(round(period_2_plants.CTI.mean() - period_1_plants.CTI.mean(), 2))+u"\u2103", fontsize=10,
         color='k',  horizontalalignment='center', verticalalignment='center', transform=plant_ax.transAxes)

bird_ax = fig.add_subplot(132)
sns.kdeplot(period_1_birds.CTI, shade=True, color='teal', alpha=0.4, label="2005-2009")
sns.kdeplot(period_2_birds.CTI, shade=True, color='orangered', alpha=0.4, label="2015-2019")
plt.xlabel('')
plt.axvline(period_1_birds.CTI.mean(), color='teal', linestyle='dashed', linewidth=1.5)
plt.axvline(period_2_birds.CTI.mean(), color='orangered', linestyle='dashed', linewidth=1.5)
plt.legend(loc='upper right')
plt.title("Birds")
plt.text(0.2, 0.7, '\u0394'+'$T_{avg}$ = ' +
         str(round(period_2_birds.CTI.mean() - period_1_birds.CTI.mean(), 2))+u"\u2103",
         fontsize=10, color='k',  horizontalalignment='center', verticalalignment='center',
         transform=bird_ax.transAxes)
plt.ylabel('')

butter_ax = fig.add_subplot(133)
sns.kdeplot(period_1_butter.CTI, shade=True, color='teal', alpha=0.4, label="2005-2009")
sns.kdeplot(period_2_butter.CTI, shade=True, color='orangered', alpha=0.4, label="2015-2019")
plt.axvline(period_1_butter.CTI.mean(), color='teal', linestyle='dashed', linewidth=1.5)
plt.axvline(period_2_butter.CTI.mean(), color='orangered', linestyle='dashed', linewidth=1.5)
plt.legend(loc='upper left')
plt.title("Butterflies")
plt.xlabel('')
plt.ylabel('')
plt.text(0.2, 0.7, '\u0394'+'$T_{avg}$ = ' +
         str(round(period_2_butter.CTI.mean() - period_1_butter.CTI.mean(), 2))+u"\u2103",
         fontsize=10, color='k', horizontalalignment='center', verticalalignment='center',
         transform=butter_ax.transAxes)
fig.supxlabel("Temperature Indices of species communities ["+u"\u2103"+"]")
fig.savefig(path_plots+"CTIs_plants_birds_butter_english.png", dpi=600, bbox_inches='tight')
plt.close()


