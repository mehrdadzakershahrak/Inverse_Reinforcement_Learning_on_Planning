
# Order Matters
This repository, contains the code for the paper: 

Abstract:




This work tries to prove that, when an agent has to explain numerous details to a human, the cognitive load of processing the information, is directly correlated to with the order in which the explanations are given. 
The domain selected is that of a maze-escape.
For training, a human is told that he/she is to help a trapped human escape by explaining the presence of dangerous locations in the maze in the best order.
For testing, the order suggested by our algorithm is used to measure the cognitive load on humans who are to suggest the best possible path to escape the maze.  We measure the cognitive load on the human using the standard NASA TLX indices and compare the indices with a random ordering of the explanations and an ordering based on the manhattan distance of a location from the start position.

The maze_peg.py file contains the code for the progressive explanation generation. The search_greedy_test.py file contains the code to run uniform cost search using the rewards matrix generated from Max-Ent IRL. 
In order to run the file, the value of the theta matrix (list) should be replaced with the ones returned from IRL or the rewards.npy matrix can be imported directly using numpy.
The problem is modelled as a Goal-based-MDP with deterministic transitions.

The algorithm works as follows:
* The state space and the transition probability matrix for the MDP is generated based on the number of actions given.
* For each valid state-pair, the features using domain-dependent and domain-independent features are calculated.
* The expert traces (from human trials) are stored in a dictionary.
* Using the matrices calculated above, Maximum Entropy IRL is run to generate the weights for each feature.
* Since in the current situation, different scenarios correspond to the same MDP with the same initial state and different goal-states, the reward matrix is used to perform simple Uniform-Cost-Search to find the best order of explanations.

Code written by :
* Shashank Rao Marpally [https://github.com/raoshashank] 
* Akshay Sharma [https://github.com/] 
* Mehrdad Zaker Shahrak [https://github.com/mehrdadzakershahrak]
 
