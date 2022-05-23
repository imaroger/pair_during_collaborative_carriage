import sys
import numpy as np
import matplotlib.pyplot as plt
from math import pi,floor,atan2,atan
import json
from scipy import stats

# list_targets = ['d1_p4_jaune_1', 'd1_p4_gris_1', 'd1_p5_jaune_1', 'd1_p5_gris_1', 'd1_p6_jaune_1', 'd1_p6_gris_1', 'd2_p7_jaune_1', 'd2_p7_gris_1', 'd3_p7_gris_1',
# 				'd1_p4_jaune_2', 'd1_p4_gris_2', 'd1_p5_jaune_2', 'd1_p5_gris_2', 'd1_p6_jaune_2', 'd1_p6_gris_2', 'd2_p7_jaune_2', 'd2_p7_gris_2', 'd3_p7_gris_2']
# for file_name in list_targets:
# 	print("### ",file_name," ###")
# 	f = open(path + file_name + ".json")
# 	data = json.load(f)["Trajectoires_Individuelles"]
# 	print(len(data['Table']),len(data['Sujet 1']),len(data['Sujet 2']))
# 	for i in range(len(data['Table'])):
# 		if data['Table'][i]['Binome'] != data['Sujet 1'][i]['Binome'] or \
# 		data['Sujet 2'][i]['Binome'] != data['Sujet 1'][i]['Binome'] or \
# 		data['Sujet 2'][i]['Binome'] != data['Table'][i]['Binome']:
# 			print("binome different")		
# 		if data['Table'][i]['Leader'] != data['Sujet 1'][i]['Leader'] or \
# 		data['Sujet 2'][i]['Leader'] != data['Sujet 1'][i]['Leader'] or \
# 		data['Sujet 2'][i]['Leader'] != data['Table'][i]['Leader']:
# 			print("leader different")	

list_leaders = ['Sujet 1','Sujet 2','Sujet 1 et 2','All data']
list_sub = ['Sujet 1','Sujet 2','Table']
colors_mean = {'Sujet 1': 'blue','Sujet 2': 'red','Table': 'green'}
colors = {'Sujet 1': 'cyan','Sujet 2': 'orange','Table': 'lime'}
labels_mean = {'Sujet 1': 'Subject 1 (average)','Sujet 2': 'Subject 2 (average)','Table': 'Table (average)'}
labels = {'Sujet 1': 'Subject 1','Sujet 2': 'Subject 2','Table': 'Table'}
arg = sys.argv
file_name = arg[1] # ex : d1_p4_gris
path = 'Data/Human/'

### Go ###
f = open(path + file_name + "_1.json")
data = json.load(f)["Trajectoires_Individuelles"]
f_m = open(path + file_name + "_1_mean.json")
data_mean = json.load(f_m)["Trajectoires_Moyennes"]

count = 1
count_sub = 0
arrow_len = 0.1
leader = "Sujet 1 et 2"

nb_ori = len([n for n in data_mean["Table"][leader]])
for ori in data_mean["Table"][leader]:
	plt.subplot(2,nb_ori,count)
	for sub in data:
		first = True
		for i in range(len(data[sub])):
			# print(mean["nb"])
			if (data[sub][i]["Leader"] == leader and \
			data["Table"][i]["Orientation_End_Theorique"] == float(ori[23:]))\
			or (leader =="All data" and \
			data["Table"][i]["Orientation_End_Theorique"] == float(ori[23:])):
				if first:
					first = False
					plt.plot(data[sub][i]["x"],data[sub][i]["y"],alpha = 0.5,linewidth = 0.5,color = colors[sub],label = labels[sub])
				else:
					plt.plot(data[sub][i]["x"],data[sub][i]["y"],alpha = 0.5,linewidth = 0.5,color = colors[sub])
		mean = data_mean[sub][leader][ori]
		plt.plot(mean["x"],mean["y"],color = colors_mean[sub],label = labels_mean[sub])
		for i in range(len(mean['x'])):
			if i%10 == 0:
				plt.arrow(mean['x'][i], mean['y'][i], \
				np.cos(mean['Orientation_Globale'][i])*arrow_len,\
				np.sin(mean['Orientation_Globale'][i])*arrow_len, head_width=.02, color = colors_mean[sub])
	if mean["nb"] < 10:
		plt.title("Forward paths ("+str(mean["nb"])+" measurements) - Configuration 2")
	else:
		plt.title("Forward paths ("+str(mean["nb"])+" measurements) - Configuration 1")		
	plt.xlabel("x (m)")
	plt.ylabel("y (m)")	
	plt.text(data_mean["Table"]["All data"][ori]["x"][0],\
		data_mean["Table"]["All data"][ori]["y"][0]+0.15 , 'Start',\
		fontsize='x-large',ha='center')
	plt.text(data_mean["Table"]["All data"][ori]["x"][-1],\
		data_mean["Table"]["All data"][ori]["y"][-1]-0.3 , 'Goal',\
		fontsize='x-large',ha='center')
	plt.legend()
	count += 1

### Return ###

count = 4

f = open(path + file_name + "_2.json")
data = json.load(f)["Trajectoires_Individuelles"]
f_m = open(path + file_name + "_2_mean.json")
data_mean = json.load(f_m)["Trajectoires_Moyennes"]

nb_ori = len([n for n in data_mean["Table"]["All data"]])
for ori in data_mean["Table"]["All data"]:
	plt.subplot(2,nb_ori,count)
	for sub in data:
		first = True
		for i in range(len(data[sub])):
			if data["Table"][i]["Orientation_Init_Theorique"] == float(ori[24:]):
				if first:
					first = False
					plt.plot(data[sub][i]["x"],data[sub][i]["y"],alpha = 0.5,linewidth = 0.5,color = colors[sub],label = labels[sub])
				else:
					plt.plot(data[sub][i]["x"],data[sub][i]["y"],alpha = 0.5,linewidth = 0.5,color = colors[sub])
		mean = data_mean[sub]["All data"][ori]
		plt.plot(mean["x"],mean["y"],color = colors_mean[sub],label = labels_mean[sub])
		for i in range(len(mean['x'])):
			if i%10 == 0:
				plt.arrow(mean['x'][i], mean['y'][i], \
				np.cos(mean['Orientation_Globale'][i])*arrow_len,\
				np.sin(mean['Orientation_Globale'][i])*arrow_len, head_width=.02, color = colors_mean[sub])	
	
	if data_mean[sub]["All data"][ori]["nb"] < 20:
		plt.title("Return paths ("+str(data_mean[sub]["All data"][ori]["nb"])+" measurements) - Configuration 2")
	else:
		plt.title("Return paths ("+str(data_mean[sub]["All data"][ori]["nb"])+" measurements) - Configuration 1")

	plt.legend()
	plt.xlabel("x (m)")
	plt.ylabel("y (m)")	
	plt.text(data_mean["Table"]["All data"][ori]["x"][0],\
		data_mean["Table"]["All data"][ori]["y"][0]-0.3 , 'Goal',\
		fontsize='x-large',ha='center')
	plt.text(data_mean["Table"]["All data"][ori]["x"][-1],\
		data_mean["Table"]["All data"][ori]["y"][-1]+0.15 , 'Start',\
		fontsize='x-large',ha='center')
	count -= 1

plt.show()

# for sub in data_mean:
# 	print(sub)
# 	if file_name[-1] == '1':
# 		for leader in list_leaders[:3]:
# 			nb_ori = len([n for n in data_mean[sub][leader]])
# 			for ori in data_mean[sub][leader]:
# 				plt.subplot(3,6,count+count_sub*6)
# 				for i in range(len(data[sub])):
# 					# print(mean["nb"])
# 					if data[sub][i]["Leader"] == leader and \
# 					data["Table"][i]["Orientation_End_Theorique"] == float(ori[23:]):
# 						plt.plot(data[sub][i]["x"],data[sub][i]["y"],linewidth = 0.5)
# 				plt.plot(mean["x"],mean["y"],color = 'black')
# 				plt.title(sub+", "+leader+" ("+str(mean["nb"])+" trajs)")
# 				count += 1
# 		count_sub += 1
# 		count = 1
# 	else:
# 		leader = "All data"
# 		nb_ori = len([n for n in data_mean[sub][leader]])
# 		for ori in data_mean[sub][leader]:
# 			plt.subplot(3,2,count)
# 			for i in range(len(data[sub])):
# 				if data["Table"][i]["Orientation_Init_Theorique"] == float(ori[24:]):
# 					plt.plot(data[sub][i]["x"],data[sub][i]["y"],linewidth = 0.5)
# 			plt.plot(mean["x"],mean["y"],color = 'black')
# 			plt.title(sub+", "+leader+" ("+str(mean["nb"])+" trajs)")
# 			count += 1
			
# plt.show()

