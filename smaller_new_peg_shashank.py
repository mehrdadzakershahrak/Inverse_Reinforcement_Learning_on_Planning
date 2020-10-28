import numpy as np
import pprint
import re
import os
from itertools import chain, combinations
from feature_functions import laven_dist, plan_distance,action_distance
import pickle
from os import path
import sys
import copy
from utils import *


def store_traces(trace_files,scenario_wise = False):
    '''
    input: tuple containing full path of demonstration files(Explanations)
    This function parses the explanation files and stores in the global tuple traces in the order of scenarios
    '''
    global TRACE_ROOT_PATH
    if scenario_wise:
        traces = {}
    else:
        traces = []

    num_scenarios = len(trace_files)

    for i in range(num_scenarios):
        scenario_file = open(trace_files[i],'r')
        lines = scenario_file.readlines()
        scenario_file.close()
        trace = []
        if scenario_wise:
            traces[i]=[]
        for line in lines:
            if line[0]=='-':
                if scenario_wise:
                    traces[i].append(trace)
                else:
                    traces.append(trace)
                trace = []
            else:
                trace.append(line.rstrip())
    return traces

def render_domain_template(D):
    '''
    This function renders the domain (scavenger_edited.pddl) file from substitutions corresponding to dictionary
    input: dictionary of substitutions
    '''
    global PROBLEM_ROOT_PATH
    with open(PROBLEM_ROOT_PATH+'scavenger_edited.tpl.pddl','r') as f:
        domain = f.readlines()
    for j in range(len(domain)):
        if '$' in domain[j]:
            for word in D.keys():  # replace all occurences of dictionary keys with corresponding values
                domain[j] = domain[j].replace(word, D[word])

    domain_template = open(PROBLEM_ROOT_PATH + 'scavenger_edited.pddl', 'w')
    domain_template.write(''.join(domain))
    domain_template.close()


def get_actions(domain_file_lines, all_possible_actions):  # overloaded function
    '''
    input: all_possible_actions: is the dict with every possible explanation enumerated
    This function reads the domain template file and records all predicates with '$' which are the possible explanations/actions in the MDP
    :return: action_set
    '''
    lines = list(domain_file_lines)
    unique_words = set()
    for line in lines:
        if '$' in line:
            word = re.findall(r"\$\w+", line)
            unique_words.update(word)

    possible_actions = []
    for word in unique_words:
        if word in all_possible_actions.keys():
            possible_actions.append(all_possible_actions[word])
    return possible_actions


def get_actions(domain_file_lines):
    '''
    This function reads the domain template file and records all predicates with '$' which are the possible explanations/actions in the MDP
    :return: action_set
    '''
    global PROBLEM_ROOT_PATH
    lines = list(domain_file_lines)
    unique_words = set()
    for line in lines:
        if '$' in line:
            word = re.findall(r"\$\w+", line)
            unique_words.update(word)
    all_possible_actions= {k: v for v, k in enumerate(unique_words)}
    return all_possible_actions


def get_transition_matrix(all_actions,states_dict):
    '''

    :param actions: dict, all possible actions
    :param states_dict: states to number mapping
    :return: P_a transition probability matrix
    '''
    num_actions = len(all_actions)
    transition_matrix = np.zeros((2 ** num_actions, num_actions, 2 ** num_actions))
    for i in states_dict.keys():  # for each state,
        for a in list(set(all_actions.values()) - set(i)):  # for each explanation not yet done..
            try:
                new_state = list(i)
                new_state.append(a)
                transition_matrix[states_dict[i], a, states_dict[tuple(sorted(new_state))]] = 1  # update transition matrix
            except (IndexError,KeyError) as e:
                print("incorrect new state!")
                print(new_state)
                print(a)
                #input()

    return transition_matrix


def powerset(iterable):
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))


def get_state_map(actions):
    states = list(powerset(sorted(actions.values())))
    states_dict = {}
    reverse_states_dict = {}
    for i in range(len(states)):
        states_dict[states[i]] = i
        reverse_states_dict[i] = states[i]

    return states_dict, reverse_states_dict


def get_plan(state,all_actions,problem_file_used):
    '''
    input: state: tuple of all actions taken till reaching state, all_actions: dict of all actions assigned to a number
    output: plan obtained by running planner on input files
    '''
    global PLANNER_RELATIVE_PATH

    # generate dictionary corresponding to substitutions and render domain template to get plan
    subs_dict = {}
    for action_template in all_actions.keys():
        if all_actions[action_template] in state:
            subs_dict[action_template] = '(' + str.lower(action_template[1:]) + ')'
        else:
            subs_dict[action_template] = ''
    render_domain_template(subs_dict)

    cmd = '.' + PLANNER_RELATIVE_PATH + 'fast-downward.py --sas-file temp_' + str(0) + '.sas --plan-file plan_' + str(
        0) + ' ' + 'Archive/scavenger_edited.pddl' + ' ' + 'Archive/' + 'p' + str(
        problem_file_used) + '_edited.pddl' + ' --search "astar(lmcut())"'
    # print(cmd)
    plan = os.popen(cmd).read()
    proc_plan = plan.split('\n')
    cost = [i for i, s in enumerate(proc_plan) if 'Plan cost:' in s]
    if 'Solution found!' not in proc_plan:
        # print("No Solution")
        return [], 0
    plan = proc_plan[proc_plan.index('Solution found!') + 2: cost[0] - 1]
    plan_cost = float(proc_plan[cost[0]].split(' ')[-1])
    #print(plan)
    return plan, plan_cost


def calculate_features(plan1, plan2, plan1_cost, plan2_cost,state1,state2):
    '''
    input: 2 plans and an explanation
    output: feature vectors corresponding to the inputs

    calculate_lavenstein_distance
    calculate_plan_cost
    calculate_plan_distance
    calculate_domain_dependent_features based on explanation
    return all values in an array
    '''
    all_actions = ['$HAS_KEY','$HAS_PASSWORD','$HAS_ACCESSKEY','$HAS_LADDER','$HAS_ELECTRICITY']
    lav_dist = laven_dist(plan1, plan2) 
    plan_dist = action_distance(plan1, plan2)
    f1 = [0]*len(all_actions)
    f2 = [0]*len(all_actions)
    f3 = [0]*len(all_actions)
    # for a in range(len(all_actions)):
    #     if a in state1:
    #         f1[a]=1
    #     if a in state2:
    #         f2[a]=1
    for a in range(len(all_actions)):
        if a in state1 and a not in state2:
            f3[a]=0
        if a in state2 and a not in state1:
            f3[a]=1
        if a in state1 and a in state2 :
            f3[a]=2
        if a not in state1 and a not in state2:
            f3[a]=3 
    
    #f = [lav_dist,plan_dist,abs(plan1_cost-plan2_cost),*np.append(np.array(f1),np.array(f2)).tolist()]
    f = [lav_dist,plan_dist,abs(plan1_cost-plan2_cost),*f3]
    
    return f


def get_feat_map_from_states(states_dict,feat_map,applicable_states,P_a,applicable_actions,problem_file_used,all_actions):
    '''
    OVERLOADED FUNCTION: for updating feat_map from applicable actions
    This function calculates the features corresponding to the states containined in states_dict
    :param actions:     tuple containing all possible actions (numeric)
    :param num_features: number of features
    :param transition_P: Transition matrix of the form (s,a,s') [NxAxN]
    :return: feature map containing features for all state-next_state pair.
    '''
    global state_pairs_found, num_features
    total_number = 1.0*len(applicable_states)**2
    count = 0.0
    c = 0
    for state in applicable_states:
        for next_state in applicable_states:
            c+=1
            s1 = set(sorted(state))
            s2 = set(sorted(next_state))
            if s1.issubset(s2) and (len(s2)-len(s1)==1): #possible state-pair
                if [s1,s2] not in state_pairs_found:
                    state_pairs_found.append([state,next_state])
                count+=1
                state_id = states_dict[state]
                next_state_id = states_dict[next_state]
                plan, plan_cost = get_plan(state,all_actions,problem_file_used)
                feat_map[state_id, state_id] = np.zeros([1,num_features])# calculate_features(plan,plan,plan_cost,plan_cost)
                if any(P_a[state_id, :, next_state_id]) == 1:
                    new_plan, new_plan_cost = get_plan(next_state,all_actions,problem_file_used)
                    features = calculate_features(plan, new_plan, plan_cost, new_plan_cost,state,next_state)
                    feat_map[state_id, next_state_id] = features


            sys.stdout.write('\r' + "Progress:"+ str(count) + "/" +str(total_number)+" ,applicable states:"+str(len(applicable_states)))
            sys.stdout.flush()

    return feat_map


def get_trajectories_from_traces(all_actions,trace_list,states_dict,initial_states):
    '''
    This function converts expert demos into state-next_state-trajectories of the shape: TXLx2 where T is the number of trajectories, L is the length of each trajectory
    and each item is a state-next_state (int) pair
    '''
    num_traces = len(trace_list[0])*len(trace_list)
    trajectories = np.zeros([num_traces, len(all_actions), 2])
    count = 0
    for sc in range(len(trace_list)): #for each scenario
        for i in range(len(trace_list[sc])): # for each trace of each scenario
            try:
                state = list(initial_states[sc])
            except IndexError as e:
                print("HERE")
                input()
            for j in range(len(trace_list[sc][i])): #for each explanation of each trace
                action = all_actions['$' + str.upper(trace_list[sc][i][j])]                
                try:
                    trajectories[count, j, 0] = states_dict[tuple(sorted(state))]
                except KeyError:
                    print([i, j])
                state.append(action)
                try:
                    trajectories[count, j, 1] = states_dict[tuple(sorted(state))]
                except KeyError:
                    print([i, j])
            count+=1

    return trajectories


def update_domain_template_and_problem_file(og_domain_template,problem_file_used,all_actions):
    '''
    This function updates the domain.tpl.pddl file by replacing $terms which are already present in initial state as defined in the problem file
    '''
    global PROBLEM_ROOT_PATH
    domain = og_domain_template
    problem_file = open(PROBLEM_ROOT_PATH + "p" + str(problem_file_used) + ".pddl", 'r')
    problem = problem_file.readlines()
    problem_file.close()
    situation_variables = []

    for i in range(len(problem)):  # find all situation variables in problem file
        if '$' in problem[i]:
            [situation_variables.append(str.upper(s.replace('(', '').replace(')', ''))) for s in
             re.findall(r'\$\(\w+\)+', problem[i])]
            problem[i] = problem[i].replace('$', '')  # remove $ in problem file

    common = list(
        set(all_actions.keys()).intersection(set(situation_variables)))  # Situation variables which are also explanations

    subs_dict = dict.fromkeys(all_actions.keys(), '')
    applicable_actions = {}
    for action in all_actions:
        if action not in common:
            applicable_actions[action] = all_actions[action]
            subs_dict[action] = action
        else:
            subs_dict[action] = '(' + str.lower(action[1:]) + ')'

    print("Common predicates: " + str(common))
    print("New action set:")
    pp.pprint(applicable_actions.values())
    domain_subs_dict = dict.fromkeys(all_actions.keys(), '')

    problem_file = open(PROBLEM_ROOT_PATH + "p" + str(problem_file_used) + "_edited.pddl", 'w')
    problem_file.write(''.join(problem))
    problem_file.close()

    for i in range(len(domain)):
        if '$' in domain[i]:
            for word in subs_dict.keys():  # replace all occurences of dictionary keys with corresponding values
                domain[i] = domain[i].replace(word, subs_dict[word])

    domain_template = open(PROBLEM_ROOT_PATH + 'scavenger_edited.tpl.pddl', 'w')
    domain_template.write(''.join(domain))
    domain_template.close()
    print("Updated domain template and problem file")

    return domain, applicable_actions,common


if __name__ == "__main__":
    TRACE_ROOT_PATH = '/data/Distance-Learning/Train/'
    PROBLEM_ROOT_PATH = '/data/Distance-Learning/Archive/'
    PLANNER_RELATIVE_PATH = '/FD/'
    pp = pprint.PrettyPrinter(indent=4)
    num_features = 8


    files_used = [1,2,3,4,5,6,7,8]

    with open(PROBLEM_ROOT_PATH+'scavenger.tpl.pddl', 'r') as f:
        og_template = f.readlines()

    all_actions = get_actions(og_template) #dict: find all possible actions in original domain, actions are now all_actions.values()

    states_dict, reverse_states_dict = get_state_map(all_actions) #need all states
    N = len(states_dict)
    print("total number of states: "+str(N))   
    feat_map = np.zeros([N, N, num_features])
    
    with open('states_dict.pickle', 'wb') as handle:
        pickle.dump(states_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)
    with open('all_actions.pickle', 'wb') as handle:
        pickle.dump(all_actions, handle, protocol=pickle.HIGHEST_PROTOCOL)
    
    P_a = get_transition_matrix(all_actions, states_dict)

    state_pairs_found = []

    trace_files = [TRACE_ROOT_PATH + 'p' + str(i) + '.txt' for i in files_used]
    traces = store_traces(trace_files,scenario_wise=True)
    initial_states = []
    print("All Actions:")
    pp.pprint(all_actions)
    problem_file_used = 0
    updated_domain_template_lines,applicable_actions,difference_actions = \
        update_domain_template_and_problem_file(og_template,problem_file_used,all_actions)
   
    applicable_states = []
    #pass only applicable states to feat_map
    for state in states_dict.keys():
        dont_add = False
        for action in difference_actions:
            if all_actions[action] in state:
                dont_add = True
        if not dont_add:
            applicable_states.append(state)

    print("Calculating feature map")
    feat_map = get_feat_map_from_states(states_dict,feat_map,applicable_states,P_a,applicable_actions,problem_file_used,all_actions)
    np.save("feat_map_problem_"+str(problem_file_used)+str(".npy"),feat_map)
    
    for i in range(np.shape(feat_map)[-1]):
        feat_map[:,:,i]=normalize(feat_map[:,:,i])



    print("\n Done "+str(problem_file_used))
    print("---------------------------------")


    for problem_file_used in files_used:
        updated_domain_template_lines,applicable_actions,difference_actions = \
            update_domain_template_and_problem_file(og_template,problem_file_used,all_actions)
        s = [] #initial state for the problem file used
        for a in difference_actions:
            s.append(all_actions[a])
        initial_states.append(tuple(s))
        print(initial_states)
        
    trajectories = get_trajectories_from_traces(all_actions, traces, states_dict,initial_states)
    print(trajectories)
    for i in range(np.shape(trajectories)[0]):
        if list(trajectories[i,-1,:])==[0.0,0.0]:
            trajectories[i,-1,:]=[31,31]
        if list(trajectories[i,-2,:])==[0.0,0.0]:
            trajectories[i,-2,:]=[31,31]


    np.save("feat_map_final.npy",feat_map)
    np.save("trajectories.npy",trajectories)
    np.save("P_a.npy",P_a)
    for state in states_dict.keys():
        for next_state in states_dict.keys():
            if [state,next_state] not in state_pairs_found:
                s1 = set(sorted(state))
                s2 = set(sorted(next_state))
                if s1.issubset(s2) and (len(s2)-len(s1) == 1): #possible state-pair
                    print(str([state,next_state]))

    initial_states = []
    for problem_file_used in [0,1,2,3,4,5,6,7,8]:
        updated_domain_template_lines,applicable_actions,difference_actions = \
            update_domain_template_and_problem_file(og_template,problem_file_used,all_actions)
        s = [] #initial state for the problem file used
        for a in difference_actions:
            s.append(all_actions[a])
        initial_states.append(tuple(s))
        print(initial_states)
    
    #print(len(state_pairs_found))
    #print(trajectories)
    #print(initial_states)
    