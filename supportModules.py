import pygame
import sqlite3 as sq
font_name = pygame.font.match_font("arial")
def draw_text(surf, text, size, x, y, clr):
    """Create a font object"""
    try:
        font = pygame.font.Font(font_name, size)
        text_surface = font.render(text, True, clr)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        surf.blit(text_surface, text_rect)
    except pygame.error as e:
        print(f"Pygame Error: {e}")


def dbConnector():
    """Connect to the database and return a connection object"""
    try:
        conn = sq.connect("RickAndMortyGame.db")
        cur = conn.cursor()
        return conn, cur
    except sq.Error as e:
        print(f"Database connection error: {e}")

def WriteNewToDatabase(playerName, score):
    """Writes to the database"""
    conn, cur = dbConnector() # connect to the database
    id = primKeyGen()
    query = """INSERT INTO Scores VALUES(?,?,?,?,?)"""
    cur.execute(query,(playerName,id,0,0,score))
    conn.commit()
    conn.close()
    print(f"Success! n\A score for {playerName} has been successfully saved.")

def readDatabaseRecords():
    """Reads records from a database"""
    conn, cur = dbConnector()
    query = """SELECT * FROM Scores"""
    cur.execute(query)
    results = cur.fetchall()
    print(results)
    conn.close()

def writeNewRecord(playerName, id, score):
    """writes a value to a specific record"""
    #query option to be written too
    query = """SELECT COUNT(*) FROM Scores WHERE name = ?"""
    # prepare data to be written
    # open connection, write data, close connection
    conn, cur = dbConnector()
    cur.execute(query,(playerName,))
    results = cur.fetchall()
    if results[0][0] ==1:
        print('call append method')
    else:
        WriteNewToDatabase(playerName, id, score)
    conn.commit
    conn.close

def WriteToSpecific(playerName,score):
    """Writes a value to a specific record"""
    conn,cur =dbConnector()
    query = """SELECT COUNT(*) FROM Scores WHERE Name=?"""
    cur.execute(query,(playerName,))
    results = cur.fetchall()
    if results[0][0] == 0:
        WriteNewToDatabase(playerName, score)
    else:
        updateExisting(playerName, score)
        print(f"{playerName}'s record was updated")
            

def primKeyGen():
    '''Generates a new PK for a new record using last PK'''
    conn, cur= dbConnector()
    query = """SELECT ID from Scores"""
    cur.execute(query,)
    results = cur.fetchall()
    newID = results[-1][0]+1
    conn.close
    return newID

def updateExisting(playerName, score):
    '''Reads existing records and updates the score
       Shuffling out the oldest score and edding new
    '''
    conn, cur = dbConnector()
    query ="""SELECT Score1, Score2, Score3 FROM Scores WHERE Name=?"""
    cur.execute(query,(playerName,))
    results = cur.fetchall()
    updateQuery ="""UPDATE Scores SET Score1=?,Score2=?,Score3=? WHERE Name=?"""
    Score1, Score2, Score3 = results[0][1], results[0][2], score
    cur.execute(updateQuery,(Score1, Score2, score, playerName))
    conn.commit()
    conn.close()



# test dbConnector works
#print(dbConnector())
# writeToDatabase
#readDatabaseRecords()
#WriteNewToDatabase(playerName,score)
#WriteToSpecific('Gio')
#print(primKeyGen())
#WriteNewToDatabase("Jordan", 9)
#updateExisting('Gio')