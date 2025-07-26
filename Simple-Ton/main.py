# main.py
# Main script file for Simple-Ton
# New: 7/25/25
#

from createKG import loadKG
from createKG import plotG
from processInput import processUserInput


if __name__ == "__main__":

    LTG, nLTG = loadKG()

    plotG(LTG)
    plotG(nLTG)

    inputSentObj = processUserInput()
    
    if inputSentObj != None:
        inputSentObj.printAll()

    
