import sqlite3 as db

try:
    global connect, cursor, rows
    connect = db.connect("fb_db.db",check_same_thread = False)
    cursor = connect.cursor()
except:
    print 'Error handling Database'

def insertTestUsers(userId,name,email,password):
    for i in range(len(email)):
        try:
            cursor.execute("INSERT INTO testUsers (id, name, email, password,logged, blocked) VALUES(?, ?, ?, ?,0,0)", (userId[i], name[i], email[i], password[i]))
        except:
            print 'No se realizo la iteracion %d \n' % i
             
    connect.commit()

def insertTestUsersDev(userId,name):
    for i in range(len(userId)):
        try:
            cursor.execute("INSERT INTO testUsers (id, name, email, password,logged, blocked) VALUES(?, ?, 0, 1234567890,0,0)", (userId[i], name[i]))
        except:
            print 'No se realizo la iteracion %d \n' % i
             
    connect.commit()

def removeTestUsers(userId):
    query = "DELETE FROM testUsers WHERE id = %d;" % int(userId)
    try:
        cursor.execute(query)
        print '\rSuccesfull deleted %d                                    \r' % int(userId),
    except:
        print 'No se pudo eliminar el id de usuario %d                    \r' % int(userId),
    print ''             
    connect.commit()
    
def getUsers():
    cursor.execute("SELECT * FROM testUsers;")
    rows = cursor.fetchall()
    return rows

def setLogged(c_user):
    query = "UPDATE testUsers SET logged=1 WHERE id = %d;" % int(c_user)
    try:
        cursor.execute(query)
    except:
        print 'Error en setLogged() \n'  
    
    connect.commit()

def setLoggedOut(c_user):
    query = "UPDATE testUsers SET logged=0 WHERE id = %d;" % int(c_user)
    try:
        cursor.execute(query)
    except:
        print 'Error en setLogged() \n'  
    
    connect.commit()
    
def status():
    queries = ["SELECT count(*) FROM testUsers;","SELECT count(*) FROM testUsers WHERE logged=0;","SELECT count(*) FROM testUsers WHERE logged=1;",
             "SELECT count(*) FROM testUsers WHERE blocked=1;"]
    try:
        for query in queries:
            cursor.execute(query)
            row = cursor.fetchall()
            for rows in row:
                print 'The query: ' + query + ' dump the result: %s' % (rows,) + '\n'
    except:
        print 'Error in status() \n' 

def getUsersNotLogged():
    cursor.execute("SELECT * FROM testUsers WHERE logged=0;")
    rows = cursor.fetchall()
    return rows

def createVictimTable(victim):
    try:
        victim = victim.replace(".","_")
        cursor.execute("CREATE TABLE "+str(victim)+"_nodes(friendName text, friendId text)")
        cursor.execute("CREATE TABLE "+str(victim)+"_friends_edges(friendName text, friendId text, edges text, edgesIDS text)")
    except:
        print 'Error al crear la tabla'
        return -1
    connect.commit()

def addNode(victim,friendName, friendId):

    try:
        victim = victim.replace(".","_")
        if (checkNodeExistence(victim, friendName, friendId) == False):
            cursor.execute("INSERT INTO "+str(victim)+"_nodes (friendName, friendId) VALUES(?, ?)", (friendName, friendId))
            cursor.execute("INSERT INTO "+str(victim)+"_friends_edges (friendName, friendId) VALUES(?, ?)", (friendName, friendId))
    except:
        print 'Error al ingresar el nodo %s' %friendName
             
    connect.commit()

def addEdge(victim,friendName, friendId, edge, edgeID):
    if checkNodeExistence(victim,friendName, friendId) == True:
        try:
            victim = victim.replace(".","_")
            cursor.execute("SELECT edges FROM "+str(victim)+"_friends_edges WHERE friendName=\""+str(friendName)+"\" OR friendId=\""+str(friendId)+"\";")
            rows = str(cursor.fetchone()).strip("(None,)").strip("'")
            rows = rows.encode('ascii','replace') + edge + ";"
            cursor.execute("UPDATE "+str(victim)+"_friends_edges SET edges=\""+rows+"\" WHERE friendName=\""+str(friendName)+"\" OR friendId=\""+str(friendId)+"\";")
            cursor.execute("SELECT edgesIDS FROM "+str(victim)+"_friends_edges WHERE friendName=\""+str(friendName)+"\" OR friendId=\""+str(friendId)+"\";")
            rows = str(cursor.fetchone()).strip("(None,)").strip("'")
            rows = rows.encode('ascii','replace') + edgeID + ";"
            cursor.execute("UPDATE "+str(victim)+"_friends_edges SET edgesIDS=\""+rows+"\" WHERE friendName=\""+str(friendName)+"\" OR friendId=\""+str(friendId)+"\";")
        
        except db.Error as e:
            print "An error occurred:", e.args[0]
        
        except:
            print 'Error al hacer update para el nodo %s' %edge
                 
        connect.commit()
    else:
        return -1

def getNodes(victim):
    victim = victim.replace(".","_")
    cursor.execute("SELECT * FROM "+str(victim)+"_nodes;")
    rows = cursor.fetchall()
    return rows

def getEdges(victim, friendName, friendId):
    victim = victim.replace(".","_")
    cursor.execute("SELECT * FROM "+str(victim)+"_friends_edges WHERE friendName=\""+str(friendName)+"\" OR friendId=\""+str(friendId)+"\";")
    rows = cursor.fetchall()
    return rows    
    
def checkNodeExistence(victim, friendName, friendId):
    victim = victim.replace(".","_")
    cursor.execute("SELECT * FROM "+str(victim)+"_nodes WHERE friendName=\""+str(friendName)+"\" OR friendId=\""+str(friendId)+"\";")
    rows = cursor.fetchall()
    if rows != []:
        return True
    else:
        return False

def checkTableExistence(victim):
    try:
        cursor.execute("SELECT count(*) FROM "+victim.replace(".","_")+"_nodes;")
        res = cursor.fetchone()
        return bool(res[0])
    except:
        return False