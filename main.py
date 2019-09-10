import lavenstein
import os
import maxent

def get_plan_distance(plan_a, plan_b):
	plan_a = set(plan_a)
	plan_b = set(plan_b)
	return len(plan_a.intersection(plan_b))/len(plan_a.union(plan_b))

def get_plan():
	plan = os.popen('./planner/fast-downward.py domain.pddl pfile01 --search "astar(lmcut())"').read()
	proc_plan = plan.split('\n')
	cost = [i for i, s in enumerate(proc_plan) if 'Plan cost:' in s]
	plan = proc_plan[proc_plan.index('Solution found!')+2: cost[0]-1]
	plan_cost = proc_plan[cost[0]].split(' ')[-1]
	return plan, plan_cost

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




def main():

	#plan = os.popen('./planner/fast-downward.py domain.pddl pfile01 --search "astar(lmcut())"').read()
	#proc_plan = plan.split('\n')

	# get base plan
	curent_plan, current_cost = get_plan()

	# cost = [i for i, s in enumerate(proc_plan) if 'Plan cost:' in s]
	# cost distance
	#plan_cost = proc_plan[cost[0]].split(' ')[-1]

	# plan_h = proc_plan[proc_plan.index('Solution found!')+2: cost[0]-1]
	# plan_r = proc_plan[proc_plan.index('Solution found!')+2: cost[0]]

	# plan_h will be generated from the list of the explanations

	explanation_set = [[1]]
	trajectories = []
	for explanations in explanation_set:
		trajectory = []
		for explanation in explanations:

			#modify pddl


			#get plan
			new_plan, new_cost = get_plan()

			#generate features
			cost_distance = abs(int(new_cost) - int(current_cost))
			plan_distance = get_plan_distance(new_plan, curent_plan)
			lavenstein_distance =  lavenstein.leven(lavenstein.listToString(new_plan), lavenstein.listToString(curent_plan))

			features = [cost_distance, plan_distance, lavenstein_distance]
			trajectory += [features]

			curent_plan = new_plan
			current_cost =  new_cost

		trajectories += [trajectory]

	print(trajectories)

	# call IRL Function ( reward-----> R(s, s') )

	n_iters = 1000
	learning_rate = 0.01
	num_actions = 3
	num_states = 2**num_actions
	gamma =0.9

	#transition function (needs to be computed)

	rewards = maxent.irl(feature_matrix, num_actions, gamma, transition_matrix, trajectories, n_iters, learning_rate)

	# print(plan_dist(plan_h, plan_r))

	# print(lavenstein.leven(lavenstein.listToString(plan_h),lavenstein.listToString(plan_r)))
	# print(lavenstein.listToString(plan_h))
	# print(lavenstein.listToString(plan_r))

main()
