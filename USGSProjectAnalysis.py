#5/23/17
#GOAL: parse data from USGS water resources software list into something
#uploadable to the ontosoft portal for USGS. Use this formatted data and upload
#to USGS Ontosoft portal

from urllib.request import urlopen
import requests
import json

def main():
    #readURL(url, fileName)
    usgsData = getInfo('usgsData')
    loginUrl = 'http://usgs.ontosoft.org/repository/login'
    ID = authenticateUser(loginUrl, 'mknoblock','testPassword')
    for software in usgsData:
        postSoftware(software, ID)

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
    [name, description, [os], version]. If software name already exists in portal, will
    not post anything but request will go through.
    Input: list softwareInfo, string sessionID
    Output: none'''
    osVals = []
    url = 'http://usgs.ontosoft.org/repository/software'
    headers = {'content-type': 'application/json','X-Ontosoft-Session':sessionID}
    nameInfo = {"@type":"TextEntity", "type":"http://ontosoft.org/software#TextEntity"}
    descInfo = {"@type":"TextEntity", "type":"http://ontosoft.org/software#TextEntity"}
    versionInfo = {"@type":"EnumerationEntity", "id":"http://usgs.ontosoft.org/repository/software/SoftwareVersion", "type":"http://ontosoft.org/software#SoftwareVersion"}
    for os in softwareInfo[2]:
        osVals += [{"@type":"EnumerationEntity", "type":"http://ontosoft.org/software#OperatingSystem", "value": os}]
    print(osVals)
    values = {}
    nameInfo['value'] = softwareInfo[0]
    descInfo['value'] = softwareInfo[1]
    versionInfo['value'] = softwareInfo[3]
    values["http://ontosoft.org/software#hasName"] = [nameInfo]
    values["http://ontosoft.org/software#hasShortDescription"] = [descInfo]
    values["http://ontosoft.org/software#supportsOperatingSystem"] = osVals
    values["http://ontosoft.org/software#hasSoftwareVersion"] =[versionInfo]
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
    Output: list of software informations where each software has a list of information '''
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
    [name, description, [os], version]
    Input: string line
    Output: list '''
    software = ['','','','']
    version = False
    formattedOS = []
    versionNum = ''
    separated = line.split('\u2028') #splits information by identifier for new line
    if 'Version' in separated[0]: #if there is a version number
        version = True
        versionInd = separated[0].index('Version')

    if '(' in separated[0]: #if there is an os
        osInd = separated[0].index('(') #starting index for os
        title = separated[0][3:osInd] #starts at 5 to eliminate spacing and bullet point
        os = separated[0][osInd+1:line.index(')')]
        formattedOS = formatOS(os)
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

    return [title, separated[1].strip('\n'), formattedOS, versionNum]

def formatOS(osString):
    ''' This function takes in an osString which may have multiple OSes separated
    by '/' and puts them into the list. Also changes OS abbreviations as specified
    on USGS website and puts them into full form
    Input: string of OS abbreviations
    Output: list of OS full names'''
    if osString == '':
        numOS = 0
    else: 
        numOS = 1 + osString.count('/')
    os = []
    while numOS > 0:
        if numOS == 1:
            osAbbrev = osString
        else:
            ind = osString.index('/')
            osAbbrev = osString[0:ind]
            osString = osString[ind+1:]
        osName = fullName(osAbbrev)
        os += [osName]
        numOS -= 1
    return os
            
def fullName(osAbbrev):
    ''' Given an OS abbreviation, returns the full OS name. OS names and abbreviations
    given by https://water.usgs.gov/software/lists/alphabetical under 'Abbreviations for OSs section'
    Input: string osAbbrev
    Output: string osName'''
    osName = osAbbrev
    OSs = {'DOS':'IBM-compatible PC', 'DG':'Data General AViiON DG/UX', 'Mac':'Macintosh',\
           'SGI': 'Silicon Graphics Indigo', 'Sun': 'Sun SPARCstation Solaris', 'Win': 'Microsoft Windows'}
    if osAbbrev in OSs:
        osName = OSs[osAbbrev]
    return osName




        
