
# import student's functions
from solution import *

#Select what to test
test_heur_displaced = True
test_bfs = False
test_heur_1 = False
test_weighted_astar = False
test_heur_3 = False


if test_heur_displaced:
    ##############################################################
    print('Testing Heuristic with 5 second time bound')


    solved = 0; unsolved = []; timebound = 5;

    for i in range(0,30):
        print("*************************************") 
        print("PROBLEM {}".format(i))
        s0 = PROBLEMS[i]
        se = SearchEngine('best_first', 'full')
        final = se.search(initState=s0, heur_fn=heur_displaced, timebound=timebound, goal_fn=Lightsout_goal_state)

        if final:
            solved += 1
            #If you want to see the path
            final.print_path()
        else:
            unsolved.append(i)   

    print("\n*************************************")  
    print("In the problem set provided, {} were solved in less than {} seconds by this solver.".format(solved, timebound))  
    print("Problems that remain unsolved in the set are Problems: {}".format(unsolved))   
    print("*************************************\n")
    ##############################################################

    print('Testing Heuristic with 10 second time bound')

    solved = 0;
    unsolved = [];
    timebound = 10;

    for i in range(0, 30):
        print("*************************************")
        print("PROBLEM {}".format(i))
        s0 = PROBLEMS[i]
        se = SearchEngine('best_first', 'full')
        final = se.search(initState=s0, heur_fn=heur_displaced, timebound=timebound, goal_fn=Lightsout_goal_state)

        if final:
            solved += 1
            # If you want to see the path
            final.print_path()
        else:
            unsolved.append(i)

    print("\n*************************************")
    print(
        "In the problem set provided, {} were solved in less than {} seconds by this solver.".format(solved, timebound))
    print("Problems that remain unsolved in the set are Problems: {}".format(unsolved))
    print("*************************************\n")
    ##############################################################

if test_heur_1:
    ##############################################################
    print('Testing Heuristic with 5 second time bound')


    solved = 0; unsolved = []; timebound = 5;

    for i in range(0,30):
        print("*************************************")
        print("PROBLEM {}".format(i))
        s0 = PROBLEMS[i]
        se = SearchEngine('best_first', 'full')
        final = se.search(initState=s0, heur_fn=heur_alternate, timebound=timebound, goal_fn=Lightsout_goal_state)

        if final:
            solved += 1
            #If you want to see the path
            final.print_path()
        else:
            unsolved.append(i)

    print("\n*************************************")
    print("In the problem set provided, {} were solved in less than {} seconds by this solver.".format(solved, timebound))
    print("Problems that remain unsolved in the set are Problems: {}".format(unsolved))
    print("*************************************\n")
    ##############################################################

    ##############################################################
    print('Testing Heuristic with 10 second time bound')

    solved = 0;
    unsolved = [];
    timebound = 10;

    for i in range(0, 30):
        print("*************************************")
        print("PROBLEM {}".format(i))
        s0 = PROBLEMS[i]
        se = SearchEngine('best_first', 'full')
        final = se.search(initState=s0, heur_fn=heur_alternate, timebound=timebound, goal_fn=Lightsout_goal_state)

        if final:
            solved += 1
            # If you want to see the path
            final.print_path()
        else:
            unsolved.append(i)

    print("\n*************************************")
    print(
        "In the problem set provided, {} were solved in less than {} seconds by this solver.".format(solved, timebound))
    print("Problems that remain unsolved in the set are Problems: {}".format(unsolved))
    print("*************************************\n")
    ##############################################################


if test_weighted_astar:

  ##############################################################
  # TEST ANYTIME WEIGHTED A STAR
  print('Testing Anytime Weighted A Star')

  solved = 0; unsolved = []; benchmark = 0; timebound = 8 #8 second time limit 
  for i in range(0,30):
    print("*************************************")  
    print("PROBLEM {}".format(i))

    s0 = PROBLEMS[i] #Problems get harder as i gets bigger
    final = weighted_astar(s0, timebound)

    if final:
      final.print_path()
      solved += 1 
    else:
      unsolved.append(i)  

  print("\n*************************************")  
  print("Of 30 initial problems, {} were solved in less than {} seconds by this solver.".format(solved, timebound))
  print("Problems that remain unsolved in the set are Problems: {}".format(unsolved))
  print("*************************************\n")
  ##############################################################


if test_bfs:
    print('Testing Heuristic with 5 second time bound')

    solved = 0;
    unsolved = [];
    timebound = 5;

    for i in range(0, 30):
        print("*************************************")
        print("PROBLEM {}".format(i))
        s0 = PROBLEMS[i]
        se = SearchEngine('breadth_first', 'full')
        final = se.search(initState=s0, heur_fn=heur_alternate, timebound=timebound, goal_fn=Lightsout_goal_state)

        if final:
            solved += 1
            # If you want to see the path
            final.print_path()
        else:
            unsolved.append(i)

    print("\n*************************************")
    print(
        "In the problem set provided, {} were solved in less than {} seconds by this solver.".format(solved, timebound))
    print("Problems that remain unsolved in the set are Problems: {}".format(unsolved))
    print("*************************************\n")
    ##############################################################

    ##############################################################
    print('Testing Heuristic with 10 second time bound')

    solved = 0;
    unsolved = [];
    timebound = 10;

    for i in range(0, 30):
        print("*************************************")
        print("PROBLEM {}".format(i))
        s0 = PROBLEMS[i]
        se = SearchEngine('breadth_first', 'full')
        final = se.search(initState=s0, heur_fn=heur_alternate, timebound=timebound, goal_fn=Lightsout_goal_state)

        if final:
            solved += 1
            # If you want to see the path
            final.print_path()
        else:
            unsolved.append(i)

    print("\n*************************************")
    print(
        "In the problem set provided, {} were solved in less than {} seconds by this solver.".format(solved, timebound))
    print("Problems that remain unsolved in the set are Problems: {}".format(unsolved))
    print("*************************************\n")

if test_heur_3:
    ##############################################################
    print('Testing Heuristic with 5 second time bound')


    solved = 0; unsolved = []; timebound = 5;

    for i in range(0,30):
        print("*************************************")
        print("PROBLEM {}".format(i))
        s0 = PROBLEMS[i]
        se = SearchEngine('best_first', 'full')
        final = se.search(initState=s0, heur_fn=heur_alternate_3, timebound=timebound, goal_fn=Lightsout_goal_state)

        if final:
            solved += 1
            #If you want to see the path
            final.print_path()
        else:
            unsolved.append(i)

    print("\n*************************************")
    print("In the problem set provided, {} were solved in less than {} seconds by this solver.".format(solved, timebound))
    print("Problems that remain unsolved in the set are Problems: {}".format(unsolved))
    print("*************************************\n")
    ##############################################################

    ##############################################################
    print('Testing Heuristic with 10 second time bound')

    solved = 0;
    unsolved = [];
    timebound = 10;

    for i in range(0, 30):
        print("*************************************")
        print("PROBLEM {}".format(i))
        s0 = PROBLEMS[i]
        se = SearchEngine('best_first', 'full')
        final = se.search(initState=s0, heur_fn=heur_alternate, timebound=timebound, goal_fn=Lightsout_goal_state)

        if final:
            solved += 1
            # If you want to see the path
            final.print_path()
        else:
            unsolved.append(i)

    print("\n*************************************")
    print(
        "In the problem set provided, {} were solved in less than {} seconds by this solver.".format(solved, timebound))
    print("Problems that remain unsolved in the set are Problems: {}".format(unsolved))
    print("*************************************\n")




