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
import IPython  

def render_problem_template(D):
    '''
    This function renders the domain (problem.tpl.pddl) file from substitutions corresponding to dictionary
    input: dictionary of substitutions
    '''
    global PROBLEM_ROOT_PATH, cost_dict
    with open(PROBLEM_ROOT_PATH + 'problem.tpl.pddl', 'r') as f:
        og = f.readlines()
    for i in range(len(og)):
        if 'can_go' in og[i]:
            for e in D.keys():
                if D[e] == 1:
                    if str(e) + ')' in og[i]:
                        og[i] = ';'+og[i]       #if an explanation is present, block the path from start to the goal.

    problem_template = open(PROBLEM_ROOT_PATH + 'p0.pddl', 'w')
    problem_template.write(''.join(og))
    problem_template.close()

def get_plan(exp_dict):
    '''
    input: state: tuple of all actions taken till reaching state, all_actions: dict of all actions assigned to a number
    output: plan obtained by running planner on input files
    '''
    global PLANNER_RELATIVE_PATH

    # generate dictionary corresponding to substitutions and render domain template to get plan
    # subs_dict = {}
    # for action_template in all_actions.keys():
    #     if all_actions[action_template] in state:
    #         #print(action_template)
    #         subs_dict[action_template] = 1
    #     else:
    #         subs_dict[action_template] = 0
    render_problem_template(exp_dict)

    #calculate plan and plan-cost using fast-downward planner
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


orders = {}
orders['3'] = {}
orders['5']={}
orders['7']={}
orders['3']['manhattan'] = ['A','E','C','D','B']
orders['3']['random'] = ['C','A','E','B','D']
orders['3']['peg'] = ['E','A','C','B','D']

orders['5']['manhattan'] =['A','E','C','D'] 
orders['5']['random'] =['D','E','C','A'] 
orders['5']['peg'] = ['E','A','C','D']

orders['7']['manhattan'] = ['A','E','F','B']
orders['7']['random'] = ['B','A','F','E']
orders['7']['peg'] = ['E','A','F','B']

dir_path = os.path.dirname(os.path.realpath('__file__'))
TRACE_ROOT_PATH = dir_path+'/'+'Train/'
PROBLEM_ROOT_PATH = dir_path+'/'+'Archive/'
PLANNER_RELATIVE_PATH = '/FD/'
pp = pprint.PrettyPrinter(indent=4)
problem_file_used = 0
plan_costs = {}

optimal_plan = {}
optimal_plan['3'],_ = get_plan({'A':1,'B':1,'C':1,'D':1,'E':1,'F':0})
optimal_plan['5'],_ = get_plan({'A':1,'B':0,'C':1,'D':1,'E':1,'F':0})
optimal_plan['7'],_ = get_plan({'A':1,'B':1,'C':0,'D':0,'E':1,'F':1})

first_plan,first_plan_cost = get_plan({'A':0,'B':0,'C':0,'D':0,'E':0,'F':0})

all_plans = {}
all_plans['3'] = {}
all_plans['5']={}
all_plans['7']={}
all_plans['3']['manhattan'] = [first_plan]
all_plans['3']['random'] = [first_plan]
all_plans['3']['peg'] = [first_plan]
all_plans['5']['manhattan'] =[first_plan] 
all_plans['5']['random'] =[first_plan] 
all_plans['5']['peg'] = [first_plan]
all_plans['7']['manhattan'] = [first_plan]
all_plans['7']['random'] = [first_plan]
all_plans['7']['peg'] = [first_plan]


for problem_number in orders.keys():
    plan_costs[problem_number] = {}
    for order_type in orders[problem_number]:
        #plan_costs[problem_number][order_type] = [optimal_plan[problem_number],first_plan)]
        print("*******")
        plan_costs[problem_number][order_type] = []
        for i in range(len(orders[problem_number][order_type])):
            exp_dict = {'A':0,'B':0,'C':0,'D':0,'E':0,'F':0}
            for j,e in enumerate(orders[problem_number][order_type]):
                exp_dict[e]=1
                if j>=i:
                    break
            print('-----'+str(problem_number)+'-----'+str(order_type)+'-----')
            print(exp_dict)
            plan,plan_cost = get_plan(exp_dict)
            #print(plan)
            #IPython.embed()
            #plan_costs[problem_number][order_type].append(plan_distance(optimal_plan[problem_number],plan))
            all_plans[problem_number][order_type].append(plan)
            #print(all_plans[problem_number][order_type])
            # if i>0:
            #     print(all_plans[problem_number][order_type][i-1])
            #     print(plan)
            #     plan_costs[problem_number][order_type].append(plan_distance(plan,all_plans[problem_number][order_type][i-1]))
            # else:
            #     print(first_plan)
            #     print(plan)
            #     plan_costs[problem_number][order_type].append(plan_distance(plan,first_plan))


for problem_number in orders.keys():
    plan_costs[problem_number] = {}
    for order_type in orders[problem_number]:
        plan_costs[problem_number][order_type] = []
        for i in range(1,len(all_plans[problem_number][order_type])):
            plan1 = all_plans[problem_number][order_type][i]
            plan2 = all_plans[problem_number][order_type][i-1]
            plan_costs[problem_number][order_type].append(plan_distance(plan1,plan2))   

IPython.embed()
