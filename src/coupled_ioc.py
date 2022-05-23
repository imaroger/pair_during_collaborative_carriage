
import numpy as np
import matplotlib.pylab as plt
import crocoddyl
from math import pi, floor, sqrt, cos, sin, atan2, exp
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


def optimizeT(T,x0,T_guess,T_list):
	T = int(T[0])
	# print(T)
	if len(T_list) > 0:
		T_in_list = np.where(np.transpose(T_list)[0] == T)[0]
	else:
		T_in_list = []
	if len(T_in_list) > 0:
		# print(T,"already computed",T_list[T_in_list[0]][1])
		return T_list[T_in_list[0]][1]
	else:
		if T > 50:#T_guess/2 and T < 2*T_guess:
			problem = crocoddyl.ShootingProblem(x0, [ model ] * T, terminal_model)
			ddp = crocoddyl.SolverDDP(problem)
			done = ddp.solve()
			# print(T,done,ddp.iter,ddp.cost)
			cost = ddp.cost
		else:
			cost = exp(min(max(8,abs(30-T)),500))
			# print("T< 0",T,cost)	
		T_list.append([T,cost])
		return cost	

def translate(xs,x0_sub1,x0_sub2):
	x1,y1,th1,x2,y2,th2 = [],[],[],[],[],[]
	for state in xs:
		x1.append(x0_sub1[0] + state[0])
		y1.append(x0_sub1[1] + state[1])
		th1.append(state[2])
		x2.append(x0_sub2[0] + state[6])
		y2.append(x0_sub2[1] + state[7])
		th2.append(state[8])		
	return (x1,y1,th1,x2,y2,th2)

def plotOC(x,y,theta):
	arrow_len = 0.08
	count = 0
	for i in range (len(x)):
		if count%50 == 0:
			c, s = np.cos(theta[i]), np.sin(theta[i])	
			plt.arrow(x[i], y[i], c * arrow_len, s * arrow_len, head_width=.05)
		count += 1
	c, s = np.cos(theta[-1]), np.sin(theta[-1])	
	plt.arrow(x[-1], y[-1], c * arrow_len, s * arrow_len, head_width=.05)		
	plt.plot(x,y)
	#plt.grid(True)

def plotHuman(x,y,theta):
	arrow_len = 0.08
	count = 0
	for i in range (len(x)):
		if count%50 == 0:
			c, s = np.cos(theta[i]), np.sin(theta[i])	
			plt.arrow(x[i], y[i], c * arrow_len, s * arrow_len, head_width=.05)
		count += 1
	c, s = np.cos(theta[-1]), np.sin(theta[-1])	
	plt.arrow(x[-1], y[-1], c * arrow_len, s * arrow_len, head_width=.05)		
	plt.plot(x,y,linewidth = 0.5)

def solveCoupledDdp(pos_i_sub1,pos_f_sub1,pos_i_sub2,pos_f_sub2,graph_disp,title):
	dist_init = sqrt((pos_i_sub1[0]-pos_i_sub2[0])**2+(pos_i_sub1[1]-pos_i_sub2[1])**2)
	dist_end = sqrt((pos_f_sub1[0]-pos_f_sub2[0])**2+(pos_f_sub1[1]-pos_f_sub2[1])**2)
	assert(1.5 <= dist_init <= 2.2 and 1.5 <= dist_end <= 2.2)
	model.initialDistance = np.matrix([pos_i_sub1[0]-pos_i_sub2[0],pos_i_sub1[1]-pos_i_sub2[1]]).T
	# print("--- Ddp ---")
	final_state_sub1 = [(pos_f_sub1[0]-pos_i_sub1[0]),(pos_f_sub1[1]-pos_i_sub1[1]),pos_f_sub1[2]]
	final_state_sub2 = [(pos_f_sub2[0]-pos_i_sub2[0]),(pos_f_sub2[1]-pos_i_sub2[1]),pos_f_sub2[2]]
	model.finalStateSubject1 = np.matrix([final_state_sub1[0],final_state_sub1[1],final_state_sub1[2]]).T
	model.finalStateSubject2 = np.matrix([final_state_sub2[0],final_state_sub2[1],final_state_sub2[2]]).T	
	terminal_model.finalStateSubject1 = np.matrix([final_state_sub1[0],final_state_sub1[1],final_state_sub1[2]]).T
	terminal_model.finalStateSubject2 = np.matrix([final_state_sub2[0],final_state_sub2[1],final_state_sub2[2]]).T	
	# print("init & end (sub 1) : ",pos_i_sub1,pos_f_sub1)
	# print("init & end (sub 2) : ",pos_i_sub2,pos_f_sub2)

	init_state = np.matrix([ 0, 0,pos_i_sub1[2] , 0, 0, 0, 0, 0,pos_i_sub2[2] , 0, 0, 0]).T
	T_guess = 150
	T_list = []
	# distance1 = sqrt((pos_f_sub1[0]-pos_i_sub1[0])**2+(pos_f_sub1[1]-pos_i_sub1[1])**2)
	# distance2 = sqrt((pos_f_sub2[0]-pos_i_sub2[0])**2+(pos_f_sub2[1]-pos_i_sub2[1])**2)
	# distance = min(distance1, distance2) #NB : different results if max instead of max
	# T_guess = int(distance*100/1.38)
	optimal = minimize(optimizeT, T_guess, args=(init_state,T_guess,T_list),\
	method='Powell',options = {'xtol': 0.01,'ftol': 0.001})
	T_opt = int(optimal.x)
	# print("----",T_guess,T_opt)

	# T_opt = 1000 #int(distance*100)

	problem = crocoddyl.ShootingProblem(init_state, [ model ] * T_opt, terminal_model)
	ddp = crocoddyl.SolverDDP(problem)
	done = ddp.solve()
	# print(done,ddp.cost)

	# pos_i_sub1,pos_i_sub2 = [0,0,0],[0,0,0]
	x1,y1,theta1,x2,y2,theta2 = translate(ddp.xs, pos_i_sub1, pos_i_sub2)

	dist_betwen_sub = np.sqrt((np.array(x1)-np.array(x2))**2+(np.array(y1)-np.array(y2))**2)
	# print(min(dist_betwen_sub),max(dist_betwen_sub))


	if graph_disp:
		plotOC(x1,y1,theta1)
		plotOC(x2,y2,theta2)	
		# for i in range(len(x1)):
		# 	if i%25 == 0:
		# 		plt.plot([x1[i],x2[i]], [y1[i],y2[i]], color = 'black', linewidth = 0.5)			

	path = "Data/CoupledOptimalControl/"+title+".dat"
	# print(path)
	sol = [x1,y1,theta1,x2,y2,theta2]
	np.savetxt(path,np.transpose(sol))
	# print("--- End of Ddp ---")

def normalizeAngle(angle): 
	new_angle = angle
	while new_angle > pi:
		new_angle -= 2*pi
	while new_angle < -pi:
		new_angle += 2*pi
	return new_angle	

def computeMultipleTraj(start_and_end,leader):
	print("Compute them all")
	# time_list = []
	n_go,n_return = 0,0
	for traj in list_trajs:
		# print("### ",traj," ###")
		if leader == "All data" or leader == "Sujet 1 et 2": #Returns exist
			pos_go_sub1 = start_and_end[traj+'_1']["Sujet 1"][leader]
			pos_go_sub2 = start_and_end[traj+'_1']["Sujet 2"][leader]
			pos_return_sub1 = start_and_end[traj+'_2']["Sujet 1"]
			pos_return_sub2 = start_and_end[traj+'_2']["Sujet 2"]		
			for ori in pos_go_sub1:
				# print("Go - ",ori)
				pos_i_sub1 = [pos_go_sub1[ori][0][0],pos_go_sub1[ori][0][1],pos_go_sub1[ori][0][2]]
				pos_f_sub1 = [pos_go_sub1[ori][1][0],pos_go_sub1[ori][1][1],pos_go_sub1[ori][1][2]]
				pos_i_sub2 = [pos_go_sub2[ori][0][0],pos_go_sub2[ori][0][1],pos_go_sub2[ori][0][2]]
				pos_f_sub2 = [pos_go_sub2[ori][1][0],pos_go_sub2[ori][1][1],pos_go_sub2[ori][1][2]]
				start_time = time.time()
				title = traj+'_1_'+leader + "_" + str(ori[23:min(28,len(ori))])
				solveCoupledDdp(pos_i_sub1,pos_f_sub1,pos_i_sub2,pos_f_sub2,graph_disp,title)		
				# time_list.append(time.time() - start_time)
				n_go += 1
			for ori in pos_return_sub1:
				# print("Return - ",ori)		
				pos_i_sub2 = [pos_return_sub1[ori][0][0],pos_return_sub1[ori][0][1],pos_return_sub1[ori][0][2]]
				pos_f_sub2 = [pos_return_sub1[ori][1][0],pos_return_sub1[ori][1][1],pos_return_sub1[ori][1][2]]
				pos_i_sub1 = [pos_return_sub2[ori][0][0],pos_return_sub2[ori][0][1],pos_return_sub2[ori][0][2]]
				pos_f_sub1 = [pos_return_sub2[ori][1][0],pos_return_sub2[ori][1][1],pos_return_sub2[ori][1][2]]
				start_time = time.time()
				title = traj+'_2_'+ leader + "_" + str(ori[24:min(29,len(ori))])				
				solveCoupledDdp(pos_i_sub1,pos_f_sub1,pos_i_sub2,pos_f_sub2,graph_disp,title)								
				# time_list.append(time.time() - start_time)	
				n_return += 1
		if graph_disp:
			plt.show()
	print("go : ",n_go," and return : ",n_return)
	# print(time_list,len(time_list),np.mean(time_list))
	print("End of Compute them all")
	# print(time_list,len(time_list),np.mean(time_list))

def linearDistance(x_human,y_human,x_oc,y_oc,display):
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
		if display:
			if i%25 == 0:
				plt.plot([x_human[i],x_oc[i]], [y_human[i],y_oc[i]], color = 'red', linewidth = 0.5)
	if display:
		print(dist/length)
		plt.plot(x_human,y_human)
		plt.plot(x_oc,y_oc)
		plt.show()	
	return dist/length

def angularDistance(th_human,th_oc):
	length = len(th_human)	
	th_oc2 = np.interp(np.arange(0,length,1),np.linspace(0,length,len(th_oc)),th_oc)

	dist = 0
	for i in range(length):
		dist += abs(th_human[i]-th_oc2[i])

	# if dist > 1:
	# 	print(dist/length)
	# 	time2 = np.linspace(1,100,500)
	# 	time = np.linspace(1,100,len(th_oc))
	# 	plt.plot(time2,th_human)
	# 	plt.plot(time,th_oc)		
	# 	plt.plot(time2,th_oc2)
	# 	plt.show()
	return dist/length

def distanceBetweenCurvs(leader):
	print("------- Compute Distance -------")
	global_dist = 0
	global_dist_ang = 0
	# final_dist = 0
	dist1,dist2,dist_table = 0,0,0
	ang_dist1,ang_dist2,ang_dist_table = 0,0,0
	nb = 0
	for traj in list_trajs:
		# print(traj)
		if leader == "Sujet 1 et 2" or leader == "All data":
			display = False
			human_path = "Data/Human/" + traj + "_1_mean.json"
			f = open(human_path)
			human = json.load(f)['Trajectoires_Moyennes']
			for ori in human['Table'][leader]:
				# print(ori)
				sub1 = human['Sujet 1'][leader][ori]
				sub2 = human['Sujet 2'][leader][ori]
				oc = np.transpose(np.loadtxt("Data/CoupledOptimalControl/" + traj + "_1_" + leader + "_" + str(ori[23:min(28,len(ori))]) + ".dat"))

				dist1 += linearDistance(sub1["x"], sub1["y"], oc[0], oc[1],display)
				dist2 += linearDistance(sub2["x"], sub2["y"], oc[3], oc[4],display)				

				ang_dist1 += angularDistance(sub1["Orientation_Globale"], oc[2])
				ang_dist2 += angularDistance(sub2["Orientation_Globale"], oc[5])				

				nb += 1
			human_path = "Data/Human/" + traj + "_2_mean.json"
			f = open(human_path)
			human = json.load(f)['Trajectoires_Moyennes']
			# old_dist_table = dist_table
			for ori in human['Table']["All data"]:
				# print(ori)
				sub1 = human['Sujet 1']["All data"][ori]
				sub2 = human['Sujet 2']["All data"][ori]
				oc = np.transpose(np.loadtxt("Data/CoupledOptimalControl/" + traj + "_2_" + leader + "_" + str(ori[24:min(29,len(ori))]) + ".dat"))

				# display = True
				dist2 += linearDistance(sub2["x"], sub2["y"], oc[0], oc[1],display)
				# display = False				
				dist1 += linearDistance(sub1["x"], sub1["y"], oc[3], oc[4],display)							

				ang_dist2 += angularDistance(sub2["Orientation_Globale"], oc[2])
				ang_dist1 += angularDistance(sub1["Orientation_Globale"], oc[5])				

				nb += 1				
				# print(dist_table-old_dist_table)
	global_dist = dist1/nb+dist2/nb
	global_dist_ang = ang_dist1/nb+ang_dist2/nb
	# print(nb)
	print("linear dist",dist1/nb,dist2/nb)
	print("angular dist",ang_dist1/nb,ang_dist2/nb)
	print("final cost : ",global_dist+(1/2)*global_dist_ang)
	print("------- End of Compute distance -------")
	return (global_dist+(1/2)*global_dist_ang)

def ioc(wt):
	# wt = list(wt)[:10] + [0] + list(wt)[10:]
	# wt = list(wt)[:-2] + [0.5,0.25,20,30] + list(wt)[:-2]
	wt = list([np.float32(w) for w in wt])
	print(wt)	
		
	if (len(np.where(np.array(wt) < 0)[0]) == 0):
		start_time = time.time()	
		model.costWeights = np.matrix(wt[:11]).T
		terminal_model.costWeights = np.matrix(wt[11:]).T

		# print("Weights :", model.costWeights,terminal_model.costWeights)
		computeMultipleTraj(start_and_end,leader)
		print(time.time() - start_time)
		cost = distanceBetweenCurvs(leader)
		print("final cost : ",cost)
		return cost
	else:
		return 100


########################################################################
################################## MAIN ################################
########################################################################

model = crocoddyl.ActionRunningModelPair()
data  = model.createData()

terminal_model = crocoddyl.ActionTerminalModelPair()
terminal_data  = terminal_model.createData()

path = 'Data/Human/'
list_trajs = ['d1_p4_jaune', 'd1_p4_gris', 'd1_p5_jaune', 'd1_p5_gris', 'd1_p6_jaune', 'd1_p6_gris', 'd2_p7_jaune', 'd2_p7_gris', 'd3_p7_gris']

f = open(path + "start_and_end.json")
start_and_end = json.load(f)

graph_disp = False
leader = "Sujet 1 et 2"

w0 = [3.8538349, 
	2.2903018, 10.374566, 0.0996108,
	2.7038107, 8.992064, 3.0013099,
	10.42393, 1.8188067e-06,
	0.4999896, 0.03344339,
	19.770494, 30.23781, 8.767153, 9.1456375]
ioc(w0)