# expandSentence.py
#
# Expand word contractions
# New: 8/9/25
#


from config import simple_contractions

def expandSentence(s):
    
    xS1 = []
    xS2 = []
    tmpSent = []
    positions = []
    listPositions = []
    simple = True
    
    if len(s) < 1 or s == '':
        return None, None

    s = s.replace(',', '') # Remove all ","
    start = 0
    while True:
        start = s.find("'", start)
        if start == -1:
            break
        positions.append(start)
        start += len("'")

    if len(positions) > 0: # Process contraction(s)
        sList = s.split()
        wordIdx = 0
        for w in sList:
            if w.find("'") != -1:
                listPositions.append(wordIdx)
            wordIdx += 1
        for p in listPositions:
            if sList[p] in simple_contractions.keys():
                r = simple_contractions[sList[p]]
                rList = r.split()
                if len(rList) > 2:
                    simple = False
        if simple:
            for w in sList:
                if w in simple_contractions.keys():
                    result = simple_contractions[w]
                    for r in rList:
                        xS1.append(r)
                else:
                    xS1.append(w)
        else:
            wIdx = 0
            for w in sList:
                if w in simple_contractions.keys():
                    result = simple_contractions[w]
                    rList = result.split()
                    if len(rList) == 2:
                        xS1.append(rList[0])
                        xS1.append(rList[1])
                        xS2.append(rList[0])
                        xS2.append(rList[1])
                    elif len(rList) > 2:
                        xS1.append(rList[0])
                        xS1.append(rList[1])   
                        xS2.append(rList[2])
                        xS2.append(rList[3])
                else:
                    xS1.append(w)
                    xS2.append(w)
                wIdx +=1    
    
    return xS1, xS2


#
if __name__ == "__main__":
    """ Test sentences """
    #
    s = "I'd never bused so many dishes in one night"
    # [('I', 'PRP'), ('had', 'VBD'), ('never', 'RB'), ('bused', 'VBN'), ('so', 'RB'), ('many', 'JJ'), ('dishes', 'NNS'), ('in', 'IN'), ('one', 'CD'), ('night', 'NN')]
    #
    #s = "I wish I'd waited longer"
    # [('I', 'PRP'), ('wish', 'VBP'), ('I', 'PRP'), ('had', 'VBD'), ('waited', 'VBN'), ('longer', 'RBR')]
    #
    #s = "He'd gone home"
    # [('He', 'PRP'), ('had', 'VBD'), ('gone', 'VBN'), ('home', 'RB')]
    #
    #s = "She'd just spoken to her"
    # [('She', 'PRP'), ('had', 'VBD'), ('just', 'RB'), ('spoken', 'VBN'), ('to', 'IN'), ('her', 'PRP')]
    #
    #s = "I'd like some tea"
    # [('I', 'PRP'), ('would', 'MD'), ('like', 'VB'), ('some', 'DT'), ('tea', 'NN')]
    #
    #s = "I'd have gone if I had had time"
    # [('I', 'PRP'), ('would', 'MD'), ('have', 'VB'), ('gone', 'VBN'), ('if', 'IN'), ('I', 'PRP'), ('had', 'VBD'), ('had', 'VBN'), ('time', 'NN')]
    #
    #s = "I'd agreed to go"
    #   Should return "I had agreed to go"
    #
    #s = "He'd have been 70 today"
    # [('He', 'PRP'), ('would', 'MD'), ('have', 'VB'), ('been', 'VBN'), ('70', 'CD'), ('today', 'NN')]
    #
    #s = "I'll see you tomorrow"
    # [('I', 'PRP'), ('will', 'MD'), ('see', 'VB'), ('you', 'PRP'), ('tomorrow', 'NN')]
    #
    #s = "I'd go to the store if she'd go too"
    #   Should retunr: would...would
    #
    #s = "She's been waiting for hours, but they haven't shown up yet"
    #
    #s = "I've been waiting while she's been playing"
    #s = "I thought love was only true in fairy tales"
    # [('I', 'PRP'), ('thought', 'VBD'), ('love', 'NN'), ('was', 'VBD'), ('only', 'RB'), ('true', 'JJ'), ('in', 'IN'), ('fairy', 'NN'), ('tales', 'NNS')]
    #
    #s = ''

    print('START -- expandSentence -- main --')
    print('s:')
    print(s)
    print('----')

    xS, xS2 = expandSentence(s)

    print('----')
    print("xS:")
    print(xS)
    print("xS2:")
    print(xS2)


    print('END   -- expandSentence -- main --')


