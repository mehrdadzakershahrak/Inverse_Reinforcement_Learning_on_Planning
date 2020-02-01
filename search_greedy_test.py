import numpy as np
import heapq
import pickle
from utils import *
import copy

def findnode(q,item):
    for i in range(len(q)):
        if q[i][-1] == item:
            return i
    return -1


#weights from the IRL
correct_data_thetas = [152.572, -3.398, 121.587, 128.642, 131.703, 142.071] 
feat_map = np.load('feat_map_final.npy')

thetas = correct_data_thetas.copy()
rewards = normalize(np.dot(feat_map,thetas))
P_a = np.load("P_a.npy")

with open('states_dict.pickle','rb') as f:
    states_dict = pickle.load(f)

train_scenarios = [[3],[1],[1,3],[3,5],[1,2]]
test_scenarios = [[5],[1,5],[2,3]]
inv_actions_dict = {0:'A', 1:'B', 2:'C',3:'D', 4:'E', 5:'F'}
actions_dict = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5}
all_actions = [0,1,2,3,4,5]

#perform Uniform Cost Search on the testing scenarios
scenarios = train_scenarios.copy()
for sc in range(len(scenarios)):
    frontier = []
    item = []
    action_list = list(set(all_actions).difference(set(scenarios[sc])))
    goal = states_dict[tuple(sorted(action_list))]
    cost_so_far = 0.0
    counter = 0
    root = 0
    item = [cost_so_far,counter,[],root]
    frontier.append(item)
    explored = []
    while len(frontier)!=0:
        top_node = frontier.pop(frontier.index(min(frontier)))
        node = top_node.pop()
        actions_so_far = top_node.pop()
        cost_so_far = top_node.pop(0)
        if node == goal:
            print(actions_so_far)
            break
        successor_actions = []
        explored.append(node)
        for a in action_list:
            if any(P_a[node, :, a] == 1.0):
                successor_actions.append(a)
        for action in successor_actions:
            counter+=1
            actions_so_far_child = actions_so_far[:]
            actions_so_far_child.append(action)
            child_node = np.where(P_a[node, :, action] == 1)[0][0]
            child_cost = cost_so_far+(100.0-rewards[node,child_node])
            if child_node not in explored:
                frontier.append([child_cost,counter,actions_so_far_child,child_node])



















'''
scenarios = train_scenarios.copy()
for sc in range(len(scenarios)):
    action_list = list(set(all_actions).difference(set(scenarios[sc])))
    root = 0
    frontier = []
    explored = set()
    counter = 0
    item = [0.0, counter, [], root]
    successor_actions = []
    #heapq.heappush(frontier, item)
    frontier.append(item)
    counter += 1

    goal_state = states_dict[tuple(sorted(action_list))]

    goals = []

    while True:
        if len(frontier) == 0:
            print("No path possible!")
            print(goals)
            break

        #item = heapq.heappop(frontier)
        item = frontier.pop(frontier.index(max(frontier)))
        node = item.pop()
        node_actions = item.pop()
        node_cum_cost = item.pop(0)
        #print(node_cum_cost)

        if node == goal_state:
            print(node_actions)
            for a in node_actions:
                print(inv_actions_dict[a])
            print(node_cum_cost)
            goals.append([node_cum_cost,node_actions])


        #print(frontier)
        explored.add(str(node))
        sucs = []
        for a in action_list:
            if any(P_a[node,:,a]==1.0):
                sucs.append(a)


        for action in sucs:
            counter += 1
            actions = node_actions[:]
            child_node = np.where(P_a[node,:,action]==1)[0][0]

            child_cost = rewards[node,child_node]
            child_cost += node_cum_cost

            if (str(child_node) not in explored):  # and (child_node not in frontier):
                index = findnode(frontier, child_node)
                if index != -1:
                    if frontier[index][0] > child_cost:
                        del frontier[index]
                        print("THIS NEVER HAPPENS")
                actions.append(action)
                item = [child_cost, counter, actions, child_node]
                #heapq.heappush(frontier, item)
                frontier.append(item)
'''