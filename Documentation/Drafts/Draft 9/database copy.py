# DATABASE SCRIPT
# import libaries
import sqlite3
# import my own libraries
import credentials

# creates a connection with database
con = sqlite3.connect('herakles.db')
# cursor allows me to execute commands
cur = con.cursor()

# creates table
cur.execute('''CREATE TABLE IF NOT EXISTS accounts (username text, password text)''')

# commits changes to database
con.commit()
# closes the connection
cur.close()

# returns true is the username is already taken
def isUsername(username):
	# creates a connection with database
	con = sqlite3.connect('herakles.db')
	# cursor allows me to execute commands
	cur = con.cursor()

	# selects accounts with credentials
	cur.execute("SELECT * FROM accounts WHERE username = ? ", (username,))
	
	# fetches accounts with credentials
	account=cur.fetchall()

	# checks if account with credentials exists
	if account == []:
		return False
	elif account[0][0]==username:
		return True
	else:
		return False

# returns true is the account exists
def isAccount(username, password):
	# creates a connection with database
	con = sqlite3.connect('herakles.db')
	# cursor allows me to execute commands
	cur = con.cursor()

	# selects accounts with credentials
	cur.execute("SELECT * FROM accounts WHERE username = ? AND password = ?", (username ,password))
	
	# fetches accounts with credentials
	account=cur.fetchall()

	# checks if account with credentials exists
	if account == []:
		return False
	elif account[0][0]==username and account[0][1]==password:
		return True
	else:
		return False

	# commits changes to database
	con.commit()
	# closes the connection
	cur.close()

# creates a new account
def createAccount(username, password):
	# creates a connection with database
	con = sqlite3.connect('herakles.db')
	# cursor allows me to execute commands
	cur = con.cursor()

	# creates new record in the accounts table
	cur.execute('INSERT INTO accounts VALUES (?, ?)', (username, password))

	# create a personal table to the account to store save files
	script = f"""CREATE TABLE {username} (fileid integer, filename text, lastSavePoint text, hearts integer, 
		arrows integer, coins integer, bosses_killed integer, items text, map_discovered text, settings text)"""
	# settings layout " windowsize, difficulty, volume, music, sfx "
	cur.execute(script)
	# create 3 save files
	for ID in range(3):
		script = f"""INSERT INTO {username} VALUES ({ID}, 'Empty', 'maps/hell/hell1', 100, 
			25, 0, 0, '', '', '900x600,hero,100,100,100')"""
		cur.execute(script)
	
	# commits changes to database
	con.commit()
	# closes the connection
	cur.close()

def loadCredentials(username, password):
	# creates a connection with database
	con = sqlite3.connect('herakles.db')
	# cursor allows me to execute commands
	cur = con.cursor()

	# selects user account
	cur.execute("SELECT * FROM accounts WHERE username = ? AND password = ?", (username ,password))
	data = cur.fetchall()

	# commits changes to database
	con.commit()
	# closes the connection
	cur.close()

	return data

def loadSaveFiles(username):
	# creates a connection with database
	con = sqlite3.connect('herakles.db')
	# cursor allows me to execute commands
	cur = con.cursor()

	# selects users account
	script = "SELECT * FROM " + username
	cur.execute(script)

	# fetches users account
	data = cur.fetchall()

	# commits changes to database
	con.commit()
	# closes the connection
	cur.close()

	return data

def renameSaveFile(fileID, newfilename):
	# creates a connection with database
	con = sqlite3.connect('herakles.db')
	# cursor allows me to execute commands
	cur = con.cursor()

	# fetches users username
	username = credentials.username

	# updates the filename
	script = "UPDATE "+	username+" SET filename = '"+newfilename+"' WHERE fileid = "+str(fileID)
	cur.execute(script)

	# commits changes to database
	con.commit()
	# closes the connection
	cur.close()

def deleteSaveFile(fileID):
	# creates a connection with database
	con = sqlite3.connect('herakles.db')
	# cursor allows me to execute commands
	cur = con.cursor()

	# fetches users username
	username = credentials.username

	# updates the savefile with default settings
	script = f"UPDATE {username} SET filename='Empty', lastSavePoint='X,Y', hearts=100, arrows=25, coins=0, bosses_killed=0, items='', map_discovered='', settings='900x600,hero,100,100,100' WHERE fileid = "+str(fileID)
	cur.execute(script)

	# commits changes to database
	con.commit()
	# closes the connection
	cur.close()

def loadSaveFile(username, ID):
	# creates a connection with database
	con = sqlite3.connect('herakles.db')
	# cursor allows me to execute commands
	cur = con.cursor()

	# selects users account
	script = "SELECT * FROM "+username+" WHERE fileid = "+str(ID)
	cur.execute(script)

	# fetches users account
	data = cur.fetchall()

	# commits changes to database
	con.commit()
	# closes the connection
	cur.close()

	return data

def save_settings(settings):
	# retrieves user data from credentials file
	username = credentials.username
	savefile = int(credentials.savefile)

	# creates a connection with database
	con = sqlite3.connect('herakles.db')
	# cursor allows me to execute commands
	cur = con.cursor()

	# updates the savefile to it's new settings
	script = f"UPDATE {username} SET settings = '{settings}' WHERE fileid = {savefile}"
	cur.execute(script)

	# commits changes to database
	con.commit()
	# closes the connection
	cur.close()

# used for debugging and view all created accounts
def printall():
	# creates a connection with database
	con = sqlite3.connect('herakles.db')
	# cursor allows me to execute commands
	cur = con.cursor()

	cur.execute('SELECT * FROM accounts')

	print(cur.fetchall())

	# commits changes to database
	con.commit()
	# closes the connection
	cur.close()

def save(savePoint, hearts, arrows, coins):
	# fileid, filename, lastSavePoint, hearts, arrows, coins, bosses_killed, items, map_discovered, settings

	# retrieves user data from credentials file
	username = credentials.username
	savefile = int(credentials.savefile)

	# creates a connection with database
	con = sqlite3.connect('herakles.db')
	# cursor allows me to execute commands
	cur = con.cursor()

	# updates the savefile to it's new settings
	script = f"UPDATE {username} SET lastSavePoint = '{savePoint}', hearts = {hearts}, arrows = {arrows}, coins = {coins} WHERE fileid = {savefile}"
	cur.execute(script)

	# commits changes to database
	con.commit()
	# closes the connection
	cur.close()
