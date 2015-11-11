from HTMLParser import HTMLParser
import simplejson as json
import database
import re

class MyHTMLParser(HTMLParser):
    def array(self):
        self.dataArray = []
    def handle_data(self, data):
        self.dataArray.append(data)       

def htmlFormat(json_dump):
    html = "<p><img src=\"https://graph.facebook.com/%s/picture\" > Name: %s - Link: <a href=\"%s\">facebook profile</a> - Gender: %s -Locale: %s</p>" %(json_dump['username'],json_dump['name'], json_dump['link'], json_dump['gender'], json_dump['locale']) 
    return html

def parceros(json_dump):
    parser = MyHTMLParser()
    parser.array()
    names = []
    userIds = []
    try:
        to_parse = str(json_dump['domops'][0][3]['__html'])
        parser.feed(to_parse)
    except:
        print 'Error in json dump or parser.feed'
    i = 0
    while True:
        if ((parser.dataArray[i] == 'Test Users') or (parser.dataArray[i] == 'Delete') or (parser.dataArray[i] == 'Add') or
            (parser.dataArray[i] == 'Name') or (parser.dataArray[i] == 'User ID') or (parser.dataArray[i] == 'Email') or
            (parser.dataArray[i] == 'Edit') or (parser.dataArray[i] == 'tfbnw.net')):
            del parser.dataArray[i]
        else:
            i += 1
        if i == len(parser.dataArray):
            break
    
    i = 0
            
    while i < (len(parser.dataArray) - 2):
        names.append(parser.dataArray[i])
        userIds.append(parser.dataArray[i+1])
        i = i + 3

    if ( userIds!=[] and names!=[]) and (parser.dataArray[0] != 'This app has no Test Users.'):
        database.insertTestUsersDev(userIds,names)
        return 1
    else:
        return -1    
    
  
def parseData(dataRaw):
    parser = MyHTMLParser()
    parser.array()
    names = []
    userIds = []
    emails = []
    passwords = []
    
    

    for data in dataRaw:    
        if data=="":
            continue
        text = data.strip("for (;;);")
        json_dump = json.loads(text)
        try:
            to_parse = str(json_dump['jsmods']['markup'][0][1]['__html'])
            parser.feed(to_parse)
        except:
            print 'Error in json dump or parser.feed'

    for i in range(len(parser.dataArray)):
        if parser.dataArray[i] == 'Name':
            names.append(parser.dataArray[i+1])
            continue
        if parser.dataArray[i] == 'User ID':
            userIds.append(parser.dataArray[i+1])
            continue
        if parser.dataArray[i] == 'Login email':
            emails.append(parser.dataArray[i+1]+'@'+parser.dataArray[i+2])
            continue
        if parser.dataArray[i] == 'Login password':
            passwords.append(parser.dataArray[i+1])
            continue
    
    if ( userIds!=[] and names!=[] and emails!=[] and passwords!=[] ):
        database.insertTestUsers(userIds,names,emails,passwords)
        return 1
    else:
        return -1
    '''
    try:
        for i in range(len(names)):
            print names[i] + ' ' + userIds[i] + ' ' + emails[i] + ' ' + passwords[i] + ' ' 
    except:
        print 'for error in MyParser'
    '''
    
def parseOnline(data):
    buddies = []
    start = 0
    while True:
        match = re.search("fbid=", data[start:])
        if match is not None:
            start += match.end()
            matchBis = re.search("&",data[start:])
            if matchBis is not None:
                end = matchBis.end() + start
                buddies.append(str(data[start:end-1]))
                start = end
                end = 0
        else:
            break
    return buddies

def parseFriends(data):
    start = 0
    end = 0
    lines = []
    friends = []
    while True:
        match = re.search(r'href="/([a-zA-Z]*[0-9]*[\.]*)+(\?fref=fr_tab)',data[start:])
        if match is not None:
            lines.append(match.group())
            start += match.end()
        else:
            break
        
    for linea in lines:
        name = linea.split('/')[1].split('?')[0]
        friends.append(name)
    match = re.search("[a-zA-Z]+\?v=friends&amp;mutual&amp;startindex=[0-9]+",data)
    if match is not None:
        raw = match.group()
        next = raw.replace("&amp;","&")
    else:
        match = re.search("[a-zA-Z]+/friends\?([a-zA-Z]+=[0-9]+)+(&amp;)*([a-zA-Z]+=[0-9]+)*",data)
        if match is not None:
            raw = match.group()
            next = raw.replace("&amp;","&")
        else:
            next = -1
    return friends,next

def parsePending():
    response = open("respuesta.html","r")
    struct = []
    aux = []
    while True:

        linea = response.readline()
        if not linea: break
        match = re.search('/ajax/reqs.php'+'(.+)',str(linea))
        if match is not None:
            struct.append(re.search('/ajax/reqs.php'+'(.+)',str(linea)).group())
    
    
    for lines in struct:
        start = 0
        while True:
            match = re.search('[0-9]{15}',str(lines)[start:])
            if match is not None:
                if str(lines)[start + match.start():start + match.end()] not in aux:
                    aux.append(str(lines)[start + match.start():start + match.end()])
                start += match.end()
            else:
                break;        
    return aux 