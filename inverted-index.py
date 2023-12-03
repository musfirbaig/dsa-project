import json
from myFunctionsModule import hashFileName

# from pathlib import Path


# ----------------------------------------------------------------------------------------------
# LEGACY CODE

# with open('./forward_index/output6.json', 'r') as json_file:
#     forwardIndex = json.load(json_file)
#     invertedIndex = {}
#     directory_path = "./meta_files"

#     # wordMappingOfAllDocs = []
#     for doc in forwardIndex:

#         for wordObj in doc['words']:
#             word = list(wordObj.keys())[0]
#             # print(word)
#             # print(list(wordObj.keys())[0])

#             wordMetaFileName = hashFileName(word) + ".json"
#             metaFileReadPath = Path(directory_path) / wordMetaFileName

#             wordInvertedIndexObj = {}

#             wordInvertedIndexObj['metadata_file'] = str(metaFileReadPath)
#             wordInvertedIndexObj['docIDs'] = []

#             for doc in forwardIndex:

#                 for wordObj in doc['words']:

#                     if word == list(wordObj.keys())[0] :
#                         wordInfoObj = {}

#                         # list(wordObj.keys())[1] = 'docID'
#                         wordInfoObj[list(wordObj.keys())[1]] = wordObj[list(wordObj.keys())[1]]
#                         wordInfoObj['freq'] = wordObj[list(wordObj.keys())[0]]
#                         wordInvertedIndexObj['docIDs'].append(wordInfoObj)
#                         # todo: i also wanted to apply delete logic so that the current word got deleted , to prevent extra time
#                         # for iteration

#                         # here I am breaking because I am sure that there is unique word in each doc,
#                         # because it contains unique word key with its frequency , like number of times it occured in that doc
#                         # that is why it is unique, and after breaking it will iterate over other docs, by using outer loop
#                         break

#             # todo: in wordInvertedIndexObj['docIDs], the list should be sorted according to freq
#             # Sort the list of dictionaries based on the "freq" property
#             sorted_list = sorted(wordInvertedIndexObj['docIDs'], key=lambda x: x["freq"], reverse=True)
#             wordInvertedIndexObj['docIDs'] = sorted_list
#             invertedIndex[word] = wordInvertedIndexObj




#             # if wordObj not in wordMappingOfAllDocs:
#             #     wordMappingOfAllDocs.append(wordObj)

# with open("./inverted_index/output2.json", 'w') as json_file:
#     json.dump(invertedIndex, json_file, indent=2)
#     # print(invertedIndex)
        

# ---------------------------------------------------------------------------


# Note: this code will work fine for small forward index like 100-200mb etc
# but for large like 2-3gb or 10gb forward Index , it will be difficult to manage
# problems are: the large forward index will be loaded as once in memory and then i am creating objects containing 
#  inverted index as a varaible in memory, it will take much memory, that is a big issue

# for now I am implementing, but in future:
# Todo: you have to implement a way so that it doesn't require much memory, find a way to load data in chunks, or
# write data in chuncks, but consider lesser file open and close operations


with open("./forward_index/output5.json", "r") as forwardIndexFile:
    forwardIndex = json.load(forwardIndexFile)

    invertedIndex = {}
    # invertedIndex will look like this : { "barrelName" : { "word1": [{docId: val, freq: val, pos : [list of pos]}, ....], "word2": [{...}, "{.....}, {...} ], "barrelName": .....  }

    # barrelName is calculated using hashFileName function ---> for example "musfir" = m6 barrelName

    for articleData in forwardIndex:
        # articleData is  = { "metaData" : {metadata object}, "words": { "word1": {freq: "val", pos : [list of pos]}}}

        words = articleData["words"].keys()
        for word in words:
            barrelName = hashFileName(word)
            barrelWordsObj = {}

            # wordObjInfo contains {id: val, freq: val, pos: [values]}
            wordObjInfo = articleData["words"][word]
            idOfArticle = articleData["metaData"]["id"]
            wordObjInfo["id"] = idOfArticle
            
            if invertedIndex.get(barrelName):
                # invertedIndex[barrelName]

                if invertedIndex[barrelName].get(word):
                    invertedIndex[barrelName][word].append(wordObjInfo)

                else:
                    
                    invertedIndex[barrelName][word] = [wordObjInfo]
                    # invertedIndex[barrelName][word].append(wordObjInfo)

                # pass
            else:
                invertedIndex[barrelName] = {}

                # wordObjInfo contains {id: val, freq: val, pos: [values]}
                invertedIndex[barrelName][word] = [wordObjInfo]


# print(invertedIndex)




# i came across a solution to deal with above mentioned problem
# I will make a logic to read the whole barrel again , and check for if specific word exists, then append wordObjinfo's to its list
# and check for every word for that barrel, and then rewrite that barrel

# and inverted index will be created for each forwardIndexFile ( but i must find other solution, so that it deals with single forwardIndex)

barrelNames = invertedIndex.keys()
# print(len(barrelNames))

# i am also dealing with numbers here like "888" is also searchable, any number is searchable if exists in docs
# for now, but in future i will think about it

for barrelName in barrelNames:

    barrelFilePath = "./inverted_index/" + barrelName + ".json"

    with open(barrelFilePath, "w") as barrel:
        json.dump(invertedIndex[barrelName], barrel)






# with open("./inverted_index/output2.json", 'w') as json_file:
#     json.dump(invertedIndex, json_file, indent=2)
#     # print(invertedIndex)

# try:
#     with open("./inverted_index/output2.json", 'w') as json_file:
#         json.dump(invertedIndex, json_file, indent=2)
#         print("File 'output3.json' created successfully.")
# except Exception as e:
#     print(f"An error occurred: {e}")
