# expandAndTag.py
#
# Take input sentence and
# attempt to provide the correct grammatical form.
# Ex: I'd can be I would or I had
#

import nltk
from nltk.tag import pos_tag

from expandSentence import expandSentence as es


def simpleVerbCheck(tagSent1, tagSent2):

    sent = []
    v1 = []
    vM1 = []
    v2 = []
    vM2 = []
    vbAll     = {'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ'}
    vbPresent = {'VB', 'VBG', 'VBP', 'VBZ'}
    vbPast    = {'VBD', 'VBD', 'VBN'}

    for w in tagSent1:
        if w[1] in vbAll:
            v1.append(w)

    for w in tagSent2:
        if w[1] in vbAll:
            v2.append(w)

    print('1 verbs: ', v1)
    print('2 verbs: ', v2)

    for v in v1:
        print("checking 1: ", v)
        if v[1] in vbPresent:
            print(f"{v} Match present {vbPresent}")
            vM1.append(1)
        elif v[1] in vbPast:
            vM1.append(2)
            print(f"{v} Match past {vbPast}")
        else:
            vM1.append(3)
            print(f"{v} No match ")
    print(vM1)
    vM1Result = all(x == vM1[0] for x in vM1)
    print(vM1Result)
    print('---------')
    for v in v2:
        print("checking 2: ", v)
        if v[1] in vbPresent:
            print("Match present ", v)
            vM2.append(1)
        elif v[1] in vbPast:
            print("Match past ", v)
            vM2.append(2)
        else:
            print("No match ", v)
            vM2.append(3)
    print(vM2)
    vM2Result = all(x == vM2[0] for x in vM2)
    print(vM2Result)

    if vM1Result:
        return tagSent1
    elif vM2Result:
        return tagSent2
    else:
        return None

def expandAndTag(inputSentence):

    expandedSentence = []
    tagSent1 = []
    tagSent2 = []
    simple = False
    
    if len(inputSentence) == 0:
        return ['Error: input len 0']

    
    if inputSentence.find("'") != -1: # Possible contraction

        eS1, eS2 = es(inputSentence)

        print('+++++')
        print(type(eS1))
        print(eS1)

        
        if len(eS2) > 0:
            tagSent2 = pos_tag(eS2)
        tagSent1 = pos_tag(eS1)
        
        print("tagSent1:")
        print(tagSent1)
        print("tagSent2:")
        print(tagSent2)

        # Determine correct sentence
        print("WHICH ONE?")
        tagSent1 = simpleVerbCheck(tagSent1, tagSent2)

        print("This one:")
        print(tagSent1)
        
    else: # No ' in sentence, so just tag it

        

        tagSent1 = pos_tag(inputSentence.split())
        print("tagSent1:")
        print(tagSent1)
    
    return tagSent1

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
    
    
