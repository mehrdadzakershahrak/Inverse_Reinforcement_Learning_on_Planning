import numpy as np

def laven_dist(list1, list2):
    m = len(list1)
    n = len(list2)
    dp = [[0 for x in range(n+1)] for x in range(m+1)] 
  
    # Fill d[][] in bottom up manner 
    for i in range(m+1): 
        for j in range(n+1): 
  
            # If first string is empty, only option is to 
            # insert all characters of second string 
            if i == 0: 
                dp[i][j] = j    # Min. operations = j 
  
            # If second string is empty, only option is to 
            # remove all characters of second string 
            elif j == 0: 
                dp[i][j] = i    # Min. operations = i 
  
            # If last characters are same, ignore last char 
            # and recur for remaining string 
            elif list1[i-1] == list2[j-1]: 
                dp[i][j] = dp[i-1][j-1] 
  
            # If last character are different, consider all 
            # possibilities and find minimum 
            else: 
                dp[i][j] = 1 + min(dp[i][j-1],        # Insert 
                                   dp[i-1][j],        # Remove 
                                   dp[i-1][j-1])    # Replace 
  
    return dp[m][n] 

def action_distance(plan_1, plan_2):
    if (not plan_1) and (not plan_2):
        return 0
    if plan_1 == plan_2:
        return 0
    #print(plan_a)
    plan_a = set(plan_1)
    plan_b = set(plan_2)
    a_p = {}
    b_p = {}
    for action in plan_1:
        if action not in a_p.keys():
           a_p[action] = 1
        else:
            a_p[action]+=1
    
    for action in plan_2:
        if action not in b_p.keys():
           b_p[action] = 1
        else:
            b_p[action]+=1
    
    common_actions = set(a_p).intersection(set(b_p))
    a_d_b = set(a_p).difference(set(b_p))
    b_d_a = set(b_p).difference(set(a_p))
    num = 0
    for action in list(common_actions):
        num+=abs(a_p[action]-b_p[action])
    for action in list(a_d_b):
        num+=a_p[action]
    for action in list(b_d_a):
        num+=b_p[action]
    d = (num)*1.0/((max(len(plan_a),len(plan_b)))*1.0)
    return d
