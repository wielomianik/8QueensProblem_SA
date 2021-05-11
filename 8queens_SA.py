import numpy as np
import time


def goalFunction(queens, size, queensAmmount):

    s = 0                            #sum
    for i in range(size):            #columns
        for j in range(size):        #rows

            if queens[i][j] == 0:
                continue
            else:

                for k in range(size):
                    s += queens[i][k] + queens[k][j]
                s -= 2
                k = 1

                while i - k >= 0 and j - k >= 0:
                    s += queens[i - k][j - k]
                    k += 1
                k = 1

                while i + k <= size - 1 and j + k <= size - 1:
                    s += queens[i + k][j + k]
                    k += 1
                k = 1

                while i - k >= 0 and j + k <= size - 1:
                    s += queens[i - k][j + k]
                    k += 1
                k = 1

                while i + k <= size - 1 and j - k >= 0:
                    s += queens[i + k][j - k]
                    k += 1

    return s / queensAmmount


def randomX(queensAmmount, size):   #Generating matrix with random queens arrangement

    indexes = [i for i in range(size ** 2)]
    queens = [0 for i in range(size ** 2)]

    unique_indexes = []
    while len(unique_indexes) != queensAmmount:

        drawn_number = np.random.choice(indexes)
        if drawn_number not in unique_indexes:
            unique_indexes.append(drawn_number)
    
    for element in unique_indexes:
        queens[element] = 1

    queens = np.array(queens)
    queens = list(queens.reshape(size, size))
    queens = [list(i) for i in queens]

    return queens


def chooseRandomX(queens):  #I choose a random solution located near the initial one.
    
    '''print("\nInitial solution X: ")
    for row in queens:
        print(row)'''
    
    queens_size = len(queens)
    for i in range(queens_size - 1):
        for j in range(queens_size - 1):

            if queens[i][j] == 1:

                if queens[i][j + 1] == 0:

                    queens[i][j + 1] = 1
                    queens[i][j] = 0
                    break

                if queens[i][j - 1] == 0:

                    queens[i][j - 1] = 1
                    queens[i][j] = 0
                    break
                
                if queens[i + 1][j] == 0:
                    
                    queens[i + 1][j] = 1
                    queens[i][j] = 0
                    break

                if queens[i + 1][j - 1] == 0:

                    queens[i + 1][j - 1] = 1
                    queens[i][j] = 0
                    break
                    
                if queens[i + 1][j + 1] == 0:

                    queens[i + 1][j + 1] = 1
                    queens[i][j] = 0
                    break
                    
                if queens[i - 1][j] == 0:

                    queens[i - 1][j] = 1
                    queens[i][j] = 0
                    break
                    
                if queens[i][j + 1] == 0:

                    queens[i][j + 1] = 1
                    queens[i][j] = 0
                    break
                    
                if queens[i][j + 1] == 0:

                    queens[i][j + 1] = 1
                    queens[i][j] = 0
                    break
        
        else:
            continue
        break
                    

    '''print("\nRandom solution X' located nearby X: ")
    for row in queens:
        print(row)'''

    return queens


def boltzmannFunction(x, xPrim, temperature):
    return np.e ** ((x - xPrim)/temperature)


def acceptingSolution(probability):
    check = np.random.uniform(0,1)
    if check < probability:
        return True


def findMin(solutions):
    minimum = []
    for element in solutions:
        minimum.append(element[0])
    return min(minimum)

            
start_time = time.time()

queensOnBoard = 8                       #Variables needed for the algorithm
boardSize = 8
T = 4000
triesNumber = 8
epochsNumber = 20000
coefficient = 0.99
solutions = []


for epoka in range(epochsNumber):       #Execution of simulated annealing algorithm
    for proba in range(triesNumber):

        queens = randomX(queensOnBoard, boardSize)
        queensPrim = chooseRandomX(queens)
        avg_het = goalFunction(queens, boardSize, queensOnBoard)
        avg_het_prim = goalFunction(queensPrim, boardSize, queensOnBoard)

        if avg_het_prim < avg_het:
            solutions.append([avg_het_prim, queensPrim])
        else:
            prob = boltzmannFunction(avg_het, avg_het_prim, T)
            check = acceptingSolution(prob)

            if check:
                solutions.append([avg_het_prim, queensPrim])
            else:
                solutions.append([avg_het, queens])

    T *= coefficient

minimum = findMin(solutions)
for element in solutions:
    if element[0] == minimum:
        print("\nAverage: ", element[0])
        print("Expected queen placement:")
        for row in element[1]:
            print(row)

print("\n--- %s seconds ---" % (time.time() - start_time))