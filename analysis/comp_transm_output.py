# -*- coding: utf-8 -*-
"""
Desc: script to compare forest transmissivity from different model configurations
Created on 21.03.22 13:29
@author: malle
"""

from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import datetime
import numpy as np
import os

site='BDM_3'
basefolder = Path('/home/malle/transm_calcs/') / site
#thislist = ["Output_CR_5m","Output_CR_10m", "Output_CR_5m_manual", "Output_CR_10m_manual","Output_CR_5m_random0.5","Output_CR_10m_random0.5"]
thislist = ["Output_CR_10m_summer","Output_CR_10m_winter","Output_CR_10m_summer_025_fm1_0mbuffer","Output_CR_10m_summer_075_fm1_0mbuffer","Output_CR_10m_summer_manual"]
labellist = ["original CHM - leaf on","original CHM - leaf off","Mild forest management scenario (25%)","Severe forest management scenario (75%)","Wind-throw event"]

plot_dir = basefolder / 'Plots_comp'
isExist = os.path.exists(plot_dir)
if not isExist:
    os.makedirs(plot_dir)
    print("Plot directory is created!")

summer_sol_all=[]
summer_sol_for_all=[]
all_data=[]
all_data_for=[]


for x in thislist:
    transm_run = pd.read_pickle(basefolder / Path(x) / "Plots" / "combined_frame.pkl")
    t3 = transm_run[['Forest_Transmissivity', 'Vf_hemi', 'datetime']]

    transm_run_for = pd.read_pickle(basefolder / Path(x) / "Plots" / "combined_frame_forest.pkl")
    t3_for = transm_run_for[['Forest_Transmissivity', 'Vf_hemi', 'datetime']]

    summer_sol = t3.loc[(t3["datetime"] > pd.to_datetime(datetime.date(2020, 6, 19))) & (t3["datetime"] < pd.to_datetime(datetime.date(2020, 6, 21)))]
    summer_sol = transm_run.loc[(transm_run["datetime"] > pd.to_datetime(datetime.date(2020, 6, 19))) & (transm_run["datetime"] < pd.to_datetime(datetime.date(2020, 6, 21)))]
    summer_sol.insert(0,'index',np.arange(len(summer_sol)),True)
    summer_sol1 = summer_sol.set_index('index')

    summer_sol_for = t3_for.loc[(t3_for["datetime"] > pd.to_datetime(datetime.date(2020, 6, 19))) & (t3_for["datetime"] < pd.to_datetime(datetime.date(2020, 6, 21)))]
    summer_sol_for = transm_run_for.loc[(transm_run_for["datetime"] > pd.to_datetime(datetime.date(2020, 6, 19))) & (transm_run_for["datetime"] < pd.to_datetime(datetime.date(2020, 6, 21)))]
    summer_sol_for.insert(0,'index',np.arange(len(summer_sol_for)),True)
    summer_sol_for1 = summer_sol_for.set_index('index')

    t3.insert(0,'index',np.arange(len(t3)),True)
    t31 = t3.set_index('index')
    summer_sol_all.append(summer_sol1)
    all_data.append(t31)

    t3_for.insert(0,'index',np.arange(len(t3)),True)
    t31_for = t3_for.set_index('index')
    summer_sol_for_all.append(summer_sol_for1)
    all_data_for.append(t31_for)

all_data[0].set_index('datetime')
all_data_for[0].set_index('datetime')

prop_cycle = plt.rcParams['axes.prop_cycle']
colors = prop_cycle.by_key()['color']

fig1 = plt.figure(figsize=(13, 5))
ax = fig1.add_subplot(111)
for num in range(len(all_data)):
    a2 = all_data_for[num].groupby('datetime').Forest_Transmissivity.describe()
    a2a = all_data_for[num].groupby('datetime').Forest_Transmissivity.median()
    #if (num % 2) == 0:
    #    plt.plot(a2.index, a2['mean'], linestyle='dashed', label=thislist[num])
   # else:
    plt.plot(a2.index, a2['mean'], label=labellist[num]+' (mean)', color=colors[num])
    plt.plot(a2.index, a2a, linestyle='dashed', label=labellist[num]+' (median)', color=colors[num])
    #plt.plot(all_data[1].datetime.groupby('datetime'),all_data[1].Forest_Transmissivity.groupby('datetime'),color='blue',linestyle='dashed',label=thislist[1])
#plt.plot(all_data[2].datetime.groupby('datetime'),all_data[2].Forest_Transmissivity.groupby('datetime'),color='red',label=thislist[2])
#plt.plot(all_data[3].datetime.groupby('datetime'),all_data[3].Forest_Transmissivity.groupby('datetime'),color='orange',linestyle='dashed',label=thislist[3])
#plt.legend(loc='lower left')
l5 = plt.legend(bbox_to_anchor=(0.93,-0.15), loc="lower right",
                bbox_transform=fig1.transFigure, ncol=3)
plt.ylabel('Forest Transmissivity [%]')
plt.grid(True)
if site == 'BDM_1':
    plt.title("BDM1 @ Lungerersee (mixed forest)")
elif site == 'BDM_2':
    plt.title("BDM2 @ Sion (conifers)")
elif site == 'BDM_3':
    plt.title("BDM3 @ Bodensee (beech forest)")
else:
    plt.title("")

ax.set_xlim([datetime.date(2020, 6, 1), datetime.date(2020, 9, 1)])
plt.gcf().autofmt_xdate()
fig_save1 = plot_dir / "time_comp1a.png"
fig1.savefig(fig_save1, dpi=350, bbox_inches='tight')
plt.close()


def tsplot(ax, data,**kw):
    x = np.arange(data.shape[0])
    est = data['mean']
    sd = data['std']
    cis = (data['25%'],data['75%'])  # (est - sd, est + sd)
    ax.fill_between(data.index,cis[0],cis[1],alpha=0.2, **kw)
    ax.plot(data.index,est,**kw)
    ax.margins(x=0)

fig1 = plt.figure(figsize=(13, 5))
ax = fig1.add_subplot(111)
for num in range(len(all_data)):
    a2 = all_data_for[num].groupby('datetime').Forest_Transmissivity.describe()
    tsplot(ax, a2)

plt.ylabel('Forest Transmissivity [%]')
plt.grid(True)
ax.set_xlim([datetime.date(2020, 6, 1), datetime.date(2020, 9, 1)])
plt.gcf().autofmt_xdate()
fig_save1 = plot_dir / "time_comp1a_25_75.png"
fig1.savefig(fig_save1, dpi=250, bbox_inches='tight')
plt.close()

fig = plt.figure(figsize=(13, 5))
sns.histplot(summer_sol_for_all[0].Forest_Transmissivity , stat = "probability", color='teal', alpha=0.4, bins=20,label=labellist[0]) # stat = "probability",
plt.axvline(summer_sol_for_all[0].Forest_Transmissivity.median(), color='teal', linestyle='dashed', linewidth=1.5)
sns.histplot(summer_sol_for_all[1].Forest_Transmissivity , stat = "probability", color='orangered', alpha=0.4, bins=20,label=labellist[1])
plt.axvline(summer_sol_for_all[1].Forest_Transmissivity.median(), color='orangered', linestyle='dashed', linewidth=1.5)

sns.histplot(summer_sol_for_all[3].Forest_Transmissivity , stat = "probability", color='blue', alpha=0.4, bins=20,label=labellist[3]) # stat = "probability",
plt.axvline(summer_sol_for_all[3].Forest_Transmissivity.median(), color='blue', linestyle='dashed', linewidth=1.5)
sns.histplot(summer_sol_for_all[2].Forest_Transmissivity , stat = "probability", color='yellow', alpha=0.4, bins=20,label=labellist[2])
plt.axvline(summer_sol_for_all[2].Forest_Transmissivity.median(), color='yellow', linestyle='dashed', linewidth=1.5)

#plt.legend(loc='upper left')
l5 = plt.legend(bbox_to_anchor=(0.93,-0.08), loc="lower right",
                bbox_transform=fig.transFigure, ncol=4)
plt.title("20.06.2020")
plt.xlabel('Forest Transmissivity [%]')
fig_save = plot_dir / "summer_5m_10m_comp_man_ran2.png"
fig.savefig(fig_save, dpi=250, bbox_inches='tight')
plt.close()
test=1


fig = plt.figure(figsize=(10, 5))
ax1 = fig.add_subplot(111)
sns.kdeplot(summer_sol_for_all[0].Forest_Transmissivity, shade=True, color='teal', alpha=0.4, label=labellist[0]) # stat = "probability",
sns.kdeplot(summer_sol_for_all[1].Forest_Transmissivity, shade=True, color='orangered', alpha=0.4, label=labellist[1])
sns.kdeplot(summer_sol_for_all[3].Forest_Transmissivity, shade=True, color='blue', alpha=0.4, label=labellist[3])
sns.kdeplot(summer_sol_for_all[2].Forest_Transmissivity, shade=True, color='yellow', alpha=0.4, label=labellist[2])

plt.axvline(summer_sol_for_all[0].Forest_Transmissivity.mean(), color='teal', linestyle='dashed', linewidth=1.5)
plt.axvline(summer_sol_for_all[1].Forest_Transmissivity.mean(), color='orangered', linestyle='dashed', linewidth=1.5)
plt.axvline(summer_sol_for_all[3].Forest_Transmissivity.mean(), color='blue', linestyle='dashed', linewidth=1.5)
plt.axvline(summer_sol_for_all[2].Forest_Transmissivity.mean(), color='yellow', linestyle='dashed', linewidth=1.5)
#plt.legend(loc='upper right')
l5 = plt.legend(bbox_to_anchor=(0.8,-0.11), loc="lower right",
                bbox_transform=fig.transFigure, ncol=2)
plt.title("20.06.2020")
plt.xlabel('Forest Transmissivity [%]')
fig_save = plot_dir / "kde_comp_winter_summer.png"
fig.savefig(fig_save, dpi=350, bbox_inches='tight')
plt.close()