# DATABASE SCRIPT
import sqlite3

# creates a connection with database
con = sqlite3.connect('example.db')
# cursor allows me to execute commands
cur = con.cursor()

# returns true is the account exists
def isAccount(username, password):
	return