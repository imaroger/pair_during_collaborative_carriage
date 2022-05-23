import numpy as np
import matplotlib.pylab as plt
from math import pi,floor,atan2,atan,nan,sqrt
import json
from scipy.interpolate import splprep, splev, interp1d
from scipy import stats

path = 'Data/Human/'
list_targets = ['d1_p4_jaune_1', 'd1_p4_gris_1', 'd1_p5_jaune_1', 'd1_p5_gris_1', 'd1_p6_jaune_1', 'd1_p6_gris_1', 'd2_p7_jaune_1', 'd2_p7_gris_1', 'd3_p7_gris_1',
				'd1_p4_jaune_2', 'd1_p4_gris_2', 'd1_p5_jaune_2', 'd1_p5_gris_2', 'd1_p6_jaune_2', 'd1_p6_gris_2', 'd2_p7_jaune_2', 'd2_p7_gris_2', 'd3_p7_gris_2']
list_leaders = ['Sujet 1','Sujet 2','Sujet 1 et 2']
list_sub = ['Sujet 1','Sujet 2','Table']
list_pair = ['Sujet1_Aurélie&Sujet2_Stanislas', 'Sujet1_Rémy&Sujet2_Margaux', 'Sujet1_Zaki&Sujet2_Yanis', 'Sujet1_Thanh&Sujet2_Diane', 'Sujet1_Sabrina&Sujet2_Quentin', 'Sujet1_Aniss&Sujet2_Louise', 'Sujet1_Hugo&Sujet2_Alexandre', 'Sujet1_Alexia&Sujet2_Bénédicte', 'Sujet1_Adénikè&Sujet2_Médéric', 'Sujet1_Anaïs&Sujet2_Mariem', 'Sujet1_Stéphane&Sujet2_Angélique', 'Sujet1_Fanny&Sujet2_William', 'Sujet1_Romane&Sujet2_Corentin', 'Sujet1_Paul&Sujet2_Mathieu', 'Sujet1_Marine&Sujet2_Hélène', 'Sujet1_Sébastien&Sujet2_Nils', 'Sujet1_Antoine&Sujet2_Médéric_LAAS', 'Sujet1_Amaury&Sujet2_Jason', 'Sujet1_Guilhem&Sujet2_César', 'Sujet1_Alexis&Sujet2_Thibaud']

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
	th1,th2 = [normalizeAngle(th) for th in data1['th']],[normalizeAngle(th) for th in data2['th']]
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

	# if dist/length > 1:
	# 	arrow_len = 0.1
	# 	print(th1[0],th1[-1])
	# 	print(th2[0],th2[-1])
	# 	print(dist/length)
	# 	plt.plot(data1['x'],data1['y'],color = 'red')
	# 	plt.plot(data2['x'],data2['y'],color = 'blue')	
	# 	for i in range(len(data1['x'])):
	# 		if i%10 == 0:
	# 			plt.arrow(data1['x'][i], data1['y'][i], \
	# 			np.cos(data1['th'][i])*arrow_len,\
	# 			np.sin(data1['th'][i])*arrow_len, head_width=.02, color = 'red')
	# 			plt.arrow(data2['x'][i], data2['y'][i], \
	# 			np.cos(data2['th'][i])*arrow_len,\
	# 			np.sin(data2['th'][i])*arrow_len, head_width=.02, color = 'blue')

		# time2 = np.linspace(1,100,500)
		# time = np.linspace(1,100,len(th2))
		# plt.plot(time2,th1)
		# plt.plot(time,th2)		
		# plt.plot(time2,th2)
		# plt.show()
	return dist/length

traj_go_return = {}
dist = {}
for sub in list_sub:
	traj_go_return[sub] = {}
	dist[sub] = {}
	dist[sub]["Linear"] = []
	dist[sub]["Angular"] = []
	for traj in list_targets[:9]:
		traj_go_return[sub][traj[:-2]] = {}
		for pair in list_pair:
			traj_go_return[sub][traj[:-2]][pair] = {}		
			traj_go_return[sub][traj[:-2]][pair]["Go"] = []
			traj_go_return[sub][traj[:-2]][pair]["Return"] = []		


for file in list_targets[:9]:
	print("### ", file[:-2]," ###")
	f_go = open(path+file+'.json')
	data_go = json.load(f_go)['Trajectoires_Individuelles']
	f_return = open(path+file[:-1]+'2.json')
	data_return = json.load(f_return)['Trajectoires_Individuelles']
	for sub in data_go:
		for i in range(len(data_go[sub])):
			if data_go[sub][i]["Leader"] == "Sujet 1 et 2":
				pair = data_go[sub][i]["Binome"]
				traj = {}			
				traj["x"],traj["y"],traj["th"] = data_go[sub][i]["x"], \
					data_go[sub][i]["y"], data_go[sub][i]["Orientation_Globale"]
				traj_go_return[sub][file[:-2]][pair]["Go"] = traj
				traj_go_return[sub][file[:-2]][pair]["Orientation_End"] = data_go[sub][i]["Orientation_End_Theorique"]				
				traj_go_return[sub][file[:-2]][pair]["Orientation_Init"] = data_go[sub][i]["Orientation_Init_Theorique"]				
		for i in range(len(data_return[sub])):
			pair = data_return[sub][i]["Binome"]
			if data_return[sub][i]["Orientation_Init_Theorique"] == traj_go_return[sub][file[:-2]][pair]["Orientation_End"]:
				traj_go = traj_go_return[sub][file[:-2]][pair]["Go"]
				ori_init_go = traj_go_return[sub][file[:-2]][pair]["Orientation_Init"]
				traj = {}	
				traj["x"],traj["y"],traj["th"] = data_return[sub][i]["x"], \
					data_return[sub][i]["y"], data_return[sub][i]["Orientation_Globale"]
				
				return_ok_dist = (sqrt((traj_go["x"][0]-traj["x"][-1])**2+\
					(traj_go["y"][0]-traj["y"][-1])**2) < 1) #Pairs go to the wrong configuration when returning the table to its original positions
				return_ok_ori = (ori_init_go == data_return[sub][i]["Orientation_End_Theorique"])#Pairs go to the wrong configuration when returning the table to its original positions
				if return_ok_ori and return_ok_dist: 
					traj_go_return[sub][file[:-2]][pair]["Return"].append(traj)
				
					traj_return = {}
					traj_return["x"] = traj["x"][::-1]
					traj_return["y"] = traj["y"][::-1]
					traj_return["th"] = traj["th"][::-1]					
					linear_dist = linearDistance(traj_go,traj_return)
					ang_dist = angularDistance(traj_go,traj_return)
					# if ang_dist > 1:
					# 	print(file[:-2],sub,pair)
					# 	print(linear_dist,ang_dist)
					# 	print(sqrt((traj_go["x"][0]-traj["x"][-1])**2+(traj_go["y"][0]-traj["y"][-1])**2))
					# 	plt.plot(traj_go["x"],traj_go["y"],color="red")
					# 	plt.plot(traj["x"],traj["y"],color = "blue")
					# 	for i in range(len(traj_go['x'])):
					# 		arrow_len = 0.1
					# 		if i%10 == 0:
					# 			plt.arrow(traj_go['x'][i], traj_go['y'][i], \
					# 			np.cos(traj_go['th'][i])*arrow_len,\
					# 			np.sin(traj_go['th'][i])*arrow_len, head_width=.02, color = 'red')
					# 			plt.arrow(traj['x'][i], traj['y'][i], \
					# 			np.cos(traj['th'][i])*arrow_len,\
					# 			np.sin(traj['th'][i])*arrow_len, head_width=.02, color = 'blue')
					# 	plt.show()				
					dist[sub]["Linear"].append(linear_dist)
					dist[sub]["Angular"].append(ang_dist)					
	# for sub in data_go:
	# 	test = traj_go_return[sub][file[:-2]]['Sujet1_Stéphane&Sujet2_Angélique']
	# 	for i in range(len(test["Go"])):
	# 		plt.plot(test["Go"][i]["x"],test["Go"][i]["y"],color='red')
	# 	for i in range(len(test["Return"])):
	# 		plt.plot(test["Return"][i]["x"],test["Return"][i]["y"],color='green')
	# plt.show()


count = 1
for sub in list_sub:
	plt.subplot(1,3,count)
	count += 1
	plt.boxplot([dist[sub]["Linear"]])
	print(sub,np.mean(dist[sub]["Linear"]),"+-",np.std(dist[sub]["Linear"]))
	plt.ylabel("Linear distance between forward and return paths (m)")
	plt.ylim(0, 0.9)
	if sub == "Sujet 1":
		plt.title("Subject 1")
	elif sub == "Sujet 2":
		plt.title("Subject 2")
	else:
		plt.title(sub)
plt.show()

count = 1
for sub in list_sub:
	plt.subplot(1,3,count)
	count += 1
	plt.boxplot([dist[sub]["Angular"]])
	print(sub,np.mean(dist[sub]["Angular"]),"+-",np.std(dist[sub]["Angular"]))	
	plt.ylabel("Angular distance between forward and return paths (rad)")
	plt.ylim(0, 2.05)
	if sub == "Sujet 1":
		plt.title("Subject 1")
	elif sub == "Sujet 2":
		plt.title("Subject 2")
	else:
		plt.title(sub)
plt.show()

##################################
######### Normality test #########
##################################

print("### Normality test for all : Normal if p > 0.05 ###")
for sub in list_sub:
	test = stats.shapiro(dist[sub]["Linear"])
	print("linear : ",test)
	test = stats.shapiro(dist[sub]["Angular"])
	print("angualr : ",test)

##################################
#### Kruskal test - Scenarios ####
##################################

print("### kruskal_test for all : Significant difference if p < 0.05 ###")
kruskal_test = stats.mannwhitneyu(dist["Sujet 1"]["Linear"]+\
	dist["Sujet 2"]["Linear"],dist["Table"]["Linear"])
print("linear : ",kruskal_test)
kruskal_test = stats.mannwhitneyu(dist["Sujet 1"]["Angular"]+\
	dist["Sujet 2"]["Angular"],dist["Table"]["Angular"])
print("angular : ",kruskal_test)	

