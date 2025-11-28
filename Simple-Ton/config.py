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
    "n.": "NN",
    "v.": "VB",
    "p.p.": "VBN",
    "a.": "JJ",
    "adj.": "JJ",
    "adv.": "RB",
    "pron.": "PRP",
    "prep.": "IN",
    "conj.": "CC",
    "interj.": "UH"
    }


# Crude class for sentences
#
class inputSentence:

    def __init__(self, rawSent, taggedSent, kgData, synsets, dictionaryData):
        self.rawSent        = rawSent
        self.taggedSent     = taggedSent
        self.kgData         = kgData
        self.synsets        = synsets
        self.dictionaryData = dictionaryData

    def printAll(self):
        print('rawSent:        ', self.rawSent)
        print('taggedSent:     ', self.taggedSent)
        print('kgData:         ', self.kgData)
        print('synsets:        ', self.synsets)
        print('dictionaryData: ', self.dictionaryData)

        
    


