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
		dist_lin += sqrt((x[i]-xm[i])**2+(y[i]-ym[i])**2)
	# if dist_lin/length > 0.65 and data1["Orientation_End_Theorique"] == data2["Orientation_End_Theorique"]:
	# 	print(dist_lin/length)
	# 	plt.plot(data1['x'],data1['y'])
	# 	plt.plot(data2['x'],data2['y'])	
	# 	for i in range(length):
	# 		# d = sqrt((x[i]-xm[i])**2+(y[i]-ym[i])**2)
	# 		# if d > 0.65:
	# 			# print(i,d,x[i],y[i],xm[i],ym[i])
	# 		if i%25 == 0:
	# 			plt.plot([x[i],xm[i]], [y[i],ym[i]], color = 'red', linewidth = 0.5)				
	# 	plt.show()
	return dist_lin/length


dist = {}
kruskal = {}
for sub in list_sub:
	dist[sub] = {}
	kruskal[sub] = {}
	for pair in list_pair:
		dist[sub][pair] = []
		kruskal[sub][pair] = []

for file in list_targets[9:]:
	print("### ", file," ###")
	f = open(path+file+'.json')
	data = json.load(f)['Trajectoires_Individuelles']
	for sub in data:
		i = 0
		while i < len(data[sub]):
			pair = data[sub][i]["Binome"]
			ind = []
			while i < len(data[sub]) and data[sub][i]["Binome"] == pair:
				ind.append(i)	
				i += 1	
			if len(ind) == 3:
				# print("-- 3 trajs --")
				for k in range(len(ind)):
					l = k+1
					if l == len(ind):
						l = 0
					if data[sub][ind[k]]["Orientation_Init_Theorique"] == \
						data[sub][ind[l]]["Orientation_Init_Theorique"] and \
						data[sub][ind[k]]["Orientation_End_Theorique"] == \
						data[sub][ind[l]]["Orientation_End_Theorique"]:
						dist[sub][pair].append(distance(data[sub][ind[k]],data[sub][ind[l]]))					
				if data[sub][ind[0]]["Orientation_Init_Theorique"] == \
					data[sub][ind[1]]["Orientation_Init_Theorique"] == \
					data[sub][ind[2]]["Orientation_Init_Theorique"] and \
					data[sub][ind[0]]["Orientation_End_Theorique"] == \
					data[sub][ind[1]]["Orientation_End_Theorique"] == \
					data[sub][ind[2]]["Orientation_End_Theorique"]:
					data0 = list(np.array(data[sub][ind[0]]["x"])+np.array(data[sub][ind[0]]["y"]))
					data1 = list(np.array(data[sub][ind[1]]["x"])+np.array(data[sub][ind[1]]["y"]))
					data2 = list(np.array(data[sub][ind[2]]["x"])+np.array(data[sub][ind[2]]["y"]))				
					kruskal[sub][pair].append(stats.kruskal(data0,data1,data2)[1])
			if len(ind) == 2:
				# print("-- only 2 --")
				if data[sub][ind[0]]["Orientation_Init_Theorique"] == \
					data[sub][ind[1]]["Orientation_Init_Theorique"]and \
					data[sub][ind[0]]["Orientation_End_Theorique"] == \
					data[sub][ind[1]]["Orientation_End_Theorique"]:
					dist[sub][pair].append(distance(data[sub][ind[0]],data[sub][ind[1]]))
					data0 = list(np.array(data[sub][ind[0]]["x"])+np.array(data[sub][ind[0]]["y"]))
					data1 = list(np.array(data[sub][ind[1]]["x"])+np.array(data[sub][ind[1]]["y"]))	
					kruskal[sub][pair].append(stats.kruskal(data0,data1)[1])

# print(len(dist["Table"]['Sujet1_Aurélie&Sujet2_Stanislas']))
# print(len(dist["Table"]['Sujet1_Rémy&Sujet2_Margaux']))

mean_sub1 = [np.mean(dist["Sujet 1"][pair]) for pair in list_pair]
mean_sub2 = [np.mean(dist["Sujet 2"][pair]) for pair in list_pair]
mean_tab = [np.mean(dist["Table"][pair]) for pair in list_pair]
print("min/max linear distance for sub1 : ", np.min(mean_sub1),np.max(mean_sub1))
print("min/max linear distance for sub2 : ", np.min(mean_sub2),np.max(mean_sub2))
print("min/max linear distance for tab : ", np.min(mean_tab),np.max(mean_tab))

diff = {}
for sub in kruskal:
	diff[sub] = {}
	diff[sub]["p < 1e-3"] = 0
	diff[sub]["1e-3 < p < 0.05"] = 0
	diff[sub]["0.05 < p"] = 0	
	for pair in kruskal[sub]:
		for i in range(len(kruskal[sub][pair])):
			if kruskal[sub][pair][i] < 1e-3:
				diff[sub]["p < 1e-3"] += 1
			elif kruskal[sub][pair][i] < 0.05:
				diff[sub]["1e-3 < p < 0.05"] += 1
			else:
				diff[sub]["0.05 < p"] += 1

count = 1
for sub in diff:
	plt.subplot(1,3,count)
	nb = [diff[sub]["p < 1e-3"],diff[sub]["1e-3 < p < 0.05"],diff[sub]["0.05 < p"]]
	labels = ["p < 1e-3","1e-3 < p < 0.05","0.05 < p"]
	colors = ['#ff7f0e','#1f77b4','#2ca02c']
	plt.pie(nb, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90)
	if sub == "Sujet 1":
		plt.title("Subject 1")
	elif sub == "Sujet 2":
		plt.title("Subject 2")
	else:
		plt.title(sub)			
	count += 1
plt.show()

# ind = 0
# axs = ['ax1','ax2','ax3']
# fig,axs = plt.subplots(3)
# for sub in list_sub: 
# 	axs[ind].boxplot([dist[sub][list_pair[0]],\
# 		dist[sub][list_pair[1]],dist[sub][list_pair[2]],\
# 		dist[sub][list_pair[3]],dist[sub][list_pair[4]],\
# 		dist[sub][list_pair[5]],dist[sub][list_pair[6]],\
# 		dist[sub][list_pair[7]],dist[sub][list_pair[8]],\
# 		dist[sub][list_pair[9]],dist[sub][list_pair[10]],\
# 		dist[sub][list_pair[11]],dist[sub][list_pair[12]],\
# 		dist[sub][list_pair[13]],dist[sub][list_pair[14]],\
# 		dist[sub][list_pair[15]],dist[sub][list_pair[16]],\
# 		dist[sub][list_pair[17]],dist[sub][list_pair[18]],\
# 		dist[sub][list_pair[19]]])
# 	axs[ind].set_ylabel("Linear distance (m)")
# 	axs[ind].set_xticklabels(pairs)
# 	axs[ind].set_ylim(0, 0.8)
# 	if sub == "Sujet 1":
# 		axs[ind].set_title("Subject 1")
# 	elif sub == "Sujet 2":
# 		axs[ind].set_title("Subject 2")	
# 	else:
# 		axs[ind].set_title(sub)				
# 	ind += 1
# plt.show()

count = 1
for sub in list_sub: 
	plt.subplot(1,3,count)
	all_dist = []
	for pair in dist[sub]:
		for i in range(len(dist[sub][pair])):
			all_dist.append(dist[sub][pair][i])
	plt.boxplot(all_dist)
	plt.ylim(0, 0.8)
	plt.ylabel("Linear distance between the return paths (m)")
	if sub == "Sujet 1":
		plt.title("Subject 1")
	elif sub == "Sujet 2":
		plt.title("Subject 2")	
	else:
		plt.title(sub)			
	count += 1
plt.show()
