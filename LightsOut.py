'''Lights out .

    A) Class lights out 

    A specializion of the StateSpace Class that is tailored to the game of Lights out.

    Code also contains a list of lights out problems for the purpose of testing.
'''

from search import *

class LightsOutState(StateSpace):

    def __init__(self, action, gval, parent,height, width, lights, toggled):
        '''
        Creates a new Lights Out state.
        @param width: The room's X dimension (excluding walls).
        @param height: The room's Y dimension (excluding walls).
        @param obstacles: A list of all the lights.
        '''
        StateSpace.__init__(self, action, gval, parent)
        self.height = height
        self.width = width
        self.lights = lights
        self.toggled = toggled

    def successors(self):
        '''
        Generates all the actions that can be performed from this state, and the states those actions will create.        
        '''
        successors = []
        transition_cost = 1
        for i in range(0,self.width) :
            for j in range(0,self.height):
                new_lights = []
                temp_lights = list(self.lights)
                if (i,j) not in self.lights:
                    new_lights.append((i,j))
                if (i,j) in self.lights:
                    temp_lights.remove((i,j))
                if ((i+1) < self.width):
                    if (i+1,j) in self.lights:
                        temp_lights.remove((i+1,j))
                    else:
                        new_lights.append((i+1,j))
                if ((j+1) < self.height):
                    if (i,j+1) in self.lights :
                        temp_lights.remove((i,j+1))
                    else:
                        new_lights.append((i,j+1))
                if ((i-1) > -1):
                    if (i-1,j) in self.lights:
                        temp_lights.remove((i-1,j))
                    else:
                        new_lights.append((i-1,j))
                        
                if ((j-1)>-1):
                    if (i,j-1) in self.lights :
                        temp_lights.remove((i,j-1))
                    else:
                        new_lights.append((i,j-1))         
                        
                total_lights = new_lights + temp_lights

                self.toggled.append((i, j))

                new_state = LightsOutState("press " + str((i,j)), self.gval + transition_cost, self, self.height, self.width, total_lights, self.toggled)
                
                successors.append(new_state)
                        
        return successors               
   
   
   
    def hashable_state(self):
        '''Return a data item that can be used as a dictionary key to UNIQUELY represent a state.'''
        return hash(((self.height,self.width),frozenset(self.lights)))              
        
    def state_string(self):
        '''Returns a string representation fo a state that can be printed to stdout.'''        
        map = []
        for y in range(0, self.height):
            row = []
            for x in range(0, self.width):
                row += [' ']
            map += [row]
        
        for light in self.lights :            map[light[1]][light[0]] = '1'
                
        
        for y in range(0, self.height):
            map[y] = ['#'] + map[y]
            map[y] = map[y] + ['#']
        map = ['#' * (self.width + 2)] + map
        map = map + ['#' * (self.width + 2)]        
       
        s = ''
        for row in map:
            for char in row:
                s += char
            s += '\n'

        return s        

    def print_state(self):
        '''
        Prints the string representation of the state. ASCII art FTW!
        '''        
        print("ACTION was " + self.action)      
        print(self.state_string())


def Lightsout_goal_state(state):
  '''Returns True if we have reached a goal state'''
  '''INPUT: a sokoban state'''
  '''OUTPUT: True (if goal) or False (if not)'''  
  #for box in state.boxes:
    #if box not in state.storage:
      #return False
  #return True
  for i in range(0,state.width):
    for j in range (0,state.height):
        if (i,j) in state.lights:
            return False
  return True        
'''
Lights Out Problem Set, for testing
'''
PROBLEMS = (
    LightsOutState("START", 0, None, 2, 2,
                                    [(0, 0)], [] #lights
                                    ),     
        LightsOutState("START", 0, None, 2, 2,
                                    [(0, 0),(1, 1)], [] #lights
                                    ),     
        LightsOutState("START", 0, None, 3, 3,
                                    [(0, 0)], [] #lights
                                    ),     
        LightsOutState("START", 0, None, 3, 3,
                                 [(0, 0),(1, 1)], [] #lights
                                 ),      
        LightsOutState("START", 0, None, 3, 3,
                         [(1, 0),(1, 1),(1,2),(2,1)], [] #lights
                         ),
        LightsOutState("START", 0, None, 3, 3,
                         [(1, 0),(1, 1),(1,2)], [] #lights
                         ),
        LightsOutState("START", 0, None, 3, 3,
                         [(1, 0),(1,2),(2,1)], [] #lights
                         ),
        LightsOutState("START", 0, None, 3, 3,
                         [(1, 0),(1, 1)], [] #lights
                         ),
        LightsOutState("START", 0, None, 3, 3,
                         [(1, 0)], [] #lights
                         ),
        LightsOutState("START", 0, None, 3, 4,
                 [(0, 2),(1, 1), (2, 2)], [] #lights
                 ),
    
        LightsOutState("START", 0, None, 3, 4,
                     [(0, 0),(0, 1)], [] #lights
                     ),
        LightsOutState("START", 0, None, 3, 4,
                 [(0, 0), (0, 1), (2, 1), (2, 2)], [] #lights
                 ),

        LightsOutState("START", 0, None, 4, 4,
                                        [(1, 1),(2,2), (1, 3), (2, 3)], [] #lights
                                        ),     
        LightsOutState("START", 0, None, 4, 4,
                                        [(0, 1),(3, 0),(3,1), (3, 3)], [] #lights
                                        ),     
        LightsOutState("START", 0, None, 4, 4,
                                        [(2, 1),(3, 1),(0,3),(1,3), (3, 3)], [] #lights
                                        ),    
        LightsOutState("START", 0, None, 4, 4,
                                        [(0, 0),(0, 3),(3,0),(3,3)], [] #lights
                                        ),     
        LightsOutState("START", 0, None, 4, 4,
                                        [(0,0),(1,0),(0,1)], [] #lights
                                        ), 
    
        LightsOutState("START", 0, None, 4, 5,
                                        [(0,0),(1,0),(0,1)], [] #lights
                                        ), 
        LightsOutState("START", 0, None, 4, 5,
                                        [(4,0),(4,1),(3,0)], [] #lights
                                        ),
        LightsOutState("START", 0, None, 4, 5,
                                        [(0,0),(1,1),(3,0)], [] #lights
                                        ),    
    
        LightsOutState("START", 0, None, 4, 5,
                                        [(0,0),(1,1),(2,2),(3,0)], [] #lights
                                        ), 
        LightsOutState("START", 0, None, 4, 5,
                                        [(0,0),(1,1),(2,2),(3,0),(3,3)], [] #lights
                                        ), 
        LightsOutState("START", 0, None, 4, 5,
                                        [(0,0),(1,1),(2,2),(3,0),(4,3)], [] #lights
                                        ),  
        LightsOutState("START", 0, None, 4, 5,
                                        [(1,1),(1,2),(1,3)], [] #lights
                                        ),
                                        
        LightsOutState("START", 0, None, 5, 5,
                                        [(0,0),(0,4),(4,0),(4,4)], [] #lights
                                        ),
        LightsOutState("START", 0, None, 5, 5,
                                        [(1,1),(1,2),(2,0),(3,4)], [] #lights
                                        ),    
        LightsOutState("START", 0, None, 5, 5,
                                        [(0,0),(0,1),(2,0),(2,1),(3,0)], [] #lights
                                        ),
        LightsOutState("START", 0, None, 5, 5,
                                        [(2,0),(2,1),(2,2),(2,3),(2,4)], [] #lights
                                        ),
        LightsOutState("START", 0, None, 7, 7,
                                           [(0,0),(1,1),(2,2),(1,3),(0,4)], [] #lights
                                           ),
        LightsOutState("START", 0, None, 7, 7,
                                            [(0, 0),(1, 0), (2, 0), (1, 1), (2, 2), (1, 3), (0, 4)], []  # lights
                                            )
    

    )





  
