'''
Implementation of maximum entropy inverse reinforcement learning in
  Ziebart et al. 2008 paper: Maximum Entropy Inverse Reinforcement Learning
  https://www.aaai.org/Papers/AAAI/2008/AAAI08-227.pdf
Acknowledgement:
  This implementation is largely influenced by Matthew Alger's maxent implementation here:
  https://github.com/MatthewJA/Inverse-Reinforcement-Learning/blob/master/irl/maxent.py
By Yiren Lu (luyirenmax@gmail.com), May 2017
'''
import numpy as np
import value_iteration
from utils import *
import sys


def generate_stochastic_policy(P_a, rewards):
  T = 2
  N_STATES, _, N_ACTIONS = np.shape(P_a)
  z_s = np.ones((N_STATES,))
  z_a = np.zeros((N_STATES, N_ACTIONS))

  for t in range(T):
    for s in range(N_STATES):
      for a in range(N_ACTIONS):
        try:
          z_a[s, a] = sum([ P_a[s, s1, a] * math.exp(rewards[s, s1]) * z_s[s1] for s1 in range(N_STATES)])

        except OverflowError:
          [print(rewards[s, s1]) for s1 in range(N_STATES)]
          input()
    z_s = np.sum(z_a, 1)
    for i in range(len(z_s)):
      #print(i)
      if z_s[i]==0:
        #print(z_s[i])
        z_s[i]=1
  policy = (z_a.T/z_s).T
  for i in range(len(z_s)):
    if np.sum(policy[i, :])==0:
      policy[i, :] = np.array([1/N_ACTIONS]*N_ACTIONS)
  return policy

def generate_trajectories(P_a, policy,scenarios):

  N_TRAJS_PER_SC = 10

  N_STATES, _, N_ACTIONS = np.shape(P_a)
  N_SCENARIOS = len(scenarios)
  trajectories = []
  all_actions = [0,1,2,3,4,5]

  for sc in range(N_SCENARIOS):
    for index in range(N_TRAJS_PER_SC):
      trajectory = []
      current_state = 0
      i=0
      applicable_actions = list(set(all_actions).difference(set(scenarios[sc])))  #only actions available for particular scenario
      while(i<len(applicable_actions)):
        while True:   #pick till an applicable action is chosen
          action = np.random.choice(np.arange(0,N_ACTIONS), p=policy[current_state])
          if action in applicable_actions:
            break

        next_state = np.where(P_a[current_state,:,action]==1.0)[0][0]
        trajectory += [(current_state, next_state)]
        current_state = next_state
        i+=1
      trajectories += [trajectory]
  trajectories = np.array(trajectories)
  return trajectories


def compute_state_visition_freq(P_a, gamma, policy, scenarios):
  T = 10
  N_STATES, _, N_ACTIONS = np.shape(P_a)
  
  #print(policy)

  #####generate only trajectories which use the goal
  trajs = generate_trajectories(P_a, policy,scenarios)

  # mu[s, s', t] is the prob of visiting state s at time t
  mu = np.zeros([N_STATES, N_STATES, T]) 

  for traj in trajs:
    mu[traj[0][0], traj[0][1], 0] += 1

  mu[:,:,0] = mu[:,:,0]/len(trajs)

  for s in range(N_STATES):
    for s1 in range(N_STATES):
      for t in range(T-1):
        temp = np.dot(policy[s, :], P_a[s, s1, :].T)
        sum_a=0
        for s2 in range(N_STATES):
          sum_a += mu[s2, s, t] * temp
        mu[s, s1, t+1] = sum_a

  return np.sum(mu, 2)


def maxent_irl(feat_map, P_a, gamma, trajs, lr, n_iters,scenarios):
  N_STATES, _, N_ACTIONS = np.shape(P_a)
  N_TRACES_PER_SC = 5
  N_SCENARIOS = len(scenarios)
  np.set_printoptions(formatter={'float': lambda x: "{0:0.3f}".format(x)})
  N_FEATURES = feat_map.shape[2]
  theta = np.random.uniform(size=(N_FEATURES,))

  feat_exp = np.zeros([N_FEATURES])
  for sc in scenarios:
    feat_exp_sc = np.zeros([N_FEATURES])
    count = 0
    for episode in trajs:
      for prev, nex in episode:
        feat_exp_sc+= feat_map[int(prev), int(nex), :]
        count+=1
        if count>=N_TRACES_PER_SC:
          break

    feat_exp += feat_exp_sc/N_TRACES_PER_SC

  # training
  lr_const = lr/n_iters
  print("Running...")
  rewards = np.zeros([N_STATES,N_STATES])
  for iteration in range(n_iters):

    rewards_new = normalize(np.dot(feat_map, theta))
    print("--")
    print(np.sum(abs(rewards-rewards_new)))
    rewards =rewards_new.copy()


    #print(rewards)
    policy = generate_stochastic_policy(P_a, rewards)
    #print(policy)

    # compute state visition frequences
    svf = compute_state_visition_freq(P_a, gamma, policy,scenarios)
    fm = feat_map.reshape((N_STATES*N_STATES, N_FEATURES))
    sv = svf.reshape(N_STATES*N_STATES, 1)
    print(sv[0:20])
    val = fm.T.dot(sv).reshape((N_FEATURES,))
    #print(val)
    grad = feat_exp - val
    #print(val)
  
    # update params
    theta += lr * grad

    #print("******************************"+ str(iteration) +"******************************************")
    #print(theta)
    np.save("final_thetas", arr=theta)
    lr -= lr_const
    sys.stdout.write('\r' + "Progress:"+ str(iteration) + "/" +str(n_iters))#+" ,applicable states:"+str(theta))
    sys.stdout.flush()  
  print(theta)
  rewards = np.dot(feat_map, theta)

  return normalize(rewards)


