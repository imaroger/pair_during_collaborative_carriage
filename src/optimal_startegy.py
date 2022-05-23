import numpy as np
import matplotlib.pylab as plt
from math import pi,floor,atan2,atan, nan, sqrt
import json
from scipy.interpolate import splprep, splev, interp1d
from scipy import stats


#######################################################
############ Optimal choice of trajectory #############
#######################################################

def is_optimal(dist,dist_pos1,dist_pos2):
	if abs(dist_pos1-dist) < abs(dist_pos2-dist)\
	and min(dist_pos1,dist_pos2) == dist_pos1: #pos 1 chosen et pos 1 optim
		return True,'pos 1'
	if abs(dist_pos1-dist) > abs(dist_pos2-dist)\
	and min(dist_pos1,dist_pos2) == dist_pos1: #pos 2 chosen et pos 1 optim			
		return False,'pos 2'	
	if abs(dist_pos1-dist) > abs(dist_pos2-dist)\
	and min(dist_pos1,dist_pos2) == dist_pos2: #pos 2 chosen et pos 2 optim	
		return True,'pos 2'
	if abs(dist_pos1-dist) < abs(dist_pos2-dist)\
	and min(dist_pos1,dist_pos2) == dist_pos2: #pos 1 chosen et pos 2 optim
		return False,'pos 1'	
	if dist_pos1 == dist_pos2:
		return True,'pos 1'

def is_optimal_for_pair(pos1, dist_pos1, dist_pos2):
	if min(dist_pos1,dist_pos2) == dist_pos1 and pos1 == 'pos 1': # pos 1 is opt for sub 1
		return True
	if min(dist_pos1,dist_pos2) == dist_pos1 and pos1 == 'pos 2':
		return False
	if min(dist_pos1,dist_pos2) == dist_pos2 and pos1 == 'pos 2':
		return True
	if min(dist_pos1,dist_pos2) == dist_pos2 and pos1 == 'pos 1':
		return False
	if dist_pos1 == dist_pos2:
		return True

path = 'Data/Human/'
list_targets = ['d1_p4_jaune_1', 'd1_p4_gris_1', 'd1_p5_jaune_1', 'd1_p5_gris_1', 'd1_p6_jaune_1', 'd1_p6_gris_1', 'd2_p7_jaune_1', 'd2_p7_gris_1', 'd3_p7_gris_1',
				'd1_p4_jaune_2', 'd1_p4_gris_2', 'd1_p5_jaune_2', 'd1_p5_gris_2', 'd1_p6_jaune_2', 'd1_p6_gris_2', 'd2_p7_jaune_2', 'd2_p7_gris_2', 'd3_p7_gris_2']
list_leaders = ['Sujet 1','Sujet 2','Sujet 1 et 2']
list_sub = ['Sujet 1','Sujet 2','Pair']

list_coord_init_go = [(0,0)]*9
list_coord_end_go = [(-3.1,-2.25)]*2+[(-1.5,-2.25)]*2+[(-3,-4.5)]*2+[(0,-4.5),(0,-4.7),(0,-4.5)]
dist_from_table = 0.9
list_coord_init_go_sub1 = [(0,dist_from_table)]*8+[(-dist_from_table,0)]
list_coord_init_go_sub2 = [(0,-dist_from_table)]*8+[(dist_from_table,0)]
dist_from_table = 0.95
list_coord_end_go_pos1 = [(-3.1,-2.25+dist_from_table),(-3.1-dist_from_table,-2.25),\
	(-1.5,-2.25+dist_from_table),(-1.5-dist_from_table,-2.25),(-3,-4.5+dist_from_table),\
	(-3-dist_from_table,-4.5),(0,-4.5+dist_from_table),(-dist_from_table,-4.7),\
	(-dist_from_table,-4.5)]
list_coord_end_go_pos2 = [(-3.1,-2.25-dist_from_table),(-3.1+dist_from_table,-2.25),\
	(-1.5,-2.25-dist_from_table),(-1.5+dist_from_table,-2.25),(-3,-4.5-dist_from_table),\
	(-3+dist_from_table,-4.5),(0,-4.5-dist_from_table),(dist_from_table,-4.7),\
	(dist_from_table,-4.5)]


# list_colors = ['red','orange','green','blue','grey','black','lime','cyan','purple']
# ind = 4
# for i in range(len(list_targets)):
# 	f = open(path+list_targets[i]+'.json')
# 	data = json.load(f)['Trajectoires_Individuelles']
# 	# print(data['Table'][ind]['Binome'],data['Table'][ind]['Leader'])
# 	# print(list_targets[i])
# 	# print("(",data['Table'][ind]['x'][0],",",data['Table'][ind]['y'][0],")")
# 	# print("(",data['Table'][ind]['x'][-1],",",data['Table'][ind]['y'][-1],")")
# 	if list_targets[i][-1] == '1':
# 		plt.plot(data['Table'][ind]['x'],data['Table'][ind]['y'],color = list_colors[i],linewidth = 0.5)
		
# 		plt.plot(data['Sujet 1'][ind]['x'],data['Sujet 1'][ind]['y'],color = list_colors[i])
# 	# else:
# 	# 	plt.plot(data['Table'][ind]['x'],data['Table'][ind]['y'],color = list_colors[i%9],linestyle = 'dotted',linewidth = 0.5)		

# for i in range(len(list_coord_end_go)):
# 	plt.scatter(list_coord_end_go[i][0], list_coord_end_go[i][1],color = 'black',marker = 'x')
# 	plt.scatter(list_coord_init_go[i][0], list_coord_init_go[i][1],color = 'black',marker = 'x')
# 	plt.scatter(list_coord_end_go_pos1[i][0], list_coord_end_go_pos1[i][1],color = 'blue',marker = 'x')
# 	plt.scatter(list_coord_init_go_sub1[i][0], list_coord_init_go_sub1[i][1],color = 'blue',marker = 'x')
# 	plt.scatter(list_coord_end_go_pos2[i][0], list_coord_end_go_pos2[i][1],color = 'red',marker = 'x')
# 	plt.scatter(list_coord_init_go_sub2[i][0], list_coord_init_go_sub2[i][1],color = 'red',marker = 'x')
# plt.show()

end_go = {}

for i in range(9):
	# print(list_targets[i])
	traj = list_targets[i]
	f = open(path+traj+'.json')
	data = json.load(f)['Trajectoires_Individuelles']
	end_go[traj] = {}
	# init_go[traj] = {}
	for sub in list_sub[:2]:
		end_go[traj][sub] = {}
		# init_go[traj][sub] = {}
		for leader in list_leaders:
			end_go[traj][sub][leader] = {}		
			end_go[traj][sub][leader]['x'] = []
			end_go[traj][sub][leader]['y'] = []
			# init_go[traj][sub][leader] = {}		
			# init_go[traj][sub][leader]['x'] = []
			# init_go[traj][sub][leader]['y'] = []
		for i in range(len(data[sub])):
			end_go[traj][sub][data[sub][i]['Leader']]['x'].append(data[sub][i]['x'][-1])
			end_go[traj][sub][data[sub][i]['Leader']]['y'].append(data[sub][i]['y'][-1])
			# init_go[traj][sub][data[sub][i]['Leader']]['x'].append(data[sub][i]['x'][0])
			# init_go[traj][sub][data[sub][i]['Leader']]['y'].append(data[sub][i]['y'][0])

# plt.scatter(end_go['Table']['Sujet 1']['x'],end_go['Table']['Sujet 1']['y'],marker='o')
# plt.scatter(end_go['Sujet 1']['Sujet 1']['x'],end_go['Sujet 1']['Sujet 1']['y'],marker='o')
# plt.scatter(end_go['Sujet 2']['Sujet 1']['x'],end_go['Sujet 2']['Sujet 1']['y'],marker='o')
# plt.show()

dist_sub1_pos1,dist_sub1_pos2,dist_sub2_pos1,dist_sub2_pos2 = [],[],[],[]
dist_pair_sub1_pos1,dist_pair_sub1_pos2 = [],[]

for i in range(len(list_coord_init_go_sub1)):
	dist_sub1_pos1.append(sqrt((list_coord_init_go_sub1[i][0]-\
		list_coord_end_go_pos1[i][0])**2+(list_coord_init_go_sub1[i][1]-\
		list_coord_end_go_pos1[i][1])**2))
	dist_sub1_pos2.append(sqrt((list_coord_init_go_sub1[i][0]-\
		list_coord_end_go_pos2[i][0])**2+(list_coord_init_go_sub1[i][1]-\
		list_coord_end_go_pos2[i][1])**2))		
	dist_sub2_pos1.append(sqrt((list_coord_init_go_sub2[i][0]-\
		list_coord_end_go_pos1[i][0])**2+(list_coord_init_go_sub2[i][1]-\
		list_coord_end_go_pos1[i][1])**2))	
	dist_sub2_pos2.append(sqrt((list_coord_init_go_sub2[i][0]-\
		list_coord_end_go_pos2[i][0])**2+(list_coord_init_go_sub2[i][1]-\
		list_coord_end_go_pos2[i][1])**2))
	dist_pair_sub1_pos1.append(dist_sub1_pos1[-1]+dist_sub2_pos2[-1])
	dist_pair_sub1_pos2.append(dist_sub1_pos2[-1]+dist_sub2_pos1[-1])	

# print(dist_sub1_pos1)
# print(dist_sub1_pos2)
# print(dist_sub2_pos1)
# print(dist_sub2_pos2)
# print(dist_pair_sub1_pos1)
# print(dist_pair_sub1_pos2)

optim = {}
for sub in list_sub:
	optim[sub] = {}
	for leader in list_leaders:
		optim[sub][leader] = {} 		
		optim[sub][leader]["Optimal"] = 0
		optim[sub][leader]["Not optimal"] = 0
for i in range(9):	
	traj = list_targets[i]
	# print(traj)
	for leader in list_leaders:
		# nb = 0
		end1 = end_go[traj]["Sujet 1"][leader]
		end2 = end_go[traj]["Sujet 2"][leader]
		init1 = list_coord_init_go_sub1
		init2 = list_coord_init_go_sub2				
		for j in range(len(end1['x'])):
			dist1 = sqrt((end1['x'][j]-init1[i][0])**2+(end1['y'][j]-init1[i][1])**2)
			dist2 = sqrt((end2['x'][j]-init2[i][0])**2+(end2['y'][j]-init2[i][1])**2)

			opt1,pos1 = is_optimal(dist1, dist_sub1_pos1[i], dist_sub1_pos2[i])
			opt2,pos2 = is_optimal(dist2, dist_sub2_pos1[i], dist_sub2_pos2[i])	

						
			opt_pair = is_optimal_for_pair(pos1, dist_pair_sub1_pos1[i], dist_pair_sub1_pos2[i])

			if opt1:
				optim["Sujet 1"][leader]["Optimal"] += 1
			else:
				optim["Sujet 1"][leader]["Not optimal"] += 1	
			if opt2:
				optim["Sujet 2"][leader]["Optimal"] += 1
			else:
				optim["Sujet 2"][leader]["Not optimal"] += 1					
			if opt_pair:
				optim["Pair"][leader]["Optimal"] += 1
			else:
				optim["Pair"][leader]["Not optimal"] += 1
print(optim)

count = 1
for sub in optim:
	for leader in optim[sub]:
		plt.subplot(3,3,count)
		nb = [optim[sub][leader]['Optimal'],optim[sub][leader]['Not optimal']]
		labels = ["True","False"]
		colors = ['#2ca02c','red']
		plt.pie(nb, labels=labels, autopct='%1.1f%%',colors=colors, startangle=90)
		if sub == 'Sujet 1' or sub == 'Sujet 2':
			if leader == "Sujet 1":
				leader = "Scenario 1"
			if leader == "Sujet 2":
				leader = "Scenario 2"
			if leader == "Sujet 1 et 2":
				leader = "Scenario 3"				
			plt.title("Is the configuration optimal for Subject "+sub[-1]+" ? \n ("+leader+")")
		else:
			if leader == "Sujet 1":
				leader = "Scenario 1"
			if leader == "Sujet 2":
				leader = "Scenario 2"
			if leader == "Sujet 1 et 2":
				leader = "Scenario 3"				
			plt.title("Is the configuration optimal for the pair ? \n ("+leader+")")

		count += 1
plt.show()

