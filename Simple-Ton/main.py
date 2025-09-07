# main.py
# Single-pass main script for Simple-Ton 2.0
# New: 7/25/25
#

import sys
from createKG import loadKG
from createKG import plotG
from processInput import processUserInput
from utils import checkWordNet, checkMongoDictionary, searchKG, searchMongoWiki


def getUnknowns(inputSentObj):
    unknowns = []
    for d in inputSentObj.data:
        if "Unknown" in d:
            unknowns.append(d["Unknown"])         
    
    return unknowns

if __name__ == "__main__":

    docs = []

    
    # Build/load KG
    LTG, nLTG = loadKG()

    #plotG(LTG)
    #plotG(nLTG)

    # Get input from user, expand contractions, and POS tag
    inputSentObj = processUserInput()
    
    if inputSentObj != None:
        print('---- inputSentObj:')
        inputSentObj.printAll()

        #sys.exit("Debug Stop/exit...")
        
        print('---- checkMongoDictionary:')
        mongoDef = checkMongoDictionary(inputSentObj)

        for d in mongoDef:
            print("d: ")
            print(d)

        print('---- checkWordNet:')
        synsets = checkWordNet(inputSentObj)

        for s in synsets:
            print('s:')
            print(s)

        print('------------')
        print(inputSentObj.rawSent)
        sys.exit("Debug Stop/exit...")
        
        print('---- start searchKB:')
        searchKG(LTG, inputSentObj)
        print('---- afer searchKB:')
        inputSentObj.printAll()
        
        print('---- start getUnknowns:')
        unk = getUnknowns(inputSentObj)
        for u in unk:
            print("u: ", u)
            doc = searchMongoWiki(u[0])
            docs.append(doc)
            
        for d in docs:
            print(d)
        

    
