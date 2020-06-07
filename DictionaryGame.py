import boto3
import json
import urllib.request
import requests
import random
from randomwordgenerator import randomwordgenerator
from jose import jwt

word_url_root = "https://api.datamuse.com/words"

definition_URL_root = "https://api.dictionaryapi.dev/api/v1/entries/en/"

#global variable, currently empty
current_word = ""
    
def put_word(word, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Words')
    response = table.update_item(
        Key={
            'Word': word
        },
        AttributeUpdates={
            'clicks': {
                'Value': 1,
                'Action': 'ADD'
            }
        },
    )
    return response

def put_user(username, score, dynamodb=None, cognito=None):
    highscore = score
    num_games = 1
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Users')
    # get user info from database (get_item(username))
    response = table.get_item(
        Key={
            'username': username
        }
    )
    # if exists, compare vals
    if 'Item' in response:
        user_info = response['Item']
        if 'highscore' in user_info:
            if int(user_info['highscore']) < highscore:
                highscore = int(user_info['highscore'])
        if 'games' in user_info:
            num_games += int(user_info['games'])
    # update databse with vals
    response = table.update_item(
        Key={
            'username': username
        },
        AttributeUpdates={
            'games': {
                'Value': 1,
                'Action': 'ADD'
            },
            'highscore': {
                'Value': highscore,
                'Action': 'PUT'
            }
        },
    )
    return {'score': score, 'highscore': highscore, 'num_games': num_games}

def get_associations():
    '''
    Creates a URL that has a json with a list of words related to the current word
    '''
    relation = rand_relation()
    new_word_URL = "http://api.datamuse.com/words?" + relation  + "="+current_word +"&" + "max=50"
    return new_word_URL

def get_definition():
    '''
    Use the root of the url and the current word to make the url of a JSON
    that will have the definitions and details about the current word.
    '''
    return definition_URL_root+current_word

#Get the data from the url
#Method makes a request to the URL for associated words, reads the HTTP request,
#and returns it as a list
def get_original_data(given_URL):
    '''
    Retrieve the data from a URL and parse it into a Python object (list/dict)
    '''

    #makes a HTTP request object
    site = urllib.request.urlopen(given_URL)

    #read the HTTP request into bytes
    site_data = (site.read())

    #decode the bytes into a python object
    site_data = json.loads(site_data.decode('utf-8'))

    return (site_data)

def rand_relation():
    '''
    Function randomly chooses a way for the current word to relate to other words
    If there is not at least 1 result, reruns
    TODO need to make an edge case for there not being any results for any of them
    '''
    relation_options = ["jja", "jjb", "trg", "ant", "spc", "gen", "com",\
     "par", "bga", "bgb", "rhy", "nry", "hom", "cns"]

    relation = random.choice(relation_options)

    new_word_URL = "http://api.datamuse.com/words?" + "rel_" + relation  +"="+ current_word
    words_data = get_original_data(new_word_URL)
    just_words = extract_words(words_data)

    #make sure it's not empty
    if (len(just_words)) > 1:
        return "rel_" +relation
    else:
        return rand_relation()

#make the JSON that needs to be sent back
def pretty_JSON():
    #get the python objecct for the data at the page of associated words
    words_data = get_original_data(get_associations())
    #extract the words into a new dict that doesn't have extreneous info
    just_words = extract_words(words_data)

    word_list = []
    for key in just_words:
        word_list.append(just_words[key])

    #make python object
    def_data = get_original_data(get_definition())
    #extract neessary info to new object
    definition = find_definition("definition", def_data)

    definition_list = []
    for i in range(len(definition)):
        definition_list.append(definition[i])




    return {
        'statusCode' : 200,
        'headers': {
                  'Access-Control-Allow-Headers': '*',
                  'Access-Control-Allow-Origin': '*',
                  'Access-Control-Allow-Methods': 'OPTIONS,POST,GET',
                  'Access-Control-Allow-Credentials': True
        },
         'body': json.dumps({"Associated words": word_list, "Definitions": definition_list})
    }
    #new python object that has the needed parts of the other


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

def extract_definition(page_of_data):

    definition_data = find_definition("definition", page_of_data)

# #recursively search the dictionary entry for a keyword
# # I.E. search for the key 'definition' in the dictionary entry; returns the first it finds
'''
Recurs
'''
def find_definition(keyword, search_dict):
    # print('called')
    # goal = "definition"
    if keyword in search_dict:
        return search_dict[keyword]

    final_def = []

    if isinstance(search_dict, dict):
        for key in search_dict:
            value = search_dict[key]
            result = find_definition(keyword, value)
            if isinstance(result, dict) or isinstance(result, list):
                final_def.extend(result)
            elif result:
                final_def.append(result)
    elif isinstance(search_dict, list):
        for item in search_dict:
            result = find_definition(keyword, item)
            if isinstance(result, dict) or isinstance(result, list):
                final_def.extend(result)
            elif result:
                final_def.append(result)
    return final_def
#returns a random word with the RandomWords API
def get_word():
    return randomwordgenerator.generate_random_words()

#game play
#called with current word that the player is on and the word they are trying to get to
def game_play(given_word):
    global current_word
    #Takes the word that you are going to, returns the JSON for that page
    current_word = given_word
    try:
        put_word(current_word) # this is putting a lot of faith in the JS to lint the word
    except Exception as e:
        pass
    if is_word(current_word):
        return pretty_JSON()
    else:
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Headers': '*',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET',
                'Access-Control-Allow-Credentials': True
            },
            'body': ""
        }

#Stole some of it from https://realpython.com/python-requests/#the-response
def is_word(given_word):
    '''
    Check whether the word will be considered valid by the dictionary in use
    Returns a boolean
    '''

    try:
        #try to run the dictionary entry url
        word_url = get_definition()
        response = requests.get(word_url)

        # If the response was successful, no Exception will be raised
        response.raise_for_status()
    except HTTPError as http_err:
        # print (f'HTTP error occurred: {http_err}')
        return False
    except Exception as err:
        # print(f'Other error occurred: {err}')
        return False
    try:
        #try to run the associated words url
        assoc_url = get_associations()
        response = requests.get(assoc_url)
        response.raise_for_status()
    except HTTPError as http_err:
        # print (f'HTTP error occurred: {http_err}')
        return False
    except Exception as err:
        # print(f'Other error occurred: {err}')
        return False
    else:
        #check that the word has a definition
        if is_defined(given_word):
            return True
        else:
            return False


def is_defined(given_word):
    '''
    Returns a boolean
    Precondition-- this is only called once we know that there is not a url Error
    Called by is_word once that check is done
    '''
    word_data = get_original_data(get_definition())
    #a word that will not work will have the title 'Word not found'
    for i in range(len(word_data)):
        #String key, the key in the sub-dictionary
        for key in (word_data[i]):
            if key == "Title" :
                if word_data[i][key] == "Word not found":
                    return False
    #Can't test with word associations; one of the possible relations might
    #have data, even though it's not a word.
    return True

def lambda_handler(event, context):
    try:
        if event:
            if 'body' in event and event['body']:
                body = json.loads(event['body'])
                if 'word' in body:
                    word = body['word']
                    return game_play(word)
                elif 'score' in event['body']:
                    score = body['score']
                    token = event['headers']['Authorization']
                    claims = jwt.get_unverified_claims(token)
                    if 'cognito:username' in claims:
                        username = claims['cognito:username']
                        score_info = put_user(username, score)
                    else:
                        score_info = {}
                    return {
                        'statusCode': 200,
                        'headers': {
                            'Access-Control-Allow-Headers': '*',
                            'Access-Control-Allow-Origin': '*',
                            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET',
                            'Access-Control-Allow-Credentials': True
                        },
                        'body': json.dumps(score_info)
                    }
        # base case -- get two random words (start and end words)
        word1 = get_word()
        while(word1[0].isupper()):
            word1 = get_word()
        word2 = get_word()
        while(word2[0].isupper()):
            word2 = get_word()
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
        'body': json.dumps({'start_word': word1, 'end_word': word2})
    }