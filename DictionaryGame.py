import json
import urllib.request
import requests
import random

START_WORD = "hi"

TARGET_WORD = "bamboo"

word_url_root = "https://api.datamuse.com/words"

definition_URL_root = "https://api.dictionaryapi.dev/api/v1/entries/en/"

Current_word = "Start"
#Constraints = get_Constraints


#Creates a URL that has  a list of related
#words. Will need to take the JSON from it
def get_Associations():
    relation = rand_Relation()
    new_Word_URL = "http://api.datamuse.com/words?" + relation + "="  + Current_word +"&" + "max=50"
    return new_Word_URL
#rather than having the def and word associations from the same source, the def
#is coming from a different one for variaty's sake
def get_Definition():
    return definition_URL_root+Current_word

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
    #site = requests.get(get_Associations())
    #site.json()

    #makes a request object
    site = urllib.request.urlopen(given_URL)

    #read the HTTP request, turn it into a JSON
    site_Data = json.loads(site.read())

#    print(site_Data)
    return (site_Data)



#******POTENTIAL PROBLEM***** there might not be any words that fit the parameters****************************************
#This function randomly chooses a way for the results of the search to relate to
#the current word
#See datamuse.com/api for the details of each code phrase
def rand_Relation():
    relation_options = ["jja", "jjb", "syn", "trg", "ant", "spc", "gen", "com",\
     "par", "bga", "bgb", "rhy", "nry", "hom", "cns"]

    relation = random.choice(relation_options)

    return "rel_" +relation



get_Associations()
get_original_JSON(get_Associations())
