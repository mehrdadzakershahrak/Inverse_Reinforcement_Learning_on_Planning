import numpy as np
import pickle 
states_dict1 =  pickle.load( open( "states_dict1.pickle", "rb" ) )
states_dict2 =  pickle.load( open( "states_dict2.pickle", "rb" ) )
feat_map1 = np.load('feat_map_new1.npy')
feat_map2 = np.load('feat_map_new2.npy')

print(len(states_dict1))
print(len(states_dict2))

common = []
for state in states_dict1.keys():
	if 3 not in state:
		common.append(states_dict1[state])

print(common)
print(len(common))
result = []
for state1 in common:
	for state2 in common:
		result.append(all(feat_map1[state1,state2]==feat_map2[state1,state2]))
print(result)
print(all(result))
