# multiAgents.py
# --------------
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

from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        currentFood = currentGameState.getFood()            # food currently in board
        currentCapsules = currentGameState.getCapsules()    # capsules currently in board

        if successorGameState.isWin():  # if we have won return +infinity
            from gtk.keysyms import infinity
            return infinity

        if successorGameState.isLose():  # if we have lost return -infinity
            from gtk.keysyms import infinity
            return -infinity

        totalScore = 0                           # initialize total score that we are going to return
        for ghost in newGhostStates:                # for each ghost...
            ghostDist = manhattanDistance(newPos, ghost.getPosition())  # ...calculate ghost's estimated distance
            if (ghostDist <= 1):                    # if it's next to us
                if (ghost.scaredTimer != 0):        # if it's scared
                    totalScore += 150              # that's very very good
                else:                               # if not
                    totalScore -= 15               # that's kind of bad

        for capsule in currentCapsules:             # for each capsule...
            capsuleDist = manhattanDistance(newPos, capsule)    # ...calculate capsule's estimated distance
            if (capsuleDist == 0):                  # if we are about to eat that capsule
                totalScore += 10                   # that's very good
            else:                                   # if not
                totalScore += 1.0 / capsuleDist    # the closer we are the better

        for x in xrange(currentFood.width):         # in the range where we can find food
            for y in xrange(currentFood.height):
                if (currentFood[x][y]):             # if there is food
                    distFromCurrentFood = manhattanDistance((x, y), newPos) # calculate food's estimated distance
                    if (distFromCurrentFood == 0):  # if we are about to eat that food
                        totalScore += 10           # that's vary good
                    else:                           # if not
                        totalScore += 0.1 / distFromCurrentFood**2  # the closer we are the better (but not as good as being close to a capsule)

        return totalScore

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """
    """*** Assistant functions for getAction ***"""
    # this member function checks whether we have reached a terminal state for minimax or not
    def is_terminal(self, gameState, depth):
        if gameState.isWin() or gameState.isLose() or depth == self.depth:  # if we have won, or we have lost, or we have searched as deep as we were requested...
            return True                                                     # ...then we have a terminal state
        return False

    # this member function sets in motion minimax search and oversees the decision for the move to be made
    def minimax_decision(self, gameState, agentNumber, depth):
        move = None                                 # initialy we have no "best" move

        from gtk.keysyms import infinity
        v = -infinity                                           # initialize best (MAX) utility
        legalActions = gameState.getLegalActions(agentNumber)   # list of legal actions for a certain agent
        for action in legalActions:                             # for each legal action...
            temp = v                                            # remember best (MAX) utility so far
            v = max(v, self.min_value(gameState.generateSuccessor(agentNumber, action), agentNumber+1, depth))  # call MIN for next agent (same depth)
            if v != temp:                                       # if best (MAX) utility has changed
                move = action                                   # new "best" move is the currently tested legal action

        return move

    # this member function calculated "max value" for minimax
    def max_value(self, gameState, agentNumber, depth):
        if self.is_terminal(gameState,depth):                   # if we have reached a terminal state
            return self.evaluationFunction(gameState)           # evaluate this terminal state and return the result

        from gtk.keysyms import infinity
        v = -infinity                                           # initialize best (MAX) utility
        legalActions = gameState.getLegalActions(agentNumber)   # list of legal actions for a certain agent
        for action in legalActions:
            v = max(v, self.min_value(gameState.generateSuccessor(agentNumber, action), agentNumber+1, depth))  # call MIN for the next agent (same depth)

        return v                                                # return calculated utility

    # this member function calculated "min value" for minimax
    def min_value(self, gameState, agentNumber, depth):
        if self.is_terminal(gameState, depth):                  # if we have reached a terminal state
            return self.evaluationFunction(gameState)           # evaluate this terminal state and return the result

        from gtk.keysyms import infinity
        v = infinity                                            # initialize best (MIN) utility
        legalActions = gameState.getLegalActions(agentNumber)   # list of legal actions for a certain agent
        if agentNumber == gameState.getNumAgents()-1:           # if we are in the last ghost agent
            for action in legalActions:
                v = min(v, self.max_value(gameState.generateSuccessor(agentNumber, action), 0, depth+1))  # call MAX for pacman agent and increase depth
        else:
            for action in legalActions:
                v = min(v, self.min_value(gameState.generateSuccessor(agentNumber, action), agentNumber+1, depth))  # call MIN for the next agent (same depth)

        return v                                                # return calculated utility

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        return self.minimax_decision(gameState, self.index, 0)  # call minimax algorithm to decide


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """
    """*** Assistant functions for getAction ***"""
    # this member function checks whether we have reached a terminal state for minimax or not
    def is_terminal(self, gameState, depth):
        if gameState.isWin() or gameState.isLose() or depth == self.depth:  # if we have won, or we have lost, or we have searched as deep as we were requested...
            return True                                                     # ...then we have a terminal state
        return False

    # this member function sets in motion alpha-beta search and oversees the decision for the move to be made
    def alphaBeta_decision(self, gameState, agentNumber, depth, a, b):
        move = None                                 # initialy we have no "best" move

        from gtk.keysyms import infinity
        v = -infinity                                           # initialize best (MAX) utility
        legalActions = gameState.getLegalActions(agentNumber)   # list of legal actions for a certain agent
        for action in legalActions:                             # for each legal action...
            temp = v                                            # remember best (MAX) utility so far
            v = max(v, self.min_value(gameState.generateSuccessor(agentNumber, action), agentNumber + 1, depth, a, b))  # call MIN for next agent (same depth)
            if v != temp:                                       # if best (MAX) utility has changed
                move = action                                   # new "best" move is the currently tested legal action
            if v > b:                                           # if we have exceeded "beta" value then STOP
                break
            a = max(a,v)                                        # update "alpha" value if needed

        return move

    # this member function calculated "max value" for alpha-beta
    def max_value(self, gameState, agentNumber, depth, a, b):
        if self.is_terminal(gameState, depth):                  # if we have reached a terminal state
            return self.evaluationFunction(gameState)           # evaluate this terminal state and return the result

        from gtk.keysyms import infinity
        v = -infinity                                           # initialize best (MAX) utility
        legalActions = gameState.getLegalActions(agentNumber)   # list of legal actions for a certain agent
        for action in legalActions:
            v = max(v, self.min_value(gameState.generateSuccessor(agentNumber, action), agentNumber + 1, depth, a, b))  # call MIN for the next agent (same depth)
            if v > b:                                           # if we have exceeded "beta" value then STOP
                return v
            a = max(a,v)                                        # update "alpha" value if needed

        return v                                                # return calculated utility

    # this member function calculated "min value" for alpha beta
    def min_value(self, gameState, agentNumber, depth, a, b):
        if self.is_terminal(gameState, depth):                  # if we have reached a terminal state
            return self.evaluationFunction(gameState)           # evaluate this terminal state and return the result

        from gtk.keysyms import infinity
        v = infinity                                            # initialize best (MIN) utility
        legalActions = gameState.getLegalActions(agentNumber)   # list of legal actions for a certain agent
        if agentNumber == gameState.getNumAgents() - 1:  # if we are in the last ghost agent
            for action in legalActions:
                v = min(v, self.max_value(gameState.generateSuccessor(agentNumber, action), 0, depth + 1, a, b))    # call MAX for pacman agent and increase depth
                if v < a:                                       # if we have exceeded "alpha" value
                    return v                                    # return current utility
                b = min(b,v)                                    # update "beta" value if needed
        else:
            for action in legalActions:
                v = min(v, self.min_value(gameState.generateSuccessor(agentNumber, action), agentNumber + 1, depth, a, b))  # call MIN for the next agent (same depth)
                if v < a:                                       # if we have exceeded "alpha" value
                    return v                                    # return current utility
                b = min(b,v)                                    # update "beta" value if needed

        return v                                                # return calculated utility

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        from gtk.keysyms import infinity
        a = -infinity                           # initialize "alpha" and "beta"
        b = infinity

        return self.alphaBeta_decision(gameState, self.index, 0, a, b)  # call alpha-beta algorithm to decide


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """
    """*** Assistant functions for getAction ***"""
    # this member function checks whether we have reached a terminal state for minimax or not
    def is_terminal(self, gameState, depth):
        if gameState.isWin() or gameState.isLose() or depth == self.depth:  # if we have won, or we have lost, or we have searched as deep as we were requested...
            return True                                                     # ...then we have a terminal state
        return False

    # this member function sets in motion expectimax search and oversees the decision for the move to be made
    def expectimax_decision(self, gameState, agentNumber, depth):
        move = None                                         # initialy we have no "best" move

        from gtk.keysyms import infinity
        v = -infinity                                       # initialize best (MAX) utility
        legalActions = gameState.getLegalActions(agentNumber)   # list of legal actions for a certain agent
        for action in legalActions:                             # for each legal action
            temp = v                                            # remember best (MAX) utility so far
            v = max(v, self.exp_value(gameState.generateSuccessor(agentNumber, action), agentNumber + 1, depth))    # call exp for the next agent (same depth)
            if v != temp:                                       # if best (MAX) utility has changed
                move = action                                   # new "best" move is the currently tested legal action

        return move

    # this member function calculated "max value" for expectimax
    def max_value(self, gameState, agentNumber, depth):
        if self.is_terminal(gameState, depth):                  # if we have reached a terminal state
            return self.evaluationFunction(gameState)           # evaluate this terminal state and return the result

        from gtk.keysyms import infinity
        v = -infinity                                           # initialize best (MAX) utility
        legalActions = gameState.getLegalActions(agentNumber)   # list of legal actions for a certain agent
        for action in legalActions:
            v = max(v, self.exp_value(gameState.generateSuccessor(agentNumber, action), agentNumber + 1, depth))    # call exp for the next agent (same depth)

        return v                                                # return calculated utility

    # this member function calculated "exp value" for expectimax
    def exp_value(self, gameState, agentNumber, depth):
        if self.is_terminal(gameState, depth):                  # if we have reached a terminal state
            return self.evaluationFunction(gameState)           # evaluate this terminal state and return the result

        v = 0                                                   # initialize best (EXP) utility
        legalActions = gameState.getLegalActions(agentNumber)   # list of legal actions for a certain agent
        p = 1.0 / float(len(legalActions))                      # successor's probability
        if agentNumber == gameState.getNumAgents() - 1:         # if we are in the last ghost agent
            for action in legalActions:
                v += p * self.max_value(gameState.generateSuccessor(agentNumber, action), 0, depth + 1)             # call MAX for the pacman agent (increase depth)
        else:
            for action in legalActions:
                v += p * self.exp_value(gameState.generateSuccessor(agentNumber, action), agentNumber + 1, depth)   # call exp for the next agent (same depth)

        return v                                                # return calculated utility

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        return self.expectimax_decision(gameState, self.index, 0)   # call expectimax algorithm to decide


def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
      In this evaluation function, I use the following criteria:
        - if we have just won or lost (an obvious way to start)
        - current score in the game
        - distance to the closest non-scared ghost
        - distance to the closest scared ghost
        - number of capsules left
        - number of foods left
        - distance to the closest food

        I formulated my evaluation in the basis that:
        - if we have just won or lost there is a pretty definite way to evaluate our game state
        - the current score is definitely a factor to take into serious consideration
        - having a non-scared ghost nearby is no good news
        - having a scared ghost nearby is really good for us
        - capsules are important to be eaten when passing near them
        - it's good for pacman to eat food as often as possible, so it's good to be close to food
        - we don't want many food left in board
        I weighted the above factors based on common sense and experimentation with a wide variety of weight-values
    """
    "*** YOUR CODE HERE ***"
    if currentGameState.isWin():                    # if we have won return +infinity
        from gtk.keysyms import infinity
        return float(infinity)

    if currentGameState.isLose():                   # if we have lost return -infinity
        from gtk.keysyms import infinity
        return -float(infinity)

    currentScore = currentGameState.getScore()      # get current game score

    currentGhostStates = currentGameState.getGhostStates()  # get current ghost states
    scaredGhosts = []                               # initialize a list for the scared ghosts...
    nonScaredGhosts = []                            # ...and a list for the non-scared ones
    for ghost in currentGhostStates:                # add ghosts to their respective lists (scared / non-scared)
        if ghost.scaredTimer != 0:
            scaredGhosts.append(ghost)
        else:
            nonScaredGhosts.append(ghost)

    if scaredGhosts:                                # if there are any scared ghosts
        # create a list with their expected distances from our pacman agent
        scaredGhostsDist = [util.manhattanDistance(currentGameState.getPacmanPosition(), ghost.getPosition()) for ghost in scaredGhosts]
        minScaredGhostDist = min(scaredGhostsDist)  # and find the minimum distance
    else:
        minScaredGhostDist = 0                      # if no scared ghosts then no minimum distance

    if nonScaredGhosts:                             # if there are any non-scared ghosts
        # create a list with their expected distances from our pacman agent
        nonScaredGhostsDist = [util.manhattanDistance(currentGameState.getPacmanPosition(), ghost.getPosition()) for ghost in nonScaredGhosts]
        minNonScaredGhostDist = min(nonScaredGhostsDist)     # and find the minimum distance
    else:
        from gtk.keysyms import infinity
        minNonScaredGhostDist = float(infinity)     # if no non-cared ghosts then infinite minimum distance

    currentCapsules = currentGameState.getCapsules()    # get current game capsules
    numberOfCapsulesLeft = len(currentCapsules)         # how many capsules have been left

    currentFoodList = currentGameState.getFood().asList()   # get current foods in the game as a List
    # create a list with their expected distances from our pacman agent
    foodDist = [manhattanDistance(currentGameState.getPacmanPosition(), food) for food in currentFoodList]
    minFoodDist = min(foodDist)                         # and find the minimum distance
    numberOfFoodsLeft = len(currentFoodList)            # hoe many foods have been left

    # I formulate my evaluation
    evaluation = currentScore\
                 - 1.5 * (1.0/minNonScaredGhostDist)\
                 - 2.5 * minScaredGhostDist \
                 - 20 * numberOfCapsulesLeft \
                 - 1.5 * minFoodDist \
                 - 4 * numberOfFoodsLeft

    return evaluation   # return evaluation

# Abbreviation
better = betterEvaluationFunction
