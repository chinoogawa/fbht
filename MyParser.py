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

def parseData(dataRaw):
    parser = MyHTMLParser()
    parser.array()
    names = []
    userIds = []
    emails = []
    passwords = []
    
    

    for data in dataRaw:    
        text = data.strip("for (;;);")
        json_dump = json.loads(text)
        try:
            to_parse = str(json_dump['jsmods']['markup'][0][1]['__html'])
            parser.feed(to_parse)
        except:
            print 'Error in json dump or parser.feed'

    for i in range(len(parser.dataArray)):
        if parser.dataArray[i] == 'Name:':
            names.append(parser.dataArray[i+1])
            continue
        if parser.dataArray[i] == 'User ID:':
            userIds.append(parser.dataArray[i+1])
            continue
        if parser.dataArray[i] == 'Login email:':
            emails.append(parser.dataArray[i+1]+'@'+parser.dataArray[i+2])
            continue
        if parser.dataArray[i] == 'Login password:':
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