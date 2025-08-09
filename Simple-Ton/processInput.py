# processInput.py
# New: 7/26/25
#

from config import inputSentence #, nnx, prpx
from string import punctuation
from expandAndTag import expandAndTag


def processUserInput():
    # Rudimentary input processing
    inSentObj = None
    
    
    print('-' * 10)
    uI = input('Please enter a sentence: ')

    if uI == '':
        print('Exiting...')
        return None
    else:
        print("Echo: ", uI)
        print('-' * 10)
        print('Processing user input...')
        
        uI = uI.rstrip(punctuation)
        taggedInput = expandAndTag(uI)
        print('taggedInput: ', taggedInput)

        inSentObj = inputSentence(uI, taggedInput, [])
        
    print('-' * 30)
    
    return inSentObj


#
#
if __name__ == "__main__":

    print('Start processInput (__main__)...')

    inputSentObj = processUserInput()
    if inputSentObj != None:
        inputSentObj.printAll()

    print('End -- processInput (__main__)')

