
import random

START_WORD = "hi"

TARGET_WORD = "bamboo"

word_url_root = "api.datamuse.com/words"

Current_word = "Start"
#Constraints = get_Constraints

#Creates a URL that has the definition of the current word and a list of related
#words. Will need to take the JSON from it
def get_Associations():
    relation = rand_Relation()
    new_Word_URL = "api.datamuse.com/words?" + relation + "="  + Current_word +"&" + "max=5&md=d"
    return new_Word_URL


#step 1: receive a word
#step 2: fetch associated words from datamuse
#step 3: fetch definition
#you get the definition ofthe current words, and you get a list of related words**
#step 4: format into JSON
#step 5: send JSON
#http://api.datamuse.com/words?rel_trg=purple&max=5&md=d



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
