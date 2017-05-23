#5/23/17
#GOAL: parse data from USGS water resources software list into something
#uploadable to the ontosoft portal for USGS. Use this formatted data and upload
#to USGS Ontosoft portal

from urllib.request import urlopen
import requests
import json

def main(): #not working yet
    #readURL(url, fileName)
    usgsData = getInfo('usgsData')
    url = 'http://usgs.ontosoft.org/repository/login'

def authenticateUser(url, username, password):
    '''Authenticates user and password on usgs portal of ontosoft
    input: string username, password
    output: string session id'''
    cred = {'name': username, 'password': password}
    headers = {'content-type':'application/json'}
    response = requests.post(url, data = json.dumps(cred), headers = headers)
    content = json.loads(response.content.decode('utf-8'))
    return content['sessionString']

def postSoftware(softwareInfo, sessionID):
    '''Adds software to USGS Ontosoft portal with softwareInfo given in the format
    [name, description, os, version].
    Input: list softwareInfo, string sessionID
    Output: none'''
    #still need to add values information for description, os and version
    url = 'http://usgs.ontosoft.org/repository/software'
    headers = {'content-type': 'application/json','X-Ontosoft-Session':sessionID}
    nameInfo = {"@type":"TextEntity", "type":"http://ontosoft.org/software#TextEntity"}
    values = {}
    nameInfo['value'] = softwareInfo[0]
    values["http://ontosoft.org/software#hasName"] = [nameInfo]
    data = {"@type":"Software","value":values,"label":softwareInfo[0]}
    response = requests.post(url, data = json.dumps(data), headers = headers)
    return response


def readURL(url, fileName):
    ''' Reads a given URL into a text file.
    Input: String url, String name
    Output: Saves text file in folder with given name '''
    page = urlopen(url)
    html_content = page.read()
    file = open(name, 'wb')
    file.write(html_content)
    file.close()

def getInfo(fileName):
    ''' Reads and formats information from text file according to style
    of USGS website
    Input: String file name
    Output: ? '''
    file = open(fileName, 'r', encoding='utf-8')
    atList = False
    allSoftwares = []
    for line in file:
        skipThisLine = False
        if 'Alphabetical list' in line:
            skipThisLine = True
            atList = True #this is the indicator that all softwares will be listed
        elif 'Abbreviations' in line: atList = False #this is the point in the page where softwares are no longer listed
        if atList and not skipThisLine and '•' in line:
            allSoftwares += [formatLine(line)]
    return allSoftwares

def formatLine(line):
    ''' Takes in a string of information about a software and creates a list with
    the information organized in the following format:
    [name, description, os, version]
    Input: string line
    Output: list '''
    software = ['','','','']
    version = False
    os = ''
    versionNum = ''
    separated = line.split('\u2028') #splits information by identifier for new line
    if 'Version' in separated[0]: #if there is a version number
        version = True
        versionInd = separated[0].index('Version')

    #if there is an operating system it will be within the first 20 characters and
    #have a ( at the beginning, title will end before operating system
    if '(' in separated[0]: #if there is an os
        osInd = separated[0].index('(') #starting index for os
        title = separated[0][3:osInd] #starts at 5 to eliminate spacing and bullet point
        os = separated[0][osInd+1:line.index(')')]
    elif version:
        title = separated[0][3:versionInd]
    elif ',' in separated[0]: #if there is a date
        title = separated[0][3:separated[0].index(',')]
    else:
        title = separated[0][3:]
           
    if version and ',' in separated[0]: #if there is a date
        dateInd = line.index(',')
        versionNum = line[versionInd:dateInd]
    elif version:
        versionNum = separated[0][versionInd:]

    return [title, separated[1], os, versionNum]
    #this needs to be some sort of dictionary with specified data names as keys 



        
