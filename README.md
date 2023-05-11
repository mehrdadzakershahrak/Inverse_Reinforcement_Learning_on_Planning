# Order Matters

This repository contains the code for our research paper, where we explore the impact of explanation order on cognitive load during maze navigation.

## Abstract

Our work seeks to establish a correlation between the sequence of explanations provided to a human agent and the cognitive load experienced by the agent. We employ a maze-escape scenario where an individual must guide a trapped human to safety by explaining the dangerous locations in the maze in an optimal sequence. 

During testing, we utilize the sequence proposed by our algorithm to measure the cognitive load on humans tasked with suggesting the best possible escape route. We assess cognitive load using the standard NASA TLX indices, comparing our method against a random ordering of explanations and an ordering based on the Manhattan distance of a location from the starting position.

## Files and Usage

- `maze_peg.py`: This file contains the code for the progressive explanation generation.

- `search_greedy_test.py`: This file contains the code to run uniform cost search using the rewards matrix generated from Maximum Entropy Inverse Reinforcement Learning (Max-Ent IRL). To run the file, replace the value of the theta matrix (list) with the ones returned from IRL or import the `rewards.npy` matrix directly using numpy.

The problem is modeled as a goal-based Markov Decision Process (MDP) with deterministic transitions.

## Algorithm Overview

1. **State space and transition probability matrix generation:** The state space and the transition probability matrix for the MDP are generated based on the number of actions given.

2. **Feature calculation:** For each valid state-pair, we calculate the features using domain-dependent and domain-independent factors.

3. **Expert traces storage:** The expert traces (from human trials) are stored in a dictionary.

4. **Maximum Entropy IRL for weight generation:** Using the matrices calculated in the previous steps, Maximum Entropy Inverse Reinforcement Learning (Max-Ent IRL) is applied to generate the weights for each feature.

### More on Maximum Entropy IRL

Max-Ent IRL is a method used to infer the reward function given a policy or behavior. It's based on the principle of Maximum Entropy, which is rooted in information theory. The Maximum Entropy principle dictates that we should select a distribution that is consistent with all the provided information, but also as uniform as possible. In the context of IRL, this means we aim to find a reward function that makes the observed behavior appear as optimal as possible, while also maintaining a level of uncertainty in areas of the state space where we lack information.

5. **Uniform-Cost-Search for optimal explanation order:** Since different scenarios in the current context correspond to the same MDP (with the same initial state and different goal-states), we use the reward matrix to perform a simple Uniform-Cost-Search to find the best order of explanations.