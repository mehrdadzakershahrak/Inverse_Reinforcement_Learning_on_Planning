#  function to modify pddl files
    # create a template of all files and change accordingly
    # $HAS_PASSWORD is replaced with either ' ' or '(has_password)'
    # read domain template and p-i template, read the expert demonstration for p-i line by line and modify domainH
    # (template after each explanation) after each action.
# plan the modified pddl files after each change
    # run the planner
# calculate features from the plan
# create the P_a NxNxN (transition probabilities) last N is action where the probabilities are either 0 or 1
# input the features to irl
# use the learned reward of the last step to perform value iteration on MDP

#Expert demos:
ladder, password, get_key, fire_ext, hammer, power_generator
password, get_key, fire_ext, hammer, ladder, power_generator
password, get_key, fire_ext, power_generator, hammer, ladder
password, get_key, fire_ext, hammer, ladder, power_generator
power_generator, get_key, password, hammer, ladder, fire_ext
power_generator, get_key, password, fire_ext, hammer, ladder

'''
DONE
render_template(p-i, dict){
    read scavenger.tpl.pddl into s1
    read p-i.tpl.pddl into s2
    for (key, value) in dict {
        replace all instances of key with value in both s1 and s2
    }
    write s1 to domainH.pddl
    write s2 to p-i.pddl
}
'''
update_dict(D, explanation) {
    switch explanation {
        case('ladder'):
            D['$HAS_LADDER'] = '(has_ladder)'
            .....
    }
}
'''
DONE
run_planner(p-i) {
    returns the calculated plan from p-i.pddl and domainH.pddl
}
'''

calculate_features(plan_old, plan_new, explanation) {
    calculate_lavenstein_distance
    calculate_plan_cost
    calculate_plan_distance
    calculate_domain_dependent_features based on explanation
    return all values in an array
}
'''
DONE
calculate_states() {
    initialize S = {}
    initialize R = {}
    n = 0
    for i in 1 to 8 { # number of scenarios
        read expert demonstartion for that scenario line by line
        for each line {
            let s = string(i) + '_'    #s is (4_,password),(4_,password,get_key) and so on
            for each word in line {
                s += ',' + word
                if s not in S {
                    S[s] = n      #S now contains mapping between number and 
                    R[n] = s
                    n += 1
                }
            }                   
        }
    }
    return S, R                 # S now contains mapping from explanation (history format) to number (like id)
                                # R now contains mapping from number (like id) to explanation (history-format)
}
'''
main() {
    S, R = calculate_states()
    # N is |S|
    # A is number of unique words in all demonstration files
    initialize feat_map to an empty map
    initialize P_a to an NxNxA matrix of all zeros
    initialize traj to an empty array (of 3-tuples)

    for i = 1 to 8 { # Number of scenarios
        read expert demonstartion for  scenario i line by line

        for each line {
            s = string(i) + '_'
            initialize D with all $ variables with ''
            render_template(i, D)
            plan_old = run_planner(i)
            features = calculate_features(plan_old, plan_old, '') #feature for each individual state
            if s not in feat_map {
                feat_map[S[s]] = features  #applying 's' explanation to 'S' results in a state with feature value 'features'

            }

            for each word in line {
                update_dict(D, word)
                render_template(i, D)
                plan_new = run_planner(i)
                s_old = s
                s += ',' + word
                if s not in feat_map {
                    features = calculate_features(plan_old, plan_new, word)
                    feat_map[S[s]] = features
                }
                P_a[S[s_old], S[s], word] = 1
                traj.push((S[s_old], S[s], word))
                plan_old = plan_new
            }
        }
    }
    call maxent_irl with feat_map, P_a, traj and other parameters
    # use the learned reward of the last step to perform value iteration on MDP
    use R to map state numbers to state strings
}


