import lavenstein
import os

plan = os.popen('./planner/fast-downward.py domain.pddl pfile01 --search "astar(lmcut())"').read()
proc_plan = plan.split('\n')
cost = [i for i, s in enumerate(proc_plan) if 'Plan cost:' in s]
# cost distance
plan_cost = proc_plan[cost[0]].split(' ')[-1]
print(plan_cost)

# lavenstein distance
# plan_h will be generated from the list of the explanations
plan_h = proc_plan[proc_plan.index('Solution found!')+2: cost[0]-1]
plan_r = proc_plan[proc_plan.index('Solution found!')+2: cost[0]]

print(lavenstein.leven(lavenstein.listToString(plan_h),lavenstein.listToString(plan_r)))
#print(lavenstein.listToString(plan_h))
#print(lavenstein.listToString(plan_r))

# action distance

# causal distance