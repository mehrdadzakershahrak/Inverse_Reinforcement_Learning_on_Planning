import lavenstein
import os
import numpy as np
import maxent
import math
from itertools import chain, combinations
import pandas as pd



def powerset(iterable):
	s = list(iterable)
	return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

def get_plan_distance(plan_a, plan_b):
	plan_a = set(plan_a)
	plan_b = set(plan_b)
	return len(plan_a.intersection(plan_b))/len(plan_a.union(plan_b))

def get_plan():
	plan = os.popen('./planner/fast-downward.py meeting_1.pddl sc1.pddl --search "astar(lmcut())"').read()
	proc_plan = plan.split('\n')
	cost = [i for i, s in enumerate(proc_plan) if 'Plan cost:' in s]
	plan = proc_plan[proc_plan.index('Solution found!')+2: cost[0]-1]
	plan_cost = proc_plan[cost[0]].split(' ')[-1]
	return plan, plan_cost

def get_state_map(num_actions):
	states = list(powerset(range(num_actions)))
	states_dict = {}
	for i in range(len(states)):
		#states_dict[i] = list(states[i])
		states_dict[states[i]] = i
	return states_dict

def get_transition_function(num_actions):
	transition_matrix = np.zeros((2**num_actions, num_actions, 2**num_actions))
	states_dict = get_state_map(num_actions)
	
	for i in list(states_dict.keys()):
		for a in range(num_actions):
			if a not in i:
				temp = set(i)
				temp.add(a)
				transition_matrix[states_dict[i], a, states_dict[tuple(temp)]]=1
				#print(states_dict[i], a, states_dict[tuple(temp)])

	return transition_matrix

def write_file(explanation, add):
	expl_line = {'(not_have_coffee_beans ?j)': 23, '(have_five_minutes_for_breakfast ?j)' : 33,
					 '(have_formall_meeting ?j)' : 40, '(not_enough_lunch_time ?j)': 49,
					 '(dressed_for_formal-meeting ?j)': 65, '(at ?j ?h)' : 81}
	line = expl_line[explanation]

	with open('file_name', 'r') as file:
		data = file.readlines()
	
	if add:
		data[line] = data[line] + " " + explanation
	else:
		data[line] = data[line].replace(explanation, '')

	with open('file_name', '+w') as file:
		file.writelines(data)

def get_predicate():
	predicate_map = {
					'There are no coffee beans':'(not_have_coffee_beans ?j)',
					'There is a formal meeting':'(dressed_for_formal-meeting ?j)',
					'Not enough lunch time':'(not_enough_lunch_time ?j)',
					"Car doesn't start":'(car_not_works ?j)',
					"Car maintenance appointment at 8:15":'(car_not_works ?j)',
					"There is a meeting today": 'has_normal_meeting ?j'
					}
	return predicate_map
		
def get_explanation_map(problem_num):
	if problem_num==1:
		explanation_map = {
							"Car doesn't start": 0,
							'Not enough lunch time': 1,
							'There is a formal meeting': 2,
							'There are no coffee beans': 3
							}
	elif problem_num==2:
		explanation_map = {
							"Car doesn't start": 0,
							'Not enough lunch time': 1,
							'There is a formal meeting': 2,
							'There are no coffee beans': 3
							}
	elif problem_num==3:
		explanation_map = {
							"Car maintenance appointment at 8:15": 0,
							'Not enough lunch time': 1,
							'There are no coffee beans': 2
							}
	elif problem_num==4:
		explanation_map = {
							"Car doesn't start": 0,
							'Not enough lunch time': 1,
							"There is a meeting today": 2,
							'There are no coffee beans': 3
							}
	elif problem_num==5:
		explanation_map = {
							"Car doesn't start": 0,
							'Not enough lunch time': 1,
							'There is a formal meeting': 2,
							'There are no coffee beans': 3
							}
	elif problem_num==6:
		explanation_map = {
							"Car maintenance appointment at 8:15": 0,
							'There is a formal meeting': 1,
							'There are no coffee beans': 2
							}
	elif problem_num==7:
		explanation_map = {
							"Car doesn't start": 0,
							'Not enough lunch time': 1,
							'There is a formal meeting': 2,
							'There are no coffee beans': 3
							}
	elif problem_num==8:
		explanation_map = {
							"Car doesn't start": 0,
							'There is a formal meeting': 1,
							'There are no coffee beans': 2
							}
	elif problem_num==9:
		explanation_map = {
							"Car doesn't start": 0,
							"There is a meeting today": 1,
							'There are no coffee beans': 2,
							'Not enough lunch time': 3
							}
	elif problem_num==10:
		explanation_map = {
							"Car doesn't start": 0,
							'There is a formal meeting': 1,
							'There are no coffee beans': 2
							}

	return explanation_map

def get_explanation_map_r(problem_num):
	if problem_num==1:
		explanation_map_r = [
							"Car doesn't start",
							'Not enough lunch time',
							'There is a formal meeting',
							'There are no coffee beans'
							]
	return explanation_map_r

def get_feature_matrix(num_features, num_states, num_actions, explanation_map_r):
	feature_matrix = np.zeros((num_features, num_states, num_states))
	
	states_dict = get_state_map(num_actions)

	predicate_map = get_predicate()

	for i in list(states_dict.keys()):
		for a in i:
			write_file(predicate_map[explanation_map_r[a]], True)

		curent_plan, current_cost = get_plan()
		for action in range(num_actions):
			if action not in i:
				temp = set(i)
				temp.add(action)

				print(temp)

				#add explanation to domain
				write_file(predicate_map[explanation_map_r[action]], True)

				#Re-Plan
				new_plan, new_cost = get_plan()

				#get Features
				feature_matrix[0, states_dict[i], states_dict[tuple(temp)]] = abs(int(new_cost) - int(current_cost))
				feature_matrix[1, states_dict[i], states_dict[tuple(temp)]] = get_plan_distance(new_plan, curent_plan)
				feature_matrix[2, states_dict[i], states_dict[tuple(temp)]] = lavenstein.leven(lavenstein.listToString(new_plan), lavenstein.listToString(curent_plan))

				write_file(predicate_map[explanation_map_r[action]], False)
		for a in i:
			write_file(predicate_map[explanation_map_r[a]], false)

def get_explanation_data():
	# data = pd.read_csv("datap1.csv")
	# #data = np.array(data)
	# print(data.sample(3))
	# jefgei
	# return data[:,3:]
	data = [["There are no coffee beans", "There is a formal meeting", "Car doesn't start", "Not enough lunch time"],
			["There are no coffee beans", "Car doesn't start", "There is a formal meeting", "Not enough lunch time"],
			["There is a formal meeting", "There are no coffee beans", "Not enough lunch time", "Car doesn't start"],
			["There are no coffee beans", "There is a formal meeting", "Not enough lunch time", "Car doesn't start"],
			["Car doesn't start", "There are no coffee beans", "There is a formal meeting", "Not enough lunch time"],
			["There are no coffee beans", "Car doesn't start", "There is a formal meeting", "Not enough lunch time"]
			]
	return data

def main():
	
	num_actions = 4
	problem_num = 1

	#map of states and corresponding state numbers
	states_dict = get_state_map(num_actions)
	
	#map of explanations and actions
	explanation_map = get_explanation_map(problem_num)
	explanation_map_r = get_explanation_map_r(problem_num)

	# explanations from train data (3-D data)
	explanation_set = get_explanation_data()
	#print(explanation_set)


	#make trajectories
	trajectories = []
	for explanations in explanation_set:
		trajectory = [0]
		actions_taken=[]
		for explanation in explanations:
			action = explanation_map[explanation]
			temp = set(actions_taken)
			temp.add(action)
			next_state = states_dict[tuple(temp)]

			trajectory += [next_state] 
			actions_taken += [action]
			
		trajectories += [trajectory]

	#print(trajectories)

	# call IRL Function ( reward-----> R(s, s') )
	n_iters = 1000
	learning_rate = 0.01
	num_states = 2**num_actions
	gamma =0.9
	num_features = 3

	#transition function
	transition_matrix = get_transition_function(num_actions)
	#print(transition_matrix)

	#get feature mattrix
	feature_matrix =  get_feature_matrix(num_features, num_states, num_actions, explanation_map_r)
	print(feature_matrix)
	jvuy

	feature_matrix = feature_matrix.reshape((num_features, num_states*num_states))

	#call IRL
	rewards = maxent.irl(feature_matrix, num_actions, gamma, transition_matrix, trajectories, n_iters, learning_rate)

main()