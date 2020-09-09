import sys
import csv
sys.path.append('modules')
from modules.FreightTrainService import FreightTrainService

print("Welcome to Fright Booking system")

# Read the input file and store the information in a graph using adjacency matrix
freightTrainService = FreightTrainService()
freightTrainService.readCityTrainfile("files/inputPS4.txt")

# Show all details
freightTrainService.showAll()

# Start reading user prompt file
freightTrainService.writeMsgToFile("--------------Reading user prompt file-----------------")

try:
    with open('files/promptsPS4.txt') as csvFile:
        fileReader = csv.reader(csvFile, delimiter=':')
        
        lineCount = 0
        for line in fileReader:
            if line:
                lineCount += 1
                # Display transport Hub
                if line[0].strip()=='searchTransportHub':
                    freightTrainService.writeMsgToFile("Processing line number: " + str(lineCount))
                    freightTrainService.displayTransportHub()
                    continue
                # Find the cities connected by a Train
                if line[0].strip()=='searchTrain':
                    freightTrainService.writeMsgToFile("Processing line number: " + str(lineCount))
                    if len(line) == 2:
                        freightTrainService.displayConnectedCities(line[1].strip())
                    else:
                        freightTrainService.writeMsgToFile("Invalid number of arguments given for searchTrain")
                    continue
                # Display direct train between two cities
                if line[0].strip()=='searchCities':
                    freightTrainService.writeMsgToFile("Processing line number: " + str(lineCount))
                    if len(line) == 3:
                        freightTrainService.displayDirectTrain(line[1].strip(), line[2].strip())
                    else:
                        freightTrainService.writeMsgToFile("Invalid number of arguments given for searchCities")
                    continue
                # Find path    
                if line[0].strip()=='ServiceAvailability':
                    freightTrainService.writeMsgToFile("Processing line number: " + str(lineCount))
                    if len(line) == 3:
                        freightTrainService.findServiceAvailable(line[1].strip(), line[2].strip())
                    else:
                        freightTrainService.writeMsgToFile("Invalid number of arguments given for ServiceAvailability")
                    continue
            else:
                lineCount += 1
except:
    print("User prompt file not found at: files/promptsPS4.txt")