
from variables import *
import numpy as np
import math
import copy as cp

class Node:
    def __init__(self, x, y, heuristic, cost = NBROW * NBCOLUMN ):
        self.x = x
        self.y = y
        self.heuristic = heuristic
        self.cost = cost
        self.previousNode = []

    def testPreviousNode(self, n):
        if(n.previousNode != []):
            if(n.x - n.previousNode[0] == self.x - n.x and n.y - n.previousNode[1] == self.y - n.y):
                weight = 1
            else:
                weight = 50
                self.heuristic += 50
        else:
            weight = 1
        if(self.cost > n.cost + weight):
            self.cost = n.cost + 1
            self.previousNode = [n.x, n.y]


    def __lt__(self, other):
        if(self.heuristic < other.heuristic):
            return True
        elif(self.heuristic == other.heuristic):
            return self.cost < other.cost
        else:
            return False

    def __gt__(self, other):
        if (self.heuristic > other.heuristic):
            return True
        elif (self.heuristic == other.heuristic):
            return self.cost > other.cost
        else:
            return False

    def __str__(self):
        return "["+str(self.x)+", "+str(self.y)+", "+str(self.heuristic) + "]"

    def __repr__(self):
        return "[" + str(self.x) + ", " + str(self.y) + ", " + str(self.heuristic) + "]"

class NodeMax:
    def __init__(self, x, y, heuristic, cost=NBROW * NBCOLUMN):
        self.x = x
        self.y = y
        self.heuristic = heuristic
        self.cost = cost
        self.previousNode = []

    def testPreviousNode(self, n):
        if (self.cost < n.cost + 1):
            self.cost = n.cost + 1
            self.previousNode = [n.x, n.y]

    def __lt__(self, other):
        if (self.heuristic > other.heuristic):
            return True
        elif (self.heuristic == other.heuristic):
            return self.cost > other.cost
        else:
            return False

    def __gt__(self, other):
        if (self.heuristic < other.heuristic):
            return True
        elif (self.heuristic == other.heuristic):
            return self.cost > other.cost
        else:
            return False
    # def __eq__(self, other):
    #     return self.y == other.y and self.x == other.x

    def __str__(self):
        return "["+str(self.x)+", "+str(self.y)+", "+str(self.heuristic) + "]"

    def __repr__(self):
        return "[" + str(self.x) + ", " + str(self.y) + ", " + str(self.heuristic) + "]"

#Function which sort the nodes into a list
def removeIdenticalNodes(listNode = []):
    newList = []
    strList = []
    for i in listNode:
        if (str(i) not in strList):
            strList.append(str(i))
            newList.append(cp.copy(i))
    return newList

def removeNodesAlreadyVisited(standByList = [], visitedList = []):
    newList = []
    visitedStrList = []
    for i in visitedList:
        visitedStrList.append(str(i))
    for i in standByList:
        if(str(i) not in visitedStrList):
            newList.append(cp.copy(i))
    return newList


# function that initializes the graph
def graphInitialization(board, snake, food):
    graph = np.full((NBROW*NBCOLUMN, NBROW*NBCOLUMN), -1)
    for i in range(NBROW*NBCOLUMN):
        for j in range(NBROW*NBCOLUMN):
            if((abs(i-j) == 1 or abs(i-j) == NBCOLUMN) and not(i%NBCOLUMN == 0 and j%NBCOLUMN == NBCOLUMN - 1) and not(j%NBCOLUMN == 0 and i%NBCOLUMN == NBCOLUMN - 1)):
                if((board[math.floor(i/NBCOLUMN)][i%NBCOLUMN] == 0 or board[math.floor(i/NBCOLUMN)][i%NBCOLUMN] == 2) and (board[math.floor(j/NBCOLUMN)][j%NBCOLUMN] == 0 or board[math.floor(j/NBCOLUMN)][j%NBCOLUMN] == 2)):
                    graph[i][j] = 1
    return graph

# Function which return the euclidean distance between two points ([X, Y])
def euclideanDistance(x, y):
    return math.sqrt((x[0] - y[0])**2 + (x[1] - y[1])**2)

# Function which list all the nodes
def listNodes(board, start, end):
    listNodes = []
    for i in range(NBROW):
        for j in range(NBCOLUMN):
            listNodes.append(Node(i, j, euclideanDistance([i, j], start) + euclideanDistance([i, j], end)))
    return listNodes

def findNodeInList(x, y, list = []):
    for i in list:
        if(i.x == x and i.y == y):
            return cp.copy(i)
    else:
        return []


# Function which return the list of neighboring nodes of the current node
def findNeighbors(graph, n: Node, start, end):
    neighbors = []
    for j in range(NBCOLUMN*NBROW):
        if(graph[n.x * NBCOLUMN + n.y][j] == 1):
            neighbors.append(Node(math.floor(j/NBCOLUMN), j%NBCOLUMN, euclideanDistance([math.floor(j/NBCOLUMN), j%NBCOLUMN], start) + euclideanDistance([math.floor(j/NBCOLUMN), j%NBCOLUMN], end)))
    return neighbors

def findNeighborsMax(graph, n: NodeMax, start, end):
    neighbors = []
    for j in range(NBCOLUMN*NBROW):
        if(graph[n.x * NBCOLUMN + n.y][j] == 1):
            neighbors.append(NodeMax(math.floor(j/NBCOLUMN), j%NBCOLUMN, euclideanDistance([math.floor(j/NBCOLUMN), j%NBCOLUMN], start) + euclideanDistance([math.floor(j/NBCOLUMN), j%NBCOLUMN], end)))
    return neighbors


def pathfinding(graph, start, end):
    visitedNodes = []
    standByNodes = [Node(start[0], start[1], 0, 0)]
    while(len(standByNodes) != 0):

        actualNode = standByNodes.pop(0)
        visitedNodes.append(cp.copy(actualNode))
        if(actualNode.x == end[0] and actualNode.y == end[1]):
            path = []
            path.append([cp.copy(actualNode.x), cp.copy(actualNode.y)])
            actualNode = findNodeInList(actualNode.previousNode[0], actualNode.previousNode[1], visitedNodes)
            while(actualNode.previousNode != []):
                path.append([cp.copy(actualNode.x), cp.copy(actualNode.y)])
                actualNode = findNodeInList(actualNode.previousNode[0], actualNode.previousNode[1], visitedNodes)
                if(actualNode == []):
                    return False, []

            return True, cp.copy(path)
        neighbors = findNeighbors(graph, actualNode, start, end)
        for n in neighbors:
            n.testPreviousNode(actualNode)
            standByNodes.append(cp.copy(n))
        standByNodes.sort()
        standByNodes = removeIdenticalNodes(standByNodes)
        visitedNodes = removeIdenticalNodes(visitedNodes)
        standByNodes = removeNodesAlreadyVisited(standByNodes, visitedNodes)
    return False, []


def pathfinding2(graph, start, end):
    visitedNodes = []
    standByNodes = [NodeMax(start[0], start[1], 0, 0)]
    while(len(standByNodes) != 0):
        actualNode = standByNodes.pop(0)
        visitedNodes.append(cp.copy(actualNode))
        neighbors = findNeighborsMax(graph, actualNode, start, end)
        for n in neighbors:
            n.testPreviousNode(actualNode)
            standByNodes.append(cp.copy(n))
        standByNodes.sort()
        standByNodes = removeIdenticalNodes(standByNodes)
        visitedNodes = removeIdenticalNodes(visitedNodes)
        standByNodes = removeNodesAlreadyVisited(standByNodes, visitedNodes)
    actualNode = findNodeInList(end[0], end[1], visitedNodes)
    path = []
    path.append([cp.copy(actualNode.x), cp.copy(actualNode.y)])
    actualNode = findNodeInList(actualNode.previousNode[0], actualNode.previousNode[1], visitedNodes)
    if (actualNode == []):
        return False, []
    while (actualNode.previousNode != []):
        path.append([cp.copy(actualNode.x), cp.copy(actualNode.y)])
        actualNode = findNodeInList(actualNode.previousNode[0], actualNode.previousNode[1], visitedNodes)
        if (actualNode == []):
            return False, []
    path.append([cp.copy(actualNode.x), cp.copy(actualNode.y)])
    print(path)
    return True, cp.copy(path)




#Function which compare 2 nodes (depreciated)
def compare2Node( n1: Node, n2: Node):
    if(n1.heuristic < n2.heuristic):
        return 1
    elif(n1.heuristic == n2.heuristic):
        return 0
    else:
        return -1