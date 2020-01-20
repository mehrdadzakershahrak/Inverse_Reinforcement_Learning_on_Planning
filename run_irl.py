import numpy as np
from new_maxent_irl import maxent_irl
import time
P_a = np.load("P_a.npy")
feat_map = np.load("feat_map_final.npy")
traj = np.load("trajectories.npy",allow_pickle=True)
traj = traj.tolist()

gamma = 0.999
n_iters = 500 #500/1000
lr = 0.05
rewards = np.zeros([3,1])
#np.save("rewards.npy",rewards)
start_time = time.clock()
with open('time_taken.txt','w') as f:
	f.write(''.join(str(start_time)))


scenarios = [[3],[1],[1,3],[3,5],[1,2]]
rewards = maxent_irl(feat_map, P_a, gamma, traj, lr, n_iters,scenarios)
np.save("rewards.npy",rewards)
#print(rewards)
print("------------------DONE--------------------")
time_taken = time.clock()-start_time
with open('time_taken.txt','w') as f:
	f.write(''.join(str(time_taken)))


