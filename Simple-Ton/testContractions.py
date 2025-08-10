# testContractions.py
# Test Pascal V Kooten's contractions module
#
import contractions

    
#inputSentence = "I'd never bused so many dishes in one night"
    # [('I', 'PRP'), ('had', 'VBD'), ('never', 'RB'), ('bused', 'VBN'), ('so', 'RB'), ('many', 'JJ'), ('dishes', 'NNS'), ('in', 'IN'), ('one', 'CD'), ('night', 'NN')]
    # Returned: world

#inputSentence = "I wish I'd waited longer"
    # [('I', 'PRP'), ('wish', 'VBP'), ('I', 'PRP'), ('had', 'VBD'), ('waited', 'VBN'), ('longer', 'RBR')]
    # Returned: would
    
#inputSentence = "He'd gone home"
    # [('He', 'PRP'), ('had', 'VBD'), ('gone', 'VBN'), ('home', 'RB')]
    # Retunred: would
    
#inputSentence = "She'd just spoken to her"
    # [('She', 'PRP'), ('had', 'VBD'), ('just', 'RB'), ('spoken', 'VBN'), ('to', 'IN'), ('her', 'PRP')]
    # Returned: would
    
#inputSentence = "I'd like some tea"
    # [('I', 'PRP'), ('would', 'MD'), ('like', 'VB'), ('some', 'DT'), ('tea', 'NN')]
    # Returned: would
    
#inputSentence = "I'd have gone if I had had time"
    # [('I', 'PRP'), ('would', 'MD'), ('have', 'VB'), ('gone', 'VBN'), ('if', 'IN'), ('I', 'PRP'), ('had', 'VBD'), ('had', 'VBN'), ('time', 'NN')]
    # Returned: would
    
#inputSentence = "He'd have been 70 today"
    # [('He', 'PRP'), ('would', 'MD'), ('have', 'VB'), ('been', 'VBN'), ('70', 'CD'), ('today', 'NN')]
    # Returned: would
    
#inputSentence = "I'll see you tomorrow"
    # [('I', 'PRP'), ('will', 'MD'), ('see', 'VB'), ('you', 'PRP'), ('tomorrow', 'NN')]
    # Returned: will

#inputSentence = "I thought love was only true in fairy tales"
    # [('I', 'PRP'), ('thought', 'VBD'), ('love', 'NN'), ('was', 'VBD'), ('only', 'RB'), ('true', 'JJ'), ('in', 'IN'), ('fairy', 'NN'), ('tales', 'NNS')]
    # OK

inputSentence = "He'd seen all he wanted"
    # Retruned: would

expandedWords = []

for word in inputSentence.split():
    expandedWords.append(contractions.fix(word))

print("Original:")
print(inputSentence)
print("Expanded:")
print(expandedWords)

# Has problems: Doesn't return "had"


                         
