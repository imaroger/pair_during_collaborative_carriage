
import numpy as np
import matplotlib.pylab as plt
from math import pi, floor, sqrt, cos, sin, atan2, exp
from scipy.optimize import minimize
from scipy.interpolate import splprep, splev
import time
import json
import os
from scipy import stats

plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['ps.fonttype'] = 42


#########################################################################
########################## FUNCTION DEFINITION	#########################
#########################################################################
def normalizeAngle(angle): 
	new_angle = angle
	while new_angle > pi:
		new_angle -= 2*pi
	while new_angle < -pi:
		new_angle += 2*pi
	return new_angle	

def linearDistance(x_human,y_human,x_oc,y_oc):
	length = len(x_human)
	# print(len(x_oc),x_oc)
	# okay1 = np.where(np.abs(np.diff(x_human)) + np.abs(np.diff(x_human)) > 0)
	okay2 = np.where(np.abs(np.diff(x_oc)) + np.abs(np.diff(y_oc)) > 0)	
	# x_human,y_human = x_human[okay1],y_human[okay1]
	# print(length,okay2)
	x_oc,y_oc = x_oc[okay2],y_oc[okay2]	

	tck1, u1 = splprep([x_human, y_human], s = 0)
	tck2, u2 = splprep([x_oc, y_oc], s = 0)
	xnew = np.linspace(0, 1, length)
	x_human, y_human = splev(xnew, tck1)
	x_oc, y_oc = splev(xnew, tck2)

	dist = 0
	for i in range(length):
		dist += sqrt((x_human[i]-x_oc[i])**2+(y_human[i]-y_oc[i])**2)

		# if i%25 == 0:
		# 	plt.plot([x_human[i],x_oc[i]], [y_human[i],y_oc[i]], color = 'red', linewidth = 0.5)
	# if dist/length > 1:
	# 	print(dist/length)
	# 	plt.plot(x_human,y_human)
	# 	plt.plot(x_oc,y_oc)
	# 	plt.show()	
	return dist/length

def angularDistance(th_human,th_oc):
	length = len(th_human)	
	th_oc2 = np.interp(np.arange(0,length,1),np.linspace(0,length,len(th_oc)),th_oc)

	dist = 0
	for i in range(length):
		dist += abs(th_human[i]-th_oc2[i])

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
	print("------- Compute Distance -------")
	leader = "Sujet 1 et 2"

	dist_go, ang_dist_go,dist_return, ang_dist_return = {},{},{},{}
	dist_go_end, ang_dist_go_end,dist_return_end, ang_dist_return_end = {},{},{},{}	
	list_sub = ['Sujet 1','Sujet 2']
	for sub in list_sub:
		dist_go[sub], ang_dist_go[sub],dist_return[sub], ang_dist_return[sub] = [],[],[],[]
		dist_go_end[sub], ang_dist_go_end[sub],dist_return_end[sub], ang_dist_return_end[sub] = [],[],[],[]

	for traj in list_trajs:
		human_path = "Data/Human/" + traj + "_1_mean.json"
		f = open(human_path)
		human = json.load(f)['Trajectoires_Moyennes']
		for ori in human['Table'][leader]:
			# print(ori)
			sub1 = human['Sujet 1'][leader][ori]
			sub2 = human['Sujet 2'][leader][ori]
			oc = np.transpose(np.loadtxt("Data/CoupledOptimalControl/" + traj + "_1_" + leader + "_" + str(ori[23:min(28,len(ori))]) + ".dat"))

			dist_go["Sujet 1"].append(linearDistance(sub1["x"], sub1["y"], oc[0], oc[1]))
			dist_go["Sujet 2"].append(linearDistance(sub2["x"], sub2["y"], oc[3], oc[4]))			

			ang_dist_go["Sujet 1"].append(angularDistance(sub1["Orientation_Globale"], oc[2]))
			ang_dist_go["Sujet 2"].append(angularDistance(sub2["Orientation_Globale"], oc[5]))				

			dist_go_end["Sujet 1"].append(sqrt((sub1["x"][-1]-oc[0][-1])**2+(sub1["y"][-1]-oc[1][-1])**2))
			dist_go_end["Sujet 2"].append(sqrt((sub2["x"][-1]-oc[3][-1])**2+(sub2["y"][-1]-oc[4][-1])**2))

			ang_dist_go_end["Sujet 1"].append(abs(sub1["Orientation_Globale"][-1]-normalizeAngle(oc[2][-1])))
			ang_dist_go_end["Sujet 2"].append(abs(sub2["Orientation_Globale"][-1]-normalizeAngle(oc[5][-1])))

		human_path = "Data/Human/" + traj + "_2_mean.json"
		f = open(human_path)
		human = json.load(f)['Trajectoires_Moyennes']
		for ori in human['Table']["All data"]:
			# print(ori)
			sub1 = human['Sujet 1']["All data"][ori]
			sub2 = human['Sujet 2']["All data"][ori]
			oc = np.transpose(np.loadtxt("Data/CoupledOptimalControl/" + traj + "_2_" + leader + "_" + str(ori[24:min(29,len(ori))]) + ".dat"))

			dist_return["Sujet 2"].append(linearDistance(sub2["x"], sub2["y"], oc[0], oc[1]))				
			dist_return["Sujet 1"].append(linearDistance(sub1["x"], sub1["y"], oc[3], oc[4]))							

			ang_dist_return["Sujet 2"].append(angularDistance(sub2["Orientation_Globale"], oc[2]))
			ang_dist_return["Sujet 1"].append(angularDistance(sub1["Orientation_Globale"], oc[5]))							

			dist_return_end["Sujet 2"].append(sqrt((sub2["x"][-1]-oc[0][-1])**2+(sub2["y"][-1]-oc[1][-1])**2))
			dist_return_end["Sujet 1"].append(sqrt((sub1["x"][-1]-oc[3][-1])**2+(sub1["y"][-1]-oc[4][-1])**2))

			ang_dist_return_end["Sujet 2"].append(abs(sub2["Orientation_Globale"][-1]-normalizeAngle(oc[2][-1])))
			ang_dist_return_end["Sujet 1"].append(abs(sub1["Orientation_Globale"][-1]-normalizeAngle(oc[5][-1])))

	return (dist_go, ang_dist_go,dist_return, ang_dist_return,dist_go_end, ang_dist_go_end,dist_return_end, ang_dist_return_end)

########################################################################
################################## MAIN ################################
########################################################################

path = 'Data/Human/'
list_trajs = ['d1_p4_jaune', 'd1_p4_gris', 'd1_p5_jaune', 'd1_p5_gris', 'd1_p6_jaune', 'd1_p6_gris', 'd2_p7_jaune', 'd2_p7_gris', 'd3_p7_gris']

dist_go, ang_dist_go,dist_return, ang_dist_return,\
	dist_go_end, ang_dist_go_end,dist_return_end, ang_dist_return_end = \
	distanceBetweenCurvs()

print("--- Go ---")
print("-> Sujet 1")
print("d_lin = ",np.mean(dist_go["Sujet 1"])," +- ",np.std(dist_go["Sujet 1"]))
print("d_ang = ",np.mean(ang_dist_go["Sujet 1"])," +- ",np.std(ang_dist_go["Sujet 1"]))
# print("end lin = ",np.mean(dist_go_end["Sujet 1"])," , ang = ",np.mean(ang_dist_go_end["Sujet 1"]))
print("-> Sujet 2")
print("d_lin = ",np.mean(dist_go["Sujet 2"])," +- ",np.std(dist_go["Sujet 2"]))
print("d_ang = ",np.mean(ang_dist_go["Sujet 2"])," +- ",np.std(ang_dist_go["Sujet 2"]))
# print("end lin = ",np.mean(dist_go_end["Sujet 2"])," , ang = ",np.mean(ang_dist_go_end["Sujet 2"]))
print("-> All")
print("d_lin = ",np.mean(dist_go["Sujet 1"]+dist_go["Sujet 2"])," +- ",np.std(dist_go["Sujet 1"]+dist_go["Sujet 2"]))
print("d_ang = ",np.mean(ang_dist_go["Sujet 1"]+ang_dist_go["Sujet 2"])," +- ",np.std(ang_dist_go["Sujet 1"]+ang_dist_go["Sujet 2"]))

print("end lin = ",np.mean(dist_go_end["Sujet 1"]+dist_go_end["Sujet 2"]),\
	" , ang = ",np.mean(ang_dist_go_end["Sujet 1"]+ang_dist_go_end["Sujet 2"]))


print("--- Return ---")
print("-> Sujet 1")
print("d_lin = ",np.mean(dist_return["Sujet 1"])," +- ",np.std(dist_return["Sujet 1"]))
print("d_ang = ",np.mean(ang_dist_return["Sujet 1"])," +- ",np.std(ang_dist_return["Sujet 1"]))
# print("end lin = ",np.mean(dist_return_end["Sujet 1"])," , ang = ",np.mean(ang_dist_return_end["Sujet 1"]))
print("-> Sujet 2")
print("d_lin = ",np.mean(dist_return["Sujet 2"])," +- ",np.std(dist_return["Sujet 2"]))
print("d_ang = ",np.mean(ang_dist_return["Sujet 2"])," +- ",np.std(ang_dist_return["Sujet 2"]))
# print("end lin = ",np.mean(dist_return_end["Sujet 2"])," , ang = ",np.mean(ang_dist_return_end["Sujet 2"]))
print("-> All")
print("d_lin = ",np.mean(dist_return["Sujet 1"]+dist_return["Sujet 2"])," +- ",np.std(dist_return["Sujet 1"]+dist_return["Sujet 2"]))
print("d_ang = ",np.mean(ang_dist_return["Sujet 1"]+ang_dist_return["Sujet 2"])," +- ",np.std(ang_dist_return["Sujet 1"]+ang_dist_return["Sujet 2"]))

print("end lin = ",np.mean(dist_return_end["Sujet 1"]+dist_return_end["Sujet 2"]),\
	" , ang = ",np.mean(ang_dist_return_end["Sujet 1"]+ang_dist_return_end["Sujet 2"]))

ind = 0
axs = ['ax1','ax2']
fig,axs = plt.subplots(1,2)

axs[0].boxplot([dist_go["Sujet 1"],dist_go["Sujet 2"],
	dist_return["Sujet 1"],dist_return["Sujet 2"]])
axs[0].set_ylabel("Linear distance (m)")
axs[0].set_xticklabels(['Subject 1\n(Forward)', 'Subject 2\n(Forward)', 'Subject 1\n(Return)', 'Subject 2\n(Return)'])
# axs[0].set_ylim(0, 1.)

axs[1].boxplot([ang_dist_go["Sujet 1"],ang_dist_go["Sujet 2"],
	ang_dist_return["Sujet 1"],ang_dist_return["Sujet 2"]])
axs[1].set_xticklabels(['Subject 1\n(Forward)', 'Subject 2\n(Forward)', 'Subject 1\n(Return)', 'Subject 2\n(Return)'])
axs[1].set_ylabel("Angular distance (rad)")
plt.show()

f = open('Data/linear_distance_human_mean.json')
dist_lin = json.load(f)
f = open('Data/local_angular_distance_human_mean.json')
dist_ang = json.load(f)

##########################################
########### Significance tests ###########
##########################################

print("### kruskal_test for all : Significant difference if p < 0.05 ###")
for sub in dist_go:
	kruskal_test = stats.kruskal(dist_go[sub], dist_lin[sub]["Sujet 1 et 2"])
	print("linear ",sub, " Go : ",kruskal_test)
	kruskal_test = stats.kruskal(dist_return[sub], dist_lin[sub]["Sujet 1 et 2"])
	print("linear ",sub, " Return : ",kruskal_test)	
	kruskal_test = stats.kruskal(ang_dist_go[sub], dist_ang[sub]["Sujet 1 et 2"])	
	print("angular ",sub, " Go : ",kruskal_test)
	kruskal_test = stats.kruskal(ang_dist_return[sub], dist_ang[sub]["Sujet 1 et 2"])
	print("angular ",sub, " Return : ",kruskal_test)