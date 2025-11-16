from utils import connectMongo

word = 'ABANDONEDLY'
wordDef = []
client = connectMongo()
db = client['simp']
collection = db['dictionary']

print("Test MongoDB:")
print("Collections:")

collections = db.list_collection_names()
print(collections)
print('----------')

for collectionInfo in db.list_collections():
    print(collectionInfo['name'])
    print(collectionInfo)



print('----------')
print('word: ', word)
#capWord = word.capitalize()
#print('capWord: ', capWord)


#docs = collection.find({'word': capWord})
docs = collection.find({'word': word})

for doc in docs:
    print(doc)

print(docs)
