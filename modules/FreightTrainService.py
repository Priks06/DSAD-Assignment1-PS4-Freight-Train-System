import csv

class FreightTrainService:

    trains = []
    cities = []
    adjacencyMatrix = [[]]
    visited = []
    stack = []
    outputFileName = "files/outputPS4.txt"

    # Clear previous contents of the output file
    def __init__(self):
        outputFile = open(self.outputFileName, "w")
        outputFile.write(" ")
        outputFile.close()

    

    # This function will read the given input file and create an adjacency matrix
    # with trains and cities as vertices and their associations as edges.
    # The matrix will have trains followed by cities in rows as well as columns
    # In a row, if there is an edge between the row number and column number, value will be 1, else 0.
    # For example, if there are 4 trains and 8 cities, then matrix will be 12x12 with trains followed by cities
    def readCityTrainfile(self, inputfile):
        #print("Received file: ", inputfile)

        # Create 2 lists for distinct/unique trains and distinct cities respectively.
        try:
            with open(inputfile) as csvFile:
                fileReader = csv.reader(csvFile, delimiter='/')
                lineCount = 0
                for line in fileReader:
                    if line:
                        trainName = line[0]
                        trainName = trainName.strip()
                        if trainName not in self.trains:
                            self.trains.append(trainName)
                        
                        for city in line[1:]:
                            city = city.strip()
                            if city and not city.isspace() and city not in self.cities:
                                self.cities.append(city)
                csvFile.close()
            self.visited = [0 for i in range (len(self.trains) + len(self.cities))]
                            
            # Initialize the Adjacency matrix with vertices as trains and cities
            rows = len(self.trains) + len(self.cities)
            cols = rows
            self.adjacencyMatrix = [[0 for i in range(cols)] for j in range(rows)]

            # Read the file again and fill up the adjacency matrix
            with open(inputfile) as csvFile:
                fileReader = csv.reader(csvFile, delimiter='/')
                lineCount = 0
                isTrainDataLoaded = [0 for i in range (len(self.trains))]
                for line in fileReader:
                    if line:
                        trainName = line[0]
                        trainName = trainName.strip()
                        trainIndex = self.trains.index(trainName)
                        # Validate if data for current train has already been loaded.
                        if isTrainDataLoaded[trainIndex] == 1:
                            print("Duplicate data for train: " + trainName + " found. Ignoring it.")
                            continue
                        
                        # Update the adjacency matrix
                        for city in line[1:]:
                            city = city.strip()
                            if city and not city.isspace():
                                cityIndex = self.cities.index(city)

                                # Set the cell in matrix to 1 for train row and city column as well as city row and train column
                                # City index in matrx will be length of distinct train list + index of that city in distinct city list
                                # because, matrix has nodes with trains followed by cities
                                self.adjacencyMatrix[trainIndex][len(self.trains)+cityIndex] = 1
                                self.adjacencyMatrix[len(self.trains)+cityIndex][trainIndex] = 1
                        
                        lineCount += 1
                # Close the input file
                csvFile.close()
        except:
            print("File: " + self.outputFileName + " not found.")
        #print("File read having lines: ", lineCount, "with below content: ")
        #print("Trains: ")
        #for train in self.trains:
        #    print(train)
        #print("\nCities")
        #for city in self.cities:
        #    print(city)

        #print("Adjacency matrix formed like below:")
        #for row in self.adjacencyMatrix:
        #    print(row)


    # This function will display the details of the Freight Train syste to file outputPS4.txt.
    # It will display the total count of unique trains and cities
    # It will display the list of unique trains and cities
    def showAll(self):
        #print("Writing to file.")
        outputFile = open(self.outputFileName, "a")
        outputFile.write("\n\n-------------Function showAll--------------")
        outputFile.write("\n\nTotal number of freight trains: " + str(len(self.trains)))
        outputFile.write("\n\nTotal number of cities: " + str(len(self.cities)))
        outputFile.write("\n\nList of freight trains: ")
        # Get the list of unique trains
        for train in self.trains:
            outputFile.write("\n\n" + train)

        # Get the list of unique cities
        outputFile.write("\n\nList of cities: ")
        for city in self.cities:
            outputFile.write("\n\n" + city)
        
        # Close the output file
        outputFile.close()

    # This function will find out the Transport Hub and display it to file outputPS4.txt
    # i.e. the city which is visited by maximum number of trains
    def displayTransportHub(self):
        # Find the vertex with the highest degree. 
        # Traverse the matrix vertex by vertex and calculate the degree of each node.
        maxDegree = 0
        transportHubs = []
        degreeOfVertices = []

        # Only iterate the matrix for the rows which corrorspond to cities
        # and columns which corrospond to trains.
        # No need to traverse the entire matrix
        for cityIndex in range (len(self.trains), len(self.trains)+len(self.cities)):
            degree = 0
            for trainIndex in range (len(self.trains)):
                if self.adjacencyMatrix[cityIndex][trainIndex] == 1:
                    degree += 1
            degreeOfVertices.append(degree)

        # Now find the vertices (cities) with maximum degree
        if degreeOfVertices:
            maxDegree = max(degreeOfVertices)
            if maxDegree > 0:
                for i in range (len(degreeOfVertices)):
                    if degreeOfVertices[i] == maxDegree:
                        transportHubs.append(i)

        # Display the details of the Transport Hub, along with the trains that visit it.
        outputFile = open(self.outputFileName, "a")
        outputFile.write("\n\n-------------Function displayTransportHub--------------")
        if len(transportHubs) == 0:
            outputFile.write("\n\nThere is no Transport Hub.")
        if len(transportHubs) > 1:
            outputFile.write("\n\nThere are more than one Transport Hubs. They are: ")
        for transportHub in transportHubs:
            outputFile.write("\n\nMain Transport Hub is: " + self.cities[transportHub])
            outputFile.write("\n\nNumber of trains visited: " + str(maxDegree))
            outputFile.write("\n\nList of Freight Trains: ")
            for trainIndex in range (len(self.trains)):
                # Index of city in adjacency matrix will be no. of trains + current index of city
                if self.adjacencyMatrix[len(self.trains)+transportHub][trainIndex] == 1:
                    outputFile.write("\n\n" + self.trains[trainIndex])
        
        # Close the output file
        outputFile.close()

    # This function will find out all the cities which are visited by the given train 
    # and display it to file outputPS4.txt.
    # param: train: Freight Train number for which connected cities should be displayed.
    def displayConnectedCities(self, train):
        trainIndex = -1
        cities = []
        outputFile = open(self.outputFileName, "a")
        outputFile.write("\n\n-------------Function displayConnectedCities--------------")
        if not train:
            outputFile.write("\n\nTrain number not provided.")
            outputFile.close()
            return

        # Validate Freight Train number
        try:
            trainIndex = self.trains.index(train)
            outputFile.write("\n\nFreight Train number: " + train)
        except ValueError:
            outputFile.write("\n\nFreight Train number " + train + " not found in data store")
            return

        # Traverse the adjacency matrix only for row corresponding to the given train 
        # and columns corrosponding to cities.
        # No need to traverse the entire matrix
        for cityIndex in range (len(self.trains), len(self.trains)+len(self.cities)):
            if self.adjacencyMatrix[trainIndex][cityIndex] == 1:
                cities.append(self.cities[cityIndex-len(self.trains)])

        # Print the list of cities which were found to be associated with the trains
        outputFile.write("\n\nNumber of cities connected: " + str(len(cities)))
        for city in cities:
            outputFile.write("\n\n" + city)
        
        # Close the output file
        outputFile.close()

    # This function finds out if there is any direct train between the given cities
    # and displays the details to file outputPS4.txt
    # param: cityA: Name of the first city between which connectivity should be found
    # param: cityB: Name of the second city between which connectivity should be found
    def displayDirectTrain(self, cityA, cityB):
        errorMsg = ""
        outputFile = open(self.outputFileName, "a")

        outputFile.write("\n\n-------------Function displayDirectTrain--------------")
        if not cityA or not cityB:
            outputFile.write("\n\nInvalid number of cities provided.")
            outputFile.close()
            return
        outputFile.write("\n\nCity A: " + cityA)
        outputFile.write("\n\nCity B: " + cityB)
        # Validate the input cities
        try:
            cityAIndex = self.cities.index(cityA)
        except ValueError:
            errorMsg = "\nCity: " + cityA + " is not present in the data store"
            #outputFile.write("\n\nCity: " + cityA + "is not present in the data store")
            #return

        try:
            cityBIndex = self.cities.index(cityB)
        except ValueError:
            errorMsg += "\nCity: " + cityB + " is not present in the data store"
            #outputFile.write("\n\nCity: " + cityB + "is not present in the data store")
            #return
        
        trainConnectingCityAWithCityB = -1
        if errorMsg == "":
            # Find a direct train between input cities cityA and cityB (if any)
            # First find the Trains which connect to cityA
            trainsConnectingCityA = []
            startIndexOfCities = len(self.trains)
            for trainIndex in range (len(self.trains)):
                if self.adjacencyMatrix[startIndexOfCities+cityAIndex][trainIndex] == 1:
                    trainsConnectingCityA.append(trainIndex)

            # Now find the cities visited by the above list of trains 
            # and check if any of the cities matches the given cityB
            trainConnectingCityAWithCityB = -1
            for trainIndex in trainsConnectingCityA:
                for cityIndex in range (startIndexOfCities, startIndexOfCities+len(self.cities)):
                    if (cityIndex - startIndexOfCities) == cityBIndex and self.adjacencyMatrix[trainIndex][cityIndex]:
                        trainConnectingCityAWithCityB = trainIndex
                        break
        
        # Display the output in file
        if trainConnectingCityAWithCityB == -1:
            if errorMsg == "":
                errorMsg = "No direct Freight Train found between: " + cityA + " and " + cityB
            outputFile.write("\n\nCan the package be sent directly: No, " + errorMsg)
        else:
            outputFile.write("\n\nCan the package be sent directly: Yes, " + self.trains[trainConnectingCityAWithCityB])
        
        # Close the output file
        outputFile.close()

    # This function will find out of the given cities are connected to each other 
    # either directly by a single train or indirectly by a chain of trains
    # param: cityA: Name of the first city between which connectivity should be found
    # param: cityB: Name of the second city between which connectivity should be found
    def findServiceAvailable(self, cityA, cityB):
        errorMsg = ""
        self.resetContext()
        outputFile = open(self.outputFileName, "a")
        outputFile.write("\n\n-------------Function findServiceAvailable--------------")
        if not cityA or not cityB:
            outputFile.write("\n\nInvalid number of cities provided.")
            outputFile.close()
            return
        outputFile.write("\n\nCity A: " + cityA)
        outputFile.write("\n\nCity B: " + cityB)

        # Validate the given cities
        try:
            cityAIndex = self.cities.index(cityA)
        except ValueError:
            errorMsg = "\nCity: " + cityA + " is not present in the data store"
            #outputFile.write("\n\nCity: " + cityA + "is not present in the data store")
            #return

        try:
            cityBIndex = self.cities.index(cityB)
        except ValueError:
            errorMsg += "\nCity: " + cityB + " is not present in the data store"
            #outputFile.write("\n\nCity: " + cityA + "is not present in the data store")
            #return
        
        isPathExist = False
        if(errorMsg == ""):
            #print("City A index: ", cityAIndex, " City B index: ", cityBIndex)

            # Use DFS algorithm to find out if there is a path between the given two cities
            isPathExist = self.findPath((len(self.trains) + cityAIndex), (len(self.trains) + cityBIndex), self.stack)
        
        # Display the output in file
        if isPathExist:
            outputFile.write("\n\nCan the package be sent: Yes, ")
            path = self.getPath(self.stack)
            outputFile.write(path)
        else:
            if errorMsg == "":
                errorMsg = "No path found between city: " + cityA + " and city: " + cityB
            outputFile.write("\n\nCan the package by sent: No, " + errorMsg)

        # Close the output file
        outputFile.close()

    # This function is the recursive implementation of Depth First Search traversal
    # param: src: Adjacency matrix index of the current node being explored
    # param: dest: Adjacency matrix index of the destination city
    # param: stack: Reference of stack being used
    def findPath(self, src, dest, stack):
        stack.append(src)
        
        if(src == dest):
            return True

        self.visited[src] = True

        # Used to check if backtracking has taken place
        backTrack = 0
        numberOfVertices = len(self.adjacencyMatrix)
        for i in range (0, numberOfVertices):
            # If the vertex is associated with this vertex and has not been visited yet
            if(self.adjacencyMatrix[src][i] == 1 and not self.visited[i]):
                # Return true of recursive call for DFS returns true
                if self.findPath(i, dest, stack):
                    return True
        backTrack = 1

        # In case of backtracking, remove the node that was most recently visited, 
        # since that won't be a part of the path between cities.
        if backTrack == 1:
            del stack[-1]
        return False

    # This is a utility function which will return the path of the nodes from the stack 
    # in the order in which nodes were visited
    def getPath(self, stack):
        path = ""
        for i in range (len(stack)-1):
            #print(self.getVertexName(stack[i]), end=">")
            path += self.getVertexName(stack[i]) + ">"
        
        path += self.getVertexName(stack[-1])
        #print(self.getVertexName(stack[-1]))

        return path

    # This is a utility method which will return the name of the vertex based on its index in the adjacency matrix.
    def getVertexName(self, indexInMatrix):
        vertexName = ""
        if indexInMatrix < len(self.trains):
                vertexName = self.trains[indexInMatrix]
        else:
            vertexName = self.cities[indexInMatrix - len(self.trains)]
        return vertexName

    # This is a utility method which will clear the stack and reset the list of visited nodes from previous run
    def resetContext(self):
        self.stack.clear()
        self.visited = [0 for i in range (len(self.trains) + len(self.cities))]

    # This is a utility method which will write a message to the file outputPS4.txt
    def writeMsgToFile(self, msg):
        outputFile = open(self.outputFileName, "a")
        outputFile.write("\n\n" + msg)