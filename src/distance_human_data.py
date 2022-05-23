import numpy as np
import matplotlib.pylab as plt
from math import pi,floor,atan2,atan, nan, sqrt
import json
from scipy.interpolate import splprep, splev, interp1d
from scipy import stats

path = 'Data/Human/'
list_targets = ['d1_p4_jaune_1', 'd1_p4_gris_1', 'd1_p5_jaune_1', 'd1_p5_gris_1', 'd1_p6_jaune_1', 'd1_p6_gris_1', 'd2_p7_jaune_1', 'd2_p7_gris_1', 'd3_p7_gris_1',
				'd1_p4_jaune_2', 'd1_p4_gris_2', 'd1_p5_jaune_2', 'd1_p5_gris_2', 'd1_p6_jaune_2', 'd1_p6_gris_2', 'd2_p7_jaune_2', 'd2_p7_gris_2', 'd3_p7_gris_2']
list_leaders = ['Sujet 1','Sujet 2','Sujet 1 et 2','All data']
list_sub = ['Sujet 1','Sujet 2','Table']

dist_to_mean_lin = {}
dist_to_mean_ang_loc = {}
dist_to_mean_ang_glob = {}
for sub in list_sub:
	dist_to_mean_lin[sub] = {}
	dist_to_mean_ang_loc[sub] = {}
	dist_to_mean_ang_glob[sub] = {}		
	for leader in list_leaders:
		dist_to_mean_lin[sub][leader] = []	
		dist_to_mean_ang_loc[sub][leader] = []	
		dist_to_mean_ang_glob[sub][leader] = []				
# print(dist_to_mean)

def distance(data,data_mean):
	dist_lin,dist_ang_loc,dist_ang_glob = 0,0,0
	# print("-------")
	length = len(data['x'])
	tck1, u1 = splprep([data['x'], data['y']], s = 0)
	tck2, u2 = splprep([data_mean['x'], data_mean['y']], s = 0)
	xnew = np.linspace(0, 1, length)
	x, y = splev(xnew, tck1)
	xm, ym = splev(xnew, tck2)	
	# x,y =data['x'], data['y']
	# xm, ym = data_mean['x'], data_mean['y']

	if abs(data['Orientation_Globale'][0]-data_mean['Orientation_Globale'][0]) > 2*pi-1\
		and abs(data_mean['Orientation_Globale'][0]-pi) <= pi/2:
		data['Orientation_Globale'] = np.array(data['Orientation_Globale'])		
		data['Orientation_Globale'] += 2*pi
	if abs(data['Orientation_Globale'][0]-data_mean['Orientation_Globale'][0]) > 2*pi-1\
		and abs(data_mean['Orientation_Globale'][0]-pi) > pi/2:	
		data['Orientation_Globale'] = np.array(data['Orientation_Globale'])		
		data['Orientation_Globale'] -= 2*pi	

	if abs(data['Orientation_Locale'][0]-data_mean['Orientation_Locale'][0]) > 2*pi-1\
		and abs(data_mean['Orientation_Locale'][0]-pi) <= 2:
		data['Orientation_Locale'] = np.array(data['Orientation_Locale'])		
		data['Orientation_Locale'] += 2*pi
	if abs(data['Orientation_Locale'][0]-data_mean['Orientation_Locale'][0]) > 2*pi-1\
		and abs(data_mean['Orientation_Locale'][0]-pi) > 2:		
		data['Orientation_Locale'] = np.array(data['Orientation_Locale'])		
		data['Orientation_Locale'] -= 2*pi	

	for i in range(length):
		# print(i,sqrt((data['x'][i]-data_mean['x'][i])**2+(data['y'][i]-data_mean['y'][i])**2))
		# if i%25 == 0:
		# 	plt.plot([x[i],xm[i]], [y[i],ym[i]], color = 'red', linewidth = 0.5)
			# plt.plot([data['x'][i],data_mean['x'][i]], [data['y'][i],data_mean['y'][i]], color = 'black', linewidth = 0.5)
			
		dist_lin += sqrt((x[i]-xm[i])**2+(y[i]-ym[i])**2)
		dist_ang_loc += abs(data['Orientation_Locale'][i]-data_mean['Orientation_Locale'][i])
		# if i%25 == 0:
		# 	time = np.linspace(1, 100, length)
		# 	plt.plot([time[i],time[i]], [data['Orientation_Globale'][i],data_mean['Orientation_Globale'][i]], color = 'black', linewidth = 0.5)
		dist_ang_glob += abs(data['Orientation_Globale'][i]-data_mean['Orientation_Globale'][i])

	# plt.plot(data['x'],data['y'])
	# plt.plot(data_mean['x'],data_mean['y'])	
	# plt.show()
	# if dist_lin/length > 1:	
	# 	print("lin",dist_lin/length)
	# 	plt.plot(data['x'],data['y'])
	# 	plt.plot(data_mean['x'],data_mean['y'])	
	# 	plt.show()
	# if dist_ang_loc/length > pi:
	# 	print("ang_loc",dist_ang_loc/length)
	# 	time = np.linspace(1, 100, length)
	# 	plt.plot(time,data['Orientation_Locale'])
	# 	plt.plot(time,data_mean['Orientation_Locale'])	
	# 	plt.show()
	if dist_ang_glob/length > pi:
		print("ang_glob",dist_ang_glob/length)
		time = np.linspace(1, 100, length)
		plt.plot(time,data['Orientation_Globale'])
		plt.plot(time,data_mean['Orientation_Globale'])	
		plt.show()		
	return dist_lin/length,dist_ang_loc/length,dist_ang_glob/length

# for file in list_targets:
# 	f = open(path+file+'.json')
# 	data = json.load(f)['Trajectoires_Individuelles']
# 	f_m = open(path+file+'_mean.json')
# 	data_mean = json.load(f_m)['Trajectoires_Moyennes']

# 	print("###",file)

# 	go = (file[-1] == '1')

# 	if go:
# 		list_ind = {}
# 		for sub in list_sub:
# 			list_ind[sub] = {}		
# 			list_ind[sub]['All data'] = {}			
# 			list_ori_mean_str_all = [ori for ori in data_mean[sub]['All data']]
# 			for ori_str in list_ori_mean_str_all:
# 				list_ind[sub]['All data'][ori_str] = []	
# 			for leader in list_leaders[:3]:
# 				# print("--> ",leader)
# 				list_ind[sub][leader] = {}
# 				list_ori_mean_str = [ori for ori in data_mean[sub][leader]]				
# 				# print(list_ori_mean_str,data_mean[sub][leader][list_ori_mean_str[0]]['nb'],data_mean[sub][leader][list_ori_mean_str[-1]]['nb'])
# 				for ori_str in list_ori_mean_str:
# 					list_ind[sub][leader][ori_str] = []		
		
# 				for i in range(len(data[sub])):
# 					if data[sub][i]['Leader'] == leader:
# 						current_ori = data['Table'][i]['Orientation_End_Theorique'] 
# 						for ori in list_ind[sub][leader]:
# 							if float(ori[23:]) == current_ori:
# 								list_ind[sub][leader][ori].append(i)
# 						for ori in list_ind[sub]['All data']:
# 							if float(ori[23:]) == current_ori:
# 								list_ind[sub]['All data'][ori].append(i)
# 			# 	print(len(list_ind[sub][leader][list_ori_mean_str[0]]),len(list_ind[sub][leader][list_ori_mean_str[-1]]))

# 			# print("--> all ")
# 			# print(list_ori_mean_str_all,data_mean[sub]['All data'][list_ori_mean_str_all[0]]['nb'],data_mean[sub]['All data'][list_ori_mean_str_all[-1]]['nb'])
# 			# print(len(list_ind[sub]['All data'][list_ori_mean_str_all[0]]),len(list_ind[sub]['All data'][list_ori_mean_str_all[-1]]))
# 			# print(list_ind[sub])	
# 			# print('list ind done!')

# 			for leader in list_leaders[:3]:	
# 				for ori in list_ind[sub][leader]:
# 					for i in list_ind[sub][leader][ori]:
# 						# if leader != 'All data':
# 						# 	print("----------")
# 						# 	print(sub,leader,ori)
# 						# 	print(data[sub][i]['Leader'],data[sub][i]['Orientation_End_Theorique'])
# 						dist_lin,dist_ang_loc,dist_ang_glob = distance(\
# 							data[sub][i],data_mean[sub][leader][ori])
# 						binome = data[sub][i]['Binome']
# 						dist_to_mean_lin[sub][leader].append(dist_lin) 
# 						dist_to_mean_ang_loc[sub][leader].append(dist_ang_loc)
# 						dist_to_mean_ang_glob[sub][leader].append(dist_ang_glob)
# 						dist_to_mean_lin[sub]["All data"].append([dist_lin,binome,file]) 
# 						dist_to_mean_ang_loc[sub]["All data"].append([dist_ang_loc,binome,file])
# 						dist_to_mean_ang_glob[sub]["All data"].append([dist_ang_glob,binome,file])											
# 			print(sub,'dist computed !')

	
# 	else:
# 		list_ind = {}
# 		for sub in list_sub:		
# 			list_ind[sub] = {}					
# 			list_ori_mean_str_all = [ori for ori in data_mean[sub]['All data']]
# 			for ori_str in list_ori_mean_str_all:
# 				list_ind[sub][ori_str] = []	
		
# 			for i in range(len(data[sub])):
# 				current_ori = data['Table'][i]['Orientation_Init_Theorique'] 
# 				for ori in list_ind[sub]:
# 					if float(ori[24:]) == current_ori:
# 						list_ind[sub][ori].append(i)

# 			# print("--> all ")
# 			# print(list_ori_mean_str_all,data_mean[sub]['All data'][list_ori_mean_str_all[0]]['nb'],data_mean[sub]['All data'][list_ori_mean_str_all[-1]]['nb'])
# 			# print(len(list_ind[sub]['All data'][list_ori_mean_str_all[0]]),len(list_ind[sub]['All data'][list_ori_mean_str_all[-1]]))
# 			# print(list_ind[sub])
				
							
# 			for ori in list_ind[sub]:
# 				for i in list_ind[sub][ori]:
# 					dist_lin,dist_ang_loc,dist_ang_glob = distance(\
# 							data[sub][i],data_mean[sub]['All data'][ori])
# 					binome = data[sub][i]['Binome']					
# 					dist_to_mean_lin[sub]['Sujet 1 et 2'].append(dist_lin) 
# 					dist_to_mean_ang_loc[sub]['Sujet 1 et 2'].append(dist_ang_loc)
# 					dist_to_mean_ang_glob[sub]['Sujet 1 et 2'].append(dist_ang_glob)
# 					dist_to_mean_lin[sub]["All data"].append([dist_lin,binome,file]) 
# 					dist_to_mean_ang_loc[sub]["All data"].append([dist_ang_loc,binome,file])
# 					dist_to_mean_ang_glob[sub]["All data"].append([dist_ang_glob,binome,file])											



# 			print(sub,'--> dist computed !')

# print(len(dist_to_mean_lin['Sujet 1']['Sujet 1']))
# print(len(dist_to_mean_lin['Sujet 1']['Sujet 2']))	
# print(len(dist_to_mean_lin['Sujet 1']['Sujet 1 et 2']))
# print(len(dist_to_mean_lin['Sujet 1']['All data']))

# print(len(dist_to_mean_lin['Table']['Sujet 1']))
# print(len(dist_to_mean_lin['Table']['Sujet 2']))	
# print(len(dist_to_mean_lin['Table']['Sujet 1 et 2']))
# print(len(dist_to_mean_lin['Table']['All data']))


# file_name = './Data/linear_distance_human_mean.json'
# json_file = json.dumps(dist_to_mean_lin, indent = 4, ensure_ascii = False)
# with open(file_name, 'w') as outfile:
#     outfile.write(json_file)
# file_name = './Data/local_angular_distance_human_mean.json'
# json_file = json.dumps(dist_to_mean_ang_loc, indent = 4, ensure_ascii = False)
# with open(file_name, 'w') as outfile:
#     outfile.write(json_file)
# file_name = './Data/global_angular_distance_human_mean.json'
# json_file = json.dumps(dist_to_mean_ang_glob, indent = 4, ensure_ascii = False)
# with open(file_name, 'w') as outfile:
#     outfile.write(json_file)    

#################################################################################

f = open('Data/linear_distance_human_mean.json')
dist_lin = json.load(f)
f = open('Data/local_angular_distance_human_mean.json')
dist_ang_loc = json.load(f)
f = open('Data/global_angular_distance_human_mean.json')
dist_ang_glob = json.load(f)

dist_lin_all = {}
dist_ang_glob_all = {}
dist_ang_loc_all = {}
for subject in dist_lin:
	dist_lin_all[subject] = [float(n) for n in np.transpose(dist_lin[subject]['All data'])[0]]
	dist_ang_glob_all[subject] = [float(n) for n in np.transpose(dist_ang_glob[subject]['All data'])[0]]
	dist_ang_loc_all[subject] = [float(n) for n in np.transpose(dist_ang_loc[subject]['All data'])[0]]

###############################################
################ For all data #################
###############################################

########### Mean +- std computation ###########

print('### Mean +- std computation ###')
for subject in dist_lin:
	for leader in dist_lin[subject]:
		print("--> subject : ",subject,", leader : ",leader)
		if leader != 'All data':
			print("linear distance (m):",np.mean(dist_lin[subject][leader]),"+-",np.std(dist_lin[subject][leader]))
			print("angular distance (rad):",np.mean(dist_ang_glob[subject][leader]),"+-",np.std(dist_ang_glob[subject][leader]))
		else:
			print("linear distance (m):",np.mean(dist_lin_all[subject]),"+-",np.std(dist_lin_all[subject]))
			print("angular distance (rad):",np.mean(dist_ang_glob_all[subject]),"+-",np.std(dist_ang_glob_all[subject]))

########### Normality test ###########

# print('### Normality test - Not normal if p < 0.05 ###')
# for subject in dist_lin:
# 	for leader in dist_lin[subject]:
# 		print("--> subject : ",subject,", leader : ",leader)
# 		if leader != 'All data':
# 			k,p = stats.shapiro(dist_lin[subject][leader])
# 			print("p for linear distance = ",p)
# 			k,p = stats.shapiro(dist_ang_glob[subject][leader])
# 			print("p for angular distance = ",p)		
# 			# stats.probplot(dist_lin[subject][leader],dist='norm',plot=plt) # If our data comes from a normal distribution, we should see all the points sitting on the straight line.
# 			# plt.show()
# 		else:
# 			k,p = stats.shapiro(dist_lin_all[subject])
# 			print("p for linear distance = ",p)
# 			k,p = stats.shapiro(dist_ang_glob_all[subject])
# 			print("p for angular distance = ",p)		

########### Kruskal test ###########

# print('### Kruskal Tests ###')
# print('Kruskal test - Significant difference if p < 0.05')
# kruskal_dist = stats.kruskal(dist_lin['Table']['Sujet 1'],\
# 	dist_lin['Table']['Sujet 2'],dist_lin['Table']['Sujet 1 et 2'],\
# 	dist_lin_all['Table']) 
# print("Table/every leader: ",kruskal_dist)
# kruskal_dist = stats.kruskal(dist_lin['Sujet 1']['Sujet 1'],\
# 	dist_lin['Sujet 1']['Sujet 2'],dist_lin['Sujet 1']['Sujet 1 et 2'],\
# 	dist_lin_all['Sujet 1']) 
# print("Sujet 1/every leader: ",kruskal_dist)
# kruskal_dist = stats.kruskal(dist_lin['Sujet 2']['Sujet 1'],\
# 	dist_lin['Sujet 2']['Sujet 2'],dist_lin['Sujet 2']['Sujet 1 et 2'],\
# 	dist_lin_all['Sujet 2']) 
# print("Sujet 2/every leader: ",kruskal_dist)

# kruskal_dist = stats.kruskal(dist_lin['Sujet 1']['Sujet 1'],\
# 	dist_lin['Sujet 2']['Sujet 1'],dist_lin['Table']['Sujet 1']) 
# print('Kruskal test - Significant difference if p < 0.05')
# print("every sub/one leader (Sujet 1): ",kruskal_dist)
# kruskal_dist = stats.kruskal(dist_lin_all['Sujet 1'],dist_lin_all['Sujet 2'],\
# 	dist_lin_all['Table']) 
# print('Kruskal test - Significant difference if p < 0.05')
# print("every sub/one leader (All data): ",kruskal_dist)


########## Boxplot ###########

# plt.subplot(3,4,1)
# plt.boxplot([dist_lin['Sujet 1']['Sujet 1']])
# plt.ylabel("distance between human and mean (m)")
# plt.title("Sujet 1 (leader : Sujet 1)")
# plt.subplot(3,4,2)
# plt.boxplot([dist_lin['Sujet 1']['Sujet 2']])
# plt.title("Sujet 1 (leader : Sujet 2)")
# plt.subplot(3,4,3)
# plt.boxplot([dist_lin['Sujet 1']['Sujet 1 et 2']])
# plt.title("Sujet 1 (leader : Sujet 1 et 2)")
# plt.subplot(3,4,4)
# plt.boxplot([dist_lin_all['Sujet 1']])
# plt.title("Sujet 1 (all data)")

# plt.subplot(3,4,5)
# plt.boxplot([dist_lin['Sujet 2']['Sujet 1']])
# plt.title("Sujet 2 (leader : Sujet 1)")
# plt.subplot(3,4,6)
# plt.boxplot([dist_lin['Sujet 2']['Sujet 2']])
# plt.title("Sujet 2 (leader : Sujet 2)")
# plt.subplot(3,4,7)
# plt.boxplot([dist_lin['Sujet 2']['Sujet 1 et 2']])
# plt.title("Sujet 2 (leader : Sujet 1 et 2)")
# plt.subplot(3,4,8)
# plt.boxplot([dist_lin_all['Sujet 2']])
# plt.title("Sujet 2 (all data)")

# plt.subplot(3,4,9)
# plt.boxplot([dist_lin['Table']['Sujet 1']])
# plt.title("Table (leader : Sujet 1)")
# plt.subplot(3,4,10)
# plt.boxplot([dist_lin['Table']['Sujet 2']])
# plt.title("Table (leader : Sujet 2)")
# plt.subplot(3,4,11)
# plt.boxplot([dist_lin['Table']['Sujet 1 et 2']])
# plt.title("Table (leader : Sujet 1 et 2)")
# plt.subplot(3,4,12)
# plt.boxplot([dist_lin_all['Table']])
# plt.title("Table (all data)")

# plt.show()

# plt.subplot(3,4,1)
# plt.boxplot([dist_ang_glob['Sujet 1']['Sujet 1']])
# plt.ylabel("distance between human and mean (rad)")
# plt.title("Sujet 1 (leader : Sujet 1)")
# plt.subplot(3,4,2)
# plt.boxplot([dist_ang_glob['Sujet 1']['Sujet 2']])
# plt.title("Sujet 1 (leader : Sujet 2)")
# plt.subplot(3,4,3)
# plt.boxplot([dist_ang_glob['Sujet 1']['Sujet 1 et 2']])
# plt.title("Sujet 1 (leader : Sujet 1 et 2)")
# plt.subplot(3,4,4)
# plt.boxplot([dist_ang_glob_all['Sujet 1']])
# plt.title("Sujet 1 (all data)")

# plt.subplot(3,4,5)
# plt.boxplot([dist_ang_glob['Sujet 2']['Sujet 1']])
# plt.title("Sujet 2 (leader : Sujet 1)")
# plt.subplot(3,4,6)
# plt.boxplot([dist_ang_glob['Sujet 2']['Sujet 2']])
# plt.title("Sujet 2 (leader : Sujet 2)")
# plt.subplot(3,4,7)
# plt.boxplot([dist_ang_glob['Sujet 2']['Sujet 1 et 2']])
# plt.title("Sujet 2 (leader : Sujet 1 et 2)")
# plt.subplot(3,4,8)
# plt.boxplot([dist_ang_glob_all['Sujet 2']])
# plt.title("Sujet 2 (all data)")

# plt.subplot(3,4,9)
# plt.boxplot([dist_ang_glob['Table']['Sujet 1']])
# plt.title("Table (leader : Sujet 1)")
# plt.subplot(3,4,10)
# plt.boxplot([dist_ang_glob['Table']['Sujet 2']])
# plt.title("Table (leader : Sujet 2)")
# plt.subplot(3,4,11)
# plt.boxplot([dist_ang_glob['Table']['Sujet 1 et 2']])
# plt.title("Table (leader : Sujet 1 et 2)")
# plt.subplot(3,4,12)
# plt.boxplot([dist_ang_glob_all['Table']])
# plt.title("Table (all data)")

# plt.show()

# plt.subplot(3,4,1)
# plt.boxplot([dist_ang_loc['Sujet 1']['Sujet 1']])
# plt.ylabel("distance between human and mean (rad)")
# plt.title("Sujet 1 (leader : Sujet 1)")
# plt.subplot(3,4,2)
# plt.boxplot([dist_ang_loc['Sujet 1']['Sujet 2']])
# plt.title("Sujet 1 (leader : Sujet 2)")
# plt.subplot(3,4,3)
# plt.boxplot([dist_ang_loc['Sujet 1']['Sujet 1 et 2']])
# plt.title("Sujet 1 (leader : Sujet 1 et 2)")
# plt.subplot(3,4,4)
# plt.boxplot([dist_ang_loc_all['Sujet 1']])
# plt.title("Sujet 1 (all data)")

# plt.subplot(3,4,5)
# plt.boxplot([dist_ang_loc['Sujet 2']['Sujet 1']])
# plt.title("Sujet 2 (leader : Sujet 1)")
# plt.subplot(3,4,6)
# plt.boxplot([dist_ang_loc['Sujet 2']['Sujet 2']])
# plt.title("Sujet 2 (leader : Sujet 2)")
# plt.subplot(3,4,7)
# plt.boxplot([dist_ang_loc['Sujet 2']['Sujet 1 et 2']])
# plt.title("Sujet 2 (leader : Sujet 1 et 2)")
# plt.subplot(3,4,8)
# plt.boxplot([dist_ang_loc_all['Sujet 2']])
# plt.title("Sujet 2 (all data)")

# plt.subplot(3,4,9)
# plt.boxplot([dist_ang_loc['Table']['Sujet 1']])
# plt.title("Table (leader : Sujet 1)")
# plt.subplot(3,4,10)
# plt.boxplot([dist_ang_loc['Table']['Sujet 2']])
# plt.title("Table (leader : Sujet 2)")
# plt.subplot(3,4,11)
# plt.boxplot([dist_ang_loc['Table']['Sujet 1 et 2']])
# plt.title("Table (leader : Sujet 1 et 2)")
# plt.subplot(3,4,12)
# plt.boxplot([dist_ang_loc_all['Table']])
# plt.title("Table (all data)")

# plt.show()

###############################################
################## Per pairs ##################
###############################################

list_pair = list(set([n for n in np.transpose(dist_lin['Table']['All data'])[1]]))
dist_lin_per_pair = {}
dist_ang_per_pair = {}
for subject in dist_lin:
	dist_lin_per_pair[subject] = {}
	dist_ang_per_pair[subject] = {}	
	dl = np.transpose(dist_lin[subject]['All data'])
	da = np.transpose(dist_ang_glob[subject]['All data'])
	for pair in list_pair:
		dist_lin_per_pair[subject][pair] = []
		dist_ang_per_pair[subject][pair] = []		
	for i in range(len(dl[0])):
		dist_lin_per_pair[subject][dl[1][i]].append(float(dl[0][i]))
		dist_ang_per_pair[subject][da[1][i]].append(float(da[0][i]))
# print(len(dist_lin_per_pair['Table']),len(dist_lin_per_pair['Table']['Sujet1_Stéphane&Sujet2_Angélique']))

# ########### Kruskal test ###########

# kruskal_dist = stats.kruskal(dist_lin_per_pair['Table'][list_pair[0]],\
# 	dist_lin_per_pair['Table'][list_pair[1]],\
# 	dist_lin_per_pair['Table'][list_pair[2]],\
# 	dist_lin_per_pair['Table'][list_pair[3]],\
# 	dist_lin_per_pair['Table'][list_pair[4]],\
# 	dist_lin_per_pair['Table'][list_pair[5]],\
# 	dist_lin_per_pair['Table'][list_pair[6]],\
# 	dist_lin_per_pair['Table'][list_pair[7]],\
# 	dist_lin_per_pair['Table'][list_pair[8]],\
# 	dist_lin_per_pair['Table'][list_pair[9]],\
# 	dist_lin_per_pair['Table'][list_pair[10]],\
# 	dist_lin_per_pair['Table'][list_pair[11]],\
# 	dist_lin_per_pair['Table'][list_pair[12]],\
# 	dist_lin_per_pair['Table'][list_pair[13]],\
# 	dist_lin_per_pair['Table'][list_pair[14]],\
# 	dist_lin_per_pair['Table'][list_pair[15]],\
# 	dist_lin_per_pair['Table'][list_pair[16]],\
# 	dist_lin_per_pair['Table'][list_pair[17]],\
# 	dist_lin_per_pair['Table'][list_pair[18]],\
# 	dist_lin_per_pair['Table'][list_pair[19]],\
# 	) # f_oneway for ANOVA test (meilleur resultat)
# print('Kruskal test - Significant difference if p < 0.05')
# print("Linear distance - one sub (Table)/every pair: ",kruskal_dist)

# kruskal_dist = stats.kruskal(dist_ang_per_pair['Table'][list_pair[0]],\
# 	dist_ang_per_pair['Table'][list_pair[1]],\
# 	dist_ang_per_pair['Table'][list_pair[2]],\
# 	dist_ang_per_pair['Table'][list_pair[3]],\
# 	dist_ang_per_pair['Table'][list_pair[4]],\
# 	dist_ang_per_pair['Table'][list_pair[5]],\
# 	dist_ang_per_pair['Table'][list_pair[6]],\
# 	dist_ang_per_pair['Table'][list_pair[7]],\
# 	dist_ang_per_pair['Table'][list_pair[8]],\
# 	dist_ang_per_pair['Table'][list_pair[9]],\
# 	dist_ang_per_pair['Table'][list_pair[10]],\
# 	dist_ang_per_pair['Table'][list_pair[11]],\
# 	dist_ang_per_pair['Table'][list_pair[12]],\
# 	dist_ang_per_pair['Table'][list_pair[13]],\
# 	dist_ang_per_pair['Table'][list_pair[14]],\
# 	dist_ang_per_pair['Table'][list_pair[15]],\
# 	dist_ang_per_pair['Table'][list_pair[16]],\
# 	dist_ang_per_pair['Table'][list_pair[17]],\
# 	dist_ang_per_pair['Table'][list_pair[18]],\
# 	dist_ang_per_pair['Table'][list_pair[19]],\
# 	) 
# print("Angular distance - one sub (Table)/every pair: ",kruskal_dist)


########## Boxplot ###########

# count = 1
# for subject in dist_lin_per_pair: # /!\ pairs change between 2 plot /!\
# 	plt.subplot(3,1,count)
# 	count += 1
# 	plt.boxplot(dist_lin_per_pair[subject].values())
# 	plt.ylabel("linear distance (m)")
# 	plt.ylim(0, 2)
# 	plt.title(subject+" (all data per pairs)")
# plt.show()

# count = 1
# for subject in dist_ang_per_pair:
# 	plt.subplot(3,1,count)
# 	count += 1
# 	plt.boxplot(dist_ang_per_pair[subject].values())
# 	plt.ylabel("global angular distance (rad)")
# 	plt.ylim(0,1.25)
# 	plt.title(subject+" (all data per pairs)")
# plt.show()

###############################################
############## Per trajectories ###############
###############################################

list_traj = list(set([n for n in np.transpose(dist_lin['Table']['All data'])[2]]))
dist_lin_per_traj = {}
dist_ang_per_traj = {}
for subject in dist_lin:
	dist_lin_per_traj[subject] = {}
	dist_ang_per_traj[subject] = {}	
	dl = np.transpose(dist_lin[subject]['All data'])
	da = np.transpose(dist_ang_glob[subject]['All data'])
	for traj in list_traj:
		dist_lin_per_traj[subject][traj] = []
		dist_ang_per_traj[subject][traj] = []		
	for i in range(len(dl[0])):
		dist_lin_per_traj[subject][dl[2][i]].append(float(dl[0][i]))
		dist_ang_per_traj[subject][da[2][i]].append(float(da[0][i]))
# print(len(dist_lin_per_traj['Table']),len(dist_lin_per_traj['Table']['Sujet1_Stéphane&Sujet2_Angélique']))

########### Kruskal test ###########

# kruskal_dist = stats.kruskal(dist_lin_per_traj['Table'][list_traj[0]],\
# 	dist_lin_per_traj['Table'][list_traj[1]],\
# 	dist_lin_per_traj['Table'][list_traj[2]],\
# 	dist_lin_per_traj['Table'][list_traj[3]],\
# 	dist_lin_per_traj['Table'][list_traj[4]],\
# 	dist_lin_per_traj['Table'][list_traj[5]],\
# 	dist_lin_per_traj['Table'][list_traj[6]],\
# 	dist_lin_per_traj['Table'][list_traj[7]],\
# 	dist_lin_per_traj['Table'][list_traj[8]],\
# 	dist_lin_per_traj['Table'][list_traj[9]],\
# 	dist_lin_per_traj['Table'][list_traj[10]],\
# 	dist_lin_per_traj['Table'][list_traj[11]],\
# 	dist_lin_per_traj['Table'][list_traj[12]],\
# 	dist_lin_per_traj['Table'][list_traj[13]],\
# 	dist_lin_per_traj['Table'][list_traj[14]],\
# 	dist_lin_per_traj['Table'][list_traj[15]],\
# 	dist_lin_per_traj['Table'][list_traj[16]],\
# 	dist_lin_per_traj['Table'][list_traj[17]],\
# 	) # f_oneway for ANOVA test (meilleur resultat)
# print('Kruskal test - Significant difference if p < 0.05')
# print("Linear distance - one sub (Table)/every pair: ",kruskal_dist)

# kruskal_dist = stats.kruskal(dist_ang_per_traj['Table'][list_traj[0]],\
# 	dist_ang_per_traj['Table'][list_traj[1]],\
# 	dist_ang_per_traj['Table'][list_traj[2]],\
# 	dist_ang_per_traj['Table'][list_traj[3]],\
# 	dist_ang_per_traj['Table'][list_traj[4]],\
# 	dist_ang_per_traj['Table'][list_traj[5]],\
# 	dist_ang_per_traj['Table'][list_traj[6]],\
# 	dist_ang_per_traj['Table'][list_traj[7]],\
# 	dist_ang_per_traj['Table'][list_traj[8]],\
# 	dist_ang_per_traj['Table'][list_traj[9]],\
# 	dist_ang_per_traj['Table'][list_traj[10]],\
# 	dist_ang_per_traj['Table'][list_traj[11]],\
# 	dist_ang_per_traj['Table'][list_traj[12]],\
# 	dist_ang_per_traj['Table'][list_traj[13]],\
# 	dist_ang_per_traj['Table'][list_traj[14]],\
# 	dist_ang_per_traj['Table'][list_traj[15]],\
# 	dist_ang_per_traj['Table'][list_traj[16]],\
# 	dist_ang_per_traj['Table'][list_traj[17]],\
# 	) # f_oneway for ANOVA test (meilleur resultat)
# print('Kruskal test - Significant difference if p < 0.05')
# print("Linear distance - one sub (Table)/every pair: ",kruskal_dist)

########## Boxplot ###########

# count = 1
# for subject in dist_lin_per_traj: # /!\ pairs change between 2 plot /!\
# 	plt.subplot(3,1,count)
# 	count += 1
# 	plt.boxplot(dist_lin_per_traj[subject].values())
# 	plt.ylabel("linear distance (m)")
# 	plt.ylim(0, 2)
# 	plt.title(subject+" (all data per pairs)")
# plt.show()

# count = 1
# for subject in dist_ang_per_traj: # /!\ pairs change between 2 plot /!\
# 	plt.subplot(3,1,count)
# 	count += 1
# 	plt.boxplot(dist_ang_per_traj[subject].values())
# 	plt.ylabel("linear distance (m)")
# 	plt.ylim(0, 2)
# 	plt.title(subject+" (all data per pairs)")
# plt.show()