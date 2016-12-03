#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete the Sokoban warehouse domain.

#   You may add only standard python imports---i.e., ones that are automatically
#   available on TEACH.CS
#   You may not remove any imports.
#   You may not import or otherwise source any of your own files

#import os for time functions
from search import * #for search engines
from LightsOut import LightsOutState,PROBLEMS, Lightsout_goal_state#for Sokoban specific classes and problems

#SOKOBAN HEURISTICS
def heur_displaced(state):
  '''trivial admissible sokoban heuristic'''
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
        total += 1
    if(len(state.lights) == 0):
        return 0
    return total

def fval_function(sN, weight):

    return 0

def weighted_astar(initail_state, timebound = 10):
#IMPLEMENT
    '''Provides an implementation of weighted a-star, as described in the HW1 handout'''
    '''INPUT: a sokoban state that represents the start state and a timebound (number of seconds)'''
    '''OUTPUT: A goal state (if a goal is found), else False''' 
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
    final = se.search(s0, Lightsout_goal_state, heur_alternate, timebound)

    if final:
      final.print_path()
      solved += 1
    else:
      final.print_path()
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


