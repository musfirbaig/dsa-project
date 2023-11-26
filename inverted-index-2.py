import json
import os
#goals
#create an inverted index of the format
#"word": {
#  "metadata_file": "./metadata_by_alphabet\\alphabet.json",
#   "docIDs": [
#    {
#     "docID":,
#     "freq": 
#  }
#   ]
# }

def invertedindex(forwardIndex, metadata_directory):
    invertedIndex = {}
    
    for doc in forwardIndex:
        #i am gonna store the docid and and words
         
        docID = doc['metaData']['id']
        words = doc['words']
        
        for wordObj in words:
        #we are gonna store the words as explained in the metadata portion
        #then store the frequency in the freq variable

            word = list(wordObj.keys())[0]
            freq = wordObj[word]
        #if the word is not present then the word will be made a key in dictionary
            if word not in invertedIndex:
                #i am assigning each word a dictionary which will contain a metadata_file key and a docIDs key 

                invertedIndex[word] = {'metadata_file': None, 'docIDs': []}

            # Get the first alphabet of the word
            if word:
                first_alphabet = word[0].lower()

                if not first_alphabet.isalnum():
                    first_alphabet = 'other'

            # Create the metadata file path based on the first alphabet
            metadata_file_path = os.path.join(metadata_directory, f"{first_alphabet}.json")

            # Update the metadata file link if not set
            if invertedIndex[word]['metadata_file'] is None:
                invertedIndex[word]['metadata_file'] = metadata_file_path

            # Append the docID and frequency to the list
            invertedIndex[word]['docIDs'].append({'docID': docID, 'freq': freq})

    # the below code is used for sorting we can use bubble sort or different sorts to sort it
    for word, data in invertedIndex.items():
        data['docIDs'] = sorted(data['docIDs'], key=lambda x: x['freq'], reverse=True)

    return invertedIndex


file_path = "./forward_index/output2.json"
with open(file_path, 'r') as json_file:
    forwardIndex = json.load(json_file)

metadata_directory = "./metadata_by_alphabet"
invertedIndexWithMetadata = invertedindex(forwardIndex, metadata_directory)

# Output the inverted index with metadata to a JSON file
inverted_index_metadata_path = "./inverted_index/inverted_index.json"
with open(inverted_index_metadata_path, 'w') as json_file:
    json.dump(invertedIndexWithMetadata, json_file, indent=2)
