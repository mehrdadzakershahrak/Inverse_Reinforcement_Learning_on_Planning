# Value iteration agent
# Model-based learning which requires mdp.
#
# ---
# @author Yiren Lu
# @email luyiren [at] seas [dot] upenn [dot] edu
#
# MIT License

import math
import numpy as np


def value_iteration(P_a, rewards, gamma, error=0.01, deterministic=True):
  """
  static value iteration function. Perhaps the most useful function in this repo
  
  inputs:
    P_a         NxNxN_ACTIONS transition probabilities matrix - 
                              P_a[s0, s1, a] is the transition prob of 
                              landing at state s1 when taking action 
                              a at state s0
    rewards     Nx1 matrix - rewards for all the states
    gamma       float - RL discount
    error       float - threshold for a stop
    deterministic   bool - to return deterministic policy or stochastic policy
  
  returns:
    values    Nx1 matrix - estimated values
    policy    Nx1 (NxN_ACTIONS if non-det) matrix - policy
  """
  N_STATES,_, N_ACTIONS = np.shape(P_a)

  values = np.zeros([N_STATES])

  while True:

    values_tmp = values.copy()

    for s in range(N_STATES):
      v_s = []
      values[s] = max([sum([P_a[s,s1,a]*(rewards[s,s1] + gamma*values_tmp[s1]) for s1 in range(N_STATES)]) for a in range(N_ACTIONS)])


    if max([abs(values[s] - values_tmp[s]) for s in range(N_STATES)]) < error:
      break
    


  if deterministic:
    # generate deterministic policy
    policy = np.zeros([N_STATES])
    for s in range(N_STATES):
      policy[s] = np.argmax([sum([P_a[s,s1,a]*(rewards[s,s1]+gamma*values[s1])
                                  for s1 in range(N_STATES)]) 
                                  for a in range(N_ACTIONS)])

    return values, policy
  else:
    # generate stochastic policy
    policy = np.zeros([N_STATES, N_ACTIONS])
    for s in range(N_STATES):
      v_s = np.array([sum([P_a[s,s1,a]*(rewards[s,s1] + gamma*values[s1]) for s1 in range(N_STATES)]) for a in range(N_ACTIONS)])
      temp = np.sum(v_s)
      if not(temp==0):
        policy[s,:] = np.transpose(v_s/temp)
      else:
        policy[s,:] = [1/N_ACTIONS]*N_ACTIONS
    return values, policy

