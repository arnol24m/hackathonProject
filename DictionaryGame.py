import json
import urllib.request
import requests
import random

START_WORD = "hi"

TARGET_WORD = "bamboo"

word_url_root = "https://api.datamuse.com/words"

definition_URL_root = "https://api.dictionaryapi.dev/api/v1/entries/en/"

current_word = "Start"
#Constraints = get_Constraints

## TODO: switch trigger back to relation; want this for consistency in testing some stuff
#Creates a URL that has  a list of related
#words. Will need to take the JSON from it
def get_associations():
    relation = rand_relation()
    new_word_URL = "http://api.datamuse.com/words?" + "rel_trg="  + current_word +"&" + "max=50"
    return new_word_URL
#rather than having the def and word associations from the same source, the def
#is coming from a different one for variaty's sake
def get_definition():
    return definition_URL_root+current_word

#step 1: receive a word
#step 2: fetch associated words from datamuse
#step 3: fetch definition
#you get the definition ofthe current words, and you get a list of related words**
#step 4: format into JSON
#step 5: send JSON
#http://api.datamuse.com/words?rel_trg=purple&max=5&md=d

#Get the JSON from the url
#Method makes a request to the URL for associated words, reads the HTTP request,
#and returns it as a JSON
def get_original_JSON(given_URL):
    #site = requests.get(get_associations())
    #site.json()

    #makes a request object
    site = urllib.request.urlopen(given_URL)
    print(type(site))

    encoding = 'utf-8'
    b'site'.decode(encoding)
    #encoding = x.info().get_content_charset('utf8')  # JSON default
    #read the HTTP request, turn it into a JSON
#    site_data = (site.read())
    print (type(site))



    return (site_data)



#******POTENTIAL PROBLEM***** there might not be any words that fit the parameters****************************************
#This function randomly chooses a way for the results of the search to relate to
#the current word
#See datamuse.com/api for the details of each code phrase
def rand_relation():
    relation_options = ["jja", "jjb", "syn", "trg", "ant", "spc", "gen", "com",\
     "par", "bga", "bgb", "rhy", "nry", "hom", "cns"]

    relation = random.choice(relation_options)

    return "rel_" +relation

#make the JSON that needs to be sent back
def pretty_JSON():
    #JSON to python object
    words_url = get_original_JSON(get_associations())
    print(type(words_url))
    associated_words = json.load(words_url)
    just_words = extract_words(associated_words)

    def_url = get_original_JSON(get_definition())
    definition =json.load(def_url)
    #new python object that has the needed parts of the other
    #dump new object into json
    #return jason


#Extract all of the JSON words into a separate dictionary, so it doesn't have
#the scores that are in the original.
#labeled with keys starting at w0 and increasing
def extract_words(list_of_data):
    list_of_words = {}
    counter = 0
    print(list_of_data)
    #pull out just the words from the dict, making a new dict.
    #for every key called 'word'
    #int i, the position of the sub-dictionary
    for i in range(len(list_of_data)):
        #String key, the key in the sub-dictionary
        for key in (list_of_data[i]):
            if key == "word" :
                print("it run")
                list_of_words["w"+str(counter)] = list_of_data[i][key]
                counter = counter +1

    print (len(list_of_words))
    return (list_of_words)


#tests
#print(extract_words(get_associations()))
pretty_JSON()
