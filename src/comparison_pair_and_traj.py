import numpy as np
import matplotlib.pylab as plt
from math import pi,floor,atan2,atan, nan, sqrt
import json
from scipy.interpolate import splprep, splev, interp1d
from scipy import stats
import matplotlib.patches as mpatches
import matplotlib.markers as mmarkers

plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['ps.fonttype'] = 42

path = 'Data/Human/'
list_targets = ['d1_p4_jaune_1', 'd1_p4_gris_1', 'd1_p5_jaune_1', 'd1_p5_gris_1', 'd1_p6_jaune_1', 'd1_p6_gris_1', 'd2_p7_jaune_1', 'd2_p7_gris_1', 'd3_p7_gris_1',
				'd1_p4_jaune_2', 'd1_p4_gris_2', 'd1_p5_jaune_2', 'd1_p5_gris_2', 'd1_p6_jaune_2', 'd1_p6_gris_2', 'd2_p7_jaune_2', 'd2_p7_gris_2', 'd3_p7_gris_2']
list_leaders = ['Sujet 1','Sujet 2','Sujet 1 et 2']
list_sub = ['Sujet 1','Sujet 2','Table']
list_pair = ['Sujet1_Aurélie&Sujet2_Stanislas', 'Sujet1_Rémy&Sujet2_Margaux', 'Sujet1_Zaki&Sujet2_Yanis', 'Sujet1_Thanh&Sujet2_Diane', 'Sujet1_Sabrina&Sujet2_Quentin', 'Sujet1_Aniss&Sujet2_Louise', 'Sujet1_Hugo&Sujet2_Alexandre', 'Sujet1_Alexia&Sujet2_Bénédicte', 'Sujet1_Adénikè&Sujet2_Médéric', 'Sujet1_Anaïs&Sujet2_Mariem', 'Sujet1_Stéphane&Sujet2_Angélique', 'Sujet1_Fanny&Sujet2_William', 'Sujet1_Romane&Sujet2_Corentin', 'Sujet1_Paul&Sujet2_Mathieu', 'Sujet1_Marine&Sujet2_Hélène', 'Sujet1_Sébastien&Sujet2_Nils', 'Sujet1_Antoine&Sujet2_Médéric_LAAS', 'Sujet1_Amaury&Sujet2_Jason', 'Sujet1_Guilhem&Sujet2_César', 'Sujet1_Alexis&Sujet2_Thibaud']

list_coord_end_go = [(-3.1,-2.25)]*2+[(-1.5,-2.25)]*2+[(-3,-4.5)]*2+[(0,-4.5),(0,-4.7),(0,-4.5)]
dist_from_target = []
for init in list_coord_end_go:
	dist_from_target.append(sqrt(init[0]**2+init[1]**2))
dist_from_target *= 2 
print(dist_from_target)


def detect_discontinuity(theta):
	discontinuted_th = []
	ind_discontinuity = [0]
	for i in range (len(theta)-1):
		if abs(theta[i+1]-theta[i]) > 0.5:		
			ind_discontinuity.append(i+1)
			discontinuted_th.append(np.array(theta[ind_discontinuity[-2]:ind_discontinuity[-1]]))
			# print(i+1)
	if len(discontinuted_th) != 0:
		discontinuted_th.append(theta[ind_discontinuity[-1]:])
		for i in range(1,len(discontinuted_th)):
			discontinuted_th[i] += (discontinuted_th[i-1][-1]-discontinuted_th[i][0])
			if len(discontinuted_th[i]) > 1 :
				if np.abs(discontinuted_th[i][0]-discontinuted_th[i][1]) > 0.5:
					discontinuted_th[i][1:] += (discontinuted_th[i][0]-discontinuted_th[i][1])
		new_theta = np.concatenate(discontinuted_th)
		return new_theta
	else:
		return theta

def normalizeAngle(angle): 
	new_angle = angle
	while new_angle > pi:
		new_angle -= 2*pi
	while new_angle < -pi:
		new_angle += 2*pi
	return new_angle

def linearDistance(data1,data2):
	dist_lin = 0
	# print("-------")
	length = len(data1['x'])
	tck1, u1 = splprep([data1['x'], data1['y']], s = 0)
	tck2, u2 = splprep([data2['x'], data2['y']], s = 0)
	xnew = np.linspace(0, 1, length)
	x, y = splev(xnew, tck1)
	xm, ym = splev(xnew, tck2)	

	for i in range(length):
		# print(i,sqrt((data1['x'][i]-data2['x'][i])**2+(data1['y'][i]-data2['y'][i])**2))
		# if i%25 == 0:
		# 	plt.plot([x[i],xm[i]], [y[i],ym[i]], color = 'red', linewidth = 0.5)		
		dist_lin += sqrt((x[i]-xm[i])**2+(y[i]-ym[i])**2)
	# if dist_lin/length > 1:
	# 	plt.plot(data1['x'],data1['y'])
	# 	plt.plot(data2['x'],data2['y'])	
	# 	plt.show()
	return dist_lin/length

def angularDistance(data1,data2):
	th1,th2 = [normalizeAngle(th) for th in data1['Orientation_Globale']],[normalizeAngle(th) for th in data2['Orientation_Globale']]
	th1,th2 = detect_discontinuity(th1),detect_discontinuity(th2)
	if abs(th1[0]-th2[0]) > 2*pi-1\
		and abs(th2[0]-pi) <= pi/2:
		th1 = np.array(th1)		
		th1 += 2*pi
	if abs(th1[0]-th2[0]) > 2*pi-1\
		and abs(th2[0]-pi) > pi/2:	
		th1 = np.array(th1)		
		th1 -= 2*pi	
	length = len(th1)	
	dist = 0
	for i in range(length):
		dist += abs(th1[i]-th2[i])
	# if dist/length > 0.9:
	# 	arrow_len = 0.1
		# print(th1[0],th1[-1])
		# print(th2[0],th2[-1])
		# print(dist/length)
		# plt.subplot(1,2,1)
		# plt.plot(data1['x'],data1['y'],color = 'red')
		# plt.plot(data2['x'],data2['y'],color = 'blue')	
		# for i in range(len(data1['x'])):
		# 	if i%10 == 0:
		# 		plt.arrow(data1['x'][i], data1['y'][i], \
		# 		np.cos(data1['Orientation_Globale'][i])*arrow_len,\
		# 		np.sin(data1['Orientation_Globale'][i])*arrow_len, head_width=.02, color = 'red')
		# 		plt.arrow(data2['x'][i], data2['y'][i], \
		# 		np.cos(data2['Orientation_Globale'][i])*arrow_len,\
		# 		np.sin(data2['Orientation_Globale'][i])*arrow_len, head_width=.02, color = 'blue')
		# plt.subplot(1,2,2)
		# time = np.linspace(1,100,len(th2))
		# plt.plot(time,th2,color = 'blue')		
		# plt.plot(time,th1,color = 'red')
		# plt.plot(time,data2['Orientation_Globale'],color = 'blue',linestyle = 'dotted')		
		# plt.plot(time,data1['Orientation_Globale'],color = 'red',linestyle = 'dotted')		
		# plt.show()
	return dist/length

traj_to_compare = {}
for sub in list_sub:
	traj_to_compare[sub] = {}
	for traj in list_targets:
		traj_to_compare[sub][traj] = {}
		if traj[-1] == '1':		
			for leader in list_leaders:
				traj_to_compare[sub][traj][leader] = {}
				traj_to_compare[sub][traj][leader][pi] = []
				traj_to_compare[sub][traj][leader][0] = []	
				traj_to_compare[sub][traj][leader][pi/2] = []
				traj_to_compare[sub][traj][leader][-pi/2] = []											
		else:
			traj_to_compare[sub][traj]['All data'] = {}
			traj_to_compare[sub][traj]['All data'][pi] = []
			traj_to_compare[sub][traj]['All data'][0] = []	
			traj_to_compare[sub][traj]['All data'][pi/2] = []
			traj_to_compare[sub][traj]['All data'][-pi/2] = []					

for file in list_targets:
	print("### ", file," ###")
	f = open(path+file+'.json')
	data = json.load(f)['Trajectoires_Individuelles']

	for sub in data:
		for i in range(len(data[sub])):
			if file[-1] == '1':
				ori = data["Table"][i]["Orientation_End_Theorique"]
				traj_to_compare[sub][file][data[sub][i]["Leader"]][ori].append(i)
			else:
				ori = data["Table"][i]["Orientation_Init_Theorique"]
				if data["Table"][i]["Orientation_End_Theorique"] == pi or\
					data["Table"][i]["Orientation_End_Theorique"] == pi/2:		
					traj_to_compare[sub][file]["All data"][ori].append(i)
				else:
					print("wrong trajectory : ",file,sub,leader,data[sub][i]["Binome"])
		# print(sub,len(traj_to_compare[sub][file]["Sujet 1 et 2"][pi]),len(traj_to_compare[sub][file]["Sujet 1 et 2"][pi/2]),len(traj_to_compare[sub][file]["Sujet 1 et 2"][-pi/2]),len(traj_to_compare[sub][file]["Sujet 1 et 2"][0]))

####################################COMPUTEDIST####################################

dist_wrt_traj = {}
dist_wrt_pair = {}
dist_for_all_traj = {}
ang_dist_for_all_traj = {}
for sub in list_sub:
	dist_wrt_traj[sub] = {}
	dist_wrt_pair[sub] = {}
	dist_for_all_traj[sub] = {}	
	ang_dist_for_all_traj[sub] = {}
	for traj in list_targets:
		dist_wrt_traj[sub][traj] = {}		
		if traj[-1] == '1':		
			for leader in list_leaders:
				dist_wrt_traj[sub][traj][leader] = []
		dist_wrt_traj[sub][traj]["All data"] = []
	for leader in list_leaders:
		if leader == "Sujet 1 et 2":
			dist_for_all_traj[sub][leader] = []	
			dist_for_all_traj[sub][leader + " (Return)"] = []	
			ang_dist_for_all_traj[sub][leader] = []	
			ang_dist_for_all_traj[sub][leader + " (Return)"] = []	
		else:
			dist_for_all_traj[sub][leader] = []
			ang_dist_for_all_traj[sub][leader] = []			
	for pair in list_pair:
		dist_wrt_pair[sub][pair] = [] # leader = "Sujet 1 et 2" for all


for file in list_targets:
	print("### ", file," ###")
	f = open(path+file+'.json')
	data = json.load(f)['Trajectoires_Individuelles']
	f_m = open(path+file+'_mean.json')
	data_mean = json.load(f_m)['Trajectoires_Moyennes']

	for sub in data_mean:
		for leader in traj_to_compare[sub][file]:
			for ori_str in data_mean[sub][leader]:
				if file[-1] == '1':
					ori = float(ori_str[23:])
				else:
					ori = float(ori_str[24:])
				length = len(traj_to_compare[sub][file][leader][ori])
				# print(sub,leader,length,data_mean[sub][leader][ori_str]["nb"])
				if length > 2:
					# print(sub,leader,length)
					for ind in traj_to_compare[sub][file][leader][ori]:
						dist = linearDistance(data_mean[sub][leader][ori_str], data[sub][ind])
						ang_dist = angularDistance(data_mean[sub][leader][ori_str], data[sub][ind])
						dist_wrt_traj[sub][file][leader].append(dist)
						if leader == "Sujet 1 et 2" or leader == "All data":
							dist_wrt_pair[sub][data[sub][ind]["Binome"]].append(dist)
						if file[-1] == '1':
							dist_for_all_traj[sub][leader].append(dist)
							ang_dist_for_all_traj[sub][leader].append(ang_dist)
							dist_wrt_traj[sub][file]["All data"].append(dist)
						else:
							dist_for_all_traj[sub]["Sujet 1 et 2 (Return)"].append(dist)			
							ang_dist_for_all_traj[sub]["Sujet 1 et 2 (Return)"].append(ang_dist)			
				
				# print(len(dist_wrt_traj[sub][file]["All data"]))

print("### Linear Distance : Mean +- std ###")
for sub in dist_for_all_traj:
	print("--- Subject : ",sub,' ---')
	print("Scenario 1 : ", np.mean(dist_for_all_traj[sub]["Sujet 1"])," +- ",\
		np.std(dist_for_all_traj[sub]["Sujet 1"]))
	print("Scenario 2 : ", np.mean(dist_for_all_traj[sub]["Sujet 2"])," +- ",\
		np.std(dist_for_all_traj[sub]["Sujet 2"]))	
	print("Scenario 3 : ", np.mean(dist_for_all_traj[sub]["Sujet 1 et 2"])," +- ",\
		np.std(dist_for_all_traj[sub]["Sujet 1 et 2"]))
	print("Scenario 3 (Return) : ", np.mean(dist_for_all_traj[sub]["Sujet 1 et 2 (Return)"])," +- ",\
		np.std(dist_for_all_traj[sub]["Sujet 1 et 2 (Return)"]))
	print("Maximum (All Scenarios) : ", max(\
		np.max(dist_for_all_traj[sub]["Sujet 1"]),\
		np.max(dist_for_all_traj[sub]["Sujet 2"]),\
		np.max(dist_for_all_traj[sub]["Sujet 1 et 2"])))

print("### Angular Distance : Mean +- std ###")
for sub in dist_for_all_traj:
	print("--- Subject : ",sub,' ---')
	print("Scenario 1 : ", np.mean(ang_dist_for_all_traj[sub]["Sujet 1"])," +- ",\
		np.std(ang_dist_for_all_traj[sub]["Sujet 1"]))
	print("Scenario 2 : ", np.mean(ang_dist_for_all_traj[sub]["Sujet 2"])," +- ",\
		np.std(ang_dist_for_all_traj[sub]["Sujet 2"]))	
	print("Scenario 3 : ", np.mean(ang_dist_for_all_traj[sub]["Sujet 1 et 2"])," +- ",\
		np.std(ang_dist_for_all_traj[sub]["Sujet 1 et 2"]))
	print("Scenario 3 (Return) : ", np.mean(ang_dist_for_all_traj[sub]["Sujet 1 et 2 (Return)"])," +- ",\
		np.std(ang_dist_for_all_traj[sub]["Sujet 1 et 2 (Return)"]))
	print("Maximum (All Scenarios) : ", max(\
		np.max(ang_dist_for_all_traj[sub]["Sujet 1"]),\
		np.max(ang_dist_for_all_traj[sub]["Sujet 2"]),\
		np.max(ang_dist_for_all_traj[sub]["Sujet 1 et 2"])))	

#####################################TESTSTAT#####################################

##################################
######### Normality test #########
##################################

print("### Normality test for all : Normal if p > 0.05 ###")
for sub in dist_wrt_pair:
	test = stats.shapiro(dist_for_all_traj[sub]["Sujet 1"])
	print("linear (leader : sub 1) : ",test)
	test = stats.shapiro(dist_for_all_traj[sub]["Sujet 2"])
	print("linear (leader : sub 2) : ",test)
	test = stats.shapiro(dist_for_all_traj[sub]["Sujet 1 et 2"] + dist_for_all_traj[sub]["Sujet 1 et 2 (Return)"])
	print("linear (leader : sub 1 & 2) : ",test)	
	test = stats.shapiro(ang_dist_for_all_traj[sub]["Sujet 1"])
	print("angular (leader : sub 1) : ",test)
	test = stats.shapiro(ang_dist_for_all_traj[sub]["Sujet 2"])
	print("angular (leader : sub 2) : ",test)
	test = stats.shapiro(ang_dist_for_all_traj[sub]["Sujet 1 et 2"] + ang_dist_for_all_traj[sub]["Sujet 1 et 2 (Return)"])
	print("angular (leader : sub 1 & 2) : ",test)	

##################################
#### Kruskal test - Scenarios ####
##################################

print("### kruskal_test for all : Significant difference if p < 0.05 ###")
for sub in dist_wrt_pair:
	kruskal_test = stats.kruskal(dist_for_all_traj[sub]["Sujet 1"],\
		dist_for_all_traj[sub]["Sujet 2"],dist_for_all_traj[sub]["Sujet 1 et 2"],\
		dist_for_all_traj[sub]["Sujet 1 et 2 (Return)"])
	print("linear : ",kruskal_test)
	kruskal_test = stats.kruskal(ang_dist_for_all_traj[sub]["Sujet 1"],\
		ang_dist_for_all_traj[sub]["Sujet 2"],ang_dist_for_all_traj[sub]["Sujet 1 et 2"],\
		ang_dist_for_all_traj[sub]["Sujet 1 et 2 (Return)"])
	print("angular : ",kruskal_test)	

print("### kruskal_test for go/return : Significant difference if p < 0.05 ###")
for sub in dist_wrt_pair:
	kruskal_test = stats.kruskal(dist_for_all_traj[sub]["Sujet 1 et 2"],\
		dist_for_all_traj[sub]["Sujet 1 et 2 (Return)"])
	print("linear : ",kruskal_test)
	kruskal_test = stats.kruskal(ang_dist_for_all_traj[sub]["Sujet 1 et 2"],\
		ang_dist_for_all_traj[sub]["Sujet 1 et 2 (Return)"])
	print("angular : ",kruskal_test)	

#############################
#### Kruskal test - Pair ####
#############################

for sub in dist_wrt_pair:
	kruskal_test = stats.kruskal(dist_wrt_pair[sub][list_pair[0]],\
		dist_wrt_pair[sub][list_pair[1]],dist_wrt_pair[sub][list_pair[2]],\
		dist_wrt_pair[sub][list_pair[3]],dist_wrt_pair[sub][list_pair[4]],\
		dist_wrt_pair[sub][list_pair[5]],dist_wrt_pair[sub][list_pair[6]],\
		dist_wrt_pair[sub][list_pair[7]],dist_wrt_pair[sub][list_pair[8]],\
		dist_wrt_pair[sub][list_pair[9]],dist_wrt_pair[sub][list_pair[10]],\
		dist_wrt_pair[sub][list_pair[11]],dist_wrt_pair[sub][list_pair[12]],\
		dist_wrt_pair[sub][list_pair[13]],dist_wrt_pair[sub][list_pair[14]],\
		dist_wrt_pair[sub][list_pair[15]],dist_wrt_pair[sub][list_pair[16]],\
		dist_wrt_pair[sub][list_pair[17]],dist_wrt_pair[sub][list_pair[18]],\
		dist_wrt_pair[sub][list_pair[19]])
	print(sub,kruskal_test)

# file = 'd1_p6_jaune_1'
# print("### ", file," ###")
# f = open(path+file+'.json')
# data = json.load(f)['Trajectoires_Individuelles']
# sub = 'Table' # same list of ind for all sub
# # for leader in traj_to_compare[sub][file]:
# leader = 'Sujet 1 et 2'
# for ori in traj_to_compare[sub][file][leader]:
# 	if len(traj_to_compare[sub][file][leader][ori]) > 2:
# 		ind = traj_to_compare[sub][file][leader][ori]

# for sub in traj_to_compare:
# 	# plt.plot(np.linspace(0,1,500),np.array(data[sub][ind[0]]['x'])+np.array(data[sub][ind[0]]['y']))
# 	# plt.plot(np.linspace(0,1,500),np.array(data[sub][ind[1]]['x'])+np.array(data[sub][ind[1]]['y']))
# 	# plt.plot(np.linspace(0,1,500),np.array(data[sub][ind[2]]['x'])+np.array(data[sub][ind[2]]['y']))
# 	# plt.plot(np.linspace(0,1,500),np.array(data[sub][ind[3]]['x'])+np.array(data[sub][ind[3]]['y']))
	
# 	# plt.show()
# 	kruskal_test = stats.kruskal(np.array(data[sub][ind[0]]['x'])+np.array(data[sub][ind[0]]['y']),\
# 		np.array(data[sub][ind[1]]['x'])+np.array(data[sub][ind[1]]['y']),\
# 		np.array(data[sub][ind[2]]['x'])+np.array(data[sub][ind[2]]['y']),\
# 		np.array(data[sub][ind[3]]['x'])+np.array(data[sub][ind[3]]['y']),\
# 		np.array(data[sub][ind[4]]['x'])+np.array(data[sub][ind[4]]['y']),\
# 		np.array(data[sub][ind[5]]['x'])+np.array(data[sub][ind[5]]['y']),\
# 		np.array(data[sub][ind[6]]['x'])+np.array(data[sub][ind[6]]['y']),\
# 		np.array(data[sub][ind[7]]['x'])+np.array(data[sub][ind[7]]['y']),\
# 		np.array(data[sub][ind[8]]['x'])+np.array(data[sub][ind[8]]['y']),\
# 		np.array(data[sub][ind[9]]['x'])+np.array(data[sub][ind[9]]['y']),\
# 		np.array(data[sub][ind[10]]['x'])+np.array(data[sub][ind[10]]['y']),\
# 		np.array(data[sub][ind[11]]['x'])+np.array(data[sub][ind[11]]['y']),\
# 		np.array(data[sub][ind[12]]['x'])+np.array(data[sub][ind[12]]['y']),\
# 		np.array(data[sub][ind[13]]['x'])+np.array(data[sub][ind[13]]['y']),\
# 		np.array(data[sub][ind[14]]['x'])+np.array(data[sub][ind[14]]['y']),\
# 		np.array(data[sub][ind[15]]['x'])+np.array(data[sub][ind[15]]['y']),\
# 		np.array(data[sub][ind[16]]['x'])+np.array(data[sub][ind[16]]['y']),\
# 		np.array(data[sub][ind[17]]['x'])+np.array(data[sub][ind[17]]['y']),\
# 		np.array(data[sub][ind[18]]['x'])+np.array(data[sub][ind[18]]['y']),\
# 		np.array(data[sub][ind[19]]['x'])+np.array(data[sub][ind[19]]['y']))
# 	print(sub,kruskal_test)


#####################################BOXPLOTS#####################################

#######################################
######### Box plot for all Traj #######
#######################################

# ind = 0
# axs = ['ax1','ax2','ax3']
# fig,axs = plt.subplots(1,3)
# for sub in dist_for_all_traj: 
# 	axs[ind].boxplot([dist_for_all_traj[sub]["Sujet 1"],\
# 	dist_for_all_traj[sub]["Sujet 2"],\
# 	dist_for_all_traj[sub]["Sujet 1 et 2"],\
# 	dist_for_all_traj[sub]["Sujet 1 et 2 (Return)"]])
# 	axs[ind].set_ylabel("Linear distance (m)")
# 	axs[ind].set_xticklabels(['Scenario 1', 'Scenario 2', 'Scenario 3\n(Forward)', 'Scenario 3\n(Return)'])
# 	axs[ind].set_ylim(0, 1.)
# 	axs[ind].set_title(sub)
# 	ind += 1
# plt.show()

# ind = 0
# axs = ['ax1','ax2','ax3']
# fig,axs = plt.subplots(1,3)
# for sub in ang_dist_for_all_traj: 
# 	axs[ind].boxplot([ang_dist_for_all_traj[sub]["Sujet 1"],\
# 	ang_dist_for_all_traj[sub]["Sujet 2"],\
# 	ang_dist_for_all_traj[sub]["Sujet 1 et 2"],\
# 	ang_dist_for_all_traj[sub]["Sujet 1 et 2 (Return)"]])
# 	axs[ind].set_ylabel("Angular distance (rad)")
# 	axs[ind].set_xticklabels(['Scenario 1', 'Scenario 2', 'Scenario 3\n(Forward)', 'Scenario 3\n(Return)'])
# 	axs[ind].set_ylim(0, 1.2)
# 	axs[ind].set_title(sub)
# 	ind += 1
# plt.show()

#######################################
#### Box plot with respect to Pair ####
#######################################

# pairs = []
# for i in range (1,21):
# 	pairs.append('Pair '+str(i))

# ind = 0
# axs = ['ax1','ax2','ax3']
# fig,axs = plt.subplots(3)
# for sub in dist_for_all_traj: 
# 	axs[ind].boxplot([dist_wrt_pair[sub][list_pair[0]],\
# 		dist_wrt_pair[sub][list_pair[1]],dist_wrt_pair[sub][list_pair[2]],\
# 		dist_wrt_pair[sub][list_pair[3]],dist_wrt_pair[sub][list_pair[4]],\
# 		dist_wrt_pair[sub][list_pair[5]],dist_wrt_pair[sub][list_pair[6]],\
# 		dist_wrt_pair[sub][list_pair[7]],dist_wrt_pair[sub][list_pair[8]],\
# 		dist_wrt_pair[sub][list_pair[9]],dist_wrt_pair[sub][list_pair[10]],\
# 		dist_wrt_pair[sub][list_pair[11]],dist_wrt_pair[sub][list_pair[12]],\
# 		dist_wrt_pair[sub][list_pair[13]],dist_wrt_pair[sub][list_pair[14]],\
# 		dist_wrt_pair[sub][list_pair[15]],dist_wrt_pair[sub][list_pair[16]],\
# 		dist_wrt_pair[sub][list_pair[17]],dist_wrt_pair[sub][list_pair[18]],\
# 		dist_wrt_pair[sub][list_pair[19]]])
# 	axs[ind].set_ylabel("Linear distance (m)")
# 	axs[ind].set_xticklabels(pairs)
# 	axs[ind].set_ylim(0, 1.)
# 	if sub == "Sujet 1":
# 		axs[ind].set_title("Subject 1")
# 	elif sub == "Sujet 2":
# 		axs[ind].set_title("Subject 2")	
# 	else:
# 		axs[ind].set_title(sub)				
# 	ind += 1
# plt.show()

#######################################
#### Box plot with respect to Traj ####
#######################################

# goals = ['Goal 7','Goal 8','Goal 5','Goal 6','Goal 3','Goal 4',\
# 	'Goal 1', 'Goal 2', 'Goal 9','Goal 7\n(Return)','Goal 8\n(Return)',\
# 	'Goal 5\n(Return)','Goal 6\n(Return)','Goal 3\n(Return)','Goal 4\n(Return)',\
# 	'Goal 1\n(Return)', 'Goal 2\n(Return)', 'Goal 9\n(Return)']
# print(goals[0],list_targets[0])
# ind = 0
# axs = ['ax1','ax2','ax3']
# fig,axs = plt.subplots(3)
# for sub in dist_for_all_traj: 
# 	axs[ind].boxplot([dist_wrt_traj[sub][list_targets[0]]["Sujet 1 et 2"],\
# 		dist_wrt_traj[sub][list_targets[1]]["Sujet 1 et 2"],\
# 		dist_wrt_traj[sub][list_targets[2]]["Sujet 1 et 2"],\
# 		dist_wrt_traj[sub][list_targets[3]]["Sujet 1 et 2"],\
# 		dist_wrt_traj[sub][list_targets[4]]["Sujet 1 et 2"],\
# 		dist_wrt_traj[sub][list_targets[5]]["Sujet 1 et 2"],\
# 		dist_wrt_traj[sub][list_targets[6]]["Sujet 1 et 2"],\
# 		dist_wrt_traj[sub][list_targets[7]]["Sujet 1 et 2"],\
# 		dist_wrt_traj[sub][list_targets[8]]["Sujet 1 et 2"],\
# 		dist_wrt_traj[sub][list_targets[9]]["All data"],\
# 		dist_wrt_traj[sub][list_targets[10]]["All data"],\
# 		dist_wrt_traj[sub][list_targets[11]]["All data"],\
# 		dist_wrt_traj[sub][list_targets[12]]["All data"],\
# 		dist_wrt_traj[sub][list_targets[13]]["All data"],\
# 		dist_wrt_traj[sub][list_targets[14]]["All data"],\
# 		dist_wrt_traj[sub][list_targets[15]]["All data"],\
# 		dist_wrt_traj[sub][list_targets[16]]["All data"],\
# 		dist_wrt_traj[sub][list_targets[17]]["All data"]])
# 	axs[ind].set_ylabel("Linear distance (m)")
# 	axs[ind].set_xticklabels(goals)
# 	axs[ind].set_ylim(0, 1.)
# 	if sub == "Sujet 1":
# 		axs[ind].set_title("Subject 1")
# 	elif sub == "Sujet 2":
# 		axs[ind].set_title("Subject 2")	
# 	else:
# 		axs[ind].set_title(sub)				
# 	ind += 1
# plt.show()

#################################################
#### Plot with respect to distance to target ####
#################################################

# count = 0
# axs = ['ax1','ax2','ax3']
# fig, axs = plt.subplots(1,3)
# for sub in dist_wrt_traj: 
# 	l = [True]*4
# 	ax = axs[count]
# 	plt.title(sub)
# 	for i in range(len(list_targets)):
# 		if list_targets[i][-1] == '1':
# 			for leader in list_leaders:
# 				label = None
# 				# print(sub,leader,list_targets[i])
# 				if leader == "Sujet 1":
# 					color= "red"
# 					if l[0]:
# 						label = "Scenario 1"
# 						l[0] = False
# 				if leader == "Sujet 2":
# 					color = "blue"
# 					if l[1]:
# 						label = "Scenario 2"
# 						l[1] = False
# 				if leader == "Sujet 1 et 2":
# 					color = "green"
# 					if l[2]:
# 						label = "Scenario 3 (Go)"
# 						l[2] = False					
# 				if list_targets[i][6] == 'j':
# 					marker = 'o'
# 				else:
# 					marker = 's'
# 				if label != None:
# 					ax.scatter(dist_from_target[i],\
# 						np.mean(dist_wrt_traj[sub][list_targets[i]][leader]),\
# 						color = color,label = label,marker = marker)
# 				else:										
# 					ax.scatter(dist_from_target[i],\
# 						np.mean(dist_wrt_traj[sub][list_targets[i]][leader]),\
# 						color = color,marker = marker)

# 		else:
# 			if list_targets[i][6] == 'j' or list_targets[i][1] == '3':
# 				marker = 'o'
# 			else:
# 				marker = 's'				
# 			color,label = "orange", None
# 			if l[3]:
# 				label = "Scenario 3 (Return)"
# 				l[3] = False
# 			if label != None:	
# 				ax.scatter(dist_from_target[i],np.mean(dist_wrt_traj[sub][list_targets[i]]["All data"]),color = color,label = label,marker = marker)
# 			else:
# 				ax.scatter(dist_from_target[i],np.mean(dist_wrt_traj[sub][list_targets[i]]["All data"]),color = color,marker = marker)
# 	count += 1
# 	ax.legend()
# plt.show()

# count = 0
# axs = ['ax1','ax2','ax3']
# dist = {}
# fig, axs = plt.subplots(1,3)
# for sub in dist_wrt_traj: 
# 	l = ['True']*2
# 	dist[sub] = {}
# 	ax = axs[count]
# 	ax.set_xlabel("Global distance (m)")
# 	ax.set_ylabel("Linear distance (m)")

# 	if sub == "Sujet 1":
# 		ax.set_title("Subject 1")
# 	elif sub == "Sujet 2":
# 		ax.set_title("Subject 2")
# 	else:
# 		ax.set_title(sub)
# 	for i in range(len(list_targets)):				
# 		if list_targets[i][6] == 'j' or list_targets[i][1] == '3':
# 			color = 'blue'
# 			if l[0]:
# 				label = 'No change of orientation'
# 				l[0] = False
# 			else:
# 				label = None
# 		else:
# 			color = 'red'
# 			if l[1]:
# 				label = 'Change of orientation'
# 				l[1] = False
# 			else:
# 				label = None
# 		ax.scatter(dist_from_target[i],\
# 			np.mean(dist_wrt_traj[sub][list_targets[i]]["All data"]),\
# 			color = color,label = label)
# 		ind = np.where(np.array([n for n in dist[sub]]) == dist_from_target[i])[0]
# 		if len(ind) == 0:
# 			dist[sub][dist_from_target[i]] = []
# 		dist[sub][dist_from_target[i]].append(\
# 			np.mean(dist_wrt_traj[sub][list_targets[i]]["All data"]))
# 	count += 1
# 	# ax.legend()	
# print(dist)
# count = 0
# for sub in dist:
# 	l = True
# 	ax = axs[count] 
# 	for dist_target in dist[sub]:
# 		mean = np.mean(dist[sub][dist_target])
# 		std = np.std(dist[sub][dist_target])
# 		if l:
# 			label = 'Mean +- std'
# 			l = False
# 		else:
# 			label = None
# 		ax.scatter(dist_target, mean, color = 'gray',label = label)
# 		ax.errorbar(dist_target, mean, yerr = std, fmt='o', color='gray',\
# 			ecolor='gray', elinewidth=3, capsize=0,alpha = 0.5)
# 	count += 1	

# 	ax.legend()
# plt.show()