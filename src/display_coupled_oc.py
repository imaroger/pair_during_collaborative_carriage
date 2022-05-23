import sys
import numpy as np
import matplotlib.pyplot as plt
from math import pi,floor,atan2,atan
import json
# import matplotlib as mpl
import matplotlib.patches as mpatches
import matplotlib.lines as mlines

# mpl.rc('text', usetex=True)

path_human = 'Data/Human/'
path_oc = 'Data/CoupledOptimalControl/'
leader = "Sujet 1 et 2"
sub = "Sujet 1"
arrow_len = 0.1

#################################################################################
################################### ALL TRAJS ###################################
#################################################################################

# list_trajs = ['d1_p4_jaune', 'd1_p4_gris', 'd1_p5_jaune', 'd1_p5_gris', 'd1_p6_jaune', 'd1_p6_gris', 'd2_p7_jaune', 'd2_p7_gris', 'd3_p7_gris']

# count_go = 1
# count_return = 1
# for traj in list_trajs:
# 	f = open(path_human + traj + "_1_mean.json")
# 	data_human = json.load(f)["Trajectoires_Moyennes"]
# 	data_human_1 = data_human["Sujet 1"][leader]
# 	data_human_2 = 	data_human["Sujet 2"][leader]
# 	plt.subplot(3,3,count_go)
# 	plt.title(traj)
# 	for ori in data_human_1:
# 		# if data_human[ori]['nb'] > 5:
# 		name_oc = traj + "_1_" + leader + "_" + ori[23:min(28,len(ori))]
# 		data_oc = np.transpose(np.loadtxt(path_oc + name_oc + ".dat"))

		
# 		# plt.plot(data_oc[0],data_oc[1],color = 'orange',label = 'oc')

# 		length = len(data_human_1[ori]['x'])
# 		time = np.linspace(0,100,length)
# 		old_time = np.linspace(0,100,len(data_oc[0]))
# 		x_oc_1 = np.interp(time, old_time, data_oc[0])
# 		y_oc_1 = np.interp(time, old_time, data_oc[1])		
# 		th_oc_1 = np.interp(time, old_time, data_oc[2])
# 		x_oc_2 = np.interp(time, old_time, data_oc[3])
# 		y_oc_2 = np.interp(time, old_time, data_oc[4])		
# 		th_oc_2 = np.interp(time, old_time, data_oc[5])		

# 		for i in range(length):
# 			if i%50 == 0:
# 				plt.arrow(x_oc_1[i], y_oc_1[i],\
# 					np.cos(th_oc_1[i])*arrow_len,\
# 					np.sin(th_oc_1[i])*arrow_len, head_width=.02, color = 'red')
# 				plt.arrow(data_human_1[ori]['x'][i], data_human_1[ori]['y'][i],\
# 					np.cos(data_human_1[ori]['Orientation_Globale'][i])*arrow_len,\
# 					np.sin(data_human_1[ori]['Orientation_Globale'][i])*arrow_len, head_width=.02, color = 'red')

# 				plt.arrow(x_oc_2[i], y_oc_2[i],\
# 					np.cos(th_oc_2[i])*arrow_len,\
# 					np.sin(th_oc_2[i])*arrow_len, head_width=.02, color = 'green')
# 				plt.arrow(data_human_2[ori]['x'][i], data_human_2[ori]['y'][i],\
# 					np.cos(data_human_2[ori]['Orientation_Globale'][i])*arrow_len,\
# 					np.sin(data_human_2[ori]['Orientation_Globale'][i])*arrow_len, head_width=.02, color = 'green')

# 		plt.plot(x_oc_1,y_oc_1,color = 'red',label = 'oc')
# 		plt.plot(data_human_1[ori]['x'],data_human_1[ori]['y'],color = 'red', linestyle = 'dotted',label = 'average human')	
# 		plt.plot(x_oc_2,y_oc_2,color = 'green',label = 'oc')
# 		plt.plot(data_human_2[ori]['x'],data_human_2[ori]['y'],color = 'green', linestyle = 'dotted',label = 'average human')	


# 	# else:
# 	# 	print(data_human[ori]['nb'],"not plot")
# 	count_go += 1
# plt.show()

# for traj in list_trajs:
# 	f = open(path_human + traj + "_2_mean.json")
# 	data_human = json.load(f)["Trajectoires_Moyennes"]
# 	data_human_1 = data_human["Sujet 1"]["All data"]
# 	data_human_2 = 	data_human["Sujet 2"]["All data"]
# 	plt.subplot(3,3,count_return)
# 	plt.title(traj)
# 	for ori in data_human_1:
# 		# if data_human[ori]['nb'] > 5:
# 		name_oc = traj + "_2_" + leader + "_" + ori[24:min(29,len(ori))]
# 		data_oc = np.transpose(np.loadtxt(path_oc + name_oc + ".dat"))

		
# 		# plt.plot(data_oc[0],data_oc[1],color = 'orange',label = 'oc')

# 		length = len(data_human_1[ori]['x'])
# 		time = np.linspace(0,100,length)
# 		old_time = np.linspace(0,100,len(data_oc[0]))
# 		x_oc_2 = np.interp(time, old_time, data_oc[0])
# 		y_oc_2 = np.interp(time, old_time, data_oc[1])		
# 		th_oc_2 = np.interp(time, old_time, data_oc[2])
# 		x_oc_1 = np.interp(time, old_time, data_oc[3])
# 		y_oc_1 = np.interp(time, old_time, data_oc[4])		
# 		th_oc_1 = np.interp(time, old_time, data_oc[5])		

# 		for i in range(length):
# 			if i%50 == 0:
# 				plt.arrow(x_oc_1[i], y_oc_1[i],\
# 					np.cos(th_oc_1[i])*arrow_len,\
# 					np.sin(th_oc_1[i])*arrow_len, head_width=.02, color = 'red')
# 				plt.arrow(data_human_1[ori]['x'][i], data_human_1[ori]['y'][i],\
# 					np.cos(data_human_1[ori]['Orientation_Globale'][i])*arrow_len,\
# 					np.sin(data_human_1[ori]['Orientation_Globale'][i])*arrow_len, head_width=.02, color = 'red')

# 				plt.arrow(x_oc_2[i], y_oc_2[i],\
# 					np.cos(th_oc_2[i])*arrow_len,\
# 					np.sin(th_oc_2[i])*arrow_len, head_width=.02, color = 'green')
# 				plt.arrow(data_human_2[ori]['x'][i], data_human_2[ori]['y'][i],\
# 					np.cos(data_human_2[ori]['Orientation_Globale'][i])*arrow_len,\
# 					np.sin(data_human_2[ori]['Orientation_Globale'][i])*arrow_len, head_width=.02, color = 'green')

# 		plt.plot(x_oc_1,y_oc_1,color = 'red',label = 'oc')
# 		plt.plot(data_human_1[ori]['x'],data_human_1[ori]['y'],color = 'red', linestyle = 'dotted',label = 'average human')	
# 		plt.plot(x_oc_2,y_oc_2,color = 'green',label = 'oc')
# 		plt.plot(data_human_2[ori]['x'],data_human_2[ori]['y'],color = 'green', linestyle = 'dotted',label = 'average human')	

# 	count_return += 1
# plt.show()

#################################################################################
################################### FEW TRAJS ###################################
#################################################################################

# list_trajs_go = ['d1_p4_jaune_1', 'd1_p4_gris_1']
# list_trajs_return = ['d1_p4_jaune_2', 'd1_p4_gris_2']
# name = {'d1_p4_jaune_1':'Goal 5 (Forward path)','d1_p4_gris_1':'Goal 6 (Forward path)',
# 	'd1_p4_jaune_2':'Goal 5 (Return path)','d1_p4_gris_2':'Goal 6 (Return path)'}

list_trajs_go = ['d2_p7_gris_1', 'd1_p4_gris_1']
list_trajs_return = ['d2_p7_gris_2', 'd1_p4_gris_2']
name = {'d2_p7_gris_1':'Goal 2 (Forward path)','d1_p4_gris_1':'Goal 6 (Forward path)',
	'd2_p7_gris_2':'Goal 2 (Return path)','d1_p4_gris_2':'Goal 6 (Return path)'}

legend = True
count = 1
for traj in list_trajs_go:
	f = open(path_human + traj + "_mean.json")
	data_human = json.load(f)["Trajectoires_Moyennes"]
	data_human_1 = data_human["Sujet 1"][leader]
	data_human_2 = 	data_human["Sujet 2"][leader]
	plt.subplot(2,2,count)
	plt.title(name[traj])
	two_ori = False
	for ori in data_human_1:
		# if data_human[ori]['nb'] > 5:
		name_oc = traj + "_" + leader + "_" + ori[23:min(28,len(ori))]
		data_oc = np.transpose(np.loadtxt(path_oc + name_oc + ".dat"))

		
		# plt.plot(data_oc[0],data_oc[1],color = 'orange',label = 'oc')

		length = len(data_human_1[ori]['x'])
		time = np.linspace(0,100,length)
		old_time = np.linspace(0,100,len(data_oc[0]))
		x_oc_1 = np.interp(time, old_time, data_oc[0])
		y_oc_1 = np.interp(time, old_time, data_oc[1])		
		th_oc_1 = np.interp(time, old_time, data_oc[2])
		x_oc_2 = np.interp(time, old_time, data_oc[3])
		y_oc_2 = np.interp(time, old_time, data_oc[4])		
		th_oc_2 = np.interp(time, old_time, data_oc[5])		

		for i in range(length):
			if i%50 == 0:
				if data_human_1[ori]['nb'] > 10:
					plt.arrow(x_oc_1[i], y_oc_1[i],\
						np.cos(th_oc_1[i])*arrow_len,\
						np.sin(th_oc_1[i])*arrow_len, head_width=.02, color = 'blue')
					plt.arrow(data_human_1[ori]['x'][i], data_human_1[ori]['y'][i],\
						np.cos(data_human_1[ori]['Orientation_Globale'][i])*arrow_len,\
						np.sin(data_human_1[ori]['Orientation_Globale'][i])*arrow_len, head_width=.02, color = 'blue')

					plt.arrow(x_oc_2[i], y_oc_2[i],\
						np.cos(th_oc_2[i])*arrow_len,\
						np.sin(th_oc_2[i])*arrow_len, head_width=.02, color = 'red')
					plt.arrow(data_human_2[ori]['x'][i], data_human_2[ori]['y'][i],\
						np.cos(data_human_2[ori]['Orientation_Globale'][i])*arrow_len,\
						np.sin(data_human_2[ori]['Orientation_Globale'][i])*arrow_len, head_width=.02, color = 'red')

				else:
					plt.arrow(x_oc_1[i], y_oc_1[i],\
						np.cos(th_oc_1[i])*arrow_len,\
						np.sin(th_oc_1[i])*arrow_len, head_width=.02, color = 'cyan')
					plt.arrow(data_human_1[ori]['x'][i], data_human_1[ori]['y'][i],\
						np.cos(data_human_1[ori]['Orientation_Globale'][i])*arrow_len,\
						np.sin(data_human_1[ori]['Orientation_Globale'][i])*arrow_len, head_width=.02, color = 'cyan')

					plt.arrow(x_oc_2[i], y_oc_2[i],\
						np.cos(th_oc_2[i])*arrow_len,\
						np.sin(th_oc_2[i])*arrow_len, head_width=.02, color = 'orange')
					plt.arrow(data_human_2[ori]['x'][i], data_human_2[ori]['y'][i],\
						np.cos(data_human_2[ori]['Orientation_Globale'][i])*arrow_len,\
						np.sin(data_human_2[ori]['Orientation_Globale'][i])*arrow_len, head_width=.02, color = 'orange')
		if data_human_1[ori]['nb'] > 10:
			plt.plot(x_oc_1,y_oc_1,color = 'blue')#,label = 'OC Subject 1 - Configuration 1')
			plt.plot(data_human_1[ori]['x'],data_human_1[ori]['y'],color = 'blue', linestyle = 'dotted')#,label = 'Average Subject 1 - Configuration 1')	
			plt.plot(x_oc_2,y_oc_2,color = 'red')#,label = 'OC Subject 2 - Configuration 1')
			plt.plot(data_human_2[ori]['x'],data_human_2[ori]['y'],color = 'red', linestyle = 'dotted')#,label = 'Average Subject 2 - Configuration 1')
		else:
			two_ori = True
			plt.plot(x_oc_1,y_oc_1,color = 'cyan')#,label = 'OC Subject 1 - Configuration 2')
			plt.plot(data_human_1[ori]['x'],data_human_1[ori]['y'],color = 'cyan', linestyle = 'dotted')#,label = 'Average Subject 1 - Configuration 2')	
			plt.plot(x_oc_2,y_oc_2,color = 'orange')#,label = 'OC Subject 2 - Configuration 2')
			plt.plot(data_human_2[ori]['x'],data_human_2[ori]['y'],color = 'orange', linestyle = 'dotted')#,label = 'Average Subject 2 - Configuration 2')

		plt.ylabel("y (m)")
		plt.xlabel("x (m)")		

	line = mlines.Line2D([], [], color='black', label='Generated trajectory')
	dotted_line = mlines.Line2D([], [], color='black', linestyle = 'dotted', label='Average trajectory')			
	blue_patch = mpatches.Patch(color='blue', label='Subject 1 - Config. 1')			
	red_patch = mpatches.Patch(color='red', label='Subject 2 - Config. 1')
	if two_ori and legend:
		# legend = False
		cyan_patch = mpatches.Patch(color='cyan', label='Subject 1 - Config. 2')			
		orange_patch = mpatches.Patch(color='orange', label='Subject 2 - Config. 2')
		plt.legend(handles=[line,dotted_line,blue_patch,red_patch,cyan_patch,orange_patch])
	elif not two_ori and legend:
		plt.legend(handles=[line,dotted_line,blue_patch,red_patch])

	# else:
	# 	print(data_human[ori]['nb'],"not plot")
	count += 1

for traj in list_trajs_return:
	f = open(path_human + traj + "_mean.json")
	data_human = json.load(f)["Trajectoires_Moyennes"]
	data_human_1 = data_human["Sujet 1"]["All data"]
	data_human_2 = 	data_human["Sujet 2"]["All data"]
	plt.subplot(2,2,count)
	plt.title(name[traj])
	two_ori = False
	for ori in data_human_1:
		# if data_human[ori]['nb'] > 5:
		name_oc = traj + "_" + leader + "_" + ori[24:min(29,len(ori))]
		data_oc = np.transpose(np.loadtxt(path_oc + name_oc + ".dat"))

		
		# plt.plot(data_oc[0],data_oc[1],color = 'orange',label = 'oc')

		length = len(data_human_1[ori]['x'])
		time = np.linspace(0,100,length)
		old_time = np.linspace(0,100,len(data_oc[0]))
		x_oc_2 = np.interp(time, old_time, data_oc[0])
		y_oc_2 = np.interp(time, old_time, data_oc[1])		
		th_oc_2 = np.interp(time, old_time, data_oc[2])
		x_oc_1 = np.interp(time, old_time, data_oc[3])
		y_oc_1 = np.interp(time, old_time, data_oc[4])		
		th_oc_1 = np.interp(time, old_time, data_oc[5])		

		for i in range(length):
			if i%50 == 0:
				if data_human_1[ori]['nb'] > 20:
					plt.arrow(x_oc_1[i], y_oc_1[i],\
						np.cos(th_oc_1[i])*arrow_len,\
						np.sin(th_oc_1[i])*arrow_len, head_width=.02, color = 'blue')
					plt.arrow(data_human_1[ori]['x'][i], data_human_1[ori]['y'][i],\
						np.cos(data_human_1[ori]['Orientation_Globale'][i])*arrow_len,\
						np.sin(data_human_1[ori]['Orientation_Globale'][i])*arrow_len, head_width=.02, color = 'blue')

					plt.arrow(x_oc_2[i], y_oc_2[i],\
						np.cos(th_oc_2[i])*arrow_len,\
						np.sin(th_oc_2[i])*arrow_len, head_width=.02, color = 'red')
					plt.arrow(data_human_2[ori]['x'][i], data_human_2[ori]['y'][i],\
						np.cos(data_human_2[ori]['Orientation_Globale'][i])*arrow_len,\
						np.sin(data_human_2[ori]['Orientation_Globale'][i])*arrow_len, head_width=.02, color = 'red')

				else:
					plt.arrow(x_oc_1[i], y_oc_1[i],\
						np.cos(th_oc_1[i])*arrow_len,\
						np.sin(th_oc_1[i])*arrow_len, head_width=.02, color = 'cyan')
					plt.arrow(data_human_1[ori]['x'][i], data_human_1[ori]['y'][i],\
						np.cos(data_human_1[ori]['Orientation_Globale'][i])*arrow_len,\
						np.sin(data_human_1[ori]['Orientation_Globale'][i])*arrow_len, head_width=.02, color = 'cyan')

					plt.arrow(x_oc_2[i], y_oc_2[i],\
						np.cos(th_oc_2[i])*arrow_len,\
						np.sin(th_oc_2[i])*arrow_len, head_width=.02, color = 'orange')
					plt.arrow(data_human_2[ori]['x'][i], data_human_2[ori]['y'][i],\
						np.cos(data_human_2[ori]['Orientation_Globale'][i])*arrow_len,\
						np.sin(data_human_2[ori]['Orientation_Globale'][i])*arrow_len, head_width=.02, color = 'orange')

		if data_human_1[ori]['nb'] > 20:
			plt.plot(x_oc_1,y_oc_1,color = 'blue')#,label = 'OC Subject 1 - Configuration 1')
			plt.plot(data_human_1[ori]['x'],data_human_1[ori]['y'],color = 'blue', linestyle = 'dotted')#,label = 'Average Subject 1 - Configuration 1')	
			plt.plot(x_oc_2,y_oc_2,color = 'red')#,label = 'OC Subject 2 - Configuration 1')
			plt.plot(data_human_2[ori]['x'],data_human_2[ori]['y'],color = 'red', linestyle = 'dotted')#,label = 'Average Subject 2 - Configuration 1')
		else:
			two_ori = True
			plt.plot(x_oc_1,y_oc_1,color = 'cyan')#,label = 'OC Subject 1 - Configuration 2')
			plt.plot(data_human_1[ori]['x'],data_human_1[ori]['y'],color = 'cyan', linestyle = 'dotted')#,label = 'Average Subject 1 - Configuration 2')	
			plt.plot(x_oc_2,y_oc_2,color = 'orange')#,label = 'OC Subject 2 - Configuration 2')
			plt.plot(data_human_2[ori]['x'],data_human_2[ori]['y'],color = 'orange', linestyle = 'dotted')#,label = 'Average Subject 2 - Configuration 2')

		plt.ylabel("y (m)")
		plt.xlabel("x (m)")

	line = mlines.Line2D([], [], color='black', label='Generated trajectory')
	dotted_line = mlines.Line2D([], [], color='black', linestyle = 'dotted', label='Average trajectory')			
	blue_patch = mpatches.Patch(color='blue', label='Subject 1 - Config. 1')			
	red_patch = mpatches.Patch(color='red', label='Subject 2 - Config. 1')
	if two_ori and legend:
		cyan_patch = mpatches.Patch(color='cyan', label='Subject 1 - Config. 2')			
		orange_patch = mpatches.Patch(color='orange', label='Subject 2 - Config. 2')
		plt.legend(handles=[line,dotted_line,blue_patch,red_patch,cyan_patch,orange_patch])
	elif not two_ori and legend:
		plt.legend(handles=[line,dotted_line,blue_patch,red_patch])

	count += 1
plt.show()