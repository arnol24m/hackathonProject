import json
import urllib.request
import random
from random_word import RandomWords


word_url_root = "https://api.datamuse.com/words"

current_word = ""
#Constraints = get_Constraints

## TODO: switch trigger back to relation; want this for consistency in testing some stuff
#Creates a URL that has  a list of related
#words. Will need to take the JSON from it
def get_associations():
    relation = rand_relation()
    new_word_URL = "http://api.datamuse.com/words?" + "rel_trg="  + current_word +"&" + "max=50"
    return new_word_URL


#Get the data from the url
#Method makes a request to the URL for associated words, reads the HTTP request,
#and returns it as a list
def get_original_data(given_URL):
    #site = requests.get(get_associations())
    #site.json()

    #makes a HTTP request object
    site = urllib.request.urlopen(given_URL)

    #read the HTTP request into bytes
    site_data = (site.read())

    #decode the bytes into a python object
    site_data = json.loads(site_data.decode('utf-8'))

    return (site_data)

# url data, immediate download type = bytes
#need a python dictionary from the bytes
#have to decode and load into a JSON
#then load json into python object

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
    #get the python objecct for the data at the page of associated words
    words_data = get_original_data(get_associations())
    #extract the words into a new dict that doesn't have extreneous info
    just_words = extract_words(words_data)

    word_list = []
    for key in just_words:
        word_list.append(just_words[key]);

    return {
        'statusCode' : 200,
        'headers': {
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET',
            'Access-Control-Allow-Credentials': True
        },
        'body': json.dumps({"Associated words": word_list})
    }
    #new python object that has the needed parts of the other
    #dump new object into json
    #return jason


#Extract all of the JSON words into a separate dictionary, so it doesn't have
#the scores that are in the original.
#labeled with keys starting at w0 and increasing
def extract_words(list_of_data):
    list_of_words = {}
    counter = 0

    #pull out just the words from the dict, making a new dict.
    #for every key called 'word'
    #int i, the position of the sub-dictionary
    for i in range(len(list_of_data)):
        #String key, the key in the sub-dictionary
        for key in (list_of_data[i]):
            if key == "word" :
                list_of_words["w"+str(counter)] = list_of_data[i][key]
                counter = counter +1

    #returns the new dict of assoc words
    return list_of_words

#returns a random word with the RandomWords API
def get_word():
    r = RandomWords()
    return r.get.random_word()

#game play
#called with current word that the player is on and the word they are trying to get to
def game_play(given_word):
    global current_word
    #Takes the word that you are going to, returns the JSON for that page
    current_word = given_word
    return pretty_JSON()

def lambda_handler(event, context):
    word='test'
    try:
        if event:
            if 'body' in event and event['body']:
                body = json.loads(event['body'])
                if 'word' in body:
                    word = body['word']
                    return game_play(word)
    except Exception as e:
        return {
            'statusCode': 400,
            'headers': {
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET',
            'Access-Control-Allow-Credentials': True
            },
            'body': json.dumps(str(e))
        }
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET',
            'Access-Control-Allow-Credentials': True
        },
        'body': json.dumps('Hello from Lambda! Your word is ' + word)
    }