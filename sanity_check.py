import numpy as np
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
        'has_accesskey':{1:0,2:0,3:0,4:0,5:0},
        'has_password':{1:0,2:0,3:0,4:0,5:0},
        'has_key':{1:0,2:0,3:0,4:0,5:0},
        'has_ladder':{1:0,2:0,3:0,4:0,5:0},
        'has_electricity':{1:0,2:0,3:0,4:0,5:0}}

    
    for sc in range(len(trace_list)): #for each scenario
        for i in range(len(trace_list[sc])): # for each trace of each scenario
            actions[trace_list[sc][i]][i+1]+=1
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(actions)
    return actions


TRACE_ROOT_PATH = '/home/raoshashank/Desktop/Distance-learning-new/Distance-learning-new/repo/Distance-Learning/Train/'
files_used = [0,1,2,3,4,5,6,7,8]
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