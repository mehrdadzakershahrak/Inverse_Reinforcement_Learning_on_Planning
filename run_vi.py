import numpy as np
from value_iteration import value_iteration
import pickle
thetas = np.array([-142.12235333 ,-78.4391271 ,-142.26565079])
feat_map = np.load("feat_map_final.npy")
rewards = np.dot(feat_map,thetas)
P_a = np.load("P_a.npy")

with open('states_dict.pickle', 'r') as file:
        states_dict=pickle.load(file)
    
gamma = 0.9
values,policy= value_iteration(P_a, rewards, gamma, error=0.01, deterministic=True)
print(policy)
print(values)
print(rewards)
init_state = (1)
print(states_dict)
state_id = states_dict[init_state] #no HAS_ELECTRICITY
with open('all_actions.pickle', 'r') as file:
        all_actions=pickle.load(file)

reverse_actions={}

for key,value in all_actions:
	reverse_actions[value]=key

while True:
	action = policy[state_id]
	action_template = reverse_actions[action]
	print(action_template)
	state = list(state).append(action)
	state_id=states_dict[state]


