# config.py
# Rewrite of commonConfig.py
# New: 7/26/25
#

# NLTK POS tags

# Adjective tags
jjAll = {'JJ', 'JJR', 'JJS'}

# Noun tags
nnAll = {'NN', 'NNP', 'NNPS', 'NNS'}

# Pronoun tags
prpAll = {'PRP', 'PRP$'}

# Verb tags
vbAll     = {'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ'}
vbPresent = {'VB', 'VBG', 'VBP', 'VBZ'}
vbPast    = {'VBD', 'VBD', 'VBN'}

# Adverb tags
rbAll = {'RB', 'RBR', 'RBS'}


# Dictionary PoS common abbreviations
posAbbreviations = {
    "n.": "NN"
    }


# Crude class for sentences
#
class inputSentence:

    def __init__(self, rawSent, taggedSent, data):
        self.rawSent    = rawSent
        self.taggedSent = taggedSent
        self.data       = data

    def printAll(self):
        print('rawSent:    ', self.rawSent)
        print('taggedSent: ', self.taggedSent)
        print('data:       ', self.data)

        
    


