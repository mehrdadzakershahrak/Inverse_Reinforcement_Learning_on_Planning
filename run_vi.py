import numpy as np
from value_iteration import value_iteration
import pickle
#thetas = np.array([-142.12235333 ,-78.4391271 ,-142.26565079])
feat_map = np.load("feat_map_final.npy")
rewards = np.load("rewards.npy")
P_a = np.load("P_a.npy")

with open('states_dict.pickle', 'rb') as file:
        states_dict=pickle.load(file)
    
gamma = 0.9
values,policy= value_iteration(P_a, rewards, gamma, error=0.01, deterministic=True)
print(policy)
print(values)
print(rewards)
init_state = (1,)
state = init_state
print(states_dict)
state_id = states_dict[init_state] #no HAS_ELECTRICITY
with open('all_actions.pickle', 'rb') as file:
        all_actions=pickle.load(file)

reverse_actions={}

for key in all_actions.keys():
	reverse_actions[all_actions[key]]=key

while True:
	action = int(policy[state_id])
	action_template = reverse_actions[action]
	print(action_template)
	state = list(state)
	state.append(action)
	if sorted(state) == [0,1,2,3,4]:
		break
	state_id=states_dict[tuple(sorted(state))]

	

