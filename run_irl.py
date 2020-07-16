import numpy as np
from new_maxent_irl import maxent_irl
import time
import IPython
import os

dir_path = os.path.dirname(os.path.realpath('__file__'))
NEW_OLD_FILES_PATH = dir_path+'/old_domain_files/'
P_a = np.load("P_a.npy")
feat_map = np.load("feat_map_final.npy")
traj = np.load("trajectories.npy",allow_pickle=True)
traj = traj.tolist()

'''
All Actions:
{   '$HAS_ACCESSKEY': 3,
    '$HAS_ELECTRICITY': 1,
    '$HAS_KEY': 0,
    '$HAS_LADDER': 2,
    '$HAS_PASSWORD': 4}
'''
gamma = 0.999
n_iters = 500 #500/1000
lr = 0.05
rewards = np.zeros([3,1])
#np.save("rewards.npy",rewards)
start_time = time.clock()
with open('time_taken.txt','w') as f:
	f.write(''.join(str(start_time)))

num_runs = 1
all_thetas = []
scenarios = [[3],[1],[1,3],[3,5],[1,2]]
#init_states =[(4,), (0, 3), (2,), (2, 4), (3,), (0,), (1,), (0, 1)]
for _ in range(num_runs):
	thetas,rewards = maxent_irl(feat_map, P_a, gamma, traj, lr, n_iters,scenarios)
	all_thetas.append(thetas)
	#IPython.embed()
np.save("all_thetas.npy",all_thetas)
print(all_thetas)
print("------------------DONE--------------------")
time_taken = time.clock()-start_time
with open('time_taken.txt','w') as f:
	f.write(''.join(str(time_taken)))


