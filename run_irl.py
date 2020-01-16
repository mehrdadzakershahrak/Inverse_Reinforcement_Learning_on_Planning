import numpy as np
from new_maxent_irl import maxent_irl
import time
P_a = np.load("P_a.npy")
N_s,N_a,_ = np.shape(P_a)
P_a = P_a.reshape([N_s,N_s,N_a])
feat_map = np.load("feat_map_final.npy")
traj = np.load("trajectories.npy")
print(traj)

gamma = 0.9999999
n_iters = 500 #500/1000
lr = 0.05	
rewards = np.zeros([3,1])
#np.save("rewards.npy",rewards)
start_time = time.clock()
rewards = maxent_irl(feat_map, P_a, gamma, traj, lr, n_iters)
np.save("rewards.npy",rewards)
#print(rewards)
print("------------------DONE--------------------")
time_taken = time.clock()-start_time
with open('time_taken.txt','w') as f:
	f.write(''.join(str(time_taken)))

#[30.10696892 49.19069929 60.30356041 25.10481399 12.86120401 64.05065162 54.86760256 57.08617515 44.57909472 31.77255521 78.86747464 73.71675344 67.15740421]

