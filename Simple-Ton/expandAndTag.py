# expandAndTag.py
#
# Take input sentence and
# attempt to provide the correct grammatical form.
# Ex: I'd can be I would or I had
#

import nltk
from nltk.tag import pos_tag

#from config import simple_contractions
from config import vbAll, vbPresent, vbPast

from utils import naiveGrammar, getContraction

#from expandSentence import expandSentence as es


def expandSentence(s):
    
    tmpList1 = []
    tmpList2 = []
    
    xWords = []
    tmpSent = []
    positions = []
    listPositions = []
    simple = True
    
    if len(s) < 1 or s == '':
        return None, None, None

    s = s.replace(',', '') # Remove all ","

    sLst = s.split()

    #print('s:')
    #print(s)
    #print('---')
    #print('sLst:')
    #print(sLst)

    for w in sLst:

        if w.find("'") != -1: # Found ' in word
            expandedForm = getContraction(w)
            if expandedForm == None:
                print(f'The word: {w} Is not a proper or known contraction.')
                tmpList1.append(w) # For now, just pass it along
                tmpList2.append(w)
            else:
                #print('expandedForm: ', expandedForm)

                expFormList = expandedForm.split()

                #print('expFormList:')
                #print(expFormList)
                #print('expFormList len:')
                #print(len(expFormList))

                if len(expFormList) <= 3: # Simple or double contraction
                    for e in expFormList:
                        tmpList1.append(e)
                        tmpList2.append(e)
                else:
                    
                    tmpList1.append(expFormList[0])
                    tmpList1.append(expFormList[1])
                    tmpList2.append(expFormList[2])
                    tmpList2.append(expFormList[3])
                        
        else:
            #print('w: ', w)
            tmpList1.append(w)
            tmpList2.append(w)

    #print('-----')
    #print('tmpList1:')
    #print(tmpList1)
    tmpList1[0] = tmpList1[0].capitalize()
    #print(tmpList1)
    #print('tmpList2:')
    #print(tmpList2)
    tmpList2[0] = tmpList2[0].capitalize()
    #print(tmpList2)

    if tmpList1 == tmpList2:
        tmpList2 = []
    
    return tmpList1, tmpList2



def simpleVerbCheck(tagSent1, tagSent2):

    sent = []
    v1 = []
    vM1 = []
    v2 = []
    vM2 = []

#    print("vbPresent: ", vbPresent)
#    print("vbPast: ", vbPast)
#    print('---------')

    for w in tagSent1:
        if w[1] in vbAll:
            v1.append(w)

    for w in tagSent2:
        if w[1] in vbAll:
            v2.append(w)

#    print('v1 verbs: ', v1)
#    print('v2 verbs: ', v2)
#    print('---------')
    
    for v in v1:
#        print("checking 1: ", v)
        if v[1] in vbPresent:
#            print(f"    {v} Match present {vbPresent}")
            vM1.append(1)
        elif v[1] in vbPast:
            vM1.append(2)
#            print(f"    {v} Match past {vbPast}")
        else:
            vM1.append(3)
#            print("    No match: ", v)
#    print("vM1: ", vM1)
    vM1Result = all(x == vM1[0] for x in vM1)
#    print("vM1Result: " , vM1Result)
#    print('---------')
    for v in v2:
#        print("checking 2: ", v)
        if v[1] in vbPresent:
            #print("Match present ", v)
#            print(f"    {v} Match present {vbPresent}")
            vM2.append(1)
        elif v[1] in vbPast:
            #print("Match past ", v)
#            print(f"    {v} Match past {vbPast}")
            vM2.append(2)
        else:
            print("    No match: ", v)
            vM2.append(3)
#    print("vM2: ", vM2)
    vM2Result = all(x == vM2[0] for x in vM2)
#    print("vM2Result: ", vM2Result)

    if vM1Result:
        return tagSent1
    elif vM2Result:
        return tagSent2
    else:
        #
        return None


def expandAndTag(inputSentence):

    expandedSentence = []
    tagSent1 = []
    tagSent2 = []
    simple = False
    
    if len(inputSentence) == 0:
        return ['Error: input len 0']

    
    if inputSentence.find("'") != -1: # Possible contraction

        eS1, eS2 = expandSentence(inputSentence)

#        print('+++++ es1')
#        print(type(eS1))
#        print(eS1)
#        print('+++++ es2')
#        print(type(eS2))
#        print(eS2)       
        
        if len(eS2) > 0:
            tagSent2 = pos_tag(eS2)
        tagSent1 = pos_tag(eS1)
        
#        print("tagSent1:")
#        print(tagSent1)
#        print("tagSent2:")
#        print(tagSent2)

        # Determine correct sentence
#        print("WHICH ONE?")
        if len(tagSent2) > 0:
            correctSent = simpleVerbCheck(tagSent1, tagSent2)
        else:
            print("There is no ambiguity...")
            correctSent = tagSent1

        if correctSent == None:
            print("simpleVerbCheck was unable to determine correct sentence.")
            print("tagSent1:")
            print(tagSent1)
            print("tagSent2:")
            print(tagSent2)
            # For the time being, just ask user to choose which
            # sentence has the correct grammar and store in DB
            x = naiveGrammar(inputSentence, tagSent1, tagSent2)
            print('naiveGrammar returned (x): ', x)
            correctSent = x
        else:
            print("simpleVerbCheck determined this sentence to be correct:")
            print(correctSent)
        
    else: # No ' in sentence, so just tag it

        correctSent = pos_tag(inputSentence.split())
        print("Tagged sentence w/o simpleVerbCheck:")
        print(correctSent)

#    print("type correctSent: ", type(correctSent))
#    print("correctSent:")
#    print(correctSent)
#    print("type correctSent[0]: ", type(correctSent[0]))
#    print("correctSent[0]:")
#    print(correctSent[0])

    if isinstance(correctSent[0], list):
        list_of_tuples = []
        for sublist in correctSent:
            list_of_tuples.append(tuple(sublist))
        return list_of_tuples
    
    return correctSent

#
if __name__ == "__main__":

    print('START -- expandAndTag -- main --')

    """
    print('inputSentence:')
    print(inputSentence)

    expandedSentence = expandAndTag(inputSentence)

    print('expandedSentence:')
    print(expandedSentence)
    """
    print('END -- expandAndTag -- main --')    
    
    
