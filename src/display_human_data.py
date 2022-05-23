import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
from math import pi,floor,atan2,atan
from scipy.interpolate import splprep, splev
import sys
import json
from matplotlib.patches import Ellipse
import matplotlib.transforms as transforms

def plot_traj(subject1,subject2,table,title):
    plt.plot(subject1['x'], subject1['y'], label = 'Subject 1', color = 'green', linewidth = 1, alpha = 0.8)
    plt.plot(subject2['x'], subject2['y'], label = 'Subject 2', color = 'blue', linewidth = 1, alpha = 0.8)
    plt.plot(table['x'], table['y'], label = 'Table', color = 'red', linewidth = 1, alpha = 0.8)

    arrow_len = 0.1
    for i in range(len(subject1['x'])):
        if i%10 == 0:
            plt.arrow(subject1['x'][i], subject1['y'][i], \
            np.cos(subject1['Orientation_Globale'][i])*arrow_len,\
            np.sin(subject1['Orientation_Globale'][i])*arrow_len, head_width=.02, color = 'green')
            plt.arrow(subject2['x'][i], subject2['y'][i], \
            np.cos(subject2['Orientation_Globale'][i])*arrow_len,\
            np.sin(subject2['Orientation_Globale'][i])*arrow_len, head_width=.02, color = 'blue')
            plt.arrow(table['x'][i], table['y'][i], \
            np.cos(table['Orientation_Globale'][i])*arrow_len,\
            np.sin(table['Orientation_Globale'][i])*arrow_len, head_width=.02, color = 'red')
        # if i%50 == 0:
        #     plt.plot([subject2['x'][i],table['x'][i]], [subject2['y'][i],table['y'][i]], color = 'red', linewidth = 0.5)
        #     plt.plot([subject1['x'][i],table['x'][i]], [subject1['y'][i],table['y'][i]], color = 'black', linewidth = 0.5)

    plt.ylabel("y (m)")
    plt.xlabel("x (m)")
    plt.legend()
    plt.title(title)

def plot_go_ind(data,group_name,leader):
    traj = data['Trajectoires_Individuelles']
    ind = 0
    for i in range (len(traj['Sujet 1'])):
        if traj['Sujet 1'][i]['Binome'] == group_name\
        and traj['Sujet 1'][i]['Leader'] == leader:
            ind = i

    subject1 = traj['Sujet 1'][ind]
    subject2 = traj['Sujet 2'][ind]
    table = traj['Table'][ind]      
    # print("sujet 1 : ",subject1['Orientation_Init_Theorique'],subject1['Orientation_End_Theorique'])
    # print("sujet 2 : ",subject2['Orientation_Init_Theorique'],subject2['Orientation_End_Theorique'])
    # print("table : ",table['Orientation_Init_Theorique'],table['Orientation_End_Theorique'])
          
    # plt.plot(subject1['x'],subject1['Orientation_Globale'], color = 'lime')
    # plt.plot(subject1['x'],subject1['Orientation_Locale'], color = 'orange')
    # plt.show()

    title = "Individual trajectories (leader : "+leader+")"
    plot_traj(subject1,subject2,table,title)

    
def plot_go_mean(data,data_mean,group_name,leader):
    traj = data['Trajectoires_Individuelles']
    ind = 0
    for i in range (len(traj['Sujet 1'])):
        if traj['Sujet 1'][i]['Binome'] == group_name\
        and traj['Sujet 1'][i]['Leader'] == leader:
            ind = i
    ori_end = traj['Table'][ind]['Orientation_End_Theorique']
    str_ori = "Orientation_Table_End : "+str(ori_end)
    subject1 = data_mean['Trajectoires_Moyennes']['Sujet 1'][leader][str_ori]
    subject2 = data_mean['Trajectoires_Moyennes']['Sujet 2'][leader][str_ori] 
    table = data_mean['Trajectoires_Moyennes']['Table'][leader][str_ori]       

    title = "Mean trajectories (leader : "+leader+")"
    plot_traj(subject1,subject2,table,title)


def plot_return_ind(data,group_name,count):
    traj = data['Trajectoires_Individuelles']
    ind = []
    for i in range (len(traj['Sujet 1'])):
        if traj['Sujet 1'][i]['Binome'] == group_name:
            ind.append(i)

    subject1 = traj['Sujet 1'][ind[count]]
    subject2 = traj['Sujet 2'][ind[count]]
    table = traj['Table'][ind[count]]                

    title = "Individual trajectories"
    plot_traj(subject1,subject2,table,title)


def plot_return_mean(data,data_mean,group_name,count):
    traj = data['Trajectoires_Individuelles']
    ind = []
    for i in range (len(traj['Sujet 1'])):
        if traj['Sujet 1'][i]['Binome'] == group_name:
            ind.append(i)

    ori_init = traj['Table'][ind[count]]['Orientation_Init_Theorique']
    str_ori = "Orientation_Table_Init : "+str(ori_init)
    subject1 = data_mean['Trajectoires_Moyennes']['Sujet 1']['All data'][str_ori]
    subject2 = data_mean['Trajectoires_Moyennes']['Sujet 2']['All data'][str_ori] 
    table = data_mean['Trajectoires_Moyennes']['Table']['All data'][str_ori]   

    title = "Mean trajectories"
    plot_traj(subject1,subject2,table,title)
    
path = 'Data/Human/'

# Exemple ligne de commande : python display_human_data.py 'd2_p7_gris_1' 'Sujet1_Amaury&Sujet2_Jason'

arg = sys.argv
file_name = arg[1] # ex : d1_p4_gris_1
group_name = arg[2] # ex : Sujet1_Amaury&Sujet2_Jason

print(path + file_name + ".json")
f = open(path + file_name + ".json")
data = json.load(f)
f_m = open(path + file_name + "_mean.json")
data_mean = json.load(f_m)

if file_name[-1] == '1': # Go
    plt.subplot(2,3,1)
    plot_go_ind(data, group_name, "Sujet 1")
    plt.subplot(2,3,2)
    plot_go_ind(data, group_name, "Sujet 2")
    plt.subplot(2,3,3)
    plot_go_ind(data, group_name, "Sujet 1 et 2")
    plt.subplot(2,3,4)
    plot_go_mean(data, data_mean, group_name, "Sujet 1")
    plt.subplot(2,3,5)
    plot_go_mean(data, data_mean, group_name, "Sujet 2")
    plt.subplot(2,3,6)
    plot_go_mean(data, data_mean, group_name, "Sujet 1 et 2")
    plt.show()
else: # Return
    plt.subplot(1,4,1)    
    plot_return_ind(data, group_name,0)
    plt.subplot(1,4,2)    
    plot_return_ind(data, group_name,1)    
    plt.subplot(1,4,3)    
    plot_return_ind(data, group_name,2)
    plt.subplot(1,4,4)    
    plot_return_mean(data, data_mean, group_name,2)
    plt.show()

