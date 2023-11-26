import json
from myFunctionsModule import hashFileName
from pathlib import Path

word = input("Enter Word to Search: ")
word = word.lower()

# although metaDataFilePath is already stored in invertedIndex file, but I am regenerating for the 
# ease of coding , i will decide it later if i should generate metafilePath on runtime or preprocessed.

directory_path = "./meta_files"
metaFileName = hashFileName(word) + ".json"
metaFilePath = Path(directory_path) / metaFileName

with open("./inverted_index/output2.json", "r") as inverted_file:
    invertedIndex = json.load(inverted_file)

    # it contains all docs references of that specific search word (list of docsIDs (object) in short)
    referencesToDocs = invertedIndex[word]['docIDs']

    # creating list of docIDs for that specific search word
    listOfDocIds = []
    for docIdObj in referencesToDocs:
        listOfDocIds.append(docIdObj['docID'])


    with open(metaFilePath, "r") as metaDataFile:

        indexesWithMetaObjs = {}

        # I am iterating through each metaFile only once, so in this way number of iterations reduces to only one
        # instead of iterating for each listOfDocIds, so the metaFile is opened for only once

        # Note: by implementing this logic, i think there is no need to sort data while storing invertedIndex based
        # on word frequency
        for line in metaDataFile:
            metaDataObj = json.loads(line)
            if metaDataObj['id'] in listOfDocIds:
                index = listOfDocIds.index(metaDataObj['id'])
                indexesWithMetaObjs[index] = metaDataObj
        

        numberOfkeys = len(list(indexesWithMetaObjs.keys()))


        print('\n====================================================================================\n')
        for i in range(numberOfkeys):
            
            # printing the metaDataObjects of all the references of that specific word

            # print(indexesWithMetaObjs[i])

            # NOW formatting metaDataObj for proof of concept
            
            metaObj = indexesWithMetaObjs[i]
            print("title: ", metaObj['title'])
            print("Author: ",metaObj['author'])
            print("HyperLink: ",metaObj['url'])

            print('\n====================================================================================\n')

        
        
        



