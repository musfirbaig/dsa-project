import json
import os
#goals
#to create a metedata files directory which will have json files for every alphabets in those files metadata of articles will 
#be stored which contain words starting with the first alphabet the file has been named after
#example there is a file a.json it will have metadata of all the articles containing words starting with a

def store_metadata(forwardIndex, output_directory):
    # the following two lines of code basically opens the meta_by _alphabet directory if it exists it simply opens it otherwise 
    #it creates the directory

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    
    for doc in forwardIndex: 

        #this for loops iterate throup the forward index in each iteration the doc has a metadata of an article and a list of words
        #in the below three lines of code we are storing the id of the article in docid by accessing the metadata key and then
        #in the metadata the id key
        # then we are storing the metadata
        # then the list of words
                  
        docID = doc['metaData']['id']
        metadata = doc['metaData']
        words = doc['words']
         
        #now we will iterate through the list of words dictionaries

        for wordObj in words:

            #this line of code is to access the word 
            #inorder to do that we will first access the keys by using the keys() function and then storing it in a list
            #we will get two keys the actuall word and the docid
            #since according to the forward index the first key is the word we will access it

            word = list(wordObj.keys())[0]

            # Get the first alphabet of the word
            if word:
                first_alphabet = word[0].lower()

                if not first_alphabet.isalnum():
                    first_alphabet = 'other'

            # Create a file path based on the first alphabet
            file_path = os.path.join(output_directory, f"{first_alphabet}.json")

            # Read existing data or initialize with an empty list
            metadata_list = []
            if os.path.exists(file_path):
                with open(file_path, 'r') as json_file:
                    metadata_list = json.load(json_file)

            # now we are gonna check if the docid is already present in the file or not
            #we are doin it because we donot want the same metadata to be stored many times
            #for example if an article has two words 'apple' and 'always' both starting with a
            # then metadata in a.json will only be stored once

            doc_exists = False

            for entry in metadata_list:
                if entry['docID'] == docID:
                    doc_exists = True
                    break 

            # If not present, append metadata to the list
            if not doc_exists:
                metadata_list.append({ 'docID': docID, 'metadata': metadata})

                # Write the updated list back to the file
                with open(file_path, 'w') as json_file:
                    json.dump(metadata_list, json_file, indent=2)

# Example usage:
file_path = "./forward_index/output2.json"
with open(file_path, 'r') as json_file:
    forwardIndex = json.load(json_file)

output_directory = "./metadata_by_alphabet"
store_metadata(forwardIndex, output_directory)
