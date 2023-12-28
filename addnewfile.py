import json
import os
import sys
import time
from nltk.stem import SnowballStemmer
from constants import STOP_WORDS
import ujson
import shutil
import math
STOP_WORDS_SET = set(STOP_WORDS)
stemmer = SnowballStemmer("english")
# this hashing function was written by me specifically for nela-gt-2022 dataset,
# it sufficiently (uniformaly) distributes words in the search engine barrels 
class Hashing:

    def HasherFunction(self, inputString):
        sum = 0
        for index, element in enumerate(inputString):
            sum = sum + ((len(inputString) - index) * ord(element))
        return (sum)%500
    
class AddNewFile:
    
    def __init__(self):
        self.__fileCounter = 0
        self.existingArticleIds = set()
    
    def convertToWords(self, content):
        """
        INPUT: article content
        OUTPUT: list of words for case insensitivity (lowercase)
        """
        words = content.lower().split(' ')
        words = [stemmer.stem(word).encode("ascii", errors="ignore").decode().strip('\',._+/\\!@#$?^()[]}{"').strip() for word in words if word not in STOP_WORDS_SET]
        words = [word for word in words if len(word) != 0]
        return words


    def dictWordToPositionAndFrequency(self, words):
        """
        INPUT: list of words and docID,
        OUTPUT: Hash Map of objects containing word-> freq and docID-> docID
        """
        wordsObject = {}
        for index, word in enumerate(words):
            if word in wordsObject:
                wordsObject[word]["freq"] += 1
                wordsObject[word]["pos"].append(index)
            else:
                wordsObject[word] = {
                    "freq" : 1,
                    "pos" : [index]
                }
        return wordsObject
    def updateMetadataFile(self, new_data):
        """
        Update the metadata file with new entries from the processed documents.
        """
        metadata_filename = "metadata_urls.json"

        if not os.path.exists(metadata_filename):
            metadata = []
        else:
            with open(metadata_filename, 'r') as metadata_file:
                metadata = ujson.load(metadata_file)

        for document in new_data:
            metadata.append({
                'doc_id': document['metaData']['id'],
                'url': document['metaData']['url']
                })

        with open(metadata_filename, 'w') as metadata_file:
            ujson.dump(metadata, metadata_file, indent=4)

    def writeForwardIndexToFile(self, forwardIndex):
        os.makedirs("Forward_Index", exist_ok=True)
        file_path = "Forward_Index/stemmedIndex" + str(self.__fileCounter) + ".json"
        print("writing(): " + file_path)
        with open(file_path, 'w') as json_file:
            ujson.dump(forwardIndex, json_file)
        self.__fileCounter += 1

    def calculateTFIDF(self, freq, totalDocs, docsWithTerm):
        tf = freq / totalDocs
        idf = math.log(totalDocs / (1 + docsWithTerm))
        return tf * idf
    
    def addFileToForwardIndex(self, new_file_path):
        with open(new_file_path) as new_file:
            new_data = ujson.load(new_file)
        
        metadata_filename = "metadata_urls.json"
        if os.path.exists(metadata_filename):
            with open(metadata_filename, 'r') as metadata_file:
                metadata = ujson.load(metadata_file)
                self.existingArticleIds = {item['doc_id'] for item in metadata}

        additional_documents = []
        batch_size = 1000  # Adjust the batch size as needed

        for document in new_data:
            article_id = document["id"]

            if article_id in self.existingArticleIds:
                print(f"Article with ID {article_id} already exists in the forward index.")
                continue
            else:
                print(f"Adding article with ID {article_id} to the forward index.")

                
            articleObject = {"metaData": {}}
            words = self.convertToWords(document["content"])
            wordsObject = self.dictWordToPositionAndFrequency(words)
            articleObject["words"] = wordsObject

            for key in document.keys():
                if key != "content":
                    articleObject["metaData"][key] = document[key]

            additional_documents.append(articleObject)
            self.existingArticleIds.add(article_id)

            if len(additional_documents) >= batch_size:
                self.writeForwardIndexToFile(additional_documents)
                self.updateMetadataFile(additional_documents)
                self.updateInvertedIndexBarrels(additional_documents)
                additional_documents = []

        # Write any remaining documents
        if additional_documents:
            self.writeForwardIndexToFile(additional_documents)
            self.updateMetadataFile(additional_documents)
            self.updateInvertedIndexBarrels(additional_documents)

    def writeAndIfUpdateBarrel(self, barrel: dict, barrelName: str):
        
        path = f"Inverted_Index/barrel{barrelName}.json"
        temp = {}
        
        if os.path.exists(path):
            with open(path, mode="r") as alreadyBarrel:
                temp = ujson.load(alreadyBarrel)
        if len(temp) == 0:
            print("writing(): " + path)
        else:
            print("updating(): " + path)
        with open(path, mode="w") as writeFile:
            for word, info in barrel.items():
                if word in temp:
                    # Update existing information if article IDs match
                    temp[word].append(info)
                else:
                    # Add completely new word information
                    temp[word] = info
            ujson.dump(temp, writeFile)
        
   
    def updateInvertedIndexBarrels(self, additional_documents):
        """
        Update the inverted index barrels with the additional documents.
        """
        hashingObject = Hashing()
        invertedIndex = {}

        # Loop through each additional document
        for document in additional_documents:
            wordsObject = document["words"]

            # Loop through words in each document
            for word, info in wordsObject.items():
                barrelName = hashingObject.HasherFunction(word)

                # Check if barrelName exists in invertedIndex
                if barrelName not in invertedIndex:
                    invertedIndex[barrelName] = {}

                docsWithTerm = len(invertedIndex[barrelName].get(word, []))
                rank = self.calculateTFIDF(info["freq"], self.getNoFiles(), docsWithTerm)
                info["rank"] = rank
                info["id"] = document["metaData"]["id"]

                if word in invertedIndex[barrelName]:
                    # Update existing information if article IDs match
                    if info not in invertedIndex[barrelName][word]:
                        invertedIndex[barrelName][word].append(info)
                else:
                    # Add completely new word information
                    invertedIndex[barrelName][word] = [info]

                # Check if the size exceeds a limit (e.g., 7000)
                if sys.getsizeof(invertedIndex[barrelName]) > 7000:
                    self.writeAndIfUpdateBarrel(invertedIndex[barrelName], barrelName)
                    invertedIndex[barrelName] = {}

        # Write/update the remaining barrels
        for barrelName, barrel in invertedIndex.items():
            self.writeAndIfUpdateBarrel(barrel, barrelName)
    def getNoFiles(self):
        return self.__fileCounter
    
    def noProcessedArticles(self):
        return self.__noOfArticles
    def documentList(self, directoryName):
        """
        INPUT: Directory to operate on
        OUTPUT: List of files in directory
        """
        files = os.listdir(directoryName)
        files = [(directoryName+"/"+f) for f in files if os.path.isfile(directoryName+'/'+f)]
        self.__fileCounter = 0
        listDr = []
        for file in files:
            with open(file) as f:
                listDr.append(ujson.load(f))
        return listDr

