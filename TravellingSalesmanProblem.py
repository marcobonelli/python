import math
import copy
import random
import operator
import timeit

def readFile(file):
    source = open(file, 'r')
    lines = source.readlines()
    
    separate = []
    for i in lines:
        separate += [i.split(' ')]
    separate.remove(['EOF\n'])
    
    database = {}
    for i in range(len(separate)):
        database[int(separate[i][0])] = (float(separate[i][1]), float(separate[i][2]))
    return database

def vectorDistance(source, index, att):
    distance = {}

    if att:
        for i in range(1, len(source) + 1):
            x_distance = abs(source[index][0] - source[i][0])
            y_distance = abs(source[index][1] - source[i][1])
            distance[i] = math.sqrt((math.pow(x_distance, 2) + math.pow(y_distance, 2)) / 10)
    else:
        for i in range(1, len(source) + 1):
            x_distance = abs(source[index][0] - source[i][0])
            y_distance = abs(source[index][1] - source[i][1])
            distance[i] = math.sqrt(math.pow(x_distance, 2) + math.pow(y_distance, 2))

    return distance

def vertexDistance(source, origin, destination, att):
    if att:
        x_distance = abs(source[origin][0] - source[destination][0])
        y_distance = abs(source[origin][1] - source[destination][1])
        distance = math.sqrt((math.pow(x_distance, 2) + math.pow(y_distance, 2)) / 10)
    else:
        x_distance = abs(source[origin][0] - source[destination][0])
        y_distance = abs(source[origin][1] - source[destination][1])
        distance = math.sqrt(math.pow(x_distance, 2) + math.pow(y_distance, 2))

    return distance

def bubbleSort(distance):
    indexList = list(range(1, len(distance) + 1))
    
    for i in range(1, len(distance) + 1):
        for j in range(i, len(distance) + 1):
            if distance[i] >= distance[j]:
                temp = distance[i]
                distance[i] = distance[j]
                distance[j] = temp
                temp = indexList[i - 1]
                indexList[i - 1] = indexList[j - 1]
                indexList[j - 1] = temp
    
    return (distance, indexList)

def getNearest(indexList, usage, deep):
    temp = copy.deepcopy(usage)
    choices = []

    for i in range(0, len(indexList)):
       free = True
       for j in range(0, len(temp)):
           if indexList[i] == temp[j]:
               free = False
       if free:
           choices += [indexList[i]]
           temp += [indexList[i]]
           deep -= 1

       if deep < 1:
           break

    if len(choices) > 0:
        return choices
    else:
        return [0]

def calculateCost(source, path, att):
    cost = 0
    for i in range(0, len(path)):
        cost += vertexDistance(source, path[i][0], path[i][1], att)
    
    return cost

def nearestNeighbor(source, att):
    origin = 1
    usage = []
    path = []
    while origin != 0:
        usage += [origin]
        distance = vectorDistance(source, origin, att)
        (distance, indexList) = bubbleSort(distance)
        destination = getNearest(indexList, usage, 1)
        path += [(origin, destination[0])]
        origin = destination[0]
    path[len(path) - 1] = (path[len(path) - 1][0], path[0][0])
    cost = calculateCost(source, path, att)
    
    return (path, cost)

def nearestNeighborWithGRASP(source, att, elasticity):
    choice = random.sample(range(1, len(source) + 1), 1)
    origin = choice[0]
    usage = []
    path = []
    while origin != 0:
        deep = math.ceil(len(source) * elasticity)
        usage += [origin]
        distance = vectorDistance(source, origin, att)
        (distance, indexList) = bubbleSort(distance)
        choices = getNearest(indexList, usage, deep)
        destination = random.sample(choices, 1)
        path += [(origin, destination[0])]
        origin = destination[0]
    path[len(path) - 1] = (path[len(path) - 1][0], path[0][0])
    cost = calculateCost(source, path, att)
    
    return (path, cost)

def opt2(source, path, cost, att):
    countdown = 5000

    while countdown > 0:
        edges = [0, 0]
        while abs(edges[0] - edges[1]) <= 1:
            edges = random.sample(range(0, len(path) - 1), 2)
            edges.sort()

        (o_f_edge, d_f_edge) = path[edges[0]]
        (o_s_edge, d_s_edge) = path[edges[1]]

        partial_cost = vertexDistance(source, o_f_edge, d_f_edge, att) + vertexDistance(source, o_s_edge, d_s_edge, att)
        partial_new_cost = vertexDistance(source, o_f_edge, o_s_edge, att) + vertexDistance(source, d_f_edge, d_s_edge, att)

        if partial_new_cost < partial_cost:
            new_path = copy.deepcopy(path)
            index = edges[0] + 1
            for i in reversed(range(edges[0] + 1, edges[1])):
                (origin, destination) = path[i]
                new_path[index] = (destination, origin)
                index += 1

            new_path[edges[0]] = (o_f_edge, o_s_edge)
            new_path[edges[1]] = (d_f_edge, d_s_edge)

            cost = calculateCost(source, new_path, att)
            path = copy.deepcopy(new_path)
            countdown = 5000
        else:
            countdown -= 1

    return (path, cost)

def opt3(source, path, cost, att):
    countdown = 5000
    improvement = False

    while countdown > 0 and improvement == False:
        edges = [0, 0, 0]
        while abs(edges[0] - edges[1]) <= 1 or abs(edges[0] - edges[2]) <= 1 or abs(edges[1] - edges[2]) <= 1:
            edges = random.sample(range(0, len(path) - 1), 3)
            edges.sort()

        (o_f_edge, d_f_edge) = path[edges[0]]
        (o_s_edge, d_s_edge) = path[edges[1]]
        (o_t_edge, d_t_edge) = path[edges[2]]

        partial_cost = vertexDistance(source, o_f_edge, d_f_edge, att) + vertexDistance(source, o_s_edge, d_s_edge, att) + vertexDistance(source, o_t_edge, d_t_edge, att)
        partial_new_cost = [(0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0)]
        partial_new_cost[0] = (1, vertexDistance(source, o_f_edge, o_s_edge, att) + vertexDistance(source, d_f_edge, o_t_edge, att) + vertexDistance(source, d_s_edge, d_t_edge, att))
        partial_new_cost[1] = (2, vertexDistance(source, o_f_edge, o_s_edge, att) + vertexDistance(source, d_f_edge, d_s_edge, att) + vertexDistance(source, o_t_edge, d_t_edge, att))
        partial_new_cost[2] = (3, vertexDistance(source, o_f_edge, d_f_edge, att) + vertexDistance(source, o_s_edge, o_t_edge, att) + vertexDistance(source, d_s_edge, d_t_edge, att))
        partial_new_cost[3] = (4, vertexDistance(source, o_f_edge, o_t_edge, att) + vertexDistance(source, d_s_edge, o_s_edge, att) + vertexDistance(source, d_f_edge, d_t_edge, att))
        partial_new_cost[4] = (5, vertexDistance(source, o_f_edge, d_s_edge, att) + vertexDistance(source, o_t_edge, o_s_edge, att) + vertexDistance(source, d_f_edge, d_t_edge, att))
        partial_new_cost[5] = (6, vertexDistance(source, o_f_edge, o_t_edge, att) + vertexDistance(source, d_s_edge, o_s_edge, att) + vertexDistance(source, d_f_edge, d_t_edge, att))
        partial_new_cost[6] = (7, vertexDistance(source, o_f_edge, o_t_edge, att) + vertexDistance(source, d_s_edge, d_f_edge, att) + vertexDistance(source, o_s_edge, d_t_edge, att))
        partial_new_cost[7] = (8, vertexDistance(source, o_f_edge, d_s_edge, att) + vertexDistance(source, o_t_edge, d_f_edge, att) + vertexDistance(source, o_s_edge, d_t_edge, att))
        partial_new_cost.sort(key = operator.itemgetter(1))
        
        if partial_new_cost[0][1] < partial_cost:
            new_path = []

            if partial_new_cost[0][0] == 1:
                for i in range(0, edges[0]):
                    new_path += [path[i]]
                new_path += [(o_f_edge, o_s_edge)]
                for i in reversed(range(edges[0] + 1, edges[1])):
                    (origin, destination) = path[i]
                    new_path += [(destination, origin)]
                new_path += [(d_f_edge, o_t_edge)]
                for i in reversed(range(edges[1] + 1, edges[2])):
                    (origin, destination) = path[i]
                    new_path += [(destination, origin)]
                new_path += [(d_s_edge, d_t_edge)]
                for i in range(edges[2] + 1, len(path)):
                    new_path += [path[i]]
            
            elif partial_new_cost[0][0] == 2:
                for i in range(0, edges[0]):
                    new_path += [path[i]]
                new_path += [(o_f_edge, o_s_edge)]
                for i in reversed(range(edges[0] + 1, edges[1])):
                    (origin, destination) = path[i]
                    new_path += [(destination, origin)]
                new_path += [(d_f_edge, d_s_edge)]
                for i in range(edges[1] + 1, len(path)):
                    new_path += [path[i]]
            
            elif partial_new_cost[0][0] == 3:
                for i in range(0, edges[1]):
                    new_path += [path[i]]
                new_path += [(o_s_edge, o_t_edge)]
                for i in reversed(range(edges[1] + 1, edges[2])):
                    (origin, destination) = path[i]
                    new_path += [(destination, origin)]
                new_path += [(d_s_edge, d_t_edge)]
                for i in range(edges[2] + 1, len(path)):
                    new_path += [path[i]]
            
            elif partial_new_cost[0][0] == 4:
                for i in range(0, edges[0]):
                    new_path += [path[i]]
                new_path += [(o_f_edge, o_t_edge)]
                for i in reversed(range(edges[0] + 1, edges[2])):
                    (origin, destination) = path[i]
                    new_path += [(destination, origin)]
                new_path += [(d_f_edge, d_t_edge)]
                for i in range(edges[2] + 1, len(path)):
                    new_path += [path[i]]
            
            elif partial_new_cost[0][0] == 5:
                for i in range(0, edges[0]):
                    new_path += [path[i]]
                new_path += [(o_f_edge, d_s_edge)]
                for i in range(edges[1] + 1, edges[2]):
                    new_path += [path[i]]
                new_path += [(o_t_edge, o_s_edge)]
                for i in reversed(range(edges[0] + 1, edges[1])):
                    (origin, destination) = path[i]
                    new_path += [(destination, origin)]
                new_path += [(d_f_edge, d_t_edge)]
                for i in range(edges[2] + 1, len(path)):
                    new_path += [path[i]]

            elif partial_new_cost[0][0] == 6:
                for i in range(0, edges[0]):
                    new_path += [path[i]]
                new_path += [(o_f_edge, o_t_edge)]
                for i in reversed(range(edges[1] + 1, edges[2])):
                    (origin, destination) = path[i]
                    new_path += [(destination, origin)]
                new_path += [(d_s_edge, o_s_edge)]
                for i in reversed(range(edges[0] + 1, edges[1])):
                    (origin, destination) = path[i]
                    new_path += [(destination, origin)]
                new_path += [(d_f_edge, d_t_edge)]
                for i in range(edges[2] + 1, len(path)):
                    new_path += [path[i]]

            elif partial_new_cost[0][0] == 7:
                for i in range(0, edges[0]):
                    new_path += [path[i]]
                new_path += [(o_f_edge, o_t_edge)]
                for i in reversed(range(edges[1] + 1, edges[2])):
                    (origin, destination) = path[i]
                    new_path += [(destination, origin)]
                new_path += [(d_s_edge, d_f_edge)]
                for i in range(edges[0] + 1, edges[1]):
                    new_path += [path[i]]
                new_path += [(o_s_edge, d_t_edge)]
                for i in range(edges[2] + 1, len(path)):
                    new_path += [path[i]]

            elif partial_new_cost[0][0] == 8:
                for i in range(0, edges[0]):
                    new_path += [path[i]]
                new_path += [(o_f_edge, d_s_edge)]
                for i in range(edges[1] + 1, edges[2]):
                    new_path += [path[i]]
                new_path += [(o_t_edge, d_f_edge)]
                for i in range(edges[0] + 1, edges[1]):
                    new_path += [path[i]]
                new_path += [(o_s_edge, d_t_edge)]
                for i in range(edges[2] + 1, len(path)):
                    new_path += [path[i]]

            cost = calculateCost(source, new_path, att)
            path = copy.deepcopy(new_path)
            improvement = True
        else:
            countdown -= 1

    return (path, cost, improvement)

def variableNeighborhoodSearch(source, path, cost, att):
    improvement = True
    while improvement:
        (path, cost) = opt2(source, path, cost, att)
        (path, cost, improvement) = opt3(source, path, cost, att)

    return (path, cost)

def main():
    files = ['att48','berlin52','kroA100','kroA150','kroA200','kroB100','kroB150','kroB200','kroC100','kroD100','kroE100','lin105','pr76','pr107','pr124','pr136','pr144','pr152','rat99','rat195','st70']
    
    utilityFile = open('utility.out', 'w')
    timeFile = open('time.out', 'w')
    routeFile = open('route.out', 'w')

    random.seed(1)
    
    for i in range(len(files)):
        source = readFile(files[i] + '.tsp')
        utility_database = []
        elasticity = 0.2

        best_iteration = 0
        best_route = []
        countdown = 20

        time_start = timeit.default_timer()

        if files[i] == 'att48':
            (path, cost) = nearestNeighbor(source, True)
            (path, cost) = variableNeighborhoodSearch(source, path, cost, True)
            utility_database += [cost]
            best_iteration = cost
            best_route = copy.deepcopy(path)
            while countdown > 0:
                (path, cost) = nearestNeighborWithGRASP(source, True, elasticity)
                (path, cost) = variableNeighborhoodSearch(source, path, cost, True)
                utility_database += [cost]
                if cost < best_iteration:
                    best_iteration = cost
                    best_route = copy.deepcopy(path)
                    countdown = 20
                else:
                    countdown -= 1
        else:
            (path, cost) = nearestNeighbor(source, False)
            (path, cost) = variableNeighborhoodSearch(source, path, cost, False)
            utility_database += [cost]
            best_iteration = cost
            best_route = copy.deepcopy(path)
            while countdown > 0:
                (path, cost) = nearestNeighborWithGRASP(source, False, elasticity)
                (path, cost) = variableNeighborhoodSearch(source, path, cost, False)
                utility_database += [cost]
                if cost < best_iteration:
                    best_iteration = cost
                    best_route = copy.deepcopy(path)
                    countdown = 20
                else:
                    countdown -= 1
        
        time_limit = timeit.default_timer()

        utility_database.sort()
        print(utility_database[0])
        utilityFile.write(str(utility_database[0]) + '\n')
        timeFile.write(str(time_limit - time_start) + '\n')
        routeFile.write(str(best_route) + '\n')

    utilityFile.close()
    timeFile.close()
    routeFile.close()
	
main()