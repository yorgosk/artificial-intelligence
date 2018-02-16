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


def notInFrontier(item, frontier):
    """ Function that can find if an item is inside a given frontier. Because of the structural differences between
        the Stack, Queue (list member) and the PriorityQueue, PriorityQueueWithFunction (heap member), we need an "if"
        condition, to properly check if a given item exists inside a given frontier. """
    if isinstance(frontier, util.Stack) or isinstance(frontier, util.Queue):
        for i in frontier.list:
            if i is item:
                return False    # it DOES exist inside the frontier
    elif isinstance(frontier, util.PriorityQueue) or isinstance(frontier, util.PriorityQueueWithFunction):
        for i in frontier.heap:
            if i is item:
                return False    # it DOES exist inside the frontier

    return True # it does NOT exist inside the frontier

def graphSearch(problem, frontier):
    """ A Generic Graph-Search function """
    start = problem.getStartState() # get problem's start state
    # in the frontier I push a (state, [moves to get there]) tuple
    if isinstance(frontier, util.Stack) or isinstance(frontier, util.Queue) or isinstance(frontier, util.PriorityQueueWithFunction):
        frontier.push((start,[])) # initialize the frontier using the initial state of problem
    else:
        frontier.push((start,[]),0)
    explored = set([])  # initialize the explored set to be empty
    while not frontier.isEmpty():
        leafNode, moves = frontier.pop()  # choose a leaf node and remove it from the frontier
        if problem.isGoalState(leafNode):  # if the node contains a goal state...
            return moves  # ...return the moves (the corresponding solution)
        if leafNode not in explored:
            explored.add(leafNode)  # add the state of the node to the explored set
            successors = problem.getSuccessors(leafNode)  # expand the chosen node
            for succ in successors:
                # if the successor's state is not in the frontier or the explored set
                if succ[0] not in explored:
                    if isinstance(frontier, util.Stack) or isinstance(frontier, util.Queue) or isinstance(frontier, util.PriorityQueueWithFunction):
                        if notInFrontier((succ[0], succ[1]), frontier):
                            frontier.push((succ[0], moves+[succ[1]]))
                    else:
                        frontier.update((succ[0], moves + [succ[1]]), problem.getCostOfActions(moves + [succ[1]]))

    print("Failure!")
    return []   # if the frontier is empty then return "failure", which is an empty list of moves (no solution)

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    frontier = util.Stack()     # our frontier is a Stack
    return graphSearch(problem, frontier)   # use the above Generic Graph-Search function

    util.raiseNotDefined()


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    frontier = util.Queue()     # our frontier is a Queue
    return graphSearch(problem, frontier)      # use the above Generic Graph-Search function

    util.raiseNotDefined()


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    frontier = util.PriorityQueue()     # our frontier is a Priority Queue
    return graphSearch(problem, frontier)      # use the above Generic Graph-Search function

    util.raiseNotDefined()


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    # to define each item's priority I use a function which summarizes the result of the given heuristic, with the item's cost of actions
    f = lambda item: heuristic(item[0], problem) + problem.getCostOfActions(item[1])
    frontier = util.PriorityQueueWithFunction(f)    # our frontier is a Priority Queue with a function to define each item's priority
    return graphSearch(problem, frontier)      # use the above Generic Graph-Search function

    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
