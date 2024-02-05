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

def WriteNewToDatabase(playerName,id, score):
    """Writes to the database"""
    conn, cur = dbConnector() # connect to the database

    query = """INSERT INTO Scores VALUES(?,?,?,?,?)"""
    cur.execute(query,(playerName, id, 0,0,score))
    conn.commit()
    conn.close()
    print("Success")

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
'''
def getID():
    conn, cur = dbConnector()
    #need to read from the database to find the highest ID, then increment it by 1 for this user
'''


# test dbConnector works
#print(dbConnector())
# writeToDatabase
#readDatabaseRecrods()
#WriteNewToDatabase(playerName,score)