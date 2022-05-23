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

def distance(data1,data2):
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
	# if dist_lin/length > 1 and data1["Orientation_End_Theorique"] == data2["Orientation_End_Theorique"]:
	# 	plt.plot(data1['x'],data1['y'])
	# 	plt.plot(data2['x'],data2['y'])	
	# 	plt.show()
	return dist_lin/length

dist_to_two_leaders = {}
ori_choice = {}
nb_closer = {}
for sub in list_sub:
	dist_to_two_leaders[sub] = {}
	dist_to_two_leaders[sub]["Sujet 1 / Sujet 1 et 2"] = []
	dist_to_two_leaders[sub]["Sujet 2 / Sujet 1 et 2"] = []
	dist_to_two_leaders[sub]["Sujet 1 / Sujet 2"] = []
	ori_choice[sub] = {}
	ori_choice[sub]["Multiple orientation"] = {}
	ori_choice[sub]["Multiple orientation"]["Ori 1"] = 0 # the end orientation chosen when 2 leaders is the same chosen when Sujet 1 was leader
	ori_choice[sub]["Multiple orientation"]["Ori 2"] = 0# the end orientation chosen when 2 leaders is the same chosen when Sujet 2 was leader
	ori_choice[sub]["Multiple orientation"]["New ori"] = 0 # the end orientation chosen when 2 leaders is different from the one when Sujet 1 or Sujet 2 were leader
	ori_choice[sub]["Only one orientation"] = 0	
	nb_closer[sub] = {}
	nb_closer[sub]["Closer 1"] = 0
	nb_closer[sub]["Closer 2"] = 0



for file in list_targets[:9]:
	print("### ", file," ###")
	f = open(path+file+'.json')
	data = json.load(f)['Trajectoires_Individuelles']
	# for i in range(len(data["Sujet 1"])):
	# 	if data["Sujet 1"][i]["Leader"] != data["Table"][i]["Leader"] or data["Sujet 1"][i]["Leader"] != data["Sujet 2"][i]["Leader"]:
	# 		print(i,data["Sujet 1"][i]["Leader"],data["Sujet 2"][i]["Leader"],data["Table"][i]["Leader"])
	# 	if data["Sujet 1"][i]["Binome"] != data["Table"][i]["Binome"] or data["Sujet 1"][i]["Binome"] != data["Sujet 2"][i]["Binome"]:
	# 		print(i,data["Sujet 1"][i]["Binome"],data["Sujet 2"][i]["Binome"],data["Table"][i]["Binome"])
	for sub in data:
		i = 0
		while i < len(data[sub]):
			pair = data[sub][i]["Binome"]
			# print("--> new pair !",i)
			
			ind = [[],[],[]]
			while i < len(data[sub]) and data[sub][i]["Binome"] == pair:
				# print("same pair",i,data[sub][i]["Leader"])
				if data[sub][i]["Leader"] == "Sujet 1":
					ind[0].append(i)
				if data[sub][i]["Leader"] == "Sujet 2":
					ind[1].append(i)
				if data[sub][i]["Leader"] == "Sujet 1 et 2":
					ind[2].append(i)	
				i += 1								
			if len(ind[2]) > 0 and  len(ind[0]) > 0 and len(ind[1]) > 0:

				dist1_12 = distance(data[sub][ind[0][0]],data[sub][ind[2][0]])
				dist2_12 = distance(data[sub][ind[1][0]],data[sub][ind[2][0]])
				dist1_2 = distance(data[sub][ind[0][0]],data[sub][ind[1][0]])

				if(data[sub][ind[0][0]]["Orientation_End_Theorique"] == data[sub][ind[2][0]]["Orientation_End_Theorique"]):
					dist_to_two_leaders[sub]["Sujet 1 / Sujet 1 et 2"].append(dist1_12)
				if(data[sub][ind[1][0]]["Orientation_End_Theorique"] == data[sub][ind[2][0]]["Orientation_End_Theorique"]):
					dist_to_two_leaders[sub]["Sujet 2 / Sujet 1 et 2"].append(dist2_12)					
				if(data[sub][ind[0][0]]["Orientation_End_Theorique"] == data[sub][ind[1][0]]["Orientation_End_Theorique"]):
					dist_to_two_leaders[sub]["Sujet 1 / Sujet 2"].append(dist1_2)

				if data[sub][ind[0][0]]["Orientation_End_Theorique"] == \
				data[sub][ind[1][0]]["Orientation_End_Theorique"] == \
				data[sub][ind[2][0]]["Orientation_End_Theorique"]:
					ori_choice[sub]["Only one orientation"] += 1
					if dist1_12 < dist2_12:
						nb_closer[sub]["Closer 1"] += 1
					else:
						nb_closer[sub]["Closer 2"] += 1
				else:
					if data[sub][ind[0][0]]["Orientation_End_Theorique"] == \
					data[sub][ind[2][0]]["Orientation_End_Theorique"]:
						ori_choice[sub]["Multiple orientation"]["Ori 1"] += 1
					elif data[sub][ind[1][0]]["Orientation_End_Theorique"] == \
					data[sub][ind[2][0]]["Orientation_End_Theorique"]:
						ori_choice[sub]["Multiple orientation"]["Ori 2"] += 1
					else:
						# print(data[sub][ind[0][0]]["Orientation_End_Theorique"],\
						# data[sub][ind[1][0]]["Orientation_End_Theorique"],\
						# data[sub][ind[2][0]]["Orientation_End_Theorique"])
						# print(data[sub][ind[0][0]]["Binome"],\
						# data[sub][ind[1][0]]["Binome"],\
						# data[sub][ind[2][0]]["Binome"])						
						ori_choice[sub]["Multiple orientation"]["New ori"] += 1						

				# plt.plot(data[sub][ind[0][0]]["x"],data[sub][ind[0][0]]["y"],label='sub 1')
				# plt.plot(data[sub][ind[1][0]]["x"],data[sub][ind[1][0]]["y"],label='sub 2')
				# plt.plot(data[sub][ind[2][0]]["x"],data[sub][ind[2][0]]["y"],label='sub 1 & 2')
				# plt.legend()
				# print(data[sub][ind[1][0]]['Binome'],dist_to_two_leaders[sub]["Sujet 1"][-1],dist_to_two_leaders[sub]["Sujet 2"][-1])
				# plt.show()

print(len(dist_to_two_leaders["Table"]["Sujet 1 / Sujet 2"]))
print(len(dist_to_two_leaders["Table"]["Sujet 1 / Sujet 1 et 2"]))
print(len(dist_to_two_leaders["Table"]["Sujet 2 / Sujet 1 et 2"]))
print(ori_choice)
print(nb_closer)

print("### Mean distance 1vs3, 2vs3 and 1vs2")

print("Sujet 1 : ",np.mean(dist_to_two_leaders["Sujet 1"]["Sujet 1 / Sujet 1 et 2"]),\
	np.mean(dist_to_two_leaders["Sujet 1"]["Sujet 2 / Sujet 1 et 2"]),\
	np.mean(dist_to_two_leaders["Sujet 1"]["Sujet 1 / Sujet 2"]))
print("Sujet 2 : ",np.mean(dist_to_two_leaders["Sujet 2"]["Sujet 1 / Sujet 1 et 2"]),\
	np.mean(dist_to_two_leaders["Sujet 2"]["Sujet 2 / Sujet 1 et 2"]),\
	np.mean(dist_to_two_leaders["Sujet 2"]["Sujet 1 / Sujet 2"]))
print("Table : ",np.mean(dist_to_two_leaders["Table"]["Sujet 1 / Sujet 1 et 2"]),\
	np.mean(dist_to_two_leaders["Table"]["Sujet 2 / Sujet 1 et 2"]),\
	np.mean(dist_to_two_leaders["Table"]["Sujet 1 / Sujet 2"]))

##############################
########## Boxplot ###########
##############################

# plt.subplot(3,3,1)		
# plt.boxplot([dist_to_two_leaders["Sujet 1"]["Sujet 1 / Sujet 1 et 2"]])
# plt.ylim(0, 1.1)
# plt.title("Subject 1 - Scenario 1 / Scenario 3")
# plt.subplot(3,3,2)		
# plt.boxplot([dist_to_two_leaders["Sujet 1"]["Sujet 2 / Sujet 1 et 2"]])
# plt.ylim(0, 1.1)
# plt.title("Subject 1 - Scenario 2 / Scenario 3")
# plt.subplot(3,3,3)		
# plt.boxplot([dist_to_two_leaders["Sujet 1"]["Sujet 1 / Sujet 2"]])
# plt.ylim(0, 1.1)
# plt.title("Subject 1 - Scenario 1 / Scenario 2")
# plt.subplot(3,3,4)		
# plt.boxplot([dist_to_two_leaders["Sujet 2"]["Sujet 1 / Sujet 1 et 2"]])
# plt.ylim(0, 1.1)
# plt.title("Subject 2 - Scenario 1 / Scenario 3")
# plt.subplot(3,3,5)		
# plt.boxplot([dist_to_two_leaders["Sujet 2"]["Sujet 2 / Sujet 1 et 2"]])
# plt.ylim(0, 1.1)
# plt.title("Subject 2 - Scenario 2 / Scenario 3")
# plt.subplot(3,3,6)		
# plt.boxplot([dist_to_two_leaders["Sujet 2"]["Sujet 1 / Sujet 2"]])
# plt.ylim(0, 1.1)
# plt.title("Subject 2 - Scenario 1 / Scenario 2")
# plt.subplot(3,3,7)		
# plt.boxplot([dist_to_two_leaders["Table"]["Sujet 1 / Sujet 1 et 2"]])
# plt.ylim(0, 0.9)
# plt.title("Table - Scenario 1 / Scenario 3")
# plt.subplot(3,3,8)		
# plt.boxplot([dist_to_two_leaders["Table"]["Sujet 2 / Sujet 1 et 2"]])
# plt.ylim(0, 0.9)
# plt.title("Table - Scenario 2 / Scenario 3")
# plt.subplot(3,3,9)		
# plt.boxplot([dist_to_two_leaders["Table"]["Sujet 1 / Sujet 2"]])
# plt.ylim(0, 0.9)
# plt.title("Table - Scenario 1 / Scenario 2")
# plt.show()

###################################
########## Shapiro Test ###########
###################################

print('Normality test for all : Normal if p > 0.05 ')
for sub in dist_to_two_leaders:
	test = stats.shapiro(dist_to_two_leaders[sub]["Sujet 1 / Sujet 1 et 2"])
	print("1/3 : ",test)
	test = stats.shapiro(dist_to_two_leaders[sub]["Sujet 1 / Sujet 2"])
	print("1/2 : ",test)
	test = stats.shapiro(dist_to_two_leaders[sub]["Sujet 2 / Sujet 1 et 2"])
	print("3/2 : ",test)	


###################################
########## Kruskal Test ###########
###################################

print('Stat test - Significant difference if p < 0.05')
for sub in dist_to_two_leaders:
	print("### ", sub , " ###")
	stat_test = stats.kruskal(\
		dist_to_two_leaders[sub]["Sujet 1 / Sujet 1 et 2"],\
		dist_to_two_leaders[sub]["Sujet 2 / Sujet 1 et 2"],\
		dist_to_two_leaders[sub]["Sujet 1 / Sujet 2"])
	print("3 scenarios",stat_test)
	stat_test = stats.mannwhitneyu(\
		dist_to_two_leaders[sub]["Sujet 1 / Sujet 1 et 2"],\
		dist_to_two_leaders[sub]["Sujet 2 / Sujet 1 et 2"])
	print("2 scenarios",stat_test)

################################
########## Pie chart ###########
################################

###----------------------------------###
### For trajectory choice (close to) ###
###----------------------------------###

# closest_traj = {}
# for sub in list_sub:
# 	closest_traj[sub] = {}
# 	closest_traj[sub]["Close 1"] = 0 # The trajectory when Sujet 1 leader close (< 20cm) from the trajectory when 2 leaders but not close from Sujet 2 leader
# 	closest_traj[sub]["Close 2"] = 0 # The trajectory when Sujet 1 leader close (< 20cm) from the trajectory when 2 leaders but not close from Sujet 1 leader
# 	closest_traj[sub]["All close"] = 0 # The trajectory when Sujet 1 leader and Sujet 2 leader close (< 20cm) from the trajectory when 2 leaders
# 	closest_traj[sub]["Not close"] = 0 # No close trajectory (< 20cm) from the trajectory when 2 leaders

# close_dist = 0.2
# for sub in list_sub:
# 	for i in range(len(dist_to_two_leaders[sub]["Sujet 1 / Sujet 1 et 2"])):
		# dist1 = dist_to_two_leaders[sub]["Sujet 1 / Sujet 1 et 2"][i] 
		# dist2 = dist_to_two_leaders[sub]["Sujet 2 / Sujet 1 et 2"][i]
# 		if dist1 > close_dist and dist2 > close_dist:
# 			closest_traj[sub]["Not close"] += 1
# 		if dist1 > close_dist and dist2 < close_dist:
# 			closest_traj[sub]["Close 2"] += 1
# 		if dist1 < close_dist and dist2 > close_dist:
# 			closest_traj[sub]["Close 1"] += 1		
# 		if dist1 < close_dist and dist2 < close_dist:
# 			closest_traj[sub]["All close"] += 1

# print(closest_traj)

# count = 1
# for sub in list_sub:
# 	plt.subplot(1,3,count)
# 	nb = [closest_traj[sub]["Close 1"],closest_traj[sub]["Close 2"],\
# 		closest_traj[sub]["All close"],closest_traj[sub]["Not close"]]
# 	labels = ["Close 1","Close 2","All close","Not close"]
# 	colors = ['green','red','blue','orange']
# 	plt.pie(nb, labels=labels, autopct='%1.1f%%',colors=colors, startangle=90)
# 	plt.title(sub)
# 	count += 1
# plt.show()	

###--------------------------------###
### For trajectory choice (closer) ###
###--------------------------------###
print("### Test Fisher exact ###")
table = np.array([
	[nb_closer["Sujet 1"]["Closer 1"], nb_closer["Sujet 2"]["Closer 1"]],\
	[nb_closer["Sujet 1"]["Closer 2"], nb_closer["Sujet 2"]["Closer 2"]]])
stat_test = stats.fisher_exact(table)
print(stat_test)

count = 1
for sub in list_sub:
	plt.subplot(1,3,count)
	nb = [nb_closer[sub]["Closer 1"],nb_closer[sub]["Closer 2"]]
	labels = ["Closer to\nScenario 1","Closer to\nScenario 2"]
	# colors = ['blue','orange']
	plt.pie(nb, labels=labels, autopct='%1.1f%%', startangle=90)
	if sub == "Sujet 1":
		plt.title("Subject 1")
	elif sub == "Sujet 2":
		plt.title("Subject 2")
	else:
		plt.title(sub)				
	count += 1
plt.show()	

###-----------------------###
### For orientation choice ###
###-----------------------###

count = 1
sub = "Table"

nb = [ori_choice[sub]["Multiple orientation"]["Ori 1"],\
	ori_choice[sub]["Multiple orientation"]["Ori 2"],\
	ori_choice[sub]["Multiple orientation"]["New ori"],\
	ori_choice[sub]["Only one orientation"]]
labels = ["Same for\nScenario 1 and 3","Same for\nScenario 2 et 3","Same for\nScenario 1 et 2","Same for\nevery scenario"]
colors = ['#2ca02c','red','#1f77b4','#ff7f0e']
plt.pie(nb, labels=labels, autopct='%1.1f%%',colors=colors, startangle=90)
plt.show()	
