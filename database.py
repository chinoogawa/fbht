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