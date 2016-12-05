
#import os for time functions
from search import * #for search engines
from LightsOut import LightsOutState,PROBLEMS, Lightsout_goal_state#for Sokoban specific classes and problems

#LIGHTSOUT HEURISTICS
def heur_displaced(state):
  '''trivial admissible lightsout heuristic'''
  '''INPUT: a lights out state'''
  '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''       
 
  return len(state.lights)



def heur_alternate(state):
#IMPLEMENT
    '''a better lights out heuristic'''
    '''INPUT: a lights out state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''
    total = 0
    for light in state.lights:
        left = (light[0] - 1, light[1])
        right = (light[0] + 1, light[1])
        up = (light[0], light[1] - 1)
        down = (light[0], light[1] + 1)
        if(left not in state.lights):
            total += 1

        if (right not in state.lights):
            total += 1

        if (up not in state.lights):
            total += 1

        if (down not in state.lights):
            total += 1
    if(len(state.lights) == 0):
        return 0
    return total * len(state.lights)

def heur_alternate_2(state):
#IMPLEMENT
    '''a better lights out heuristic'''
    '''INPUT: a lights out state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''
    total = 0
    for light in state.lights:
        left = (light[0] - 1, light[1])
        right = (light[0] + 1, light[1])
        up = (light[0], light[1] - 1)
        down = (light[0], light[1] + 1)
        if(left in state.lights):
            total += 1

        if (right in state.lights):
            total += 1

        if (up in state.lights):
            total += 1

        if (down in state.lights):
            total += 1
    if(len(state.lights) == 0):
        return 0
    return total


def heur_alternate_3(state):
    penalty = 0
    if len(state.toggled) != len(set(state.toggled)):
        penalty = 10

    total = 0
    for light in state.lights:
        left = (light[0] - 1, light[1])
        right = (light[0] + 1, light[1])
        up = (light[0], light[1] - 1)
        down = (light[0], light[1] + 1)
        if (left in state.lights):
            total += 1

        if (right in state.lights):
            total += 1

        if (up in state.lights):
            total += 1

        if (down in state.lights):
            total += 1
    if (len(state.lights) == 0):
        return 0
    return total + penalty


def fval_function(sN, weight):

    return (1 - weight) * sN.gval + weight * sN.hval

def weighted_astar(initail_state, timebound = 7):
#IMPLEMENT
    '''Provides an implementation of weighted a-star'''
    '''INPUT: a lightsout state that represents the start state and a timebound (number of seconds)'''
    '''OUTPUT: A goal state (if a goal is found), else False'''


    se = SearchEngine('custom', 'full')
    weight = 1
    const = 0.15
    passed = False
    search_begin_time = os.times()[0]
    while weight != 0:

        if timebound:  # timebound check
            if (os.times()[0] - search_begin_time) > timebound:
                # exceeded time bound, must terminate search
                print("ERROR: Search has exceeeded the time bound provided.")
                return passed
        current_search_time_begin = os.times()[0]
        result = se.search(initState=initail_state, heur_fn=heur_displaced, timebound=timebound, goal_fn=Lightsout_goal_state,
                       fval_function=fval_function, weight=weight, costbound=10000000000)
        current_search_time_end = os.times()[0]
        # get the remaining time for next round search
        timebound -= current_search_time_end - current_search_time_begin
        if result and not passed:
            passed = result
        elif result and result.gval <= passed.gval:
            passed = result
        weight -= const

        if os.times()[0] - search_begin_time <= timebound:
            return passed

    return False

if __name__ == "__main__":
  #TEST CODE for astar+heur_displaced
  solved = 0; unsolved = []; counter = 0; percent = 0; timebound = 10; #2 second time limit for each problem
  print("*************************************")  
  print("Running A-star")     

  for i in range(0,len(PROBLEMS)): #note that there are some problems in the set that has been provided. 

    print("*************************************")  
    print("PROBLEM {}".format(i))
    
    s0 = PROBLEMS[i] #Problems will get harder as i gets bigger

    se = SearchEngine('astar', 'full')
    final = se.search(s0, Lightsout_goal_state, heur_displaced, timebound)

    if final:
      final.print_path()
      solved += 1
    else:
      unsolved.append(i)
    counter += 1

  if counter > 0:  
    percent = (solved/counter)*100

  print("*************************************")  
  print("{} of {} problems ({} %) solved in less than {} seconds.".format(solved, counter, percent, timebound))  
  print("Problems that remain unsolved in the set are Problems: {}".format(unsolved))      
  print("*************************************") 


  #Test code for Astar+
  #solved = 0; unsolved = []; counter = 0; percent = 0; timebound = 8; #8 second time limit 
  #print("Running Anytime Weighted A-star")   

  #for i in range(0,40):
    #print("*************************************")  
    #print("PROBLEM {}".format(i))

    #s0 = PROBLEMS[i] #Problems get harder as i gets bigger
    #final = weighted_astar(s0, timebound)

    #if final:
      #final.print_path()   
      #solved += 1 
    #else:
      #unsolved.append(i)
    #counter += 1      

  #if counter > 0:  
    #percent = (solved/counter)*100   
      
  #print("*************************************")  
  #print("{} of {} problems ({} %) solved in less than {} seconds.".format(solved, counter, percent, timebound))  
  #print("Problems that remain unsolved in the set are Problems: {}".format(unsolved))      
  #print("*************************************") 


