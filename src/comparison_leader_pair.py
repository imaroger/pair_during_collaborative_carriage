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
nb_closer = {}
for sub in list_sub:
	dist_to_two_leaders[sub] = {}
	nb_closer[sub] = {}
	for pair in list_pair:
		dist_to_two_leaders[sub][pair] = {}
		dist_to_two_leaders[sub][pair]["Sujet 1 / Sujet 1 et 2"] = []
		dist_to_two_leaders[sub][pair]["Sujet 2 / Sujet 1 et 2"] = []
		dist_to_two_leaders[sub][pair]["Sujet 1 / Sujet 2"] = []
		nb_closer[sub][pair] = {}
		nb_closer[sub][pair]["Closer 1"] = 0
		nb_closer[sub][pair]["Closer 2"] = 0

ori_choice = {}
for pair in list_pair:
	ori_choice[pair] = {}	
	ori_choice[pair]["Multiple orientation"] = {}
	ori_choice[pair]["Multiple orientation"]["Ori 1"] = 0 # the end orientation chosen when 2 leaders is the same chosen when Sujet 1 was leader
	ori_choice[pair]["Multiple orientation"]["Ori 2"] = 0# the end orientation chosen when 2 leaders is the same chosen when Sujet 2 was leader
	ori_choice[pair]["Multiple orientation"]["New ori"] = 0 # the end orientation chosen when 2 leaders is different from the one when Sujet 1 or Sujet 2 were leader
	ori_choice[pair]["Only one orientation"] = 0	


for file in list_targets[:9]:
	print("### ", file," ###")
	f = open(path+file+'.json')
	data = json.load(f)['Trajectoires_Individuelles']
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

				pair = data[sub][ind[0][0]]["Binome"]

				if(data[sub][ind[0][0]]["Orientation_End_Theorique"] == data[sub][ind[2][0]]["Orientation_End_Theorique"]):
					dist_to_two_leaders[sub][pair]["Sujet 1 / Sujet 1 et 2"].append(dist1_12)
				if(data[sub][ind[1][0]]["Orientation_End_Theorique"] == data[sub][ind[2][0]]["Orientation_End_Theorique"]):
					dist_to_two_leaders[sub][pair]["Sujet 2 / Sujet 1 et 2"].append(dist2_12)					
				if(data[sub][ind[0][0]]["Orientation_End_Theorique"] == data[sub][ind[1][0]]["Orientation_End_Theorique"]):
					dist_to_two_leaders[sub][pair]["Sujet 1 / Sujet 2"].append(dist1_2)

				if data[sub][ind[0][0]]["Orientation_End_Theorique"] == \
				data[sub][ind[1][0]]["Orientation_End_Theorique"] == \
				data[sub][ind[2][0]]["Orientation_End_Theorique"]:
					if sub == 'Table':
						ori_choice[pair]["Only one orientation"] += 1
					if dist1_12 < dist2_12:
						nb_closer[sub][pair]["Closer 1"] += 1
					else:
						nb_closer[sub][pair]["Closer 2"] += 1
				else:
					if data[sub][ind[0][0]]["Orientation_End_Theorique"] == \
					data[sub][ind[2][0]]["Orientation_End_Theorique"]:
						if sub == 'Table':
							ori_choice[pair]["Multiple orientation"]["Ori 1"] += 1
					elif data[sub][ind[1][0]]["Orientation_End_Theorique"] == \
					data[sub][ind[2][0]]["Orientation_End_Theorique"]:
						if sub == 'Table':
							ori_choice[pair]["Multiple orientation"]["Ori 2"] += 1
					else:
						# print(data[sub][ind[0][0]]["Orientation_End_Theorique"],\
						# data[sub][ind[1][0]]["Orientation_End_Theorique"],\
						# data[sub][ind[2][0]]["Orientation_End_Theorique"])
						# print(data[sub][ind[0][0]]["Binome"],\
						# data[sub][ind[1][0]]["Binome"],\
						# data[sub][ind[2][0]]["Binome"])
						if sub == 'Table':												
							ori_choice[pair]["Multiple orientation"]["New ori"] += 1						

				# plt.plot(data[sub][ind[0][0]]["x"],data[sub][ind[0][0]]["y"],label='sub 1')
				# plt.plot(data[sub][ind[1][0]]["x"],data[sub][ind[1][0]]["y"],label='sub 2')
				# plt.plot(data[sub][ind[2][0]]["x"],data[sub][ind[2][0]]["y"],label='sub 1 & 2')
				# plt.legend()
				# print(data[sub][ind[1][0]]['Binome'],dist_to_two_leaders[sub]["Sujet 1"][-1],dist_to_two_leaders[sub]["Sujet 2"][-1])
				# plt.show()

# print(len(dist_to_two_leaders["Table"][list_pair[0]]["Sujet 1 / Sujet 2"]))
# print(len(dist_to_two_leaders["Table"][list_pair[0]]["Sujet 1 / Sujet 1 et 2"]))
# print(len(dist_to_two_leaders["Table"][list_pair[0]]["Sujet 2 / Sujet 1 et 2"]))
# print(ori_choice)
# print(nb_closer)

# ################################
# ########## Pie chart ###########
# ################################

###--------------------------------###
### For trajectory choice (closer) ###
###--------------------------------###

count = 1
for sub in list_sub:
	for i in range(len(list_pair)):
		plt.subplot(6,10,count)
		pair = list_pair[i]
		nb = [nb_closer[sub][pair]["Closer 1"],nb_closer[sub][pair]["Closer 2"]]
		labels = ["Closer to\nScenario 1","Closer to\nScenario 2"]
		# colors = ['blue','orange']
		plt.pie(nb, startangle=90)
		plt.title(sub +"(Pair "+str(i+1)+")")			
		count += 1
plt.show()	


##-----------------------###
## For orientation choice ###
##-----------------------###

count = 1
sub = "Table"

for i in range(len(list_pair)):
	plt.subplot(4,5,count)
	pair = list_pair[i]
	nb = [ori_choice[pair]["Multiple orientation"]["Ori 1"],\
		ori_choice[pair]["Multiple orientation"]["Ori 2"],\
		ori_choice[pair]["Multiple orientation"]["New ori"],\
		ori_choice[pair]["Only one orientation"]]
	labels = ["Same for\nScenario 1 and 3","Same for\nScenario 2 et 3","Same for\nScenario 1 et 2","Same for\nevery scenario"]
	colors = ['#2ca02c','red','#1f77b4','#ff7f0e']
	plt.pie(nb, autopct=lambda p: '{:.1f}%'.format(round(p)) if p > 0 else '',colors=colors, startangle=90)
	plt.title("Pair "+str(i+1))
	count += 1
plt.show()	
