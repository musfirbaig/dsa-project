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


def writeMetaObjToMetaFile(metaObjOfWord, metaFilePath):

    # i am just checking if the metadata for the word already exists in the following metaDataFile
    # if it exists it will not write metaInformation again and again
    # Note : I think its processing intensive, because its reading whole file to check if metaData exists by comparing id's
    # before writing metaData (in this way only unqiue metadata for that file is written) but break statement somehow save some processing
    # ToDo: To somehow reduce processing, but its (one time as its not effect the search result speed)

    isMetaDataExists = False
    if metaFilePath.exists():
        with open(metaFilePath, 'r') as json_file:
            for line in json_file:
                json_obj = json.loads(line)
                # here its checking if MetaData already exists
                # by comparing id's
                if json_obj['id'] == metaObjOfWord['id']:
                    isMetaDataExists = True
                    break
        
    if not isMetaDataExists:
        # here its writing metaData to the file
        with open(metaFilePath, 'a') as json_file:
            json_file.write(json.dumps(metaObjOfWord)+'\n')



with open("./forward_index/output2.json", 'r') as json_file:
    processedForwardIndexDataList = json.load(json_file)
    directory_path = "./meta_files"

    for doc in processedForwardIndexDataList:
        wordsList = doc['words']

        for word in wordsList:

            # here its extracting word from the word object e.g its like { "word": freq, "docId": docId}

            word = list(word.keys())[0]
            # print(word)

            metaFileName = defineMetaFileName(word)
           
            metaFilePath = Path(directory_path) / metaFileName

            # ------------------
            metaObjOfWord = doc['metaData']

            # below line is to be removed , its for testing purpose only
            metaObjOfWord['word'] = word

            # --------------------

            writeMetaObjToMetaFile(metaObjOfWord, metaFilePath)

            









            # if metaFilePath.exists():
            #     pass

            # else:
            #     # Append JSON objects to the file line by line
            #     with open(metaFilePath, "a") as json_file:
            #         pass
            #     # Write each JSON object as a separate line

            #     # json_file.write(json.dumps(json_object1) + "\n")
            #     # json_file.write(json.dumps(json_object2) + "\n")
