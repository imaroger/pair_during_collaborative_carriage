import numpy as np
import matplotlib.pylab as plt
from math import pi,floor,atan2,atan, nan, sqrt
import json
from scipy.interpolate import splprep, splev, interp1d
from scipy import stats

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
		if new_theta[0] > 0:
			new_theta = -new_theta
		return new_theta
	else:
		return theta

def generate_mean_std(coord):
	mean,std = [],[]
	for i in range(len(np.transpose(coord))):	
		mean.append(np.mean(np.transpose(coord)[i]))
		std.append(np.std(np.transpose(coord)[i]))
	return mean, std

path = 'Data/Human/'
list_targets = ['d1_p4_jaune_1', 'd1_p4_gris_1', 'd1_p5_jaune_1', 'd1_p5_gris_1', 'd1_p6_jaune_1', 'd1_p6_gris_1', 'd2_p7_jaune_1', 'd2_p7_gris_1', 'd3_p7_gris_1',
				'd1_p4_jaune_2', 'd1_p4_gris_2', 'd1_p5_jaune_2', 'd1_p5_gris_2', 'd1_p6_jaune_2', 'd1_p6_gris_2', 'd2_p7_jaune_2', 'd2_p7_gris_2', 'd3_p7_gris_2']
list_leaders = ['Sujet 1','Sujet 2','Sujet 1 et 2']
list_sub = ['Sujet 1','Sujet 2','Table']

coord_wrt_table = {}
coord_wrt_table['Sujet 1'] = {}
coord_wrt_table['Sujet 2'] = {}
for leader in list_leaders:
	coord_wrt_table['Sujet 1'][leader] = {}
	coord_wrt_table['Sujet 2'][leader] = {}
	coord_wrt_table['Sujet 1'][leader]["Go"] = {}
	coord_wrt_table['Sujet 2'][leader]["Go"] = {}	
	coord_wrt_table['Sujet 1'][leader]["Return"] = {}
	coord_wrt_table['Sujet 2'][leader]["Return"] = {}	
	coord_wrt_table['Sujet 1'][leader]["Go"]["x"] = []
	coord_wrt_table['Sujet 1'][leader]["Go"]["y"] = []	
	coord_wrt_table['Sujet 1'][leader]["Go"]["theta"] = []
	coord_wrt_table['Sujet 2'][leader]["Go"]["x"] = []
	coord_wrt_table['Sujet 2'][leader]["Go"]["y"] = []	
	coord_wrt_table['Sujet 2'][leader]["Go"]["theta"] = []	
	coord_wrt_table['Sujet 1'][leader]["Return"]["x"] = []
	coord_wrt_table['Sujet 1'][leader]["Return"]["y"] = []
	coord_wrt_table['Sujet 1'][leader]["Return"]["theta"] = []
	coord_wrt_table['Sujet 2'][leader]["Return"]["x"] = []		
	coord_wrt_table['Sujet 2'][leader]["Return"]["y"] = []
	coord_wrt_table['Sujet 2'][leader]["Return"]["theta"] = []

time = np.linspace(0, 1, 500)

#################################################################################
############################## GENERATING DATA ##################################
#################################################################################

for traj in list_targets:
	print("### ",traj," ###")
	f = open(path+traj+'.json')
	data = json.load(f)['Trajectoires_Individuelles']
	for i in range(len(data["Table"])):
		xT = np.array(data["Table"][i]["x"])
		yT = np.array(data["Table"][i]["y"])
		thetaT = np.array(data["Table"][i]["Orientation_Globale"])
		x1 = np.array(data["Sujet 1"][i]["x"])
		y1 = np.array(data["Sujet 1"][i]["y"])
		theta1 = np.array(data["Sujet 1"][i]["Orientation_Globale"])
		x2 = np.array(data["Sujet 2"][i]["x"])
		y2 = np.array(data["Sujet 2"][i]["y"])
		theta2 = np.array(data["Sujet 2"][i]["Orientation_Globale"])

		x1_T = (x1-xT)*np.cos(thetaT) + (y1-yT)*np.sin(thetaT)
		y1_T = -(x1-xT)*np.sin(thetaT) + (y1-yT)*np.cos(thetaT)
		theta1_T = detect_discontinuity((theta1 - thetaT + pi)%(2*pi)-pi)
		x2_T = (x2-xT)*np.cos(thetaT) + (y2-yT)*np.sin(thetaT)
		y2_T = -(x2-xT)*np.sin(thetaT) + (y2-yT)*np.cos(thetaT)		
		theta2_T = detect_discontinuity((theta2 - thetaT + pi)%(2*pi)-pi)	

		leader = data["Table"][i]["Leader"]
		if traj[-1] == '1':
			# print("go")
			coord_wrt_table['Sujet 1'][leader]["Go"]["x"].append(x1_T)
			coord_wrt_table['Sujet 2'][leader]["Go"]["x"].append(x2_T)
			coord_wrt_table['Sujet 1'][leader]["Go"]["y"].append(y1_T)
			coord_wrt_table['Sujet 2'][leader]["Go"]["y"].append(y2_T)	
			coord_wrt_table['Sujet 1'][leader]["Go"]["theta"].append(theta1_T)
			coord_wrt_table['Sujet 2'][leader]["Go"]["theta"].append(theta2_T)							
		else:
			# print("return")
			coord_wrt_table['Sujet 1'][leader]["Return"]["x"].append(x1_T)
			coord_wrt_table['Sujet 2'][leader]["Return"]["x"].append(x2_T)
			coord_wrt_table['Sujet 1'][leader]["Return"]["y"].append(y1_T)
			coord_wrt_table['Sujet 2'][leader]["Return"]["y"].append(y2_T)
			coord_wrt_table['Sujet 1'][leader]["Return"]["theta"].append(theta1_T)
			coord_wrt_table['Sujet 2'][leader]["Return"]["theta"].append(theta2_T)											
		# print("----",len(coord_wrt_table['Sujet 1'][leader]["Go"]),len(coord_wrt_table['Sujet 1'][leader]["Return"]))

mean1_x,mean2_x,mean1_y,mean2_y, = [],[],[],[]
mean1_th_go,mean2_th_go, mean1_th_return, mean2_th_return= [],[],[],[]
std1_x,std2_x,std1_y,std2_y,std1_th,std2_th = [],[],[],[],[],[]
std1_th_go,std2_th_go, std1_th_return, std2_th_return= [],[],[],[]

# count = 1
# for leader in list_leaders:
# #leader = "Sujet 1 et 2"
# 	mean1_x, std1_x  = generate_mean_std(coord_wrt_table['Sujet 1'][leader]["Go"]["x"] + coord_wrt_table['Sujet 1'][leader]["Return"]["x"])
# 	mean2_x, std2_x  = generate_mean_std(coord_wrt_table['Sujet 2'][leader]["Go"]["x"] + coord_wrt_table['Sujet 2'][leader]["Return"]["x"])
# 	mean1_y, std1_y  = generate_mean_std(coord_wrt_table['Sujet 1'][leader]["Go"]["y"] + coord_wrt_table['Sujet 1'][leader]["Return"]["y"])
# 	mean2_y, std2_y  = generate_mean_std(coord_wrt_table['Sujet 2'][leader]["Go"]["y"] + coord_wrt_table['Sujet 2'][leader]["Return"]["y"])
# 	mean1_th_go, std1_th_go  = generate_mean_std(coord_wrt_table['Sujet 1'][leader]["Go"]["theta"])
# 	mean2_th_go, std2_th_go  = generate_mean_std(coord_wrt_table['Sujet 2'][leader]["Go"]["theta"])
# 	if leader == "Sujet 1 et 2":
# 		mean1_th_return, std1_th_return  = generate_mean_std(coord_wrt_table['Sujet 1'][leader]["Return"]["theta"])
# 		mean2_th_return, std2_th_return  = generate_mean_std(coord_wrt_table['Sujet 2'][leader]["Return"]["theta"])

# 	plt.subplot(3,4,count)
# 	plt.plot(time,mean1_x,label='Sujet 1',color='orange')
# 	plt.plot(time,mean2_x,label='Sujet 2',color='blue')
# 	plt.fill_between(time, -np.array(std1_x)+np.array(mean1_x), np.array(std1_x)+np.array(mean1_x), color='orange',alpha = 0.2)
# 	plt.fill_between(time, -np.array(std2_x)+np.array(mean2_x), np.array(std2_x)+np.array(mean2_x), color='blue',alpha = 0.2)
# 	plt.legend()	
# 	plt.title("All with leader : "+leader)
# 	plt.xlabel("time")
# 	plt.ylabel("distance from table along the x axis (m)")
# 	plt.subplot(3,4,count+1)
# 	plt.plot(time,mean1_y,label='Sujet 1',color='orange')
# 	plt.plot(time,mean2_y,label='Sujet 2',color='blue')
# 	plt.fill_between(time, -np.array(std1_y)+np.array(mean1_y), np.array(std1_y)+np.array(mean1_y), color='orange',alpha = 0.2)
# 	plt.fill_between(time, -np.array(std2_y)+np.array(mean2_y), np.array(std2_y)+np.array(mean2_y), color='blue',alpha = 0.2)
# 	plt.legend()	
# 	plt.title("All with leader : "+leader)
# 	plt.xlabel("time")
# 	plt.ylabel("distance from table along the y axis (m)")
# 	plt.subplot(3,4,count+2)
# 	plt.plot(time,mean1_th_go,label='Sujet 1',color='orange')
# 	plt.plot(time,mean2_th_go,label='Sujet 2',color='blue')
# 	plt.fill_between(time, -np.array(std1_th_go)+np.array(mean1_th_go), np.array(std1_th_go)+np.array(mean1_th_go), color='orange',alpha = 0.2)
# 	plt.fill_between(time, -np.array(std2_th_go)+np.array(mean2_th_go), np.array(std2_th_go)+np.array(mean2_th_go), color='blue',alpha = 0.2)
# 	plt.legend()	
# 	plt.title("Go with leader : "+leader)
# 	plt.xlabel("time")
# 	plt.ylabel("angle with table around the z axis (rad)")
# 	plt.subplot(3,4,count+3)
# 	if leader == "Sujet 1 et 2":
# 		plt.plot(time,mean1_th_return,label='Sujet 1',color='orange')
# 		plt.plot(time,mean2_th_return,label='Sujet 2',color='blue')
# 		plt.fill_between(time, -np.array(std1_th_return)+np.array(mean1_th_return), np.array(std1_th_return)+np.array(mean1_th_return), color='orange',alpha = 0.2)
# 		plt.fill_between(time, -np.array(std2_th_return)+np.array(mean2_th_return), np.array(std2_th_return)+np.array(mean2_th_return), color='blue',alpha = 0.2)
# 		plt.legend()	
# 		plt.title("Return with leader : "+leader)
# 		plt.xlabel("time")
# 		plt.ylabel("angle with table around the z axis (rad)")
# 	count += 4

# plt.show()

# plt.subplot(2,2,1)
# for i in range(len(coord_wrt_table['Sujet 1'][leader]["Go"]["theta"])):	
# 	plt.plot(coord_wrt_table['Sujet 1'][leader]["Go"]["theta"][i],linewidth = 0.2)
# plt.plot(mean1_th_go,color = 'black')
# plt.subplot(2,2,2)
# for i in range(len(coord_wrt_table['Sujet 1'][leader]["Return"]["theta"])):		
# 	plt.plot(coord_wrt_table['Sujet 1'][leader]["Return"]["theta"][i],linewidth = 0.2)
# plt.plot(mean1_th_return,color = 'black')
# plt.subplot(2,2,3)
# for i in range(len(coord_wrt_table['Sujet 2'][leader]["Go"]["theta"])):	
# 	plt.plot(coord_wrt_table['Sujet 2'][leader]["Go"]["theta"][i],linewidth = 0.2)
# plt.plot(mean2_th_go,color = 'black')
# plt.subplot(2,2,4)
# for i in range(len(coord_wrt_table['Sujet 2'][leader]["Return"]["theta"])):		
# 	plt.plot(coord_wrt_table['Sujet 2'][leader]["Return"]["theta"][i],linewidth = 0.2)
# plt.plot(mean2_th_return,color = 'black')
# plt.show()

# leader = "Sujet 1 et 2"

#################################################################################
############################## PLOT EVOLUTIONS ##################################
#################################################################################


# linestyles = {"Sujet 1":"dotted","Sujet 2":"dashed","Sujet 1 et 2":"solid"}
# leaders = {"Sujet 1":" (Scenario 1)","Sujet 2":" (Scenario 2)","Sujet 1 et 2":" (Scenario 3)"}

# for leader in list_leaders:
# 	mean1_x_go, std1_x_go  = generate_mean_std(coord_wrt_table['Sujet 1'][leader]["Go"]["x"])
# 	mean2_x_go, std2_x_go  = generate_mean_std(coord_wrt_table['Sujet 2'][leader]["Go"]["x"])
# 	mean1_y_go, std1_y_go  = generate_mean_std(coord_wrt_table['Sujet 1'][leader]["Go"]["y"])
# 	mean2_y_go, std2_y_go  = generate_mean_std(coord_wrt_table['Sujet 2'][leader]["Go"]["y"])
# 	mean1_th_go, std1_th_go  = generate_mean_std(coord_wrt_table['Sujet 1'][leader]["Go"]["theta"])
# 	mean2_th_go, std2_th_go  = generate_mean_std(coord_wrt_table['Sujet 2'][leader]["Go"]["theta"])

# 	if leader == "Sujet 1 et 2":
# 		mean1_x_return, std1_x_return  = generate_mean_std(coord_wrt_table['Sujet 1'][leader]["Return"]["x"])
# 		mean2_x_return, std2_x_return  = generate_mean_std(coord_wrt_table['Sujet 2'][leader]["Return"]["x"])
# 		mean1_y_return, std1_y_return  = generate_mean_std(coord_wrt_table['Sujet 1'][leader]["Return"]["y"])
# 		mean2_y_return, std2_y_return  = generate_mean_std(coord_wrt_table['Sujet 2'][leader]["Return"]["y"])
# 		mean1_th_return, std1_th_return  = generate_mean_std(coord_wrt_table['Sujet 1'][leader]["Return"]["theta"])
# 		mean2_th_return, std2_th_return  = generate_mean_std(coord_wrt_table['Sujet 2'][leader]["Return"]["theta"])	

# 	plt.subplot(2,3,1)
# 	plt.plot(time,mean1_x_go,label='Subject 1'+leaders[leader],color='orange',linestyle=linestyles[leader])
# 	plt.plot(time,np.array(mean2_x_go),label='Subject 2'+leaders[leader],color='blue',linestyle=linestyles[leader])	
# 	plt.title("Forward path (x)")
# 	plt.xlabel("Normalized time")
# 	plt.ylabel("Distance from table along the x axis (m)")
# 	plt.legend()
# 	plt.subplot(2,3,2)
# 	plt.plot(time,mean1_y_go,label='Subject 1'+leaders[leader],color='orange',linestyle=linestyles[leader])
# 	plt.plot(time,mean2_y_go,label='Subject 2'+leaders[leader],color='blue',linestyle=linestyles[leader])
# 	plt.title("Forward path (y)")
# 	plt.xlabel("Normalized time")
# 	plt.ylabel("Distance from table along the y axis (m)")
# 	plt.legend()
# 	plt.subplot(2,3,3)
# 	plt.plot(time,mean1_th_go,label='Subject 1'+leaders[leader],color='orange',linestyle=linestyles[leader])
# 	plt.plot(time,mean2_th_go,label='Subject 2'+leaders[leader],color='blue',linestyle=linestyles[leader])
# 	plt.title("Forward path (theta)")
# 	plt.xlabel("Normalized time")
# 	plt.ylabel("Angle with table around the z axis (rad)")
# 	plt.legend()		
# 	if leader == "Sujet 1 et 2":
# 		plt.subplot(2,3,4)
# 		plt.plot(time,mean1_x_return,label='Subject 1',color='orange')
# 		plt.plot(time,np.array(mean2_x_return),label='Subject 2',color='blue')	
# 		plt.fill_between(time, -np.array(std1_x_return)+np.array(mean1_x_return), np.array(std1_x_return)+np.array(mean1_x_return), color='orange',alpha = 0.2)
# 		plt.fill_between(time, -np.array(std2_x_return)+np.array(mean2_x_return), np.array(std2_x_return)+np.array(mean2_x_return), color='blue',alpha = 0.2)
# 		plt.title("Return path (x)")
# 		plt.xlabel("Normalized time")
# 		plt.ylabel("Distance from table along the x axis (m)")	
# 		plt.legend()
# 		plt.subplot(2,3,5)
# 		plt.plot(time,mean1_y_return,label='Subject 1',color='orange')
# 		plt.plot(time,mean2_y_return,label='Subject 2',color='blue')
# 		plt.fill_between(time, -np.array(std1_y_return)+np.array(mean1_y_return), np.array(std1_y_return)+np.array(mean1_y_return), color='orange',alpha = 0.2)
# 		plt.fill_between(time, -np.array(std2_y_return)+np.array(mean2_y_return), np.array(std2_y_return)+np.array(mean2_y_return), color='blue',alpha = 0.2)		
# 		plt.title("Return path (y)")
# 		plt.xlabel("Normalized time")
# 		plt.ylabel("Distance from table along the y axis (m)")	
# 		plt.legend()
# 		plt.subplot(2,3,6)
# 		plt.plot(time,mean1_th_return,label='Subject 1',color='orange')
# 		plt.plot(time,mean2_th_return,label='Subject 2',color='blue')	
# 		plt.fill_between(time, -np.array(std1_th_return)+np.array(mean1_th_return), np.array(std1_th_return)+np.array(mean1_th_return), color='orange',alpha = 0.2)
# 		plt.fill_between(time, -np.array(std2_th_return)+np.array(mean2_th_return), np.array(std2_th_return)+np.array(mean2_th_return), color='blue',alpha = 0.2)		
# 		plt.title("Return path (theta)")
# 		plt.xlabel("Normalized time")
# 		plt.ylabel("Angle with table around the z axis (rad)")	
# 		plt.legend()		

# #### Add mean and std ####

# # x1_go = coord_wrt_table['Sujet 1']["Sujet 1"]["Go"]["x"]+\
# # 	coord_wrt_table['Sujet 1']["Sujet 2"]["Go"]["x"]+\
# # 	coord_wrt_table['Sujet 1']["Sujet 1 et 2"]["Go"]["x"]
# # x2_go = coord_wrt_table['Sujet 2']["Sujet 1"]["Go"]["x"]+\
# # 	coord_wrt_table['Sujet 2']["Sujet 2"]["Go"]["x"]+\
# # 	coord_wrt_table['Sujet 2']["Sujet 1 et 2"]["Go"]["x"]
# # mean1_x_go, std1_x_go  = generate_mean_std(x1_go)
# # mean2_x_go, std2_x_go  = generate_mean_std(x2_go)
# # plt.subplot(2,3,1)
# # plt.plot(time,mean1_x_go,label='Subject 1 (average)',color='red')
# # plt.plot(time,mean2_x_go,label='Subject 2 (average)',color='cyan')
# # plt.fill_between(time, -np.array(std1_x_go)+np.array(mean1_x_go), np.array(std1_x_go)+np.array(mean1_x_go), color='red',alpha = 0.2)
# # plt.fill_between(time, -np.array(std2_x_go)+np.array(mean2_x_go), np.array(std2_x_go)+np.array(mean2_x_go), color='cyan',alpha = 0.2)
# # plt.legend()

# # y1_go = coord_wrt_table['Sujet 1']["Sujet 1"]["Go"]["y"]+\
# # 	coord_wrt_table['Sujet 1']["Sujet 2"]["Go"]["y"]+\
# # 	coord_wrt_table['Sujet 1']["Sujet 1 et 2"]["Go"]["y"]
# # y2_go = coord_wrt_table['Sujet 2']["Sujet 1"]["Go"]["y"]+\
# # 	coord_wrt_table['Sujet 2']["Sujet 2"]["Go"]["y"]+\
# # 	coord_wrt_table['Sujet 2']["Sujet 1 et 2"]["Go"]["y"]	
# # mean1_y_go, std1_y_go  = generate_mean_std(y1_go)
# # mean2_y_go, std2_y_go  = generate_mean_std(y2_go)
# # plt.subplot(2,3,2)
# # plt.plot(time,mean1_y_go,label='Subject 1 (average)',color='red')
# # plt.plot(time,mean2_y_go,label='Subject 2 (average)',color='cyan')
# # plt.fill_between(time, -np.array(std1_y_go)+np.array(mean1_y_go), np.array(std1_y_go)+np.array(mean1_y_go), color='red',alpha = 0.2)
# # plt.fill_between(time, -np.array(std2_y_go)+np.array(mean2_y_go), np.array(std2_y_go)+np.array(mean2_y_go), color='cyan',alpha = 0.2)
# # plt.legend()

# # th1_go = coord_wrt_table['Sujet 1']["Sujet 1"]["Go"]["theta"]+\
# # 	coord_wrt_table['Sujet 1']["Sujet 2"]["Go"]["theta"]+\
# # 	coord_wrt_table['Sujet 1']["Sujet 1 et 2"]["Go"]["theta"]
# # th2_go = coord_wrt_table['Sujet 2']["Sujet 1"]["Go"]["theta"]+\
# # 	coord_wrt_table['Sujet 2']["Sujet 2"]["Go"]["theta"]+\
# # 	coord_wrt_table['Sujet 2']["Sujet 1 et 2"]["Go"]["theta"]
# # mean1_th_go, std1_th_go  = generate_mean_std(th1_go)
# # mean2_th_go, std2_th_go  = generate_mean_std(th2_go)	
# # plt.subplot(2,3,3)	

# # plt.plot(time,mean1_th_go,label='Subject 1 (average)',color='red')
# # plt.plot(time,mean2_th_go,label='Subject 2 (average)',color='cyan')
# # plt.fill_between(time, -np.array(std1_th_go)+np.array(mean1_th_go), np.array(std1_th_go)+np.array(mean1_th_go), color='red',alpha = 0.2)
# # plt.fill_between(time, -np.array(std2_th_go)+np.array(mean2_th_go), np.array(std2_th_go)+np.array(mean2_th_go), color='cyan',alpha = 0.2)
# # plt.legend()

# plt.show()
#################################################################################
########################## PLOT EVOLUTIONS (small) ##############################
#################################################################################

linestyles = {"Sujet 1":"dotted","Sujet 2":"dashed","Sujet 1 et 2":"solid"}
leaders = {"Sujet 1":" (Forward - Sc 1)","Sujet 2":" (Forward - Sc 2)","Sujet 1 et 2":" (Forward - Sc 3)"}

for leader in list_leaders:
	mean1_x_go, std1_x_go  = generate_mean_std(coord_wrt_table['Sujet 1'][leader]["Go"]["x"])
	mean2_x_go, std2_x_go  = generate_mean_std(coord_wrt_table['Sujet 2'][leader]["Go"]["x"])
	mean1_y_go, std1_y_go  = generate_mean_std(coord_wrt_table['Sujet 1'][leader]["Go"]["y"])
	mean2_y_go, std2_y_go  = generate_mean_std(coord_wrt_table['Sujet 2'][leader]["Go"]["y"])
	mean1_th_go, std1_th_go  = generate_mean_std(coord_wrt_table['Sujet 1'][leader]["Go"]["theta"])
	mean2_th_go, std2_th_go  = generate_mean_std(coord_wrt_table['Sujet 2'][leader]["Go"]["theta"])

	if leader == "Sujet 1 et 2":
		mean1_x_return, std1_x_return  = generate_mean_std(coord_wrt_table['Sujet 1'][leader]["Return"]["x"])
		mean2_x_return, std2_x_return  = generate_mean_std(coord_wrt_table['Sujet 2'][leader]["Return"]["x"])
		mean1_y_return, std1_y_return  = generate_mean_std(coord_wrt_table['Sujet 1'][leader]["Return"]["y"])
		mean2_y_return, std2_y_return  = generate_mean_std(coord_wrt_table['Sujet 2'][leader]["Return"]["y"])
		mean1_th_return, std1_th_return  = generate_mean_std(coord_wrt_table['Sujet 1'][leader]["Return"]["theta"])
		mean2_th_return, std2_th_return  = generate_mean_std(coord_wrt_table['Sujet 2'][leader]["Return"]["theta"])	

	plt.subplot(1,3,1)
	plt.plot(time,mean1_x_go,label='Sub 1'+leaders[leader],color='orange',linestyle=linestyles[leader])
	plt.plot(time,np.array(mean2_x_go),label='Sub 2'+leaders[leader],color='blue',linestyle=linestyles[leader])	
	plt.xlabel("Normalized time",fontsize='large')
	plt.ylabel("Distance from table along the x axis (m)",fontsize='large')
	plt.legend(fontsize='large', ncol=1)
	plt.subplot(1,3,2)
	plt.plot(time,mean1_y_go,label='Sub 1'+leaders[leader],color='orange',linestyle=linestyles[leader])
	plt.plot(time,mean2_y_go,label='Sub 2'+leaders[leader],color='blue',linestyle=linestyles[leader])
	plt.xlabel("Normalized time",fontsize='large')
	plt.ylabel("Distance from table along the y axis (m)",fontsize='large')
	plt.legend(fontsize='large', ncol=1)
	# plt.ylim(-0.25,0.25)
	plt.subplot(1,3,3)
	plt.plot(time,mean1_th_go,label='Sub 1'+leaders[leader],color='orange',linestyle=linestyles[leader])
	plt.plot(time,mean2_th_go,label='Sub 2'+leaders[leader],color='blue',linestyle=linestyles[leader])
	plt.xlabel("Normalized time",fontsize='large')
	plt.ylabel("Angle with table around the z axis (rad)",fontsize='large')
	plt.legend(fontsize='large', ncol=1)		
	if leader == "Sujet 1 et 2":
		plt.subplot(1,3,1)
		plt.plot(time,mean1_x_return,label='Sub 1 (Return - Sc 3)',color='red')
		plt.plot(time,np.array(mean2_x_return),label='Sub 2 (Return - Sc 3)',color='green')	
		plt.xlabel("Normalized time",fontsize='large')
		plt.ylabel("Distance from table along the x axis (m)",fontsize='large')	
		plt.legend(fontsize='large', ncol=1)
		plt.subplot(1,3,2)
		plt.plot(time,mean1_y_return,label='Sub 1 (Return - Sc 3)',color='red')
		plt.plot(time,mean2_y_return,label='Sub 2 (Return - Sc 3)',color='green')
		plt.xlabel("Normalized time",fontsize='large')
		plt.ylabel("Distance from table along the y axis (m)",fontsize='large')	
		plt.legend(fontsize='large', ncol=1)
		# plt.ylim(-0.25,0.25)
		plt.subplot(1,3,3)
		plt.plot(time,mean1_th_return,label='Sub 1 (Return - Sc 3)',color='red')
		plt.plot(time,mean2_th_return,label='Sub 2 (Return - Sc 3)',color='green')	
		plt.xlabel("Normalized time",fontsize='large')
		plt.ylabel("Angle with table around the z axis (rad)",fontsize='large')	
		plt.legend(fontsize='large', ncol=1)		

plt.show()
#################################################################################
################################## STATISTICS ###################################
#################################################################################

# x_mean1,y_mean1,th_mean1 = [],[],[]
# x_mean2,y_mean2,th_mean2 = [],[],[]
# x_std,y_std,th_std = [],[],[]

# for leader in list_leaders:
# 	mean1_x_go, std1_x_go  = generate_mean_std(coord_wrt_table['Sujet 1'][leader]["Go"]["x"])
# 	mean2_x_go, std2_x_go  = generate_mean_std(coord_wrt_table['Sujet 2'][leader]["Go"]["x"])
# 	mean1_y_go, std1_y_go  = generate_mean_std(coord_wrt_table['Sujet 1'][leader]["Go"]["y"])
# 	mean2_y_go, std2_y_go  = generate_mean_std(coord_wrt_table['Sujet 2'][leader]["Go"]["y"])
# 	mean1_th_go, std1_th_go  = generate_mean_std(coord_wrt_table['Sujet 1'][leader]["Go"]["theta"])
# 	mean2_th_go, std2_th_go  = generate_mean_std(coord_wrt_table['Sujet 2'][leader]["Go"]["theta"])

# 	x_std.append(np.mean(std1_x_go))
# 	x_std.append(np.mean(std2_x_go))
# 	y_std.append(np.mean(std1_y_go))
# 	y_std.append(np.mean(std2_y_go))
# 	th_std.append(np.mean(std1_th_go))
# 	th_std.append(np.mean(std2_th_go))

# 	time_int = np.linspace(0,1,50)
# 	x_mean1.append(np.interp(time_int,time,mean1_x_go))
# 	y_mean1.append(np.interp(time_int,time,mean1_y_go))
# 	x_mean2.append(np.interp(time_int,time,mean2_x_go))
# 	y_mean2.append(np.interp(time_int,time,mean2_y_go))	
# 	th_mean1.append(np.interp(time_int,time,mean1_th_go))
# 	th_mean2.append(np.interp(time_int,time,mean2_th_go))		
# 	if leader == "Sujet 1 et 2":
# 		mean1_x_return, std1_x_return  = generate_mean_std(coord_wrt_table['Sujet 1'][leader]["Return"]["x"])
# 		mean2_x_return, std2_x_return  = generate_mean_std(coord_wrt_table['Sujet 2'][leader]["Return"]["x"])
# 		mean1_y_return, std1_y_return  = generate_mean_std(coord_wrt_table['Sujet 1'][leader]["Return"]["y"])
# 		mean2_y_return, std2_y_return  = generate_mean_std(coord_wrt_table['Sujet 2'][leader]["Return"]["y"])
# 		mean1_th_return, std1_th_return  = generate_mean_std(coord_wrt_table['Sujet 1'][leader]["Return"]["theta"])
# 		mean2_th_return, std2_th_return  = generate_mean_std(coord_wrt_table['Sujet 2'][leader]["Return"]["theta"])
# 		x_mean1.append(np.interp(time_int,time,mean1_x_return))
# 		y_mean1.append(np.interp(time_int,time,mean1_y_return))	
# 		x_mean2.append(np.interp(time_int,time,mean2_x_return))
# 		y_mean2.append(np.interp(time_int,time,mean2_y_return))	

# 		x_std.append(np.mean(std1_x_return))
# 		x_std.append(np.mean(std2_x_return))
# 		y_std.append(np.mean(std1_y_return))
# 		y_std.append(np.mean(std2_y_return))
# 		th_std.append(np.mean(std1_th_return))
# 		th_std.append(np.mean(std2_th_return))

# print("mean std x : ",np.mean(x_std))
# print("mean std y : ",np.mean(y_std))
# print("mean std th : ",np.mean(th_std))

# print("### kruskal_test for all : Significant difference if p < 0.05 ###")
# kruskal_test = stats.kruskal(x_mean1[0],x_mean1[1],x_mean1[2],x_mean1[3])
# print("x sub1 : ",kruskal_test)	
# kruskal_test = stats.kruskal(x_mean2[0],x_mean2[1],x_mean2[2],x_mean2[3])
# print("x sub2 : ",kruskal_test)

# kruskal_test = stats.kruskal(y_mean1[0],y_mean1[1],y_mean1[2],y_mean1[3])
# print("y sub1 : ",kruskal_test)	
# kruskal_test = stats.kruskal(y_mean2[0],y_mean2[1],y_mean2[2],y_mean2[3])
# print("y sub2 : ",kruskal_test)	

# kruskal_test = stats.kruskal(th_mean1[0],th_mean1[1],th_mean1[2])
# print("th sub1 : ",kruskal_test)	
# kruskal_test = stats.kruskal(th_mean2[0],th_mean2[1],th_mean2[2])
# print("th sub2 : ",kruskal_test)	

#################################################################################
############################## GENERATING FILES #################################
#################################################################################

# leader = "Sujet 1 et 2"
# mean1_x_go, std1_x_go  = generate_mean_std(coord_wrt_table['Sujet 1'][leader]["Go"]["x"])
# mean2_x_go, std2_x_go  = generate_mean_std(coord_wrt_table['Sujet 2'][leader]["Go"]["x"])
# mean1_y_go, std1_y_go  = generate_mean_std(coord_wrt_table['Sujet 1'][leader]["Go"]["y"])
# mean2_y_go, std2_y_go  = generate_mean_std(coord_wrt_table['Sujet 2'][leader]["Go"]["y"])
# mean1_th_go, std1_th_go  = generate_mean_std(coord_wrt_table['Sujet 1'][leader]["Go"]["theta"])
# mean2_th_go, std2_th_go  = generate_mean_std(coord_wrt_table['Sujet 2'][leader]["Go"]["theta"])
# mean1_x_return, std1_x_return  = generate_mean_std(coord_wrt_table['Sujet 1'][leader]["Return"]["x"])
# mean2_x_return, std2_x_return  = generate_mean_std(coord_wrt_table['Sujet 2'][leader]["Return"]["x"])
# mean1_y_return, std1_y_return  = generate_mean_std(coord_wrt_table['Sujet 1'][leader]["Return"]["y"])
# mean2_y_return, std2_y_return  = generate_mean_std(coord_wrt_table['Sujet 2'][leader]["Return"]["y"])
# mean1_th_return, std1_th_return  = generate_mean_std(coord_wrt_table['Sujet 1'][leader]["Return"]["theta"])
# mean2_th_return, std2_th_return  = generate_mean_std(coord_wrt_table['Sujet 2'][leader]["Return"]["theta"])

# # data1 = [mean1_x,mean1_y,mean1_th_go,mean1_th_return]
# # data2 = [mean2_x,mean2_y,mean2_th_go,mean2_th_return]
# data1 = [mean1_x_go,mean1_x_return,mean1_y_go,mean1_y_return,mean1_th_go,mean1_th_return]
# data2 = [mean2_x_go,mean2_x_return,mean2_y_go,mean2_y_return,mean2_th_go,mean2_th_return]

# np.savetxt(path+"subject1_wrt_table.dat",data1)
# np.savetxt(path+"subject2_wrt_table.dat",data2)

#################################################################################
################################## CHECKING #####################################
#################################################################################

# data1 = np.loadtxt(path+"subject1_wrt_table.dat")
# data2 = np.loadtxt(path+"subject2_wrt_table.dat")

# x = time
# y = 2*time+1
# th = np.linspace(0, pi/2,len(time))

# x1, y1, th1 = np.array(data1[0]),np.array(data1[2]),np.array(data1[4])
# x2, y2, th2 = np.array(data2[0]),np.array(data2[2]),np.array(data2[4])
# new_x1,new_y1 = x+x1*np.cos(th)-y1*np.sin(th),y+x1*np.sin(th)+y1*np.cos(th)
# new_x2,new_y2 = x+x2*np.cos(th)-y2*np.sin(th),y+x2*np.sin(th)+y2*np.cos(th)

# plt.subplot(1,2,1)
# plt.plot(x,y, color = 'red',label = 'table')
# plt.plot(new_x1,new_y1,color = 'blue',label = "Subject 1")
# plt.plot(new_x2,new_y2,color = 'green',label = "Subject 2")
# arrow_len = 0.2
# for i in range (len(x)):
# 	if i%25 == 0:
# 		plt.arrow(x[i], y[i],\
# 			np.cos(th[i])*arrow_len,\
# 			np.sin(th[i])*arrow_len, head_width=.05, color = 'red')
# 		plt.arrow(new_x1[i],new_y1[i],\
# 			np.cos(th1[i]+th[i])*arrow_len,\
# 			np.sin(th1[i]+th[i])*arrow_len, head_width=.05, color = 'blue')
# 		plt.arrow(new_x2[i],new_y2[i],\
# 			np.cos(th2[i]+th[i])*arrow_len,\
# 			np.sin(th2[i]+th[i])*arrow_len, head_width=.05, color = 'green')
# plt.legend()
# plt.title("Go")

# x1, y1, th1 = np.array(data1[1]),np.array(data1[3]),np.array(data1[5])
# x2, y2, th2 = np.array(data2[1]),np.array(data2[3]),np.array(data2[5])
# new_x1,new_y1 = x+x1*np.cos(th)-y1*np.sin(th),y+x1*np.sin(th)+y1*np.cos(th)
# new_x2,new_y2 = x+x2*np.cos(th)-y2*np.sin(th),y+x2*np.sin(th)+y2*np.cos(th)

# plt.subplot(1,2,2)
# # x = np.flip(x)
# # y = np.flip(y)
# # th = np.flip(th)
# plt.plot(x,y, color = 'red',label = 'table')
# plt.plot(new_x1,new_y1,color = 'blue',label = "Subject 1")
# plt.plot(new_x2,new_y2,color = 'green',label = "Subject 2")
# arrow_len = 0.2
# for i in range (len(x)):
# 	if i%25 == 0:
# 		plt.arrow(x[i], y[i],\
# 			np.cos(th[i])*arrow_len,\
# 			np.sin(th[i])*arrow_len, head_width=.05, color = 'red')
# 		plt.arrow(new_x1[i],new_y1[i],\
# 			np.cos(th1[i]+th[i])*arrow_len,\
# 			np.sin(th1[i]+th[i])*arrow_len, head_width=.05, color = 'blue')
# 		plt.arrow(new_x2[i],new_y2[i],\
# 			np.cos(th2[i]+th[i])*arrow_len,\
# 			np.sin(th2[i]+th[i])*arrow_len, head_width=.05, color = 'green')
# plt.legend()
# plt.title("Return")
# plt.show()