# elements1.py
#
# New; 15 Nov 2026
#
# Moudle containing simple fucnctions for o1.py
#

import time
import random
import threading
import textwrap
import math
import re
import socket

from pathlib import Path
from subprocess import call
from flask import Flask, request, jsonify

import requests
import roamConfig

currentPop = 0

whereToSearch = "/home/gary/bigO/petriDish/testData" # "/home/gary/data/primeFood"


class Child:

    def __init__(
        self,
        childID = 1,
        hostName = '',
        parent = '',
        baseFile = ''
        ):

        self.childID = childID
        self.hostName = hostName
        self.parent = parent
        self.baseFile = baseFile


    def printAll(self):
        print("Child: childID:  ", self.childID)
        print("Child: hostName: ", self.hostName)
        print("Child: parent  : ", self.parent)
        print("Child: baseFile: ", self.baseFile)
        print('*****************')
        return

    def setBaseFile(self, f):
        testChar = "/"
        res = [i for i in range(len(f)) if f.startswith(testChar, i)]
        baseFile = f[res[-1]:]
        self.baseFile = baseFile[1:]
        return

    def setHostName(self, h):
        self.hostName = h
        return
        
    # ------------------------------------------------------------------
    # Coordinator client methods -- these are the network replacement for
    # "count files in basePath" / "lock+append fileList.txt".
    # ------------------------------------------------------------------

    def registerWithCoordinator(self):
        print("*** registerWithCoordinator start: self.hostName", self.hostName)
        try:
            requests.post(roamConfig.COORDINATOR_URL + "/register", json={
                "childID": self.childID,
                "parent": self.parent,
                "baseFile": self.baseFile,
                "hostName": self.hostName,
            }, timeout=5)
        except Exception as e:
            print("!!! Could not register with coordinator: ", e)
        return

    def heartbeatCoordinator(self):
        print(f"At: {time.ctime()} A call was made to heartbeatCoordinator")
        try:
            requests.post(roamConfig.COORDINATOR_URL + "/heartbeat",
                          json={"childID": self.childID}, timeout=5)
        except Exception as e:
            print("!!! Heartbeat to coordinator failed: ", e)
        return

    def deregisterFromCoordinator(self):
        try:
            requests.post(roamConfig.COORDINATOR_URL + "/deregister",
                          json={"cellID": self.childID}, timeout=5)
        except Exception as e:
            print("!!! Could not deregister from coordinator: ", e)
        return

    def getPopulationFromCoordinator(self):
        try:
            r = requests.get(roamConfig.COORDINATOR_URL + "/status", timeout=5)
            return r.json()["population"]
        except Exception as e:
            print("!!! Could not reach coordinator for population check: ", e)
            # Fail safe: if we can't confirm we're under the cap, behave as
            # though we're at capacity rather than replicating blind.
            return 999999

    def listRegistry(self):
        try:
            r = requests.get(roamConfig.COORDINATOR_URL + "/list_registry", timeout=5)
            #print("type r: ", type(r))
            #print("r: ", r)
            #print("r.json(): ", r.json())
            return r.json()
        except Exception as e:
            print("!!! Could not reach coordinator to list registry: ", e)
            return None 

    def requestSpawnSlot(self, maxPop):
        try:
            r = requests.post(roamConfig.COORDINATOR_URL + "/spawn_request",
                              json={"maxPop": maxPop}, timeout=5)
            print("requestSpawnSlot: r.json: ", r.json)
            return r.json()
        except Exception as e:
            print("!!! Could not reach coordinator for spawn request: ", e)
            print("requestSpawnSlot: {'allow': False}: ", {"allow": False})
            return {"allow": False}

    def remoteLaunch(self, targetHostName, targetIP, childBody, childID):
        remoteDest = roamConfig.REMOTE_BASE_PATH
        userHost = "{}@{}".format(roamConfig.SSH_USER, targetIP)

        # self.baseFile is THIS cell's current file -- the
        # child inherits them (possibly mutated) under its new name.
        subprocess.run(
            ["scp", self.baseFile, "{}:{}/{}".format(userHost, remoteDest, childBody)],
            check=True)
        #subprocess.run(
        #    ["scp", self.dnaFile, "{}:{}/{}".format(userHost, remoteDest, childDNA)],
        #    check=True)

        remoteCmd = "cd {} && nohup python3 {} --cellid {} --parent {} --host {} > /dev/null 2>&1 &".format(
            remoteDest, childBody, childID, self.baseFile, targetHostName)

        subprocess.run(["ssh", userHost, remoteCmd], check=True)
        print("Launched cell {} remotely on {} ({})".format(childID, targetHostName, targetIP))
        return

    def replicate(self):
        print("-----")
        print("replicate:")

        spawn = self.requestSpawnSlot(roamConfig.MAXPOP)

        if not spawn.get("allow"):
            print("Coordinator refused spawn (at/near population cap). Skipping replication.")
            return

        childCell = spawn["childBody"]
        #childDNA = spawn["childDNA"]
        childID = spawn["childID"]
        targetHostName = spawn["targetHost"]
        targetIP = spawn["targetIP"]

        self.myChildren.append((childCell, childDNA))

        print("Replicating -> cellId: {}, host: {} ({})".format(childId, targetHostName, targetIP))

        try:
            self.remoteLaunch(targetHostName, targetIP, childCell, childDNA, childId)
        except subprocess.CalledProcessError as e:
            print("!!! Remote launch failed (scp/ssh error), child never started: ", e)
        return

    def replicateLocal(self, newChild):
        # Inelegant hack to test simple cloning/replication

        print("-----")
        print("replicateLocal: newChild: ", newChild)

        spawn = self.requestSpawnSlot(roamConfig.MAXPOP)

        print("spawn: ", spawn)

        if not spawn.get("allow"):
            print("Coordinator refused spawn (at/near population cap). Skipping replication.")
            return



def processInstruction(instruction: str):
    print(f"Processing: {instruction}")

    instructionArgs = instruction.split(";")

    print(f"instructionArgs: {instructionArgs}")

    if instructionArgs[2] == "local":
        if instructionArgs[3] == "self":
            print("seekPrime,local,self")
            return seekPrime(instructionArgs[2])
        elif instructionArgs[3] == "shell":
            # Create py file to run in shell
            createChild()
            # Run py file in shell
            #runChild("child1.py")
            
        else:
            print(f"processInstruction[2] error: else: {instructionArgs[2]}")
    else:
        print(f"processInstruction[1] error: else: {instructionArgs[1]}")


def createChild():

    if __file__ == "/home/gary/bigO/petriDish/abilities1.py":
        parent = "Mother"
    else:
        parent = "Unknown"
    

    print("---NEW CHILD")
    print("---parent: ", parent)
    mother = Child()
    mother.hostName = socket.gethostname()
    mother.parent = parent
    
    print(mother.listRegistry())

    mother.printAll()

    p = mother.getPopulationFromCoordinator()

    # For now just a simple hard coded script
    childProgram = textwrap.dedent(f"""\
        import time
        import socket
        import elements1 as e1
        
        whereToSearch = '/home/gary/bigO/petriDish/testData'
        
        if __name__ == '__main__':
            
            print('   --- START NEW __main__ CELL INSTANCE --- ')
            primesList = []
            
            start_time = time.time()
            thisChild = e1.Child()
            thisChild.setBaseFile(__file__)
            thisChild.setHostName(socket.gethostname())
            thisChild.childID = {p} + 1
            thisChild.parent = "{parent}"
            
            thisChild.registerWithCoordinator()
            thisChild.printAll()
            
            primesList = e1.seekPrime('local')

            #for p in primesList:
            #    print('Child: ', p)
            
            time.sleep(30)
            print('END CHILD #: ', thisChild.childID)
    """)

    print(p)

    if p == 0:
        print('p=0: creating first child: ', p)
        #newChild.baseFile = 'child1.py'
        #newChild.parent = 'root'

        newChild = "child1.py"

        
        
        with open("child1.py", "w") as file:
            file.write(childProgram)

        # Create first child
        #
        callStr = "gnome-terminal", "-x", "sh", "-c", "python3 " + newChild + "; bash"
        call(callStr)

        currentPop =+ 1
            
    else:
        print('p!=0: attempting to create an additional child: ', p+1)
        #newChild.baseFile = 'child' + str(p+1) + '.py'
        #newChild.parent = "Do not know"

        newChild = 'child' + str(p+1) + '.py'

        print("mother.getPopulationFromCoordinator(): ", mother.getPopulationFromCoordinator())
        print("roamConfig.MAXPOP: ", roamConfig.MAXPOP)

        # Can we spawn a new child?
        if mother.getPopulationFromCoordinator() < roamConfig.MAXPOP:

            with open(newChild, "w") as file:
                file.write(childProgram)

            # Create additional child
            #
            callStr = "gnome-terminal", "-x", "sh", "-c", "python3 " + newChild + "; bash"
            call(callStr)
        else:

            print("Reached MAXPOP. Child not created.")

    
    print('.....')
    print("Sleeping 1...")
    time.sleep(1)
    print(mother.listRegistry())
    #
    #r = newChild.listRegistry()
    #
    #print(r)
    
    #with open("child1.py", "w") as file:
    #    file.write(childProgram)
    print("END createChild")

def runChild(childProgramName: str):
    callStr = "gnome-terminal", "-x", "sh", "-c", "python3 " + childProgramName + "; bash"
    call(callStr)


def seekPrime(where2Seek: str):
    # Potential probelms: Number of files, large files, and files containing large numbers

    if where2Seek == "local":
        return find_files_with_primes(whereToSearch)
    else:
        print(f"seekPrime error: undefined where2Seek: {where2Seek}")


def is_prime(n: int) -> bool:
    """Return True if n is a prime number, False otherwise."""
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    
    # Check factors up to the square root of n using 6k +/- 1 optimization
    limit = math.isqrt(n)
    for i in range(5, limit + 1, 6):
        if n % i == 0 or n % (i + 2) == 0:
            return False
    return True


def find_files_with_primes(directory: str):
    primesCoumt = 0
    primesList = []
    folder = Path(directory)
    
    for file_path in folder.rglob("*.txt"):
        with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
            for line_num, line in enumerate(file, start=1):
                # Extract all whole numbers in the line
                numbers = re.findall(r"\b\d+\b", line)
                
                # Filter for numbers that are prime
                primes_found = [num for num in numbers if is_prime(int(num))]
                
                if primes_found:
                    primesCoumt += 1
                    print(f"{file_path.name} (Line {line_num}): Found primes {primes_found}")
                    primesList.append(file_path.name + ", " + str(line_num) + ", " + str(primes_found)) 
                    # Uncomment the line below if you only want to know *which* files 
                    # contain a prime, rather than listing every line:
                    # break
    return primesList
