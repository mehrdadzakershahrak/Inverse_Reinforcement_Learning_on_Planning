import numpy as np
import pprint
import re
import os

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
    This function renders the domain and problem file from substitutions corresponding to dictionary
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
    for i in range(len(traces)):
        for trace in traces[i]: #new expert demo
            s = str(i) + '_'    #s is (4_,password),(4_,password,get_key) and so on
            for word in trace:
                s += ','+word
                if s not in S:
                    S[s] = n      
                    R[n] = s
                    n += 1 

    return S, R                 # S now contains mapping from explanation (history format) to number (like id) and R now contains mapping from number (like id) to explanation (history-format)

def run_planner(problem_number,idx):
    '''
    input: self explanatory
    output: plan obtained by running planner on input files
    '''
    global PLANNER_RELATIVE_PATH
    cmd = '.'+PLANNER_RELATIVE_PATH+'fast-downward.py --sas-file temp_'+ str(idx) +'.sas --plan-file plan_'+ str(idx) +' '+'Archive/scavenger_edited.pddl'+' '+'Archive/'+'p'+str(problem_number)+'.pddl'+' --search "astar(lmcut())"'
    print cmd
    plan = os.popen(cmd).read()
    proc_plan = plan.split('\n')
    cost = [i for i, s in enumerate(proc_plan) if 'Plan cost:' in s]
    if 'Solution found!' not in proc_plan:
        return [], 0
    plan = proc_plan[proc_plan.index('Solution found!')+2: cost[0]-1]
    plan_cost = proc_plan[cost[0]].split(' ')[-1]
    return plan, plan_cost



if __name__ == "__main__":
    TRACE_ROOT_PATH = '/home/raoshashank/Desktop/Distance-learning-new/Distance-learning-new/Train/'
    PROBLEM_ROOT_PATH = '/home/raoshashank/Desktop/Distance-learning-new/Distance-learning-new/Archive/'
    PLANNER_RELATIVE_PATH = '/FD/'

    #trace_files = ['p1.txt','p2.txt','p3.txt','p4.txt']      
    trace_files = ['p1.txt']
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
    P = np.zeros([N,N,A])
    
    domain_template = open(PROBLEM_ROOT_PATH+'scavenger.tpl.pddl','r')
    lines = domain_template.readlines()
    domain_template.close()
    unique_words = set()
    for line in lines:
        if '$' in line:
            word = re.findall(r"\$\w+",line)
            unique_words.update(word)

    subs_dict = dict.fromkeys(unique_words,'')
    print subs_dict

    for i in range(num_scenarios):   
        '''
        create the initial domain file by removing the predicates with $ sign
        generate the plan corresponding to the domain and problem file
        generate features corresponding to the original plan
        use exaplanation to generate new plan
        generate features of new plan
        '''
        render_template(i,subs_dict)
        plan,plan_cost = run_planner(1,0)
        print plan 
