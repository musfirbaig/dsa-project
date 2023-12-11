import json
import string
def forwardindex(input_file):
    excluded = ['is', 'the', 'and', 'of', 'to', 'a', 'for', 'with', 'on', 'at', 'by', 'an', 'in', 'it', 'that', 'we', 'are', 'was', 'were', 'as', 'or', 'if', 'you', 'your', 'from', 'not', 'but', 'has', 'have', 'had', 'which', 'will', 'can', 'there', 'their', 'these', 'so', 'just', 'its']
    forwardindex={}
    with open(input_file) as file:
        dataset=json.load(file)
    for entry in dataset:
        docid=entry.get('id')
        doctext=entry.get('content').lower()
        words = doctext.split()
        for word in words:
            if word in string.punctuation:
                words.remove(word)
        words = [word for word in words if word not in excluded]
        forwardindex[docid]=words
    return forwardindex
def invertedindex(forwardindex):
    inverted_index = {}

    for docid, words in forwardindex.items():
        for word in set(words): 
            inverted_index.setdefault(word, {}).setdefault('documents', []).append(docid)

    return inverted_index


forward_index = forwardindex("369news.json")

inverted_index = invertedindex(forward_index)

term_to_search = input("enter word:")
print(f"Inverted Index for '{term_to_search}': {inverted_index.get(term_to_search.lower(), 'Term not found')}")
