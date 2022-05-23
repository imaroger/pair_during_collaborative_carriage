import numpy as np
import matplotlib.pylab as plt
from math import pi,floor,atan2,atan, nan, sqrt
import json
from scipy.interpolate import splprep, splev, interp1d
from scipy import stats

path = 'Data/Human/'
list_targets = ['d1_p4_jaune_1', 'd1_p4_gris_1', 'd1_p5_jaune_1', 'd1_p5_gris_1', 'd1_p6_jaune_1', 'd1_p6_gris_1', 'd2_p7_jaune_1', 'd2_p7_gris_1', 'd3_p7_gris_1',
				'd1_p4_jaune_2', 'd1_p4_gris_2', 'd1_p5_jaune_2', 'd1_p5_gris_2', 'd1_p6_jaune_2', 'd1_p6_gris_2', 'd2_p7_jaune_2', 'd2_p7_gris_2', 'd3_p7_gris_2']
list_leaders = ['Sujet 1','Sujet 2','Sujet 1 et 2']
list_sub = ['Sujet 1','Sujet 2','Table']

dist_from_table = {}
dist_from_table['Sujet 1'] = {}
dist_from_table['Sujet 2'] = {}
for leader in list_leaders:
	dist_from_table['Sujet 1'][leader] = {}
	dist_from_table['Sujet 2'][leader] = {}
	dist_from_table['Sujet 1'][leader]["Go"] = []
	dist_from_table['Sujet 2'][leader]["Go"] = [] 	
	dist_from_table['Sujet 1'][leader]["Return"] = []
	dist_from_table['Sujet 2'][leader]["Return"] = [] 	

count = 1
time = np.linspace(0, 100, 500)
for traj in list_targets:
	print("### ",traj," ###")
	f = open(path+traj+'.json')
	data = json.load(f)['Trajectoires_Individuelles']
	for i in range(len(data["Table"])):
		# pair = data["Table"][i]["Binome"]
		# leader = data["Table"][i]["Leader"]
		# i1,i2 = 0,0
		# for j in range(max(0,i-3),min(i+3,len(data["Table"]))):
		# 	if data["Sujet 1"][j]["Leader"] == leader and data["Sujet 1"][j]["Binome"] == pair:
		# 		i1 = j 
		# 	if data["Sujet 2"][j]["Leader"] == leader and data["Sujet 2"][j]["Binome"] == pair:
		# 		i2 = j 
		# if(i != i1 or i != i2):
		# 	print(i,i1,i2,leader,data["Sujet 1"][i1]["Leader"],data["Sujet 2"][i2]["Leader"])
		dist1 = np.sqrt((np.array(data["Table"][i]["x"])-np.array(data["Sujet 1"][i]["x"]))**2+\
			(np.array(data["Table"][i]["y"])-np.array(data["Sujet 1"][i]["y"]))**2)
		dist2 = np.sqrt((np.array(data["Table"][i]["x"])-np.array(data["Sujet 2"][i]["x"]))**2+\
			(np.array(data["Table"][i]["y"])-np.array(data["Sujet 2"][i]["y"]))**2)		
		leader = data["Table"][i]["Leader"]
		if traj[-1] == '1':
			# print("go")
			dist_from_table['Sujet 1'][leader]["Go"].append(dist1)
			dist_from_table['Sujet 2'][leader]["Go"].append(dist2)		

		else:
			# print("return")
			dist_from_table['Sujet 1'][leader]["Return"].append(dist1)
			dist_from_table['Sujet 2'][leader]["Return"].append(dist2)			
		# print("----",len(dist_from_table['Sujet 1'][leader]["Go"]),len(dist_from_table['Sujet 1'][leader]["Return"]))

count = 1
for leader in list_leaders:
	mean1,mean2 = [],[]
	std1,std2 = [],[]
	for i in range(len(np.transpose(dist_from_table['Sujet 1'][leader]["Go"]))):
		mean1.append(np.mean(np.transpose(dist_from_table['Sujet 1'][leader]["Go"])[i]))
		mean2.append(np.mean(np.transpose(dist_from_table['Sujet 2'][leader]["Go"])[i]))
		std1.append(np.std(np.transpose(dist_from_table['Sujet 1'][leader]["Go"])[i]))
		std2.append(np.std(np.transpose(dist_from_table['Sujet 2'][leader]["Go"])[i]))

	plt.subplot(1,5,count)
	plt.plot(time,mean1,label='Sujet 1',color='orange')
	plt.plot(time,mean2,label='Sujet 2',color='blue')
	plt.fill_between(time, -np.array(std1)+np.array(mean1), np.array(std1)+np.array(mean1), color='orange',alpha = 0.2)
	plt.fill_between(time, -np.array(std2)+np.array(mean2), np.array(std2)+np.array(mean2), color='blue',alpha = 0.2)
	plt.legend()	
	plt.title("Go with leader : "+leader)
	plt.xlabel("time")
	plt.ylabel("distance from table (m)")
	count += 1

mean1,mean2 = [],[]
std1,std2 = [],[]
leader = "Sujet 1 et 2"
for i in range(len(np.transpose(dist_from_table['Sujet 1'][leader]["Return"]))):	
	mean1.append(np.mean(np.transpose(dist_from_table['Sujet 1'][leader]["Return"])[i]))
	mean2.append(np.mean(np.transpose(dist_from_table['Sujet 2'][leader]["Return"])[i]))
	std1.append(np.std(np.transpose(dist_from_table['Sujet 1'][leader]["Return"])[i]))
	std2.append(np.std(np.transpose(dist_from_table['Sujet 2'][leader]["Return"])[i]))

plt.subplot(1,5,count)
plt.plot(time,mean1,label='Sujet 1',color='orange')
plt.plot(time,mean2,label='Sujet 2',color='blue')
plt.fill_between(time, -np.array(std1)+np.array(mean1), np.array(std1)+np.array(mean1), color='orange',alpha = 0.2)
plt.fill_between(time, -np.array(std2)+np.array(mean2), np.array(std2)+np.array(mean2), color='blue',alpha = 0.2)
plt.legend()	
plt.title("Return with leader : "+leader)
plt.xlabel("time")
plt.ylabel("distance from table (m)")
count += 1
# plt.show()

mean1,mean2 = [],[]
std1,std2 = [],[]
leader = "Sujet 1 et 2"
for i in range(len(np.transpose(dist_from_table['Sujet 1'][leader]["Return"]))):	
	mean1.append(np.mean(np.transpose(dist_from_table['Sujet 1'][leader]["Go"] + dist_from_table['Sujet 1'][leader]["Return"])[i]))
	mean2.append(np.mean(np.transpose(dist_from_table['Sujet 2'][leader]["Go"] + dist_from_table['Sujet 2'][leader]["Return"])[i]))
	std1.append(np.std(np.transpose(dist_from_table['Sujet 1'][leader]["Go"] + dist_from_table['Sujet 1'][leader]["Return"])[i]))
	std2.append(np.std(np.transpose(dist_from_table['Sujet 2'][leader]["Go"] + dist_from_table['Sujet 2'][leader]["Return"])[i]))

plt.subplot(1,5,count)
plt.plot(time,mean1,label='Sujet 1',color='orange')
plt.plot(time,mean2,label='Sujet 2',color='blue')
plt.fill_between(time, -np.array(std1)+np.array(mean1), np.array(std1)+np.array(mean1), color='orange',alpha = 0.2)
plt.fill_between(time, -np.array(std2)+np.array(mean2), np.array(std2)+np.array(mean2), color='blue',alpha = 0.2)
plt.legend()	
plt.title("All with leader : "+leader)
plt.xlabel("time")
plt.ylabel("distance from table (m)")
count += 1
plt.show()

