import numpy as np
import os
import pickle
import pprint
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

def get_stats(trace_list):
    counts = {}
    actions = {
        'A':{1:0,2:0,3:0,4:0,5:0},
        'B':{1:0,2:0,3:0,4:0,5:0},
        'C':{1:0,2:0,3:0,4:0,5:0},
        'D':{1:0,2:0,3:0,4:0,5:0},
        'E':{1:0,2:0,3:0,4:0,5:0},
	'F':{1:0,2:0,3:0,4:0,5:0},
	'H':{1:0,2:0,3:0,4:0,5:0},
	'J':{1:0,2:0,3:0,4:0,5:0}}
    total = {
    'A':0,
    'B':0,
    'C':0,
    'D':0,
    'E':0,'F':0,'J':0,'H':0
    }


    stats={
    0: {'A':0,'B':0,'C':0,'D':0,'E':0,'F':0,'J':0,'H':0},
    1: {'A':0,'B':0,'C':0,'D':0,'E':0,'F':0,'J':0,'H':0},
    2:{'A':0,'B':0,'C':0,'D':0,'E':0,'F':0,'J':0,'H':0},
    3:{'A':0,'B':0,'C':0,'D':0,'E':0,'F':0,'J':0,'H':0},
    4:{'A':0,'B':0,'C':0,'D':0,'E':0,'F':0,'J':0,'H':0},
    }

    for sc in range(len(trace_list)): #for each scenario
        for i in range(len(trace_list[sc])): # for each trace of each scenario
            stats[i][trace_list[sc][i]]+=1

    '''
    for a in actions:
        total[a]=sum(actions[a].values())
        for i in actions[a]:
            actions[a][i]/=total[a]/100

    '''
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(stats)
    #pp.pprint(total)
    return stats


dir_path = os.path.dirname(os.path.realpath('__file__'))
TRACE_ROOT_PATH = dir_path+'/'+'Train/'
files_used = [1,2,3,4,5,6,7,8,9,10]
trace_files = [TRACE_ROOT_PATH + 'p' + str(i) + '.txt' for i in files_used]
a = get_stats(store_traces(trace_files))
max_keys = {}
for i in a:
    stats = a[i]
    max_key = max(stats, key=lambda k: stats[k])
    max_keys[i]=max_key
    #print(i+" "+str(max_key)+" "+str(a[i][max_key]))
print(max_keys)
a = sorted(max_keys,key=max_keys.get)
print(a)
