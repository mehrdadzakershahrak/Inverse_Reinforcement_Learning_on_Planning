import numpy as np
import pprint
import re
import os
from itertools import chain, combinations
from feature_functions import laven_dist, plan_distance
import pickle
from os import path
import sys
import copy
from utils import *


def store_traces(trace_files, scenario_wise=False):
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
        scenario_file = open(trace_files[i], 'r')
        lines = scenario_file.readlines()
        scenario_file.close()
        trace = []
        if scenario_wise:
            traces[i] = []
        for line in lines:
            if line[0] == '-':
                if scenario_wise:
                    traces[i].append(trace)
                else:
                    traces.append(trace)
                trace = []
            else:
                trace.append(line.rstrip())
    return traces


def render_problem_template(D):
    '''
    This function renders the domain (scavenger_edited.pddl) file from substitutions corresponding to dictionary
    input: dictionary of substitutions
    sample dict: {A:0,B:1,C:0}
    active explanations have value 1 and others have value 0
    when any explanation is done, add the cost to every line which ends in that cell
    '''
    global PROBLEM_ROOT_PATH, cost_dict

    with open(PROBLEM_ROOT_PATH + 'problem.tpl.pddl', 'r') as f:
        og = f.readlines()

    for i in range(len(og)):
        if 'length' in og[i]:
            for e in cost_dict.keys():
                if D[e] == 1:
                    if str(e) + ')' in og[i]:
                        nums = re.findall(r'\d+', og[i])[0]
                        cost = str(int(cost_dict[e] + int(nums)))
                        og[i] = og[i].replace(nums, cost)

    problem_template = open(PROBLEM_ROOT_PATH + 'p0.pddl', 'w')
    problem_template.write(''.join(og))
    problem_template.close()


def get_transition_matrix(all_actions, states_dict):
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
                transition_matrix[
                    states_dict[i], a, states_dict[tuple(sorted(new_state))]] = 1  # update transition matrix
            except (IndexError, KeyError) as e:
                print("incorrect new state!")
                print(new_state)
                print(a)
                # input()

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


def get_plan(state, all_actions, problem_file_used):
    '''
    input: state: tuple of all actions taken till reaching state, all_actions: dict of all actions assigned to a number
    output: plan obtained by running planner on input files
    '''
    global PLANNER_RELATIVE_PATH

    # generate dictionary corresponding to substitutions and render domain template to get plan
    subs_dict = {}
    for action_template in all_actions.keys():
        if all_actions[action_template] in state:
            subs_dict[action_template] = 1
        else:
            subs_dict[action_template] = 0
    # print(subs_dict)
    render_problem_template(subs_dict)

    cmd = '.' + PLANNER_RELATIVE_PATH + 'fast-downward.py --sas-file temp_' + str(0) + '.sas --plan-file plan_' + str(
        0) + ' ' + 'Archive/domain.pddl' + ' ' + 'Archive/' + 'p' + str(
        problem_file_used) + '.pddl' + ' --search "astar(lmcut())"'
    # print(cmd)
    plan = os.popen(cmd).read()
    proc_plan = plan.split('\n')
    cost = [i for i, s in enumerate(proc_plan) if 'Plan cost:' in s]
    if 'Solution found!' not in proc_plan:
        print("No Solution")
        return [], 0
    plan = proc_plan[proc_plan.index('Solution found!') + 2: cost[0] - 1]
    plan_cost = float(proc_plan[cost[0]].split(' ')[-1])
    return plan, plan_cost


def calculate_features(plan1, plan2, plan1_cost, plan2_cost, state1, state2):
    '''
    input: 2 plans and an explanation
    output: feature vectors corresponding to the inputs

    calculate_lavenstein_distance
    calculate_plan_cost
    calculate_plan_distance
    calculate_domain_dependent_features based on explanation
    return all values in an array
    '''
    global all_actions,cost_dict,distances
    all_actions_list = ['A', 'B', 'C', 'D', 'E', 'F', 'J']

    lav_dist = laven_dist(plan1, plan2)
    plan_dist = plan_distance(plan1, plan2)

    #magnitude of just explained
    state1 = set(state1)
    state2 = set(state2)
    cost = 0
    just_explained = list(state2.difference(state1))
    for key in all_actions:
        if all_actions[key] in just_explained:
            cost = cost_dict[key]
            dist = distances[key]

    f = [lav_dist, plan_dist, abs(plan1_cost - plan2_cost),*dist]
    return f


def get_feat_map_from_states(states_dict, feat_map, P_a, problem_file_used, all_actions):
    '''
    OVERLOADED FUNCTION: for updating feat_map from applicable actions
    This function calculates the features corresponding to the states containined in states_dict
    :param actions:     tuple containing all possible actions (numeric)
    :param num_features: number of features
    :param transition_P: Transition matrix of the form (s,a,s') [NxAxN]
    :return: feature map containing features for all state-next_state pair.
    '''
    global state_pairs_found, num_features
    total_number = 1.0 * len(applicable_states) ** 2
    count = 0.0
    c = 0
    for state in applicable_states:
        for next_state in applicable_states:
            c += 1
            s1 = set(sorted(state))
            s2 = set(sorted(next_state))
            if s1.issubset(s2) and (len(s2) - len(s1) == 1):  # possible state-pair
                if [s1, s2] not in state_pairs_found:
                    state_pairs_found.append([state, next_state])
                count += 1
                state_id = states_dict[state]
                next_state_id = states_dict[next_state]
                plan, plan_cost = get_plan(state, all_actions, problem_file_used)
                feat_map[state_id, state_id] = np.zeros(
                    [1, num_features])  # calculate_features(plan,plan,plan_cost,plan_cost)
                if any(P_a[state_id, :, next_state_id]) == 1:
                    new_plan, new_plan_cost = get_plan(next_state, all_actions, problem_file_used)
                    features = calculate_features(plan, new_plan, plan_cost, new_plan_cost, state, next_state)
                    feat_map[state_id, next_state_id] = features

            sys.stdout.write('\r' + "Progress:" + str(count) + "/" + str(total_number) + " ,applicable states:" + str(
                len(applicable_states)))
            sys.stdout.flush()

    return feat_map


def get_trajectories_from_traces(all_actions, trace_list, states_dict):
    '''
    This function converts expert demos into state-next_state-trajectories of the shape: TXLx2 where T is the number of trajectories, L is the length of each trajectory
    and each item is a state-next_state (int) pair
    '''
    #global num_traces
    num_traces = len(trace_list[0]) * len(trace_list)
    trajectories = np.zeros([num_traces, 5, 2])
    count = 0
    for sc in range(len(trace_list)):  # for each scenario
        for i in range(len(trace_list[sc])):  # for each trace of each scenario
            try:
                state = list(())
            except IndexError as e:
                print("HERE")
                input()
            for j in range(len(trace_list[sc][i])):  # for each explanation of each trace
                action = all_actions[str.upper(trace_list[sc][i][j])]
                try:
                    trajectories[count, j, 0] = states_dict[tuple(sorted(state))]
                except KeyError:
                    print([i, j])
                state.append(action)
                try:
                    trajectories[count, j, 1] = states_dict[tuple(sorted(state))]
                except KeyError:
                    print([i, j])
            count += 1

    return trajectories


if __name__ == "__main__":
    dir_path = os.path.dirname(os.path.realpath('__file__'))
    TRACE_ROOT_PATH = dir_path+'/'+'Train/'
    PROBLEM_ROOT_PATH = dir_path+'/'+'Archive/'
    PLANNER_RELATIVE_PATH = '/FD/'
    num_traces = 50
    pp = pprint.PrettyPrinter(indent=4)
    problem_file_used = 0
    num_features = 5

    cost_dict = {'A': 1000, 'B': 1000, 'C': 1000, 'D': 1000, 'E': 1000, 'F': 1000}
    all_actions = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5}
    distances = {'A':[-1,0],'B':[8,2],'C':[5,1],'D':[3,4],'E':[1,1],'F':[7,1]}

    files_used = [1]

    with open(PROBLEM_ROOT_PATH + 'problem.tpl.pddl', 'r') as f:
        og_template = f.readlines()

    states_dict, reverse_states_dict = get_state_map(all_actions)  # need all states
    N = len(states_dict)
    print("total number of states: " + str(N))
    feat_map = np.zeros([N, N, num_features])

    with open('states_dict.pickle', 'wb') as handle:
        pickle.dump(states_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)
    with open('all_actions.pickle', 'wb') as handle:
        pickle.dump(all_actions, handle, protocol=pickle.HIGHEST_PROTOCOL)

    P_a = get_transition_matrix(all_actions, states_dict)

    state_pairs_found = []

    ################# CHECK WITH NEW TRACES ########
    trace_files = [TRACE_ROOT_PATH + 'p' + str(i) + '.txt' for i in files_used]
    traces = store_traces(trace_files, scenario_wise=True)
    ###############################################

    initial_states = []
    print("All Actions:")
    pp.pprint(all_actions)

    applicable_states = list(states_dict.keys())
    print("Calculating feature map")
    trajectories = get_trajectories_from_traces(all_actions, traces, states_dict)
    print(trajectories)

    feat_map = get_feat_map_from_states(states_dict, feat_map, P_a, problem_file_used, all_actions)

    for i in range(np.shape(feat_map)[-1]):
        feat_map[:, :, i] = normalize(feat_map[:, :, i])

    print("\n Done " + str(problem_file_used))
    print("---------------------------------")


    np.save("feat_map_final.npy", feat_map)
    np.save("trajectories.npy", trajectories)
    np.save("P_a.npy", P_a)
    for state in states_dict.keys():
        for next_state in states_dict.keys():
            if [state, next_state] not in state_pairs_found:
                s1 = set(sorted(state))
                s2 = set(sorted(next_state))
                if s1.issubset(s2) and (len(s2) - len(s1) == 1):  # possible state-pair
                    print(str([state, next_state]))
