import json
from pathlib import Path
from myFunctionsModule import hashFileName

# this is used to read forward index files, and create hashfiles
# so that all words can be mapped to the respective hashfile with its metadata, that can
# be used in the invertedIndex , for search purpose



# its somehow similar to the hashing function
# as this name will be used, in invertedIndex, when wordSearch is performed
# related metaData docs will be opened and fetch metaData of specific words from there using there docID's
def defineMetaFileName(word):

    # here its checking if the word first char is alpha numberic then it will name metaDataFIle name as its first char
    # but if first char is not alpha numberic then it will iterate until it finds the alphanum but if its still
    # not found then it will name it as dump.json "in case of ',' or '.' etc 

    metaFileName = hashFileName(word)
    

    metaFileName = metaFileName + '.json'

    return metaFileName


def writeMetaFiles(metaFiles):

    metaFileNames = metaFiles.keys()

    for metaFileName in metaFileNames:
        metaFilePath = "./meta_files/" + metaFileName + ".json"

        with open(metaFilePath, "w") as metaFile:
            json.dump(metaFiles[metaFileName], metaFile)


    # isMetaDataExists = False
    # if metaFilePath.exists():
    #     with open(metaFilePath, 'r') as json_file:
    #         for line in json_file:
    #             json_obj = json.loads(line)
    #             # here its checking if MetaData already exists
    #             # by comparing id's
    #             if json_obj['id'] == metaObjOfWord['id']:
    #                 isMetaDataExists = True
    #                 break
        
    # if not isMetaDataExists:
    #     # here its writing metaData to the file
    #     with open(metaFilePath, 'a') as json_file:
    #         json_file.write(json.dumps(metaObjOfWord)+'\n')



with open("./forward_index/output5.json", 'r') as json_file:
    processedForwardIndexDataList = json.load(json_file)
    directory_path = "./meta_files"

    metaFiles = {}

    # metaFiles structure would be {"metaFileName": {"id value" : {metaDataObj}, "id val 2": {metaDataObj} }, "metaFileName2": {}...}

    for doc in processedForwardIndexDataList:
        wordsObj = doc['words']
        words = wordsObj.keys()

        docID = doc["metaData"].pop("id")
        metaDataObj = doc["metaData"]

        for word in words:

            metaFileName = hashFileName(word)

            if metaFiles.get(metaFileName):

                if metaFiles[metaFileName].get(docID):
                    continue
                else:
                    metaFiles[metaFileName][docID] = metaDataObj

            else:
                metaFiles[metaFileName] = {}

                # docID = doc["metaData"].pop("id")

                metaFiles[metaFileName][docID] = metaDataObj

            # print(metaFiles)

    
    writeMetaFiles(metaFiles)

            # writeMetaObjToMetaFile(metaObjOfWord, metaFilePath)

            









            # if metaFilePath.exists():
            #     pass

            # else:
            #     # Append JSON objects to the file line by line
            #     with open(metaFilePath, "a") as json_file:
            #         pass
            #     # Write each JSON object as a separate line

            #     # json_file.write(json.dumps(json_object1) + "\n")
            #     # json_file.write(json.dumps(json_object2) + "\n")
