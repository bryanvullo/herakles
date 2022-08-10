# DATABASE SCRIPT
import sqlite3

# creates a connection with database
con = sqlite3.connect('example.db')
# cursor allows me to execute commands
cur = con.cursor()

# creates table
cur.execute('''CREATE TABLE IF NOT EXISTS accounts (username text, password text)''')

# commits changes to database
con.commit()
# closes the connection
cur.close()

# returns true is the account exists
def isAccount(username, password):
	# creates a connection with database
	con = sqlite3.connect('example.db')
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
	con = sqlite3.connect('example.db')
	# cursor allows me to execute commands
	cur = con.cursor()

	# creates new record in the accounts table
	cur.execute('INSERT INTO accounts VALUES (?, ?)', (username, password))
	# cur.execute('CREATE TABLE ? (filename text, lives integer, arrows integer, lastSavePoint text, ...etc)', username)
	# 3 Times for 3 save files
	# cur.execute('INSERT INTO ? VALUES (NEWGAME, 100, 0, 'X,Y', etc...)', username)

	# commits changes to database
	con.commit()
	# closes the connection
	cur.close()

def loadData(username, password):
	# creates a connection with database
	con = sqlite3.connect('example.db')
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
