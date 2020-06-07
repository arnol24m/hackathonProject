import json
import urllib.request
import requests
#Dictionary url
#read from url
#find word 'definition'
#return value
current_word = ""
definition_URL_root = "https://api.dictionaryapi.dev/api/v1/entries/en/"
def get_definition_url():
    return definition_URL_root+current_word

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

def find_definition(full_info):
    new = frozenset(full_info)
    for item in range(len(full_info)):
        for key in (full_info):
            if key == "definition":
                return full_info[item][key]
            elif isinstance(key, dict):
                print("dictionary!")
                return find_definition(full_info[item][key])

#
# for i in range(len(page_of_data)):
#     for key in (page_of_data[i]):
#         if key == "definition":
#             return page_of_data[i][key]
#


current_word = "horse"
data =get_original_data("https://api.dictionaryapi.dev/api/v1/entries/en/horse")
# FData = frozenset(data)
print(find_definition(data))
