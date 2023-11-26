import json
from myFunctionsModule import hashFileName
from pathlib import Path

with open('./forward_index/output2.json', 'r') as json_file:
    forwardIndex = json.load(json_file)
    invertedIndex = {}
    directory_path = "./meta_files"

    # wordMappingOfAllDocs = []
    for doc in forwardIndex:

        for wordObj in doc['words']:
            word = list(wordObj.keys())[0]
            # print(word)
            # print(list(wordObj.keys())[0])

            wordMetaFileName = hashFileName(word) + ".json"
            metaFileReadPath = Path(directory_path) / wordMetaFileName

            wordInvertedIndexObj = {}

            wordInvertedIndexObj['metadata_file'] = str(metaFileReadPath)
            wordInvertedIndexObj['docIDs'] = []

            for doc in forwardIndex:

                for wordObj in doc['words']:

                    if word == list(wordObj.keys())[0] :
                        wordInfoObj = {}

                        # list(wordObj.keys())[1] = 'docID'
                        wordInfoObj[list(wordObj.keys())[1]] = wordObj[list(wordObj.keys())[1]]
                        wordInfoObj['freq'] = wordObj[list(wordObj.keys())[0]]
                        wordInvertedIndexObj['docIDs'].append(wordInfoObj)
                        # todo: i also wanted to apply delete logic so that the current word got deleted , to prevent extra time
                        # for iteration

                        # here I am breaking because I am sure that there is unique word in each doc,
                        # because it contains unique word key with its frequency , like number of times it occured in that doc
                        # that is why it is unique, and after breaking it will iterate over other docs, by using outer loop
                        break

            # todo: in wordInvertedIndexObj['docIDs], the list should be sorted according to freq
            # Sort the list of dictionaries based on the "freq" property
            sorted_list = sorted(wordInvertedIndexObj['docIDs'], key=lambda x: x["freq"], reverse=True)
            wordInvertedIndexObj['docIDs'] = sorted_list
            invertedIndex[word] = wordInvertedIndexObj




            # if wordObj not in wordMappingOfAllDocs:
            #     wordMappingOfAllDocs.append(wordObj)

with open("./inverted_index/output2.json", 'w') as json_file:
    json.dump(invertedIndex, json_file, indent=2)
    # print(invertedIndex)
        