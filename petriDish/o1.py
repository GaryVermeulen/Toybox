# o1.py
#
# New; 15 Nov 2026
#
# A simple orchestrator program with a moudle containing simple fucnctions
#
import os
import time
import signal
import socket
from subprocess import call
from subprocess import run
import subprocess

import elements1 as e1


spawnCoordinator = "/home/gary/bigO/petriDish/spawnCoordinator.py"

        

def isScriptRunning(script_name):
    # -f matches against the full command line argument list
    result = run(
        ['pgrep', '-f', f'python.*{script_name}'], capture_output=True, text=True
    )
    return result.returncode == 0


def getPID(target):
    try:
        # -f matches against the full command line, not just the executable name
        output = subprocess.check_output(["pgrep", "-f", target], text=True)
        return [int(pid) for pid in output.strip().splitlines()]
    except subprocess.CalledProcessError:
        # pgrep exits with status 1 if no matching processes are found
        return []


def readInstructions():

    inputList = []
    instructionList = []
    
    # Read toDo.txt for instructions
    with open("toDo.txt", "r", encoding="utf-8") as file:
        inputList = [line.rstrip("\n") for line in file]

    # Process inputList
    for i in inputList:
        if i[0] != "#": # Skip comments
            instructionList.append(i)

    return instructionList


def runToDo():
    instructionList = readInstructions()
    print(instructionList)

    instructionCount = len(instructionList)
    print(instructionCount)

    for instruction in instructionList:
        result = e1.processInstruction(instruction)
        print(f"Result for {instruction} is {result}")
        print("---")
    


##########################
if __name__ == "__main__":

    print(f"---=== Orchestrator starting at: {time.ctime()} ===---")
    startTime = time.time()
    
    if isScriptRunning(spawnCoordinator):
        print("spawnCoordinator is already running...")
    else:
        print("Starting spawnCoordinator...")
        callStr = "gnome-terminal", "-x", "sh", "-c", "python3 " + spawnCoordinator + "; bash"
        call(callStr)

    while True:
        print("\n--- Main Menu ---")
        print("1. Run toDo.txt")
        print("2. Enter instruction")
        print("3. Exit")

        choice = input("Enter your choice (1-3): ").strip()

        if choice == "1":
            print("You selected Option One.")
            runToDo()

            print("-----------------End 1: runToDo")
        elif choice == "2":
            print("You selected Option Two. Testing Child class...")

            e1.createChild()
            
            print("-----------------End 2: createChild")
        elif choice == "3" or choice == "":
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

    # kill SpawnCoordinator
    processList = getPID(spawnCoordinator)
    print(processList)

    for p in reversed(processList):
        print("killing: ", p)
        os.kill(p, signal.SIGTERM)

#    time.sleep(2)
    
    print(f"---=== Orchestrator completd at: {time.ctime()} and took: {round((time.time() - startTime), 4)} seconds ===---")
