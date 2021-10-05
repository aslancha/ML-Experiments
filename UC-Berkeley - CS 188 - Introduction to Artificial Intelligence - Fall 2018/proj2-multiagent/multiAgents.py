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
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
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
        
        newFoodPositions = newFood.asList()
        # print(newFoodPositions)
        newGostPositions = [g.getPosition() for g in newGhostStates]
        # print(newGostPositions)
        # print(newPos)
        # print(newFood.width, newFood.height)
        # print("Scared Time:",newScaredTimes)
        widthHeight = newFood.width + newFood.height
        
        minGhostScore = widthHeight
        foodScore = [0]
        ghostScore = [0]
        for xyF in newFoodPositions:
            foodScore.append(widthHeight-(manhattanDistance(xyF, newPos)))
        
        # if ghost are not scared        
        if max(newScaredTimes) == 0:
            for xyG in (newGostPositions):
                if manhattanDistance(xyG, newPos) < 3:
                    return float("-inf")
        else:
            for i, xyG in enumerate(newGostPositions):
                ghostScore.append((newScaredTimes[i])*(widthHeight - manhattanDistance(xyG, newPos)))
        
        successorFood = 0
        if (currentGameState.getNumFood() > successorGameState.getNumFood()):
            successorFood = 300
        
        score = max(foodScore) + max(ghostScore) \
                + successorGameState.getScore() + successorFood
        # print("Score:", score)
        return score

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
        self.numAgents = 0


class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """
    
    def getValue(self, gameState, agentIndex, currentDepth):
        if currentDepth == self.depth or gameState.isWin() or gameState.isLose():
            # print("\t"*currentDepth + "XXX END STATE XXX")
            return self.evaluationFunction(gameState)
        if agentIndex == 0:
            return self.maxValue(gameState, agentIndex, currentDepth)
        else:
            return self.minValue(gameState, agentIndex, currentDepth)
        return []
    
    def minValue(self, gameState, agentIndex, currentDepth):
        v = float("INF")
        # print("\t"*currentDepth + "DOWN MIN NODE -> ", agentIndex, " LAYER: ", currentDepth) 
        actions = gameState.getLegalActions(agentIndex)
        # print("\t"*currentDepth + "  All Actions: ", actions)
        for action in actions:
            # print("\t"*currentDepth + "-> Action: ", action)
            successorState = gameState.generateSuccessor(agentIndex, action)
            if agentIndex == self.numAgents - 1:
                v = min(v, self.getValue(successorState, 0, currentDepth + 1))
            else:  
                # print()
                v = min(v, self.getValue(successorState, agentIndex + 1, currentDepth))
                # print("\t"*currentDepth + "BACKWARD TO MIN NODE -> ", agentIndex, "LAYER:", currentDepth)
                          
                
        # print("\t"*currentDepth + "MINIMUM Value: ", v)
        return v
    
    def maxValue(self, gameState, agentIndex, currentDepth):
        # print("\t"*currentDepth + "DOWN MAX NODE TO LAYER: ", currentDepth) 
        vMax = float("-INF")
        aMax = Directions.STOP
        actions = gameState.getLegalActions(agentIndex)
        # print("\t"*currentDepth + "  All Actions: ", actions)
        for action in actions:
            # print("\t"*currentDepth + "-> Action: ", action)
            successorState = gameState.generateSuccessor(agentIndex, action)
            v = self.getValue(successorState, 1, currentDepth)
            # print("\t"*currentDepth + "BACKWARD TO MAX NODE LAYER: ", currentDepth)
            if (v > vMax ):
                vMax = v
                aMax = action
        if currentDepth == 0:   
            # print("\t"*currentDepth + "TAKEN ACTION: ", aMax, " VALUE:", vMax)            
            return aMax
        else: 
            # print("\t"*currentDepth + "MAX NODE LAYER-> ", currentDepth, " Value: ", v)
            return vMax
            
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

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        self.numAgents = gameState.getNumAgents()
        # print()
        # print("...STARTING...")
        # print("Num Agents: ", self.numAgents)
        # print("Max Depth: ", self.depth)
        agentIndex = 0
        currentDepth = 0
        return self.getValue(gameState, agentIndex, currentDepth)
              
                        
                        
        
    # util.raiseNotDefined()

                    

            
class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        self.numAgents = gameState.getNumAgents()
        # print()
        # print("...STARTING...")
        # print("Num Agents: ", self.numAgents)
        # print("Max Depth: ", self.depth)
        agentIndex = 0
        currentDepth = 0
        alpha = float("-INF")
        beta = float("INF")
        return self.getValue(gameState, agentIndex, currentDepth, alpha, beta)
        
        # util.raiseNotDefined()
        
    def getValue(self, gameState, agentIndex, currentDepth, alpha, beta):
        if currentDepth == self.depth or gameState.isWin() or gameState.isLose():
            # print("\t"*currentDepth + "XXX END STATE XXX")
            return self.evaluationFunction(gameState)
        if agentIndex == 0:
            return self.maxValue(gameState, agentIndex, currentDepth, alpha, beta)
        else:
            return self.minValue(gameState, agentIndex, currentDepth, alpha, beta)
        return []
    
    
    def maxValue(self, gameState, agentIndex, currentDepth, alpha, beta):
        # print("\t"*currentDepth + "DOWN MAX NODE TO LAYER: ", currentDepth) 
        actionMax = Directions.STOP
        actions = gameState.getLegalActions(agentIndex)
        # print("\t"*currentDepth + "  All Actions: ", actions)
        for action in actions:
            # print("\t"*currentDepth + "-> Action: ", action)
            successorState = gameState.generateSuccessor(agentIndex, action)
            v = self.getValue(successorState, 1, currentDepth, alpha, beta)
            # print("\t"*currentDepth + "BACKWARD TO MAX NODE LAYER: ", currentDepth)
            if (v > alpha ):
                alpha = v
                actionMax = action
            if (v >= beta):
                return v
            
        if currentDepth == 0:   
            # print("\t"*currentDepth + "TAKEN ACTION: ", actionMax, " VALUE:", vMax)            
            return actionMax
        else: 
            # print("\t"*currentDepth + "MAX NODE LAYER-> ", currentDepth, " Value: ", v)
            return alpha
        
    def minValue(self, gameState, agentIndex, currentDepth, alpha, beta):
        v = float("INF")
        # print("\t"*currentDepth + "DOWN MIN NODE -> ", agentIndex, " LAYER: ", currentDepth) 
        actions = gameState.getLegalActions(agentIndex)
        # print("\t"*currentDepth + "  All Actions: ", actions)
        for action in actions:
            # print("\t"*currentDepth + "-> Action: ", action)
            successorState = gameState.generateSuccessor(agentIndex, action)
            if agentIndex == self.numAgents - 1:
                v = min(v, self.getValue(successorState, 0, currentDepth + 1, alpha, beta))
            else:  
                # print()
                v = min(v, self.getValue(successorState, agentIndex + 1, currentDepth, alpha, beta))
                # print("\t"*currentDepth + "BACKWARD TO MIN NODE -> ", agentIndex, "LAYER:", currentDepth)
            if v <= alpha:
                return v
            beta = min(v, beta)
        # print("\t"*currentDepth + "MINIMUM Value: ", v)
        return v
    
class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """
    def getValue(self, gameState, agentIndex, currentDepth):
        if currentDepth == self.depth or gameState.isWin() or gameState.isLose():
            # print("\t"*currentDepth + "XXX END STATE XXX")
            return self.evaluationFunction(gameState)
        if agentIndex == 0:
            return self.maxValue(gameState, agentIndex, currentDepth)
        else:
            return self.expValue(gameState, agentIndex, currentDepth)
        # return []
    
    def expValue(self, gameState, agentIndex, currentDepth):
        v = 0
        # print("\t"*currentDepth + "DOWN MIN NODE -> ", agentIndex, " LAYER: ", currentDepth) 
        actions = gameState.getLegalActions(agentIndex)
        # print("\t"*currentDepth + "  All Actions: ", actions)
        for action in actions:
            # print("\t"*currentDepth + "-> Action: ", action)
            successorState = gameState.generateSuccessor(agentIndex, action)
            p = 1/len(actions)
            if agentIndex == self.numAgents - 1:
                v += p * self.getValue(successorState, 0, currentDepth + 1)
            else:  
                # print()
                v += p * self.getValue(successorState, agentIndex + 1, currentDepth)
                # print("\t"*currentDepth + "BACKWARD TO MIN NODE -> ", agentIndex, "LAYER:", currentDepth)
                          
                
        # print("\t"*currentDepth + "MINIMUM Value: ", v)
        return v
    
    def maxValue(self, gameState, agentIndex, currentDepth):
        # print("\t"*currentDepth + "DOWN MAX NODE TO LAYER: ", currentDepth) 
        vMax = float("-INF")
        aMax = Directions.STOP
        actions = gameState.getLegalActions(agentIndex)
        # print("\t"*currentDepth + "  All Actions: ", actions)
        for action in actions:
            # print("\t"*currentDepth + "-> Action: ", action)
            successorState = gameState.generateSuccessor(agentIndex, action)
            v = self.getValue(successorState, 1, currentDepth)
            # print("\t"*currentDepth + "BACKWARD TO MAX NODE LAYER: ", currentDepth)
            if (v > vMax ):
                vMax = v
                aMax = action
        if currentDepth == 0:   
            # print("\t"*currentDepth + "TAKEN ACTION: ", aMax, " VALUE:", vMax)            
            return aMax
        else: 
            # print("\t"*currentDepth + "MAX NODE LAYER-> ", currentDepth, " Value: ", v)
            return vMax
    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        self.numAgents = gameState.getNumAgents()
        # print()
        # print("...STARTING...")
        # print("Num Agents: ", self.numAgents)
        # print("Max Depth: ", self.depth)
        agentIndex = 0
        currentDepth = 0
        return self.getValue(gameState, agentIndex, currentDepth)
        # util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
