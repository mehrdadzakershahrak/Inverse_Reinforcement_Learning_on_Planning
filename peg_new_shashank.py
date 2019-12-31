import numpy as np
import pprint
import re
import os
from itertools import chain, combinations
from feature_functions import laven_dist,plan_distance
import pickle
from new_maxent_irl import maxent_irl
from os import path
import copy

############## NOT USED ##################

def calculate_states_from_traces():
    '''
    input:
        applicable_actions: (tuple) all the possible actions for the current problem file
    output:
        S : explanations(history format) -> number (id)
        R : reverse mapping of S
    This function uses the traces to generate history-type string-encoded explanations used for feature generation


    '''
    global traces
    S = {}
    R = {}
    n = 0
    for i in range(len(traces)): #for each scenario
        s = str(i) + '_'
        if s not in S:
            S[s] = n
            R[n] = s
            n += 1
        for trace in traces[i]: #new expert demo
            s = str(i) + '_'    #s is (4_,password),(4_,password,get_key) and so on
            for word in trace:
                s += ','+word
                if s not in S:
                    S[s] = n
                    R[n] = s
                    n += 1



    return S, R                 # S now contains mapping from explanation (history format) to number (like id) and R now contains mapping from number (like id) to explanation (history-format)

def render_problem_template(sc,D):
    try:
        problem_template = open(PROBLEM_ROOT_PATH + 'p' + str(sc) + '.tpl.pddl', 'r')
        problem = problem_template.readlines()
        problem_template.close()

        for j in range(len(problem)):
            if '$' in problem[j]:
                for word in D.keys():  # replace all occurences of dictionary keys with corresponding values
                    problem[j].replace('$' + str.upper(word), D[word])

        problem_template = open(PROBLEM_ROOT_PATH + 'p' + str(sc) + '_edited.pddl', 'w')
        problem_template.write(''.join(problem))
        problem_template.close()

    except IOError:
        print("Problem template file doesn't exist")

##########################################
def store_traces(trace_files,scenario_wise = False):
    '''
    input: tuple containing full path of demonstration files(Explanations)
    This function parses the explanation files and stores in the global tuple traces in the order of scenarios
    '''
    global traces,TRACE_ROOT_PATH
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

def render_domain_template(D):
    '''
    This function renders the domain (scavenger_edited.pddl) file from substitutions corresponding to dictionary
    input: dictionary of substitutions
    '''
    global PROBLEM_ROOT_PATH,domain_file_lines
    domain = list(domain_file_lines)
    for j in range(len(domain)):
        if '$' in domain[j]:
            for word in D.keys():  #replace all occurences of dictionary keys with corresponding values
                #print(domain[j])
                domain[j]=domain[j].replace(word,D[word])
                #print(domain[j])
                #print(domain[j])

    domain_template = open(PROBLEM_ROOT_PATH+'scavenger_edited.pddl','w')
    domain_template.write(''.join(domain))
    domain_template.close()

def get_actions(domain_file_lines,all_possible_actions): #overloaded function
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
    return list(unique_words)

def get_transition_matrix():
    global unique_words,states_dict
    unique_explanations = []
    num_actions = len(unique_words)
    '''
    Each unique explanation is associated with the number which is its index in the unique_words tuple
    '''
    #states_dict = get_state_map(num_actions)    # each state is a unique number associated with which all explanations have bdone till then
    transition_matrix = np.zeros((2 ** num_actions, num_actions, 2 ** num_actions))
    for i in states_dict.keys():                        #for each state,
        for a in list(set(range(num_actions))-set(i)):  #for each explanation not yet done..
                try:
                    new_state = list(i)
                    new_state.append(a)
                    transition_matrix[states_dict[i], a, states_dict[tuple(sorted(new_state))]]=1 #update transition matrix
                except KeyError:
                    print("incorrect new state!")
                    input()

    return transition_matrix

def powerset(iterable):
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

def get_state_map(num_actions):
    states = list(powerset(range(num_actions)))
    states_dict = {}
    reverse_states_dict = {}
    for i in range(len(states)):
        states_dict[states[i]] = i
        reverse_states_dict[i] = states[i]

    return states_dict,reverse_states_dict

def run_planner(problem_number,idx):
    '''
    input: self explanatory
    output: plan obtained by running planner on input files
    '''
    global PLANNER_RELATIVE_PATH,problem_file_used
    cmd = '.'+PLANNER_RELATIVE_PATH+'fast-downward.py --sas-file temp_'+ str(idx) +'.sas --plan-file plan_'+ str(idx) +' '+'Archive/scavenger_edited.pddl'+' '+'Archive/'+'p'+str(problem_file_used)+'_edited.pddl'+' --search "astar(lmcut())"'
    #print(cmd)
    plan = os.popen(cmd).read()
    proc_plan = plan.split('\n')
    cost = [i for i, s in enumerate(proc_plan) if 'Plan cost:' in s]
    if 'Solution found!' not in proc_plan:
        #print("No Solution")
        return [], 0
    plan = proc_plan[proc_plan.index('Solution found!')+2: cost[0]-1]
    plan_cost = float(proc_plan[cost[0]].split(' ')[-1])
    return plan, plan_cost

def calculate_features(plan1,plan2,plan1_cost,plan2_cost):
    '''
    input: 2 plans and an explanation
    output: feature vectors corresponding to the inputs
   
    calculate_lavenstein_distance
    calculate_plan_cost
    calculate_plan_distance
    calculate_domain_dependent_features based on explanation
    return all values in an array  
    '''
    lav_dist = laven_dist(plan1,plan2)
    plan_dist = plan_distance(plan1,plan2)
    return [lav_dist,plan_dist,abs(plan1_cost-plan2_cost)]

def get_plan(problem_number,state):
    global unique_words,domain_file_lines,reverse_states_dict
    #generate dictionary corresponding to substitutions and render domain template to get plan
    subs_dict = {}
    state = reverse_states_dict[state]
    for action in range(len(unique_words)):
        action_template = unique_words[action]
        if action in state:
            subs_dict[action_template] = '('+str.lower(action_template[1:])+')'
        else:
            subs_dict[action_template]=''
    render_domain_template(subs_dict)
    plan,plan_cost = run_planner(problem_number,0)
    '''
    if plan!=[]:
        print(plan)
    '''
    return plan,plan_costdrix

def get_feat_map_from_states(num_features):
    '''
    This function calculates the features corresponding to the states containined in states_dict
    :param actions:     tuple containing all possible actions (numeric)
    :param num_features: number of features
    :param transition_P: Transition matrix of the form (s,a,s') [NxAxN]
    :return: feature map containing features for all state-next_state pair.
    '''
    global states_dict,reverse_states_dict,actions,P_a
    N = len(states_dict)
    features = np.zeros([N,N,num_features])
    for state in states_dict.values(): #states are unique numbers associated with each state here.
        plan,plan_cost = get_plan(0,state)
        features[state,state] = [0.0,0.0,0.0] #calculate_features(plan,plan,plan_cost,plan_cost)
        for next_state in states_dict.values():
            if any(P_a[state,:,next_state])==1:
                new_plan,new_plan_cost = get_plan(0,next_state)
                f = calculate_features(plan,new_plan,plan_cost,new_plan_cost)
                #if f==[0.0,0.0,0.0]:
                #   print("Zero")
                features[state,next_state] = f
    return features

def get_trajectories_from_traces():
    '''
    This funciton converts expert demos into state-action-trajectories of the shape: TXLx2 where T is the number of trajectories, L is the length of each trajectory
    and each item is a state-action (int) pair
    '''
    global traces,states_dict,actions,reverse_states_dict
    trajectories = np.zeros([len(traces),len(traces[0]),2])
    for i in range(len(traces)):
        state = [] #initial state, no explanations given
        for j in range(len(traces[i])):
            action = unique_words.index('$'+str.upper(traces[i][j]))
            try:
                trajectories[i,j,0] = states_dict[tuple(state)]
            except KeyError:
                print([i,j])

            state.append(action)
            try:
                trajectories[i, j, 1] =  states_dict[tuple(state)]
            except KeyError:
                print([i,j])
    return trajectories

def update_domain_template_and_problem_file(problem_file_used):
    '''
    This function updates the domain.tpl.pddl file by replacing $terms which are already present in initial state as defined in the problem file
    '''
    global PROBLEM_ROOT_PATH
    domain_template = open(PROBLEM_ROOT_PATH + 'scavenger.tpl.pddl', 'r')
    domain = domain_template.readlines()
    domain_template.close()

    problem_file = open(PROBLEM_ROOT_PATH+"p"+str(problem_file_used)+".pddl",'r')
    problem = problem_file.readlines()
    problem_file.close()
    situation_variables = []
    
    for i in range(len(problem)): #find all situation variables in problem file
        if '$' in problem[i]:
            [situation_variables.append(str.upper(s.replace('(','').replace(')',''))) for s in re.findall(r'\$\(\w+\)+',problem[i])]
            problem[i]=problem[i].replace('$','')  #remove $ in problem file

    common = list(set(unique_words).intersection(set(situation_variables))) #Situation variables which are also explanations
    #applicable_actions =

    print("Common predicates: "+str(common))
    domain_subs_dict = dict.fromkeys(unique_words,'')


    problem_file = open(PROBLEM_ROOT_PATH+"p"+str(problem_file_used)+"_edited.pddl",'w')
    problem_file.write(''.join(problem))
    problem_file.close()

    subs_dict=dict.fromkeys(unique_words,'')
    for s in subs_dict.keys():
        if s in common:
            subs_dict[s] = '('+str.lower(s[1:])+')'
        else:
            subs_dict[s] = s

    for i in range(len(domain)):
        if '$' in domain[i]:
            for word in subs_dict.keys():  #replace all occurences of dictionary keys with corresponding values
                domain[i]=domain[i].replace(word,subs_dict[word])
    
    domain_template = open(PROBLEM_ROOT_PATH+'scavenger_edited.tpl.pddl','w')
    domain_template.write(''.join(domain))
    domain_template.close()
    unique_words = get_actions(domain)
    print("Updated domain template and problem file")
    pp.pprint(unique_words)


    return domain,unique_words,applicable_actions

if __name__ == "__main__":
    TRACE_ROOT_PATH = '/home/raoshashank/Desktop/Distance-learning-new/Distance-learning-new/repo/Distance-Learning/Train/'
    PROBLEM_ROOT_PATH = '/home/raoshashank/Desktop/Distance-learning-new/Distance-learning-new/repo/Distance-Learning/Archive/'
    PLANNER_RELATIVE_PATH = '/FD/'
    problem_file_used = 2

    ##############STORE TRACES##########################
    #trace_files = ['p1.txt','p2.txt','p3.txt','p4.txt']      
    trace_files = ['p1.txt','p2.txt','p3.txt','p4.txt','p5.txt','p6.txt','p7.txt','p8.txt']
    scenarios = []
    [scenarios.append(int(t)) for t in re.findall(r'\d+',str(trace_files))]
    num_scenarios = len(trace_files)
    for i in range(len(trace_files)):
        trace_files[i] = TRACE_ROOT_PATH+trace_files[i]

    store_traces(trace_files)
    pp = pprint.PrettyPrinter(indent=4)

    ######################################################

    '''
        TODO:
        give each action in the original template file a unique number
        make applicable actions and change wherever unique_words is being used

    '''

    problem_file_used = 1
    domain_file_lines, unique_words = update_domain_template_and_problem_file(problem_file_used)
    unique_words = get_actions(domain_file_lines)
    
    problem_file_used = i


    actions = range(len(unique_words)) #In this case, we use action indices as the actions itself instead of the explicit action names
    A = len(actions)
    states_dict,reverse_states_dict = get_state_map(A)
    num_features = 3

    P_a = get_transition_matrix()
    '''    
    if path.exists('feat_map.npy'):
        print("Found features map file")
        feat_map = np.load('feat_map.npy')
    else:
        feat_map = get_feat_map_from_states(num_features)
        np.save('feat_map.npy',feat_map)
    '''
    with open('states_dict'+str(i)+'.pickle', 'wb') as handle:
        pickle.dump(states_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)
    with open('reverse_states_dict.pickle', 'wb') as handle:
        pickle.dump(reverse_states_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)
    
    feat_map = get_feat_map_from_states(num_features)
    np.save('feat_map_new'+str(i)+'.npy', feat_map)
    print("saved "+str(i))
    print("Done")

    '''
    trajectories = get_trajectories_from_traces()
    gamma = 0.9
    lr = 0.08
    n_iters = 10

    print("Done calculating feat_maps, running IRL")
    rewards = maxent_irl(feat_map, P_a, gamma, trajectories, lr, n_iters)
    print(rewards)
    '''
    
    #input()




























     