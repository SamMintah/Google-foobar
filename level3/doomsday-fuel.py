# Doomsday Fuel
# =============

# Making fuel for the LAMBCHOP's reactor core is a tricky process because of the exotic matter involved. It starts as raw ore, then during processing, begins randomly changing between forms, eventually reaching a stable form. There may be multiple stable forms that a sample could ultimately reach, not all of which are useful as fuel. 

# Commander Lambda has tasked you to help the scientists increase fuel creation efficiency by predicting the end state of a given ore sample. You have carefully studied the different structures that the ore can take and which transitions it undergoes. It appears that, while random, the probability of each structure transforming is fixed. That is, each time the ore is in 1 state, it has the same probabilities of entering the next state (which might be the same state).  You have recorded the observed transitions in a matrix. The others in the lab have hypothesized more exotic forms that the ore can become, but you haven't seen all of them.

# Write a function solution(m) that takes an array of array of nonnegative ints representing how many times that state has gone to the next state and return an array of ints for each terminal state giving the exact probabilities of each terminal state, represented as the numerator for each state, then the denominator for all of them at the end and in simplest form. The matrix is at most 10 by 10. It is guaranteed that no matter which state the ore is in, there is a path from that state to a terminal state. That is, the processing will always eventually end in a stable state. The ore starts in state 0. The denominator will fit within a signed 32-bit integer during the calculation, as long as the fraction is simplified regularly. 

# For example, consider the matrix m:
# [
#   [0,1,0,0,0,1],  # s0, the initial state, goes to s1 and s5 with equal probability
#   [4,0,0,3,2,0],  # s1 can become s0, s3, or s4, but with different probabilities
#   [0,0,0,0,0,0],  # s2 is terminal, and unreachable (never observed in practice)
#   [0,0,0,0,0,0],  # s3 is terminal
#   [0,0,0,0,0,0],  # s4 is terminal
#   [0,0,0,0,0,0],  # s5 is terminal
# ]
# So, we can consider different paths to terminal states, such as:
# s0 -> s1 -> s3
# s0 -> s1 -> s0 -> s1 -> s0 -> s1 -> s4
# s0 -> s1 -> s0 -> s5
# Tracing the probabilities of each, we find that
# s2 has probability 0
# s3 has probability 3/14
# s4 has probability 1/7
# s5 has probability 9/14
# So, putting that together, and making a common denominator, gives an answer in the form of
# [s2.numerator, s3.numerator, s4.numerator, s5.numerator, denominator] which is
# [0, 3, 2, 9, 14].

# Languages
# =========

# To provide a Java solution, edit Solution.java
# To provide a Python solution, edit solution.py

# Test cases
# ==========
# Your code should pass the following test cases.
# Note that it may also be run against hidden test cases not shown here.

# -- Java cases --
# Input:
# Solution.solution({{0, 2, 1, 0, 0}, {0, 0, 0, 3, 4}, {0, 0, 0, 0, 0}, {0, 0, 0, 0,0}, {0, 0, 0, 0, 0}})
# Output:
#     [7, 6, 8, 21]

# Input:
# Solution.solution({{0, 1, 0, 0, 0, 1}, {4, 0, 0, 3, 2, 0}, {0, 0, 0, 0, 0, 0}, {0, 0, 0, 0, 0, 0}, {0, 0, 0, 0, 0, 0}, {0, 0, 0, 0, 0, 0}})
# Output:
#     [0, 3, 2, 9, 14]

# -- Python cases --
# Input:
# solution.solution([[0, 2, 1, 0, 0], [0, 0, 0, 3, 4], [0, 0, 0, 0, 0], [0, 0, 0, 0,0], [0, 0, 0, 0, 0]])
# Output:
#     [7, 6, 8, 21]

# Input:
# solution.solution([[0, 1, 0, 0, 0, 1], [4, 0, 0, 3, 2, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]])
# Output:
#     [0, 3, 2, 9, 14]

# solution

def solution(m):
    
    #case when 0 is terminal state
    if(not any(m[0])):
        return [1] + ([0] * (len(m)-1)) + [1]
   
    #diagonal values arent relevant 
    cleanDiagonal(m)
    
    #useful structures
    probabilitiesMatrix = generateProbabilityMatrix(m)
    terminals, notTerminals = getTerminalsAndNotTerminals(m)
    
    #we will remove one by one all of the not-terminals nodes 
    for i in notTerminals:
        absorbNode(probabilitiesMatrix, i)
    
    #now we can take the solution
    terminalsProbabilities = list(map(lambda x: probabilitiesMatrix[0][x], terminals))
    commonDenominator = getCommonDenominator(list(map(lambda x: x[1], terminalsProbabilities)))
    unsimplifiedNumerators = list(map(lambda x: fracUnsimplify(x, commonDenominator)[0], terminalsProbabilities))
    
    return unsimplifiedNumerators + [commonDenominator]
    
   
def cleanDiagonal(m):
    for i in range(len(m)):
        m[i][i] = 0


def generateProbabilityMatrix(m):
    result = []
    for i in range(len(m)):
        result.append([None] * len(m))
        for j in range(len(m)):
            result[i][j] = fracDiv([m[i][j],1], [sum(m[i]),1])
    return result
            
            
def getTerminalsAndNotTerminals(m):
    terminals = []
    notTerminals = list(range(1, len(m)))
    for i in range(len(m)):
        if(not any(m[i])):
            terminals.append(i)
            notTerminals.remove(i)
    return terminals, notTerminals
    
    
def absorbNode(pm, node):
    for i in range(len(pm)):
        for j in range(len(pm)):
            if(i != node and j != node):
                pm[i][j] = fracAdd(pm[i][j], fracMult(pm[i][node], pm[node][j]))
                
    for k in range(len(pm)):
        pm[k][node] = [0, 1]
        pm[node][k] = [0, 1]
        
    for i in range(len(pm)):
        if(pm[i][i] != [0, 1]):
            multiplier = solveGeometricSeries(pm[i][i])
            for j in range(len(pm)):
                if(i == j):
                    pm[i][j] = [0, 1]
                else:
                    pm[i][j] = fracMult(pm[i][j] ,multiplier)
                    
                    
#we will work with fractions, so lets create some functions 

def fracSimplify(a):
    if(a[0] == 0):
        a[1] = 1
    i=2
    while (i <= max(a)):
        if(a[0]%i == 0 and a[1]%i == 0):
            a[0] //= i
            a[1] //= i
        else:
            i += 1
    return a
    
def fracAdd(a, b):
    return fracSimplify([a[0]*b[1] + b[0]*a[1] , a[1]*b[1]])
    
def fracSubs(a, b):
    return fracSimplify([a[0]*b[1] - b[0]*a[1] , a[1]*b[1]])
    
def fracMult(a, b):
    return fracSimplify([a[0]*b[0], a[1]*b[1]])

def fracDiv(a, b):
    if(a[1] == 0 or b[1] == 0):
        return [0, 1]
    return fracSimplify([a[0]*b[1], a[1]*b[0]])

def solveGeometricSeries(r):
    if(r == [1,1]):
        return [1,1]
    n = [1,1]
    d = fracSubs([1,1], r)
    return fracDiv(n, d)
    
def getCommonDenominator(l):
    greater = min(l)
    while(not all(list(map(lambda x: greater % x == 0, l)))):
        greater += 1
    return greater

def fracUnsimplify(a, d):
    return [int(a[0]*(d/a[1])), d]