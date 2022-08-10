# LOGIN MENU

# importing libraries 
import sys
import tkinter as tk
from tkinter import *
from tkinter import messagebox

# importing my own libraries
import database
import credentials

def loginScreen(size, icon, root):
	
	# button functions

	# universal function for both windows to check if credentials fit criteria
	def checkCredentials(username, password):
		# credentials criteria

		if len(username) <=0: #checks length of username
			error=messagebox.showerror('Incorrect Input','You must have a username')
			return False
	    
	    # password checks
		if len(password) < 6: #checks password length
			error=messagebox.showerror('Incorrect Input','Password must be at least 6 characters')
			return False

		capital=False
		number=False
		spChar=False
		for char in password:
			if ord(char) >=65 and ord(char)<=90: #ASCII values for capital letters
				capital=True

			if ord(char) >=48 and ord(char)<=57: #ASCII values for numbers
				number=True

			if (ord(char)>=33 and ord(char)<=47) or (ord(char)>=58 and ord(char)<= 64) or (ord(char)>=91 and ord(char)<=96) or (ord(char)>=123 and ord(char)<=126): #ASCII vales for special characters
				spChar=True

		if not capital:
			error=messagebox.showerror('Password not accepted', 'Password MUST have atleast one CAPITAL letter')
			return False

		if not number:
			error=messagebox.showerror('Password not accepted', 'Password MUST have atleast one NUMBER')
			return False

		if not spChar:
			error=messagebox.showerror('Password not accepted', 'Password MUST have atleast one SPECIAL CHARACTER')
			return False

	def verify(username, password):
		verified = database.isAccount(username, password)
		if verified:
			box=messagebox.showinfo('Success', 'Credentials Accepted')
			# stores the login details in a seperate file called 'credentials'
			credentials.username = username
			credentials.password = password
			return True
		else:
			error=messagebox.showerror('Account Not Found', 'Account Not Found. Make Sure Details Are Correct')
			return False

	def login(uname, pword):
			checkCredentials(uname, pword)
			if verify(uname, pword):
				# exits tkinter and back to the main script
				root.destroy()

	# exits program if user closes the tkinter window
	#  so that they cannot skip login process
	def onClosing():
		if messagebox.askyesno("Quit", "Would you like to quit game?")==1:
			sys.exit()

	# fuctions for showing and hiding the users password
	def showPassword():
		p_word.configure(show = '')
		check.configure(text='Hide', command=hidePassword)
	def hidePassword():
		p_word.configure(show = '*')
		check.configure(text='Show', command=showPassword)

	# creates a new window for creating a new account
	def createAccountWindow():

		# button functions for second window

		# fuctions for showing and hiding the users password
		def showPassword():
			p_word.configure(show = '')
			confirm.configure(show = '')
			check.configure(text='Hide', command=hidePassword)
		def hidePassword():
			p_word.configure(show = '*')
			confirm.configure(show = '*')
			check.configure(text='Show', command=showPassword)

		# returns to the login window
		def close():
			top.destroy()
			root.deiconify()

		def extraChecks(pword, confirm):
			if pword != confirm:
				error=messagebox.showerror('Passwords','Passwords do not match')
				return False

		def createAccount(uname,pword,confirm):
			if checkCredentials(uname, pword) == False:
				return
			if extraChecks(pword, confirm) == False:
				return
			if not database.isUsername(uname):
				database.createAccount(uname, pword)
				box=messagebox.showinfo('Success', 'Account Created, now log in!')
				close()

		# hides primary window
		root.withdraw()
		# creates second window
		top = Toplevel()

		# second window set up
		top.title('Create Free Account')
		top.iconphoto(False, tk.PhotoImage(file=icon))
		top.geometry(str(size[0])+'x'+str(size[1]))

		# second window content
		title_label=Label(top, text="HERAKLES")
		title_label.config(font=('Courier', 50))
		title_label.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

		u_name_label= Label(top, text='New Username:')
		u_name_label.grid(row=1, column=0, pady=(10,0), padx=5)
		u_name = Entry(top, width=40)
		u_name.grid(row=1, column=1, padx=20, pady=(10,0))

		p_word_label= Label(top, text='Password:')
		p_word_label.grid(row=2, column=0, padx=5)
		p_word = Entry(top, width=40, show = '*')
		p_word.grid(row=2, column=1)

		confirm_label = Label(top, text='Confirm Password:')
		confirm_label.grid(row=3, column=0, padx=5)
		confirm= Entry(top, width=40, show = '*')
		confirm.grid(row=3, column=1)

		check = Button(top, text='Show', command=showPassword)
		check.grid(row=2, column=2, padx=5)

		create_button=Button(top, text='Create Account', 
			command=lambda: createAccount(u_name.get(), p_word.get(), confirm.get()))
		create_button.config(font=('Courier', 50))
		create_button.grid(row=4, column=0, columnspan=3, padx=10, pady=10)

		close_button=Button(top, text='Close', command=close)
		close_button.config(font=('Courier', 20))
		close_button.grid(row=5, column=0, columnspan=3, padx=10, pady=10)

		# each row and column have same weighting when resizing
		top.grid_columnconfigure(0,weight=1)
		top.grid_columnconfigure(1,weight=1)
		top.grid_columnconfigure(2,weight=1)
		top.grid_rowconfigure(0,weight=1)
		top.grid_rowconfigure(1,weight=1)
		top.grid_rowconfigure(2,weight=1)
		top.grid_rowconfigure(3,weight=1)
		top.grid_rowconfigure(4,weight=1)
		top.grid_rowconfigure(5,weight=1)

		# if user is exiting game
		top.protocol("WM_DELETE_WINDOW", onClosing)


	# reveals window and sets up the name, size and icon 
	root.deiconify()
	root.title('Login Menu')
	root.iconphoto(False, tk.PhotoImage(file=icon))
	root.geometry(str(size[0])+'x'+str(size[1]))

	# window content
	# the .configure methods allow me to edit the size and font of the text
	title_label=Label(root, text="HERAKLES")
	title_label.config(font=('Courier', 50))
	title_label.grid(row=0, column=0, columnspan=3, padx=10, pady=10)
	
	u_name_label= Label(root, text='Username:')
	u_name_label.grid(row=1, column=0, pady=(10,0), padx=5)
	u_name = Entry(root, width=45)
	u_name.grid(row=1, column=1, padx=20, pady=(10,0))

	p_word_label= Label(root, text='Password:')
	p_word_label.grid(row=2, column=0, padx=5)
	p_word = Entry(root, width=45, show = '*')
	p_word.grid(row=2, column=1)

	check = Button(root, text='Show', command=showPassword)
	check.grid(row=2, column=2, padx=5)

	confirm_button=Button(root, text='LOGIN', 
		command= lambda: login(u_name.get(), p_word.get()))
	confirm_button.config(font=('Courier', 50))
	confirm_button.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

	newacc_button=Button(root, text='Create Free Account', command=createAccountWindow)
	newacc_button.config(font=('Courier', 20))
	newacc_button.grid(row=4, column=0, columnspan=3, padx=10, pady=10)

	# each row and column have same weight when resizing
	root.grid_columnconfigure(0,weight=1)
	root.grid_columnconfigure(1,weight=1)
	root.grid_columnconfigure(2,weight=1)
	root.grid_rowconfigure(0,weight=1)
	root.grid_rowconfigure(1,weight=1)
	root.grid_rowconfigure(2,weight=1)
	root.grid_rowconfigure(3,weight=1)
	root.grid_rowconfigure(4,weight=1)

	# if user is exitting game
	root.protocol("WM_DELETE_WINDOW", onClosing)
	
	# creates a loop for events
	root.mainloop()