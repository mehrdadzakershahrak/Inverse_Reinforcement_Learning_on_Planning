import numpy as np
from old_maxent_irl import maxent_irl
import os

dir_path = os.path.dirname(os.path.realpath('__file__'))
feat_map = np.load(dir_path+"/feat_map_final.npy")
traj = np.load(dir_path+"/trajectories.npy")
P_a = np.load(dir_path+"/P_a.npy")
N_s,N_a,_ = np.shape(P_a)
P_a = P_a.reshape([N_s,N_s,N_a])
#print(traj)

gamma = 0.9999999
n_iters = 1000 #500/1000
lr = 0.05	
rewards = np.zeros([3,1])
#np.save("rewards.npy",rewards)
rewards = maxent_irl(feat_map, P_a, gamma, traj, lr, n_iters)
np.save(NEW_OLD_FILES_PATH+"rewards.npy",rewards)
#print(rewards)