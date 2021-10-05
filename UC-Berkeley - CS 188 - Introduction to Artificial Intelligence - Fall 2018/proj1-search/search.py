# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch_old(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.z

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    current_path = tuple([problem.getStartState()])
    current_priority = len(current_path)
    current_directions = []
    Stack = util.Stack()
    prior_state = ()
    prior_path = current_path
    for i in range(1000):
    # while True:        
        # current_path = Stack.pop()
        print(i,".1 Current (Path, Priority)", 
               (current_path, current_priority))
        if(problem.isGoalState(current_path[-1]) == True):
                # goal_directions = list(map(directions_dict.get, current_directions))
                print("GOAL STATE REACHED AT ", current_path[-1])
                print("Found path is: ", current_path)
                print("Found directions are: ", current_directions)
                return current_directions
            
        if(problem.getSuccessors(current_path[-1]) == []):
            print("No successors!")
            return False
        else:
            successors = problem.getSuccessors(current_path[-1])
            print(i, ".2 Current successors for", current_path[-1], "->", successors)
        
            for (successor_state, d, _) in successors:
                if successor_state not in current_path:
                    new_path = current_path + (successor_state,)
                    new_priority = len(new_path)
                    new_directions = current_directions + d
                    # print("-> Add ", new_path, new_priority)
                    if (current_path, current_priority, current_directions) not in Stack.list:
                        print('Stack push!')
                        Stack.push((new_path, new_priority, new_directions))
                    else:
                        print('Stack replace!')
                        index_pos = Stack.list.index((current_path, current_priority, current_directions))
                        Stack.list[index_pos] = (new_path, new_priority, new_directions)
                elif (len(successors) == 1):
                    index_pos = Stack.list.index((current_path, current_priority, current_directions))
                    print("##### DEADEND ##### ", index_pos)
                    del Stack.list[index_pos]
                elif (prior_path == current_path):
                    index_pos = Stack.list.index((current_path, current_priority, current_directions))
                    print("##### LOOP ##### ", index_pos)
                    print("DELETE stack element:", Stack.list[index_pos])
                    del Stack.list[index_pos]
                    print("DELETED stack element!!!")
                    break
            print(i, ".3 Current Stack: ", Stack.list)
    
            p_prior = 0
            st = Stack.list
            for index, (_, p, _) in enumerate(st):
                if p > p_prior:
                    chosen_path_index = index
                p_prior = p
            prior_path = current_path
            current_path = Stack.list[chosen_path_index][0]
            prior_state = current_path[-2]
            current_priority = len(current_path)
            current_directions = Stack.list[chosen_path_index][2]
            print(i,".4 Chosen Successor:", current_path[-1])
            
            print("### ",i," END ###")
            
    
    return current_directions 
        # util.raiseNotDefined()

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.
    """
    "*** YOUR CODE HERE ***"
    current_path = tuple([problem.getStartState()])
    current_priority = len(current_path)
    current_directions = []
    Stack = util.Stack()
    Stack.push((current_path, current_priority, current_directions))
    i=0
    # for i in range(1000):
    while True:        
        current_stack = Stack.pop()
        current_path = current_stack[0]
        current_priority = current_stack[1]
        current_directions = current_stack[2]
        
        # print(i,".1 Current (Path, Priority)", (current_path, current_priority))
        if(problem.isGoalState(current_path[-1]) == True):
                # goal_directions = list(map(directions_dict.get, current_directions))
                # print("GOAL STATE REACHED AT ", current_path[-1])
                # print("Found path is: ", current_path)
                # print("Found directions are: ", current_directions)
                return current_directions
        
        successors = problem.getSuccessors(current_path[-1])
        # print(i, ".2 Current successors for", current_path[-1], "->", successors)
        for (successor_state, d, _) in successors:
            if successor_state not in current_path:
                new_path = current_path + (successor_state,)
                new_priority = len(new_path)
                new_directions = current_directions + [d]
                # print("-> Add ", new_path, new_priority)
                Stack.push((new_path, new_priority, new_directions))

        # print(i, ".3 Current Stack: ", Stack.list)            
        # print("### ",i," END ###")
            
    
    return current_directions 


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"

    current_path = tuple([problem.getStartState()])
    
    current_priority = len(current_path)
    current_directions = []
    Queue = util.Queue()
    current_queue = (current_path, current_priority, current_directions)
    Queue.push(current_queue)
    # print(Queue.list)
    visited_states = set(current_path)

    # for i in range(1000):
    while not Queue.isEmpty():  
        
        current_queue = Queue.pop()
        current_path = current_queue[0]
        current_priority = current_queue[1]
        current_directions = current_queue[2]
        # print(current_queue)
        # print(i,".1 Current (Path, Priority)", 
        #        (current_path, current_priority))
        if(problem.isGoalState(current_path[-1]) == True):
            # goal_directions = list(map(directions_dict.get, current_directions))
            # print("GOAL STATE REACHED AT ", current_path[-1])
            # print("Found path is: ", current_path)
            # print("Found directions are: ", current_directions)
            return current_directions
            
        successors = problem.getSuccessors(current_path[-1])        
        for (successor_state, d, _) in successors:
            if successor_state not in current_path \
            and successor_state not in visited_states:
                direction = d
                new_path = current_path + (successor_state,)
                new_priority = len(new_path)
                new_directions = current_directions + [direction]
                # print("-> Add ", new_path, new_priority)
                Queue.push((new_path, new_priority, new_directions))
                visited_states.add(successor_state)

            # print(i, ".3 Current Stack: ", Queue.list)            
            # print("### ",i," END ###")
    return current_directions 

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"

    current_path = tuple([problem.getStartState()])
    current_priority = 0
    current_directions = []
    PriorityQueue = util.PriorityQueue()
    PriorityQueue.push((current_path,  current_directions, current_priority), current_priority)
    visited_states = set(current_path)
    solutions = []
    i = 0
    # for i in range(1000):
    while not PriorityQueue.isEmpty():         
        current_PQueue = PriorityQueue.pop()
        current_path = current_PQueue[0]
        current_directions = current_PQueue[1]
        current_priority = current_PQueue[2]
        # print("Current Path", current_path)

        
        # print(i,".1 Current (Path, Priority)", 
               # (current_path, current_priority))
        if(problem.isGoalState(current_path[-1]) == True):
            # goal_directions = list(map(directions_dict.get, current_directions))
            solutions.append((current_PQueue))
            # visited_states = set()
            # print("Solution found")
            # print("Full PQ: ", PriorityQueue.heap)
        else:
            successors = problem.getSuccessors(current_path[-1])           
            # print(i, ".2 Current successors for", current_path[-1], "->", successors)
            for (successor_state, d, p) in successors:
                # print("Successor, Priority:", successor_state, current_priority)
    
                if successor_state not in current_path \
                and successor_state not in visited_states:
                    direction = d
                    new_path = current_path + (successor_state,)
                    new_priority = current_priority + p
                    new_directions = current_directions + [direction]
                    # print("-> Add ", new_path, new_priority)
                    PriorityQueue.update((new_path,  new_directions, new_priority), new_priority)
                    if(problem.isGoalState(successor_state) == False):
                        visited_states.add(successor_state)
                # print("Full PQ: ", PriorityQueue.heap)
    # To-Do: Find the lowest cost path to goal state
    print("Solutions #",len(solutions))
    p_prior = 1000000000000000
    for index, (path, directions, p) in enumerate(solutions):
        if p < p_prior:
            pos = index
        p_prior = p
    # print("Solution ",solutions[pos])
    return solutions[pos][1]
        # print(i, ".3 Current Stack: ", PriorityQueue.heap)            
        # print("### ",i," END ###")
    # util.raiseNotDefined()
    


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"

    current_path = tuple([problem.getStartState()])
    current_priority = 0
    current_directions = []
    PriorityQueue = util.PriorityQueue()
    PriorityQueue.push((current_path,  current_directions, current_priority), current_priority)
    visited_states = set(current_path)
    solutions = []
    i = 0
    print("Start State: ", current_path)
    # for i in range(1000):
    while not PriorityQueue.isEmpty():        
        current_PQueue = PriorityQueue.pop()
        # print("Current PQ: ", current_stack)
        current_path = current_PQueue[0]
        current_directions = current_PQueue[1]
        current_priority = current_PQueue[2]
        # print(i,".1 Current (Path, Priority)",(current_path, current_priority))
        if(problem.isGoalState(current_path[-1]) == True):
            # goal_directions = list(map(directions_dict.get, current_directions))
            # solutions.append((current_PQueue))
            return current_directions
        else:
            successors = problem.getSuccessors(current_path[-1])
            # print(i, ".2 Current successors for", current_path[-1], "->", successors)
            for (successor_state, d, p) in successors:
                if successor_state not in current_path \
                and successor_state not in visited_states:
                    direction = d
                    new_path = current_path + (successor_state,)
                    new_priority = current_priority + p + heuristic(successor_state, problem)
                    new_directions = current_directions + [direction]
                    # print("-> Add ", new_path, new_priority)
                    PriorityQueue.update((new_path,  new_directions, new_priority), new_priority)
                    if not problem.isGoalState(successor_state):
                        visited_states.add(successor_state)
    # print("Solutions #",len(solutions))
    # p_prior = 1000000000000000
    # for index, (path, directions, p) in enumerate(solutions):
    #     if p < p_prior:
    #         pos = index
    #     p_prior = p
    # # print("Solution ",solutions[pos])
    # return solutions[pos][1]
        # print(i, ".3 Current Stack: ", PriorityQueue.heap)            
        # print("### ",i," END ###")
    # util.raiseNotDefined()
    # util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
