import os
import subprocess


#---------------------- preconditions ----------------------
def checkCpurequtilsInstalled():
    try:
        mock = subprocess.check_output(["cpufreq-info", "--help"]).decode("utf-8")
    except:
        print("ERROR: Package cpufrequtils required")
        print("Exiting ...")
        exit(-1)


def exitIfNotRoot():
    #check if script is executed as with root privileges
    executingPID = subprocess.check_output(["/usr/bin/id", "-u"]).decode("utf-8")
    if not executingPID == "0\n":    
        print ("ERROR: Script requires root privileges")
        print ("Exiting ...")
        exit(-1)


#---------------------- read specs ----------------------
def getHerzMultiplier(unit):
    dictionary = {
        "kHz"   : 0.001,
        "MHz"   : 1,
        "GHz"   : 1000
    }
    return dictionary.get(unit)


def getHardwarSpecificationList():
    #read limits and available options from the hardware
    return subprocess.check_output("cpufreq-info").decode("utf-8").split("\n")


def getFreqLimits(info):
    #frequencyInfo=[]
    for line in info:
        if "hardware limits" in line:
            frequencyInfo = line.split(": ")[1].split(" - ")
            frequencyInfo[0] = frequencyInfo[0].split(" ")
            frequencyInfo[1] = frequencyInfo[1].split(" ")
            break

    min = int(float(frequencyInfo[0][0]) * getHerzMultiplier(frequencyInfo[0][1]))
    max = int(float(frequencyInfo[1][0]) * getHerzMultiplier(frequencyInfo[1][1]))
    return (min, max)

    
def getAvailableGovernors(info):
    availableGovernors = []
    for line in info:
        if "available cpufreq governors" in line:
            availableGovernors = line.split(": ")[1].split(", ")
            break
    return availableGovernors


def getCoreNumber(info):
    maxCoreIndex = 0
    for line in info:
        if "analyzing CPU " in line:
            index = int(line.split("analyzing CPU ")[1].split(":")[0])
            if index > maxCoreIndex:
                maxCoreIndex = index
    cores = maxCoreIndex + 1
    return cores


#---------------------- user interaction ----------------------
def readInFreqLimits(min, max):
    print(f"Frequencies must be between {min} and {max} (inclusive)")
    minFreqString = input(f"Please enter new minimal frequency in MHz: ")
    minFreqInt = parseEnteredString(minFreqString, min, max)

    maxFreqString = input(f"Please enter new maximal frequency in MHz: ")
    maxFreqInt = parseEnteredString(maxFreqString, min, max)

    if maxFreqInt < minFreqInt:
        print("ERROR: Entered maximal frequency smaller than entered minimal frequency")
        print("Exiting ...")
        exit (-1)

    if minFreqInt == maxFreqInt:
        print("WARNING: Frequency is fixed to only one value!")

    return [minFreqString, maxFreqString]


def parseEnteredString(s, min, max):
    try:
        enteredInt = int(s)
    except ValueError as e:
        print("ERROR: Entered value is not an integer")
        print("Exiting ...")
        exit(-1)

    if enteredInt < min or enteredInt > max:
        print (f"ERROR: Entered integer not within [{min}, {max}].")
        print ("Exiting ...")
        exit(-1)
    
    return enteredInt


def readInGovernor(availableGovernors):
    enteredGovernor = input(f"Please choose a cpufreq governor (available: {str(availableGovernors)}): ")
    if not enteredGovernor in availableGovernors:
        print("ERROR: Entered cpufreq governor invalid")
        print("Exiting ...")
        exit(-1)
    
    return enteredGovernor


#---------------------- apply changes ----------------------
def applySettings(min, max, governor, cores):
    for i in range(cores):
        os.system(f"/usr/bin/cpufreq-set -c {i} -g {governor} --min {min}MHz --max {max}MHz")
        print(f"Updated core {i}")



#main()
checkCpurequtilsInstalled()
exitIfNotRoot()

infoList = getHardwarSpecificationList()
(min, max) = getFreqLimits(infoList)
availableGovernors = getAvailableGovernors(infoList)
cores = getCoreNumber(infoList)

(enteredMin, enteredMax) = readInFreqLimits(min, max)
enteredGovernor = readInGovernor(availableGovernors)

print("----------------------------------")
print(f"Applying the following parameters for all {cores} cores:")
print("min: " + enteredMin)
print("max: " + enteredMax)
print("governor: " + enteredGovernor)
print("----------------------------------")

applySettings(enteredMin, enteredMax, enteredGovernor, cores)