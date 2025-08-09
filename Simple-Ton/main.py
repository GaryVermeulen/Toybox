# main.py
# Main script file for Simple-Ton 2.0
# New: 7/25/25
#


from createKG import loadKG
from createKG import plotG
from processInput import processUserInput
from utils import checkDictionary, searchKG, searchMongoWiki

def getUnknowns(inputSentObj):
    unknowns = []
    for d in inputSentObj.data:
        if "Unknown" in d:
            unknowns.append(d["Unknown"])         
    
    return unknowns

if __name__ == "__main__":

    docs = []

    

    LTG, nLTG = loadKG()

    #plotG(LTG)
    #plotG(nLTG)

    inputSentObj = processUserInput()
    
    if inputSentObj != None:
        print('---- inputSentObj !- None:')
        inputSentObj.printAll()
        # Check tagging ex: mongo is not a JJ and
        # hello should be an INTJ (interjection).
        # Oh joy, let's learn the English language...
        print('---- Spelling and grammar:')
        x = checkDictionary(inputSentObj)
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
        

    
