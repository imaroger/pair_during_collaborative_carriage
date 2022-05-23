
import numpy as np
import matplotlib.pylab as plt
import crocoddyl
from math import pi, floor, sqrt, cos, sin, atan2
from scipy.optimize import minimize
from scipy.interpolate import splprep, splev
import time
import json
import os


plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['ps.fonttype'] = 42


#########################################################################
########################## FUNCTION DEFINITION	#########################
#########################################################################

def trajOfInterest():
	path = 'Data/Human/'
	list_targets = ['d1_p4_jaune', 'd1_p4_gris', 'd1_p5_jaune', 'd1_p5_gris', 'd1_p6_jaune', 'd1_p6_gris', 'd2_p7_jaune', 'd2_p7_gris', 'd3_p7_gris']

	traj_table = {}
	traj_sub1 = {}
	traj_sub2 = {}
	for traj in list_targets:
		f_go = open(path+traj+'_1.json')
		traj_go = json.load(f_go)['Trajectoires_Individuelles']
		f_return = open(path+traj+'_2.json')
		traj_return = json.load(f_return)['Trajectoires_Individuelles']

		traj_table_go = traj_go["Table"]
		traj_table_return = traj_return["Table"]

		traj_table[traj+'_1'] = []
		traj_table[traj+'_2'] = []

		traj_sub1_go = traj_go['Sujet 1']
		traj_sub1_return = traj_return['Sujet 1']

		traj_sub1[traj+'_1'] = []
		traj_sub1[traj+'_2'] = []

		traj_sub2_go = traj_go['Sujet 2']
		traj_sub2_return = traj_return['Sujet 2']

		traj_sub2[traj+'_1'] = []
		traj_sub2[traj+'_2'] = []

		for i in range(len(traj_table_go)):
			if traj_table_go[i]["Leader"] == "Sujet 1 et 2":
				traj_table[traj+'_1'].append(traj_table_go[i])
				pair = traj_table_go[i]["Binome"]

				# if traj_sub1_go[i]["Binome"] != pair or traj_sub1_go[i]["Leader"] != "Sujet 1 et 2":
				# 	print("bad sub1 go") # No bad cases
				# if traj_sub2_go[i]["Binome"] != pair or traj_sub2_go[i]["Leader"] != "Sujet 1 et 2":
				# 	print("bad sub2 go") # No bad cases
				traj_sub1[traj+'_1'].append(traj_sub1_go[i])
				traj_sub2[traj+'_1'].append(traj_sub2_go[i])

				xf,yf = traj_table_go[i]["x"][-1],traj_table_go[i]["y"][-1]
				thf = traj_table_go[i]["Orientation_Globale"][-1]
				best_j, min_dist = 0,100
				for j in range(len(traj_table_return)):
					if traj_table_return[j]["Binome"] == pair:
						xi,yi = traj_table_return[j]["x"][0],traj_table_return[j]["y"][0]
						thi = traj_table_return[j]["Orientation_Globale"][0]
						dist = sqrt((xf-xi)**2+(yf-yi)**2)#+abs(thf-thi)
						if dist < min_dist:
							best_j, min_dist = j,dist
				# 		plt.plot(traj_return[j]["x"],traj_return[j]["y"],label = "j = "+str(j))

				# print(traj_return[j]["Orientation_Init_Theorique"])
				# print(traj_go[i]["Orientation_End_Theorique"])					
				# print(best_j,min_dist)
				# plt.plot(traj_go[i]["x"],traj_go[i]["y"])
				# # plt.plot(traj_return[best_j]["x"],traj_return[best_j]["y"])					
				# plt.legend()
				# plt.show()
				traj_table[traj+'_2'].append(traj_table_return[best_j])
				traj_sub1[traj+'_2'].append(traj_sub1_return[best_j])
				traj_sub2[traj+'_2'].append(traj_sub2_return[best_j])
	file_name = 'Data/Traj_from_Table/traj_table.json'
	json_file = json.dumps(traj_table, indent = 4, ensure_ascii = False)
	with open(file_name, 'w') as outfile:
		outfile.write(json_file)
	file_name = 'Data/Traj_from_Table/traj_sub1.json'
	json_file = json.dumps(traj_sub1, indent = 4, ensure_ascii = False)
	with open(file_name, 'w') as outfile:
		outfile.write(json_file)
	file_name = 'Data/Traj_from_Table/traj_sub2.json'
	json_file = json.dumps(traj_sub2, indent = 4, ensure_ascii = False)
	with open(file_name, 'w') as outfile:
		outfile.write(json_file)

def generateSubjectsTraj(data1,data2):
	path = 'Data/Traj_from_Table/'
	f_table = open(path+'traj_table.json')
	traj_table = json.load(f_table)

	traj_subjects = {}
	for traj in traj_table:

		if traj[-1]=='1':
			x1,y1,th1 = np.array(data1[0]),np.array(data1[2]),np.array(data1[4])
			x2,y2,th2 = np.array(data2[0]),np.array(data2[2]),np.array(data2[4])
		else:
			x1,y1,th1 = np.array(data1[1]),np.array(data1[3]),np.array(data1[5])
			x2,y2,th2 = np.array(data2[1]),np.array(data2[3]),np.array(data2[5])			

		traj_subjects[traj] = {}
		traj_subjects[traj]["Sujet 1"] = []
		traj_subjects[traj]["Sujet 2"] = []

		for i in range(len(traj_table[traj])):
			sub1,sub2 = {},{}
			sub1["Binome"] = traj_table[traj][i]["Binome"]
			sub2["Binome"] = traj_table[traj][i]["Binome"]

			xT, yT, thT = traj_table[traj][i]["x"],traj_table[traj][i]["y"],traj_table[traj][i]["Orientation_Globale"]

			sub1["x"] = (xT+x1*np.cos(thT)-y1*np.sin(thT)).tolist()
			sub1["y"] = (yT+x1*np.sin(thT)+y1*np.cos(thT)).tolist()
			sub1["Orientation_Globale"] = (thT+th1).tolist()
			sub2["x"] = (xT+x2*np.cos(thT)-y2*np.sin(thT)).tolist()
			sub2["y"] = (yT+x2*np.sin(thT)+y2*np.cos(thT)).tolist()
			sub2["Orientation_Globale"] = (thT+th2).tolist()

			traj_subjects[traj]["Sujet 1"].append(sub1)
			traj_subjects[traj]["Sujet 2"].append(sub2)

			# plt.plot(xT,yT, color = 'blue')
			# plt.plot(sub1["x"],sub1["y"], color = 'red')
			# plt.plot(sub2["x"],sub2["y"], color = 'green')		
			# arrow_len = 0.2
			# for i in range (len(xT)):
			# 	if i%25 == 0:
			# 		plt.arrow(xT[i], yT[i],\
			# 			np.cos(thT[i])*arrow_len,\
			# 			np.sin(thT[i])*arrow_len, head_width=.05, color = 'blue')
			# 		plt.arrow(sub1["x"][i], sub1["y"][i],\
			# 			np.cos(sub1["Orientation_Globale"][i])*arrow_len,\
			# 			np.sin(sub1["Orientation_Globale"][i])*arrow_len, head_width=.05, color = 'red')
			# 		plt.arrow(sub2["x"][i], sub2["y"][i],\
			# 			np.cos(sub2["Orientation_Globale"][i])*arrow_len,\
			# 			np.sin(sub2["Orientation_Globale"][i])*arrow_len, head_width=.05, color = 'green')									
			# plt.show()

	file_name = path+'traj_subjects.json'
	json_file = json.dumps(traj_subjects, indent = 4, ensure_ascii = False)
	with open(file_name, 'w') as outfile:
		outfile.write(json_file)


def plotOri(human,simu):
	plt.subplot(1,2,1)
	plt.plot(human["x"],human["y"], color = 'red',label='human')
	plt.plot(simu["x"],simu["y"], color = 'green',label='simu')		
	arrow_len = 0.2
	for i in range (len(human["x"])):
		if i%25 == 0:
			plt.arrow(human["x"][i], human["y"][i],\
				np.cos(human["Orientation_Globale"][i])*arrow_len,\
				np.sin(human["Orientation_Globale"][i])*arrow_len, head_width=.05, color = 'red')
			plt.arrow(simu["x"][i], simu["y"][i],\
				np.cos(simu["Orientation_Globale"][i])*arrow_len,\
				np.sin(simu["Orientation_Globale"][i])*arrow_len, head_width=.05, color = 'green')									
	plt.legend()
	plt.subplot(1,2,2)
	time = np.linspace(0,1,500)
	th_human = human["Orientation_Globale"]
	th_simu = simu["Orientation_Globale"]
	# plt.plot(time,th_human, color = 'black',label='human')
	# plt.plot(time,th_simu, color = 'black',label='simu')	
	# print(th_human[0],th_simu[0])
	# print(th_human[-1],th_simu[-1])	
	# if abs(th_human[0]) > pi: 
	# 	th_human = detect_discontinuity((np.array(th_human) + pi)%(2*pi)-pi)
	# if abs(th_simu[0]) > pi:
	# 	th_simu = detect_discontinuity((np.array(th_simu) + pi)%(2*pi)-pi)
	# if abs((abs(th_human[0]) - pi) < 0.5 and abs(abs(th_simu[0]) - pi) < 0.5):
	# 	print("ici",th_human[0],th_simu[0])
	# 	if th_human[0] < 0 and th_simu[0] > 0:
	# 		th_simu = np.array(th_simu)-2*pi
	# 	elif th_human[0] > 0 and th_simu[0] < 0:
	# 		th_simu = np.array(th_simu)+2*pi			

	plt.plot(time,th_human, color = 'red',label='human')
	plt.plot(time,th_simu, color = 'green',label='simu')			
	plt.show()

def detect_discontinuity(theta):
	discontinuted_th = []
	ind_discontinuity = [0]
	for i in range (len(theta)-1):
		if abs(theta[i+1]-theta[i]) > 0.5:		
			ind_discontinuity.append(i+1)
			discontinuted_th.append(np.array(theta[ind_discontinuity[-2]:ind_discontinuity[-1]]))
	if len(discontinuted_th) != 0:
		discontinuted_th.append(theta[ind_discontinuity[-1]:])
		for i in range(1,len(discontinuted_th)):
			discontinuted_th[i] += (discontinuted_th[i-1][-1]-discontinuted_th[i][0])
			if len(discontinuted_th[i]) > 1 :
				if np.abs(discontinuted_th[i][0]-discontinuted_th[i][1]) > 0.5:
					discontinuted_th[i][1:] += (discontinuted_th[i][0]-discontinuted_th[i][1])
		new_theta = np.concatenate(discontinuted_th)
		# if new_theta[0] > 0:
		# 	new_theta = -new_theta
		return new_theta
	else:
		return theta

def linearDistance(x_human,y_human,x_simu,y_simu):
	length = len(x_human)
	# okay1 = np.where(np.abs(np.diff(x_human)) + np.abs(np.diff(y_human)) > 0)
	# okay2 = np.where(np.abs(np.diff(x_simu)) + np.abs(np.diff(y_simu)) > 0)
	# x_simu,y_simu = np.array(x_simu)[okay2],np.array(y_simu)[okay2]	

	tck1, u1 = splprep([x_human, y_human], s = 0)
	tck2, u2 = splprep([x_simu, y_simu], s = 0)
	xnew = np.linspace(0, 1, length)
	x_human, y_human = splev(xnew, tck1)
	x_simu, y_simu = splev(xnew, tck2)

	dist = 0
	for i in range(length):
		dist += sqrt((x_human[i]-x_simu[i])**2+(y_human[i]-y_simu[i])**2)
		# if display:
		# 	if i%25 == 0:
		# 		plt.plot([x_human[i],x_simu[i]], [y_human[i],y_simu[i]], color = 'red', linewidth = 0.5)
	# if display:
	# 	print(dist/length)
	# 	plt.plot(x_human,y_human)
	# 	plt.plot(x_simu,y_simu)
	# 	plt.show()	
	return dist/length

def angularDistance(th_human,th_simu):
	length = len(th_human)	
	if abs(th_human[0]) > pi: 
		th_human = detect_discontinuity((np.array(th_human) + pi)%(2*pi)-pi)
	if abs(th_simu[0]) > pi:
		th_simu = detect_discontinuity((np.array(th_simu) + pi)%(2*pi)-pi)
	if abs((abs(th_human[0]) - pi) < 0.5 and abs(abs(th_simu[0]) - pi) < 0.5):
		if th_human[0] < 0 and th_simu[0] > 0:
			th_simu = np.array(th_simu)-2*pi
		elif th_human[0] > 0 and th_simu[0] < 0:
			th_simu = np.array(th_simu)+2*pi
	dist = 0
	for i in range(length):
		dist += abs(th_human[i]-th_simu[i])

	# if dist/length > 1:
	# 	print(dist/length)
	# 	time2 = np.linspace(1,100,500)
	# 	time = np.linspace(1,100,len(th_oc))
	# 	plt.plot(time2,th_human)
	# 	plt.plot(time,th_oc)		
	# 	plt.plot(time2,th_oc2)
	# 	plt.show()
	return dist/length

def distanceBetweenCurvs():	
	f_sub = open('Data/Traj_from_Table/traj_subjects.json')
	simu_sub = json.load(f_sub)
	f_sub1 = open('Data/Traj_from_Table/traj_sub1.json')
	human_sub1 = json.load(f_sub1)
	f_sub2 = open('Data/Traj_from_Table/traj_sub2.json')
	human_sub2 = json.load(f_sub2)
	f_table = open('Data/Traj_from_Table/traj_table.json')
	table = json.load(f_table)

	dist = {}
	dist["Linear"] = {}
	dist["Angular"] = {}
	dist["Linear"]["Sujet 1"] = []
	dist["Linear"]["Sujet 2"] = []
	dist["Angular"]["Sujet 1"] = []
	dist["Angular"]["Sujet 2"] = []		
	for traj in simu_sub:
		print("### " + traj + " ###")
		human1,human2 = human_sub1[traj],human_sub2[traj]
		simu1,simu2 = simu_sub[traj]["Sujet 1"],simu_sub[traj]["Sujet 2"]

		for i in range(len(simu1)):
			pair = simu1[i]["Binome"]
			for j in range(len(human1)):
				if human1[j]["Binome"] == pair and human1[j]["Leader"] == "Sujet 1 et 2":
					# if human2[j]["Binome"] != pair or human2[j]["Leader"] != "Sujet 1 et 2":
					# 	print("bad !") # No bad cases
					# if i%5 == 0:
					# 	print(pair)
					# 	plt.plot(human1[j]["x"],human1[j]["y"],label="human 1")
					# 	plt.plot(human2[j]["x"],human2[j]["y"],label="human 2")
					# 	plt.plot(simu1[i]["x"],simu1[i]["y"],label="simu 1")										
					# 	plt.plot(simu2[i]["x"],simu2[i]["y"],label="simu 2")
					# 	plt.plot(table[traj][i]["x"],table[traj][i]["y"],color='black')
					# 	plt.legend()
					# 	plt.show()

					dist1 = linearDistance(human1[j]["x"],human1[j]["y"],simu1[i]["x"],simu1[i]["y"])
					ang_dist1 = angularDistance(human1[j]["Orientation_Globale"],simu1[i]["Orientation_Globale"])
					dist2 = linearDistance(human2[j]["x"],human2[j]["y"],simu2[i]["x"],simu2[i]["y"])
					ang_dist2 = angularDistance(human2[j]["Orientation_Globale"],simu2[i]["Orientation_Globale"])

					dist["Linear"]["Sujet 1"].append(dist1)
					dist["Linear"]["Sujet 2"].append(dist2)					
					dist["Angular"]["Sujet 1"].append(ang_dist1)
					dist["Angular"]["Sujet 2"].append(ang_dist2)

					# if ang_dist1 > 0.5:
					# 	print(pair,"sujet 1")
					# 	plotOri(human1[j],simu1[i])	
					# if ang_dist2 > 0.5:
					# 	print(pair,"sujet 2")
					# 	plotOri(human2[j],simu2[i])										

	print("### Sujet 1 ###")
	print("linear dist : ",np.mean(dist["Linear"]["Sujet 1"]),\
		" +- ",np.std(dist["Linear"]["Sujet 1"]),\
		" | angular dist : ",np.mean(dist["Angular"]["Sujet 1"]),\
		" +- ",np.std(dist["Angular"]["Sujet 1"]))
	print("### Sujet 2 ###")
	print("linear dist : ",np.mean(dist["Linear"]["Sujet 2"]),\
		" +- ",np.std(dist["Linear"]["Sujet 2"]),\
		" | angular dist : ",np.mean(dist["Angular"]["Sujet 2"]),\
		" +- ",np.std(dist["Angular"]["Sujet 2"]))

	file_name = 'Data/Traj_from_Table/dist.json'
	json_file = json.dumps(dist, indent = 4, ensure_ascii = False)
	with open(file_name, 'w') as outfile:
		outfile.write(json_file)

########################################################################
########################## Generate Table Traj #########################
########################################################################

# trajOfInterest()

#################################################################################
############################# Generate Subjects Traj ############################
#################################################################################


# data_sub1 = np.loadtxt("Data/Human/subject1_wrt_table.dat")
# data_sub2 = np.loadtxt("Data/Human/subject2_wrt_table.dat")

# generateSubjectsTraj(data_sub1,data_sub2)

#################################################################################
################################ Compute Distances ##############################
#################################################################################

distanceBetweenCurvs()

# ### Sujet 1 ###
# linear dist :  0.08238187948826123  +-  0.05130132644407286  | angular dist :  0.5851835003424821  +-  0.25961469792743014
# ### Sujet 2 ###
# linear dist :  0.08477820642982556  +-  0.05133539558358171  | angular dist :  0.2751220096399335  +-  0.14869208918223387

#################################################################################
################################ Analyse Distances ##############################
#################################################################################

f_dist = open('Data/Traj_from_Table/dist.json')
dist = json.load(f_dist)


ind = 0
axs = ['ax1','ax2']
fig,axs = plt.subplots(1,2)

axs[0].boxplot([dist["Linear"]["Sujet 1"],dist["Linear"]["Sujet 2"]])
axs[0].set_ylabel("Linear distance (m)")
axs[0].set_xticklabels(['Subject 1', 'Subject 2'])
# axs[0].set_ylim(0, 1.)
axs[1].boxplot([dist["Angular"]["Sujet 1"],dist["Angular"]["Sujet 2"]])
axs[1].set_ylabel("Angular distance (rad)")
axs[1].set_xticklabels(['Subject 1', 'Subject 2'])
# axs[0].set_ylim(0, 1.)

plt.show()