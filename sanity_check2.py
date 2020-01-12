import numpy as np
import pickle
import pprint
import re
import os

def render_problem_template(D):
    '''
    This function renders the domain (scavenger_edited.pddl) file from substitutions corresponding to dictionary
    input: dictionary of substitutions
    sample dict: {A:0,B:1,C:0}
    active explanations have value 1 and others have value 0
    when any explanation is done, add the cost to every line which ends in that cell
    '''
    global PROBLEM_ROOT_PATH, cost_dict
    

    with open(PROBLEM_ROOT_PATH+'problem.tpl.pddl','r') as f:
        og = f.readlines()
    
    for i in range(len(og)):
        if 'length' in og[i]:
                for e in cost_dict.keys():
                    if D[e]==1:
                        if str(e)+')' in og[i]:
                                nums = re.findall(r'\d+',og[i])[0]
                                cost=str(int(cost_dict[e]+int(nums)))
                                og[i]=og[i].replace(nums,cost)


    problem_template = open(PROBLEM_ROOT_PATH + 'p1.pddl', 'w')
    problem_template.write(''.join(og))
    problem_template.close()

def get_plan(state,all_actions,problem_file_used):
    '''
    input: state: tuple of all actions taken till reaching state, all_actions: dict of all actions assigned to a number
    output: plan obtained by running planner on input files
    '''
    global PLANNER_RELATIVE_PATH

    # generate dictionary corresponding to substitutions and render domain template to get plan
    subs_dict = {}
    for action_template in all_actions.keys():
        if action_template in state:
            subs_dict[action_template] = 1
        else:
            subs_dict[action_template] = 0
    print(subs_dict)
    render_problem_template(subs_dict)

    cmd = '.' + PLANNER_RELATIVE_PATH + 'fast-downward.py --sas-file temp_' + str(0) + '.sas --plan-file plan_' + str(
        0) + ' ' + 'Archive/domain.pddl' + ' ' + 'Archive/' + 'p' + str(
        problem_file_used) + '.pddl' + ' --search "astar(lmcut())"'
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

PROBLEM_ROOT_PATH = '/headless/Desktop/Distance-Learning/Archive/'
PLANNER_RELATIVE_PATH= '/FD/'

cost_dict = {'A':5,'B':5,'C':2,'D':14,'E':4,'F':20,'J':4}
all_actions = {'A':0,'B':1,'C':2,'D':3,'E':4,'F':5,'J':6}
plan,cost = get_plan(('J','E','F'),all_actions,1)
print(plan)
print(cost)


