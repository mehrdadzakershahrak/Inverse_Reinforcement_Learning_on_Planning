import numpy as np
import pprint
import re
import os
from itertools import chain, combinations
from feature_functions import laven_dist,plan_distance
#lines[l] = re.sub(r"\$\w+",'',lines[l])

def store_traces(trace_files):
    '''
    input: tuple containing full path of demonstration files(Explanations)
    This function parses the explanation files and stores in the global tuple traces
    '''
    global traces,ROOT_PATH
    traces = {}
    num_scenarios = len(trace_files)
    for i in range(num_scenarios):
        scenario_file = open(trace_files[i],'r')
        lines = scenario_file.readlines()
        scenario_file.close()
        trace = []
        traces[i]=[]
        for line in lines:
            if line[0]=='-':
                traces[i].append(trace)
                trace = []
            else:
                trace.append(line.rstrip())
                
def render_template(sc,D):

    '''
    This function renders the domain (scavenger_edited.pddl) and problem file(pi.pddl) from substitutions corresponding to dictionary
    input: scenario file number, dictionary of substitutions
    '''
    global PROBLEM_ROOT_PATH
    domain_template = open(PROBLEM_ROOT_PATH+'scavenger.tpl.pddl','r')
    domain = domain_template.readlines()
    domain_template.close()
    
    for j in range(len(domain)):
        if '$' in domain[j]:
            for word in D.keys():  #replace all occurences of dictionary keys with corresponding values
                #print(domain[j])
                domain[j]=domain[j].replace(word,D[word])
                #print(domain[j])

    domain_template = open(PROBLEM_ROOT_PATH+'scavenger_edited.pddl','w')
    domain_template.write(''.join(domain))
    domain_template.close()
    print("Editted domain file")

    try:
        problem_template = open(PROBLEM_ROOT_PATH+'p'+str(sc)+'.tpl.pddl','r')
        problem = problem_template.readlines()
        problem_template.close()
    
        for j in range(len(problem)):
            if '$' in problem[j]:
                for word in D.keys():  #replace all occurences of dictionary keys with corresponding values
                    problem[j].replace('$'+str.upper(word),D[word])


        problem_template = open(PROBLEM_ROOT_PATH+'p'+str(sc)+'_edited.pddl','w')
        problem_template.write(''.join(problem))
        problem_template.close()

    except IOError:
        print("Problem template file doesn't exist")    

def calculate_states():
    '''
    output:
        S : explanations(history format) -> number (id)
        R : reverse mapping of S
    This function uses the traces to generate history-type string-encoded explanations used for feature generation 
    '''
    global traces,unique_words
    unique_words = []
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


def get_transition_matrix():
    global unique_words
    unique_explanations = []
    num_actions = len(unique_words)
    '''
    Each unique explanation is associated with the number which is its index in the unique_words tuple
    '''
    states_dict = get_state_map(num_actions)    # each state is a unique number associated with which all explanations have bdone till then
    transition_matrix = np.zeros((2 ** num_actions, num_actions, 2 ** num_actions))
    for i in states_dict.keys():          #for each state,
        for a in list(set(range(num_actions))-set(i)):  #for each explanation not yet done..
                try:
                    new_state = list(i)
                    new_state.append(a)
                    transition_matrix[states_dict[i], a, states_dict[tuple(sorted(new_state))]]=1 #update transition matrix
                except KeyError:
                    print(new_state)
                    input()

    return transition_matrix


def powerset(iterable):
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

def get_state_map(num_actions):
	states = list(powerset(range(num_actions)))
	states_dict = {}
	for i in range(len(states)):
		#states_dict[i] = list(states[i])
		states_dict[states[i]] = i
	return states_dict


def run_planner(problem_number,idx):
    '''
    input: self explanatory
    output: plan obtained by running planner on input files
    '''
    global PLANNER_RELATIVE_PATH
    cmd = '.'+PLANNER_RELATIVE_PATH+'fast-downward.py --sas-file temp_'+ str(idx) +'.sas --plan-file plan_'+ str(idx) +' '+'Archive/scavenger_edited.pddl'+' '+'Archive/'+'p'+str(problem_number)+'.pddl'+' --search "astar(lmcut())"'
    #print cmd
    plan = os.popen(cmd).read()
    proc_plan = plan.split('\n')
    cost = [i for i, s in enumerate(proc_plan) if 'Plan cost:' in s]
    if 'Solution found!' not in proc_plan:
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

if __name__ == "__main__":
    TRACE_ROOT_PATH = '/home/raoshashank/Desktop/Distance-learning-new/Distance-learning-new/repo/Distance-Learning/Train/'
    PROBLEM_ROOT_PATH = '/home/raoshashank/Desktop/Distance-learning-new/Distance-learning-new/repo/Distance-Learning/Archive/'
    PLANNER_RELATIVE_PATH = '/FD/'

    #trace_files = ['p1.txt','p2.txt','p3.txt','p4.txt']      
    trace_files = ['p1.txt','p2.txt','p3.txt']
    scenarios = []
    [scenarios.append(int(t)) for t in re.findall(r'\d+',str(trace_files))]

    feat_map = {}

    num_scenarios = len(trace_files)
    for i in range(len(trace_files)):
        trace_files[i] = TRACE_ROOT_PATH+trace_files[i]

    store_traces(trace_files)
    pp = pprint.PrettyPrinter(indent=4)
    #pp.pprint(traces)
    S,R = calculate_states() 
    #pp.pprint(R)   
    #pp.pprint(traces)
    N = len(S)
    A = len(unique_words)
    #pp.pprint(unique_words)
    traj = []
    
    domain_template = open(PROBLEM_ROOT_PATH+'scavenger.tpl.pddl','r')
    lines = domain_template.readlines()
    domain_template.close()
    unique_words = set()
    for line in lines:
        if '$' in line:
            word = re.findall(r"\$\w+",line)
            unique_words.update(word)


    P_a = get_transition_matrix()
    subs_dict = dict.fromkeys(unique_words,'')
    #print subs_dict
    #pp.pprint(traces)
    
    for i in range(num_scenarios):  #for each scenario 
        
        #create the initial domain file by removing the predicates with $ sign
        #generate the plan corresponding to the domain and problem file
        #generate features corresponding to the original plan
        #use exaplanation to generate new plan
        #generate features of new plan
        
        for trace in traces[i]: #each expert explanation, trace:[exp1,exp2,...]
            s = str(i)+'_'
            subs_dict = dict.fromkeys(unique_words,'')                     #initialize empty dict
            render_template(i,subs_dict)                                   #render initial empty dict
            plan_old,plan_old_cost = run_planner(i,0)                      # calculate plan
            print("old_plan : " +str(plan_old))     
            features= calculate_features(plan_old,plan_old,plan_old_cost,plan_old_cost) #calculate features for initial plan (all should be )
            if s not in feat_map:
                feat_map[S[s]] = features                                  #update feat_map
            expl_dict = subs_dict                           
        
            for word in trace:
                expl_dict['$'+str.upper(word)]='('+str.lower(word)+')'    # update dict
                render_template(i,expl_dict)                              # render new template
                plan_new,plan_new_cost = run_planner(i,0)                 # get new plan
                s_old = s
                s+=','+word
                if s not in feat_map:
                    features = calculate_features(plan_old,plan_new,plan_old_cost,plan_new_cost)
                    feat_map[S[s]] = features
                #   P[S[s_old],S[s],word]=1
                traj.append((S[s_old],S[s],word))
                plan_old = plan_new
                plan_old_cost = plan_new_cost
   

    input()































     