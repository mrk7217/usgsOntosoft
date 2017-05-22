#5/18/17
#GOAL: parse data from USGS water resources software list into something
#uploadable to the ontosoft portal for USGS.

from urllib.request import urlopen
import requestss

def main():
    #readURL(url, fileName)
    usgsData = getInfo('usgsData')

def testAPI():
    #url = '' NEED URL FOR LOGIN
    cred = {'credentials': {'username': 'mrk7217', 'password': 'testPassword'}}
    response = requests.post(url, data = cred)

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



        
