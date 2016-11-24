#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete the Sokoban warehouse domain.

#   You may add only standard python imports---i.e., ones that are automatically
#   available on TEACH.CS
#   You may not remove any imports.
#   You may not import or otherwise source any of your own files

#import os for time functions
from search import * #for search engines
from sokoban import SokobanState, Direction, PROBLEMS, sokoban_goal_state #for Sokoban specific classes and problems
from itertools import * 
import sys
import copy
#Citation: import munkres.py from https://pypi.python.org/pypi/munkres/ 
#all codes of class Munkres are from https://pypi.python.org/pypi/munkres/ as reference 
class Munkres:
    """
    Calculate the Munkres solution to the classical assignment problem.
    See the module documentation for usage.
    """

    def __init__(self):
        """Create a new instance"""
        self.C = None
        self.row_covered = []
        self.col_covered = []
        self.n = 0
        self.Z0_r = 0
        self.Z0_c = 0
        self.marked = None
        self.path = None

    def make_cost_matrix(profit_matrix, inversion_function):
        """
        **DEPRECATED**

        Please use the module function ``make_cost_matrix()``.
        """
        import munkres
        return munkres.make_cost_matrix(profit_matrix, inversion_function)

    make_cost_matrix = staticmethod(make_cost_matrix)

    def pad_matrix(self, matrix, pad_value=0):
        """
        Pad a possibly non-square matrix to make it square.

        :Parameters:
            matrix : list of lists
                matrix to pad

            pad_value : int
                value to use to pad the matrix

        :rtype: list of lists
        :return: a new, possibly padded, matrix
        """
        max_columns = 0
        total_rows = len(matrix)

        for row in matrix:
            max_columns = max(max_columns, len(row))

        total_rows = max(max_columns, total_rows)

        new_matrix = []
        for row in matrix:
            row_len = len(row)
            new_row = row[:]
            if total_rows > row_len:
                # Row too short. Pad it.
                new_row += [pad_value] * (total_rows - row_len)
            new_matrix += [new_row]

        while len(new_matrix) < total_rows:
            new_matrix += [[pad_value] * total_rows]

        return new_matrix

    def compute(self, cost_matrix):
        """
        Compute the indexes for the lowest-cost pairings between rows and
        columns in the database. Returns a list of (row, column) tuples
        that can be used to traverse the matrix.

        :Parameters:
            cost_matrix : list of lists
                The cost matrix. If this cost matrix is not square, it
                will be padded with zeros, via a call to ``pad_matrix()``.
                (This method does *not* modify the caller's matrix. It
                operates on a copy of the matrix.)

                **WARNING**: This code handles square and rectangular
                matrices. It does *not* handle irregular matrices.

        :rtype: list
        :return: A list of ``(row, column)`` tuples that describe the lowest
                 cost path through the matrix

        """
        self.C = self.pad_matrix(cost_matrix)
        self.n = len(self.C)
        self.original_length = len(cost_matrix)
        self.original_width = len(cost_matrix[0])
        self.row_covered = [False for i in range(self.n)]
        self.col_covered = [False for i in range(self.n)]
        self.Z0_r = 0
        self.Z0_c = 0
        self.path = self.__make_matrix(self.n * 2, 0)
        self.marked = self.__make_matrix(self.n, 0)

        done = False
        step = 1

        steps = { 1 : self.__step1,
                  2 : self.__step2,
                  3 : self.__step3,
                  4 : self.__step4,
                  5 : self.__step5,
                  6 : self.__step6 }

        while not done:
            try:
                func = steps[step]
                step = func()
            except KeyError:
                done = True

        # Look for the starred columns
        results = []
        for i in range(self.original_length):
            for j in range(self.original_width):
                if self.marked[i][j] == 1:
                    results += [(i, j)]

        return results

    def __copy_matrix(self, matrix):
        """Return an exact copy of the supplied matrix"""
        return copy.deepcopy(matrix)

    def __make_matrix(self, n, val):
        """Create an *n*x*n* matrix, populating it with the specific value."""
        matrix = []
        for i in range(n):
            matrix += [[val for j in range(n)]]
        return matrix

    def __step1(self):
        """
        For each row of the matrix, find the smallest element and
        subtract it from every element in its row. Go to Step 2.
        """
        C = self.C
        n = self.n
        for i in range(n):
            minval = min(self.C[i])
            # Find the minimum value for this row and subtract that minimum
            # from every element in the row.
            for j in range(n):
                self.C[i][j] -= minval

        return 2

    def __step2(self):
        """
        Find a zero (Z) in the resulting matrix. If there is no starred
        zero in its row or column, star Z. Repeat for each element in the
        matrix. Go to Step 3.
        """
        n = self.n
        for i in range(n):
            for j in range(n):
                if (self.C[i][j] == 0) and \
                        (not self.col_covered[j]) and \
                        (not self.row_covered[i]):
                    self.marked[i][j] = 1
                    self.col_covered[j] = True
                    self.row_covered[i] = True

        self.__clear_covers()
        return 3

    def __step3(self):
        """
        Cover each column containing a starred zero. If K columns are
        covered, the starred zeros describe a complete set of unique
        assignments. In this case, Go to DONE, otherwise, Go to Step 4.
        """
        n = self.n
        count = 0
        for i in range(n):
            for j in range(n):
                if self.marked[i][j] == 1:
                    self.col_covered[j] = True
                    count += 1

        if count >= n:
            step = 7 # done
        else:
            step = 4

        return step

    def __step4(self):
        """
        Find a noncovered zero and prime it. If there is no starred zero
        in the row containing this primed zero, Go to Step 5. Otherwise,
        cover this row and uncover the column containing the starred
        zero. Continue in this manner until there are no uncovered zeros
        left. Save the smallest uncovered value and Go to Step 6.
        """
        step = 0
        done = False
        row = -1
        col = -1
        star_col = -1
        while not done:
            (row, col) = self.__find_a_zero()
            if row < 0:
                done = True
                step = 6
            else:
                self.marked[row][col] = 2
                star_col = self.__find_star_in_row(row)
                if star_col >= 0:
                    col = star_col
                    self.row_covered[row] = True
                    self.col_covered[col] = False
                else:
                    done = True
                    self.Z0_r = row
                    self.Z0_c = col
                    step = 5

        return step

    def __step5(self):
        """
        Construct a series of alternating primed and starred zeros as
        follows. Let Z0 represent the uncovered primed zero found in Step 4.
        Let Z1 denote the starred zero in the column of Z0 (if any).
        Let Z2 denote the primed zero in the row of Z1 (there will always
        be one). Continue until the series terminates at a primed zero
        that has no starred zero in its column. Unstar each starred zero
        of the series, star each primed zero of the series, erase all
        primes and uncover every line in the matrix. Return to Step 3
        """
        count = 0
        path = self.path
        path[count][0] = self.Z0_r
        path[count][1] = self.Z0_c
        done = False
        while not done:
            row = self.__find_star_in_col(path[count][1])
            if row >= 0:
                count += 1
                path[count][0] = row
                path[count][1] = path[count-1][1]
            else:
                done = True

            if not done:
                col = self.__find_prime_in_row(path[count][0])
                count += 1
                path[count][0] = path[count-1][0]
                path[count][1] = col

        self.__convert_path(path, count)
        self.__clear_covers()
        self.__erase_primes()
        return 3

    def __step6(self):
        """
        Add the value found in Step 4 to every element of each covered
        row, and subtract it from every element of each uncovered column.
        Return to Step 4 without altering any stars, primes, or covered
        lines.
        """
        minval = self.__find_smallest()
        for i in range(self.n):
            for j in range(self.n):
                if self.row_covered[i]:
                    self.C[i][j] += minval
                if not self.col_covered[j]:
                    self.C[i][j] -= minval
        return 4

    def __find_smallest(self):
        """Find the smallest uncovered value in the matrix."""
        minval = sys.maxsize
        for i in range(self.n):
            for j in range(self.n):
                if (not self.row_covered[i]) and (not self.col_covered[j]):
                    if minval > self.C[i][j]:
                        minval = self.C[i][j]
        return minval

    def __find_a_zero(self):
        """Find the first uncovered element with value 0"""
        row = -1
        col = -1
        i = 0
        n = self.n
        done = False

        while not done:
            j = 0
            while True:
                if (self.C[i][j] == 0) and \
                        (not self.row_covered[i]) and \
                        (not self.col_covered[j]):
                    row = i
                    col = j
                    done = True
                j += 1
                if j >= n:
                    break
            i += 1
            if i >= n:
                done = True

        return (row, col)

    def __find_star_in_row(self, row):
        """
        Find the first starred element in the specified row. Returns
        the column index, or -1 if no starred element was found.
        """
        col = -1
        for j in range(self.n):
            if self.marked[row][j] == 1:
                col = j
                break

        return col

    def __find_star_in_col(self, col):
        """
        Find the first starred element in the specified row. Returns
        the row index, or -1 if no starred element was found.
        """
        row = -1
        for i in range(self.n):
            if self.marked[i][col] == 1:
                row = i
                break

        return row

    def __find_prime_in_row(self, row):
        """
        Find the first prime element in the specified row. Returns
        the column index, or -1 if no starred element was found.
        """
        col = -1
        for j in range(self.n):
            if self.marked[row][j] == 2:
                col = j
                break

        return col

    def __convert_path(self, path, count):
        for i in range(count+1):
            if self.marked[path[i][0]][path[i][1]] == 1:
                self.marked[path[i][0]][path[i][1]] = 0
            else:
                self.marked[path[i][0]][path[i][1]] = 1

    def __clear_covers(self):
        """Clear all covered matrix cells"""
        for i in range(self.n):
            self.row_covered[i] = False
            self.col_covered[i] = False

    def __erase_primes(self):
        """Erase all prime markings"""
        for i in range(self.n):
            for j in range(self.n):
                if self.marked[i][j] == 2:
                    self.marked[i][j] = 0





#SOKOBAN HEURISTICS
def heur_displaced(state):
  '''trivial admissible sokoban heuristic'''
  '''INPUT: a sokoban state'''
  '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''       
  count = 0
  for box in state.boxes:
    if box not in state.storage:
      count += 1
    return count
# bunch of help functions   
def distance_box_to_storage(box,storage):
    return abs(box[0]-storage[0]) + abs(box[1]-storage[1])

def closest_distance_box_to_storage(box,storages):
    distance= 1000000
    for storage in storages:
      distance=min(distance,distance_box_to_storage(box,storage))
    return distance

def distance_robot_to_box(robot,box):
    return abs(robot[0]-box[0]) + abs(robot[1]-box[1])

def distance_box_to_cloest_robot(box,robots):
   
    distance= 10000000
    for robot in robots:
      distance=min(distance,distance_robot_to_box(robot,box))
    return  distance

def closest_robot(box, robots):
    distance=10000000
    for robot in robots:
        if distance > distance_box_to_storage(robot,box):
          distance = distance_box_to_storage(robot,box)
          closest = robot 
    return closest    
  
def heur_manhattan_distance(state):
#IMPLEMENT
    '''admissible sokoban heuristic: manhattan distance'''
    '''INPUT: a sokoban state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''      
    #We want an admissible heuristic, which is an optimistic heuristic. 
    #It must always underestimate the cost to get from the current state to the goal.
    #The sum Manhattan distance of the boxes to their closest storage spaces is such a heuristic.  
    #When calculating distances, assume there are no obstacles on the grid and that several boxes can fit in one storage bin.
    #You should implement this heuristic function exactly, even if it is tempting to improve it.
    #Your function should return a numeric value; this is the estimate of the distance to the goal.
    hval = 0
    for box in state.boxes:
        hval=hval + closest_distance_box_to_storage(box,state.storage)
    return hval
 
#def distance_boxes_to_storages(boxes,storages):
    #distance=0
    #for i in range(0,len(boxes)):
      #distance = distance + distance_box_to_storage(boxes[i],storages[i])
    #return distance

# help function to clone a frozen set to list
def copy_sets(list1,sets):
    for i in sets:
      list1.append(i)
  
    return list1
# help functions to determine if there is only one entrace allow robots pass
# all obstacles are in the same row 
def check_one_entrance_row(ob,width): 
    obs =  copy_sets([],ob)
    if len(ob)== width - 1:
      initial = obs[0][1]
      for i in ob :
          if i[1] == initial:
            continue
          else:
            return None
      a= set()
      for i in range(0,width):
        a.add((i,initial))
      for o in a :
        if o not in ob:
          return o
# all obstacles are in the same colum      
def check_one_entrance_colum(ob,height):      
  obs =  copy_sets([],ob)
  if len(ob)==height -1:
      initial = obs[0][0]
      for i in ob:
        if i[0] == initial:
          continue
        else:
          return None
      a= set()
      for i in range(0,height):
        a.add((initial,i))
      for o in a :
        if o not in ob:
          return o


    
def heur_alternate(state):
#IMPLEMENT
    '''a better sokoban heuristic'''
    '''INPUT: a sokoban state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''        
    #heur_min_moves has flaws.   
    #Write a heuristic function that improves upon heur_manhattan_distance to estimate distance between the current state and the goal.
    #Your function should return a numeric value for the estimate of the distance to the goal.
    
    # I import matrix code from munkres.py from https://pypi.python.org/pypi/munkres/ , because i fined it is faster than permutations. So before run the test scripts, please
    # copy solution.py and munkres,py under the same folder. Thanks !
    # The main ideal of this heur_alternate is h-val is the minimum cost of each box to one storage. So I use matrix like 
    # [b1s1,b1s2.....]
    # [b2s1,b2s2.....]
    # [..............]     bnsn represent the distance from box n to storage n. Then I compute the minimum sum distance of boxes ro storages as h-val
    #  .
    #  .
    #  .
    # [bns1,......bnsn]
    # 
    # In order to solve more problems with the timebound, I add lots of if conditions to determine deadlocks which meaks the problem unsovlable in a particular situation:
    # 1.when a box in the corner and not in any storage, which means robot cannot move this box 
    # 2.A box adjacent to the wall , and the storage that the box wants to go is not on the same row.
    # 3.box is in the corner which made of two obstacles. For example, one obstacle in on the top of the box, and the other one is on the left of the box 
    # 4.A box is adjacent to the wall, and adjacent to another box or obstacle
    # 5.A box's lefttop is occupied by another box or obstacle and the box is adjacent to the wall.
    # The above situations will cause deadlock. So I give those cases maximum h-value which can improve to solve more problems. 
    hval=  0
    hval1= 0 
    
   
    matrix = []
    for b in state.boxes :
        sublist = []
        robots = copy_sets([],state.robots)
        # if box in the corner and not in the storage, return the biggest distance 10000000
        if b == (0,0) and b not in state.storage:
                  return 10000000          
        elif b == (0,state.height -1) and b not in state.storage :
                  return 10000000
        elif b == (state.width -1 , 0) and b not in state.storage:
                  return 10000000
        elif b == (state.width-1, state.height -1) and b not in state.storage:
                  return 10000000
                
        # if box lean the wall and adjacent to the obstacle or another box and not in any storage, return 10000000        
        elif b[0] == 0 and  ((0,b[1]+1) in state.obstacles.union(state.boxes) or (0,b[1]-1) in state.obstacles.union(state.boxes)) and b not in state.storage :
                  return 10000000
        elif b[0] == state.width -1 and  ((state.width -1,b[1]+1) in state.obstacles.union(state.boxes) or (state.width -1,b[1]-1) in state.obstacles.union(state.boxes)) and b not in state.storage : 
                  return 10000000
        elif b[1] == 0 and  ((b[0]+1,0) in state.obstacles.union(state.boxes) or (b[0]-1,0) in state.obstacles.union(state.boxes)) and b not in state.storage :  
                  return 10000000        
        elif b[1] == state.height -1 and  ((b[0]+1,state.height -1) in state.obstacles.union(state.boxes) or (b[0]-1,state.height-1) in state.obstacles.union(state.boxes)) and b not in state.storage :  
                  return 10000000 
                
        #if box is adjacent to two obstacles and not in nay storage, which is deadlock. return 10000000        
        elif (b[0]-1,b[1]) in state.obstacles and (b[0],b[1]-1) in state.obstacles and b not in state.storage :
                  return 10000000
        elif (b[0]-1,b[1]) in state.obstacles and (b[0],b[1]+1) in state.obstacles and b not in state.storage :  
                  return 10000000
        elif (b[0]+1,b[1]) in state.obstacles and (b[0],b[1]-1) in state.obstacles and b not in state.storage :
                  return 10000000
        elif (b[0]+1,b[1]) in state.obstacles and (b[0],b[1]+1) in state.obstacles and b not in state.storage :  
                  return 10000000   
            
                
        for s in state.storage : 
            if b[0] == 0 and s[0] != 0 :
                    sublist.append(10000000)
            elif b[0] == state.width -1 and s[0] != state.width-1 : 
                    sublist.append(10000000)         
            elif b[1] == 0 and s[1] != 0 :
                    sublist.append(10000000)
            elif b[1] == state.height -1 and s[1] != state.height-1:
                    sublist.append(10000000)  
                    
            # if box in the corner and it is not in any storage, make the distance to 10000000         
            elif b == (0,0) and b != s:
                    #return 10000000
                    sublist.append(10000000)
            elif b == (0,state.height -1) and b !=s :
                    #return 10000000
                    sublist.append(10000000)
            elif b == (state.width -1 , 0) and b != s:
                    #return 10000000
                    sublist.append(10000000)
            elif b == (state.width-1, state.height -1) and b !=s:
                    #return 10000000   
                    sublist.append(10000000)
      
                              
            # box near the wall and block by the obstacle or another box         
            elif b[0] == 0 and  ((0,b[1]+1) in state.obstacles.union(state.boxes) or (0,b[1]-1) in state.obstacles.union(state.boxes)) and b != s :
                    sublist.append(10000000)
            elif b[0] == state.width -1 and  ((state.width -1,b[1]+1) in state.obstacles.union(state.boxes) or (state.width -1,b[1]-1) in state.obstacles.union(state.boxes)) and b != s : 
                    sublist.append(10000000)
            elif b[1] == 0 and  ((b[0]+1,0) in state.obstacles.union(state.boxes) or (b[0]-1,0) in state.obstacles.union(state.boxes)) and b != s :  
                    sublist.append(10000000)
            elif b[1] == state.height -1 and  ((b[0]+1,state.height -1) in state.obstacles.union(state.boxes) or (b[0]-1,state.height-1) in state.obstacles.union(state.boxes)) and b != s :  
                    sublist.append(10000000)  
                                                  
            # if the box is in the croner of two onstacles        
            elif (b[0]-1,b[1]) in state.obstacles and (b[0],b[1]-1) in state.obstacles and b !=s :
                    sublist.append(10000000)
                    #return 10000000
            elif (b[0]-1,b[1]) in state.obstacles and (b[0],b[1]+1) in state.obstacles and b !=s :  
                    sublist.append(10000000)
                    #return 10000000
            elif (b[0]+1,b[1]) in state.obstacles and (b[0],b[1]-1) in state.obstacles and b !=s :
                    sublist.append(10000000)
                    #return 10000000
            elif (b[0]+1,b[1]) in state.obstacles and (b[0],b[1]+1) in state.obstacles and b !=s :  
                    sublist.append(10000000)
                    #return 10000000
                  
            # to pass some dealock siituations like question 19
            elif (b == (state.width-2,state.height-1) and (state.width-1,state.height-2) in state.boxes.union(state.obstacles))  and b!=s and (state.width-1,state.height-1) !=s and (state.width-1,state.height-1) not in state.robots:
                    sublist.append(10000000)       
            elif (b == (1,state.height-1) and (0,state.height-2) in state.boxes.union(state.obstacles))  and b!=s and (0,state.height-1) !=s and (0,state.height-1) not in state.robots:
                    sublist.append(10000000)    
            elif (b == (1,0) and (0,1) in state.boxes.union(state.obstacles))  and b!=s and (0,0) !=s and (0,0) not in state.robots:
                    sublist.append(10000000)    
            elif (b == (state.width-2,0) and (state.width-1,1) in state.boxes.union(state.obstacles))  and b!=s and (state.width-1,0) !=s and (state.width-1,0) not in state.robots:
                    sublist.append(10000000)        
                          
            else:
              # if there is only one entrace from box to storage: total distance = box-to-entrace + entrace-to-sotrage
              r= check_one_entrance_row(state.obstacles,state.width)
              c= check_one_entrance_colum(state.obstacles,state.height)
              if r != None and (s[1] < c[1] < b[1] or s[1] > c[1] >b[1]):
                sublist.append(distance_box_to_storage(b,r)+distance_box_to_storage(r,s))
              elif c != None and (s[0] < c[0] < b[0] or s[0] > c[0] > b[0]):
                sublist.append(distance_box_to_storage(b,c)+distance_box_to_storage(c,s))
              # not one entrace, we can calculate the distance simply
              else:
                sublist.append(distance_box_to_storage(b,s))
        matrix.append(sublist)
                           
    m = Munkres()
    indexes = m.compute(matrix)
    for row, column in indexes:
          value = matrix[row][column]
          hval += value        
#==========================================================    
    
    
    
         
    #for box1 in state.boxes:
      #hval1 = hval1 + distance_box_to_cloest_robot(box1,state.robots)-1
  
    
    return hval
    #return hval

def fval_function(sN, weight):
#IMPLEMENT
    """
    Provide a custom formula for f-value computation for Anytime Weighted A star.
    Returns the fval of the state contained in the sNode.

    @param sNode sN: A search node (containing a SokobanState)
    @param float weight: Weight given by Anytime Weighted A star
    @rtype: float
    """
  
    #Many searches will explore nodes (or states) that are ordered by their f-value.
    #For UCS, the fvalue is the same as the gval of the state. For best-first search, the fvalue is the hval of the state.
    #You can use this function to create an alternate f-value for states; this must be a function of the state and the weight.
    #The function must return a numeric f-value.
    #The value will determine your state's position on the Frontier list during a 'custom' search.
    #You must initialize your search engine object as a 'custom' search engine if you supply a custom fval function.
    fval = (1-weight)*sN.gval + weight*sN.hval
    return fval

def weighted_astar(initail_state, timebound = 10):
#IMPLEMENT
    '''Provides an implementation of weighted a-star, as described in the HW1 handout'''
    '''INPUT: a sokoban state that represents the start state and a timebound (number of seconds)'''
    '''OUTPUT: A goal state (if a goal is found), else False''' 
    se = SearchEngine('custom', 'full')
    maxgval = 10000000
    result = None
    Best_weight = None
    for i in range(0,11):        
        final = se.search(initail_state, heur_fn=heur_alternate,timebound=timebound, goal_fn=sokoban_goal_state,fval_function = fval_function,weight = 1 - i*0.1)
        timebound = timebound - se.total_search_time
        if final and final.gval < maxgval:
          Best_weight = i 
          maxgval = final.gval
          result = final
       
    return result

if __name__ == "__main__":
  #TEST CODE
  solved = 0; unsolved = []; counter = 0; percent = 0; timebound = 2; #2 second time limit for each problem
  print("*************************************")  
  print("Running A-star")     

  for i in range(0,40): #note that there are 40 problems in the set that has been provided.  We just run through 10 here for illustration.

    print("*************************************")  
    print("PROBLEM {}".format(i))
    
    s0 = PROBLEMS[i] #Problems will get harder as i gets bigger

    se = SearchEngine('astar', 'full')
    final = se.search(s0, sokoban_goal_state, heur_displaced, timebound)

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

  solved = 0; unsolved = []; counter = 0; percent = 0; timebound = 8; #8 second time limit 
  print("Running Anytime Weighted A-star")   

  for i in range(0,40):
    print("*************************************")  
    print("PROBLEM {}".format(i))

    s0 = PROBLEMS[i] #Problems get harder as i gets bigger
    final = weighted_astar(s0, timebound)

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


