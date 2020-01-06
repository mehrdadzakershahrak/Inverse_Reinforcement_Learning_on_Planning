import numpy as np
from new_maxent_irl import maxent_irl
P_a = np.load("P_a.npy")
N_s,N_a,_ = np.shape(P_a)
P_a = P_a.reshape([N_s,N_s,N_a])
feat_map = np.load("feat_map_final.npy")
traj = np.load("trajectories.npy")
#print(traj)

gamma = 0.9
n_iters = 1000 #500/1000
lr = 0.05	
rewards = np.zeros([3,1])
np.save("rewards.npy",rewards)
rewards = maxent_irl(feat_map, P_a, gamma, traj, lr, n_iters)
np.save("rewards.npy",rewards)
#print(rewards)
