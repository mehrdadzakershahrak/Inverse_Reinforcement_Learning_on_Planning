import numpy as np
import heapq
import pickle


def findnode(q,item):
    for i in range(len(q)):
        if q[i][-1] == item:
            return i
    return -1

thetas = np.load('final_thetas.npy')
feat_map = np.load("feat_map_final.npy")
rewards = np.dot(feat_map,thetas)
P_a = np.load("P_a.npy")
with open('states_dict.pickle','rb') as f:
    states_dict = pickle.load(f)




scenarios = [[3],[1],[1,3],[3,5],[1,2]]
all_actions = [0,1,2,3,4,5]
frontier = []
explored = set()
for sc in range(len(scenarios)):
    action_list = list(set(all_actions).difference(set(scenarios[sc])))
    root = 0
    frontier = []
    explored = set()
    counter = 0
    item = [-np.inf, counter, [], root]
    heapq.heappush(frontier, item)
    counter += 1
    goal_state = states_dict[tuple(sorted(action_list))]
    while True:
        if len(frontier) == 0:
            print("No path possible!")

        item = heapq.heappop(frontier)
        node = item.pop()
        node_actions = item.pop()
        node_cum_cost = item.pop(0)

        if node == goal_state:
            print(node_actions)

        explored.add(str(node))
        sucs = []
        for a in action_list:
            if any(P_a[node,:,a]==1.0):
                sucs.append(a)
                
        for action in sucs:
            counter += 1
            actions = node_actions[:]
            child_node = np.where(P_a[node,:,action]==1)[0][0]
            child_cost = -1.0*rewards[node,child_node]
            child_cost += node_cum_cost

            if (str(child_node) not in explored):  # and (child_node not in frontier):
                index = findnode(frontier, child_node)
                if index != -1:
                    if frontier[index][0] > child_cost:
                        del frontier[index]
                actions.append(action)
                item = [child_cost, counter, actions, child_node]
                heapq.heappush(frontier, item)

