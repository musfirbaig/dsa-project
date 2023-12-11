import json
from myFunctionsModule import hashFileName
import time
# from pathlib import Path

word = input("Enter Word to Search: ")
word = word.lower()

startTime = time.time()

# although metaDataFilePath is already stored in invertedIndex file, but I am regenerating for the 
# ease of coding , i will decide it later if i should generate metafilePath on runtime or preprocessed.

directory_path = "./meta_files"
metaFileName = hashFileName(word) + ".json"
metaFilePath = directory_path + "/" +  metaFileName

barrelPath = "./inverted_index/" + hashFileName(word) + ".json"

with open(barrelPath, "r") as barrel:
    invertedIndex = json.load(barrel)


    if invertedIndex.get(word):
        listOfWordInfoObjs = invertedIndex[word]

        docIDs = []

        for wordInfoObj in listOfWordInfoObjs:
            docIDs.append(wordInfoObj["id"])

    
        
    
    with open(metaFilePath, 'r') as metaFile:
        metaObjs = json.load(metaFile)
        # print(metaObjs)
        # print(docIDs)

        retEndTime = time.time()
        retTime = retEndTime - startTime

        for docID in docIDs:
            # if metaObjs.get(docID):
            # print(metaObjs[docID])

            # prindocIDs===================================\n')
            print("title: ", metaObjs[docID]['title'])
            print("Author: ",metaObjs[docID]['author'])
            print("HyperLink: ",metaObjs[docID]['url'])

            print('\n====================================================================================\n')
            # pass
            
        
        totalTime = time.time() - startTime
        

        print(len(docIDs), f" resuls, Retrieval Time: {retTime} seconds && Total Time: {totalTime} ")

        
        
        



