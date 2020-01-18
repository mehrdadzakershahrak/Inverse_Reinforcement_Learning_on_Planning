import numpy as np
from value_iteration import value_iteration
import pickle
#thetas = np.array([15.86783182, 22.40267407, 12.1497361 , 50.92159157, 45.28974856,
#       28.96656884])
#thetas = np.array([-10.0,-5,-5,0.0,0.0,1.0])
thetas = np.load('final_thetas.npy')
feat_map = np.load("feat_map_final.npy")
#rewards = np.load("rewards.npy")
rewards = np.dot(feat_map,thetas)
print(np.shape(rewards))
P_a = np.load("P_a.npy")

with open('states_dict.pickle', 'rb') as file:
        states_dict=pickle.load(file)

gamma = 0.8
values,policy= value_iteration(P_a, rewards, gamma, error=0.01, deterministic=True)
#print(policy)
#print('=======================')
#print(values)
#print('===========RRR===========')
#print(rewards)
count = 0
with open('all_actions.pickle', 'rb') as file:
	        all_actions=pickle.load(file)

#init_states =[(), (4,), (0, 3), (2,), (2, 4), (3,), (0,), (1,), (0, 1)]
#init_states=[[2,0,5],[1,0,5],[6,7,0],[6,7,5],[0,5,4],[3,4,6],[2,6,4],[3,2,6],[6,1,3],[7,2,3]]
init_states = [[]]
print("------------------------------------------")
#all_init_states = [(),(0,),(0,1),(0,2),(0,3),(0,4),(1,),(1,2),(1,3),(1,4),(2,),(2,3),(2,4),(3,),(3,4),(4,)]
for init_state in init_states:
	print(count)
	print("--------------------")
	state = tuple(sorted(init_state))
	#print(states_dict)
	state_id = states_dict[state] 
	reverse_actions={}

	for key in all_actions.keys():
		reverse_actions[all_actions[key]]=key

	while True:
		action = int(policy[state_id])
		action_template = reverse_actions[action]
		print(action_template)
		state = list(state)
		state.append(action)
		if sorted(state) == [0,1,2,3,4,5]:
			break
		state_id=states_dict[tuple(sorted(state))]
	count+=1
'''
print("-------------New situations:-----------------------")
for init_state in all_init_states:
	if sorted(init_state) not in init_states:
		print(count)
		state = tuple(sorted(list(init_state)))
		print(states_dict)
		state_id = states_dict[state] 
		reverse_actions={}

		for key in all_actions.keys():
			reverse_actions[all_actions[key]]=key

		while True:
			action = int(policy[state_id])
			action_template = reverse_actions[action]
			print(action_template)
			state = list(state)
			state.append(action)
			if sorted(state) == [0,1,2,3,4,5,6,7]:
				break
			state_id=states_dict[tuple(sorted(state))]
		count+=1
'''
	









