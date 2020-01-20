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
from utils import *
import sys
from value_iteration import value_iteration
import copy

def generate_stochastic_policy(P_a, rewards,gamma):
  T = 2
  N_STATES,_, N_ACTIONS = np.shape(P_a)

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
      # print(policy[i, :])
      #policy[i, :] = np.array([1/N_ACTIONS, 1/N_ACTIONS, 1/N_ACTIONS, 1/N_ACTIONS, 1/N_ACTIONS, 1/N_ACTIONS])

  return policy

def generate_trajectories(P_a, policy):
  N_TRAJS = 50
  N_STATES, _, N_ACTIONS = np.shape(P_a)
  trajectories = []
  for index in range(N_TRAJS):
    trajectory = []
    current_state = 0
    #while(current_state < N_STATES-1):
    i=0
    while(i<N_ACTIONS):
      action = np.random.choice(np.arange(0,N_ACTIONS), p=policy[current_state])
      for next_state in range(current_state, N_STATES):
        #print(i, next_state)
        if P_a[current_state, next_state, action] == 1:
          trajectory += [(current_state, next_state)]
          current_state = next_state
          break
      i+=1
    trajectories += [trajectory]
  trajectories = np.array(trajectories)
  return trajectories


def compute_state_visition_freq(P_a, gamma, policy,t,deterministic=True):
  T = 10
  N_STATES, _, N_ACTIONS = np.shape(P_a)
  
  #print(policy)
  # try with expert traces
  #trajs = []
  #for i in range(np.shape(t)[0]):
  #     trajectory = []
  #     for j in range(np.shape(t)[1]):
  #         trajectory.append(tuple(t[i,j,:]))
  #     trajs+=list(trajectory)
  #trajs = np.array(trajs)
  #for s in range(len(states_dict)):
  #  print(P_a[s, :, s])

  trajs = generate_trajectories(P_a, policy)

  # mu[s, s', t] is the prob of visiting state s at time t
  mu = np.zeros([N_STATES, N_STATES, T]) 
  #trajs = list(t)

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
          #print(s, s1, t, s2)
        mu[s, s1, t+1] = sum_a
        #print(mu)
  return np.sum(mu, 2)


def maxent_irl(feat_map, P_a, gamma, trajs, lr, n_iters):
  P_original = P_a.copy()
  N_STATES, _, N_ACTIONS = np.shape(P_a)
  np.set_printoptions(formatter={'float': lambda x: "{0:0.3f}".format(x)})
  # init parameters
  #theta = np.zeros((feat_map.shape[2],))
  N_FEATURES = feat_map.shape[2]
  theta = np.random.uniform(size=(N_FEATURES,))
  #theta = np.zeros((N_FEATURES,))

  # calc feature expectations
  feat_exp = np.zeros([N_FEATURES])
  for episode in trajs:
    for prev, nex in episode:
      try:
        feat_exp += feat_map[int(prev), int(nex), :]
      except IndexError:
        print("Error")
        input()
  feat_exp = np.array(feat_exp/len(trajs))
  grad_plot = np.zeros([n_iters,N_FEATURES])
  thetas_plot = np.zeros([n_iters,N_FEATURES])

  # training
  lr_const = lr/n_iters
  #lr_const = 0  
  print("Running...")
  policy = np.zeros([N_STATES,N_ACTIONS])
  for iteration in range(n_iters):

    if not np.array_equal(P_original,P_a):
      print("Here is the issue")


    with open('iteration.txt','w') as f:
       f.write(''.join(str(iteration)))
    # compute reward function
    rewards = normalize(np.dot(feat_map, theta))
    #rewards = np.dot(feat_map, theta)
    #print(rewards.shape)

    # compute policy
    #_, policy = value_iteration.value_iteration(P_a, rewards, gamma, error=0.01, deterministic=False)

    policy = generate_stochastic_policy(P_a, rewards,gamma)
    #_,policy = value_iteration(P_a, rewards, gamma, error=0.01, deterministic=False)
    #difference = np.sum(policy_new-policy)
    #print("  "+str(difference))
    #policy = policy_new


    # compute state visition frequences
    svf = compute_state_visition_freq(P_a, gamma, policy,trajs,deterministic=False)

    # compute gradients
    fm = feat_map.reshape((N_STATES*N_STATES, N_FEATURES))
    sv = svf.reshape(N_STATES*N_STATES, 1)
    #temp = np.zeros([N_STATES,N_STATES,N_FEATURES])

    count = 0
    not_zero = 0
    total = 0
    #for s1 in range(N_STATES):
    #  for s2 in range(N_STATES):
    #        temp[s1,s2,:] = svf[s1,s2]*feat_map[s1,s2,:]

    #print(count)
    #print(not_zero)
    #print(total)
    #input()
    #val = np.zeros([N_FEATURES])
    #for f in range(N_FEATURES):
    #  val[f]=np.sum(temp[:,:,f])

    #fm = feat_map.T.dot(svf)
    #fm = np.sum(fm, 1)
    #fm = np.sum(fm, 1)
    val = fm.T.dot(sv).reshape((N_FEATURES,))
    grad = feat_exp - val
    print(val)
    grad_plot[iteration,:]=grad
    # update params
    theta += lr * grad
    thetas_plot[iteration,:]=theta
    np.save("final_thetas", arr=theta)
    np.save('grad_plot.npy', grad_plot)
    #print("******************************"+ str(iteration) +"******************************************")
    #print(theta)
    lr -= lr_const
    sys.stdout.write('\r' + "Progress:"+ str(iteration) + "/" +str(n_iters))#+" ,applicable states:"+str(theta))
    sys.stdout.flush()  
  print(theta)
  rewards = np.dot(feat_map, theta)

  np.save("final_thetas", arr=theta)
  np.save('grad_plot.npy',grad_plot)
  np.save('theta_plot.npy',thetas_plot)


  return normalize(rewards)

