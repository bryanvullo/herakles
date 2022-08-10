# LOGIN MENU

# importing libraries 
import sys
import tkinter as tk
from tkinter import *
from tkinter import messagebox

# importing my own libraries
import database
import credentials

class start:
	def __init__(self, size, icon):
		self.size = size
		self.icon = icon

	# exits program if user closes the tkinter window so that they cannot skip login process
	def onClosing(self):
		if messagebox.askyesno("Quit", "Would you like to quit game?")==1:
			sys.exit()

	# login function for button checks and verifies user credentials
	def login(self, uname, pword, root):
		self.username = uname
		self.password = pword
		if self.checkCredentials():
			if self.verify():
				# exits tkinter and back to the main script
				root.destroy()

	def verify(self):
		verified = database.isAccount(self.username, self.password)
		if verified:
			box=messagebox.showinfo('Success', 'Credentials Accepted')
			# stores the login details in a seperate file called 'credentials'
			credentials.username = self.username
			credentials.password = self.password
			return True
		else:
			error=messagebox.showerror('Account Not Found', 'Account Not Found. Make Sure Details Are Correct')
			return False

	def checkCredentials(self):
		# credentials criteria
		if len(self.username) <=4: #checks length of username
			error=messagebox.showerror('Incorrect Input','Username must be atleast 5 characters')
			return False
	    
	    # password checks
		if len(self.password) < 6: #checks password length
			error=messagebox.showerror('Incorrect Input','Password must be at least 6 characters')
			return False

		capital=False
		number=False
		spChar=False
		for char in self.password:
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

		# if all checks are cleared then return true
		return True

	# fuctions for showing and hiding the users password
	def showPassword(self, p_word, check):
		p_word.configure(show = '')
		check.configure(text='Hide', command=lambda: self.hidePassword(p_word, check))
	def hidePassword(self, p_word, check):
		p_word.configure(show = '*')
		check.configure(text='Show', command=lambda: self.showPassword(p_word, check))

	# fuctions for showing and hiding the users passwords for creating an account
	def showPasswords(self, p_word, confirm, check):
		p_word.configure(show = '')
		confirm.configure(show = '')
		check.configure(text='Hide', command=lambda: self.hidePasswords(p_word, confirm, check))
	def hidePasswords(self, p_word, confirm, check):
		p_word.configure(show = '*')
		confirm.configure(show = '*')
		check.configure(text='Show', command=lambda: self.showPasswords(p_word, confirm, check))

	def extraChecks(self):
		if self.password != self.confirm:
			error=messagebox.showerror('Passwords','Passwords do not match')
			return False

	# returns to the login window
	def close(self):
		self.top.destroy()
		self.main.deiconify()

	def createAccount(self, uname, pword, confirm):
		self.username = uname
		self.password = pword
		self.confirm = confirm

		if self.checkCredentials() == False:
			return
		if self.extraChecks() == False:
			return
		if not database.isUsername(self.username):
			database.createAccount(self.username, self.password)
			box=messagebox.showinfo('Success', 'Account Created, now log in!')
			self.close()
		else:
			error=messagebox.showerror('Username Exists', 'Username already exists, create another')

	# login menu
	def loginScreen(self, root):
		# hides root
		root.deiconify()
		root.withdraw()

		# creates window for login menu
		main = Toplevel()
		self.main = main

		# window set up
		main.title('Login Menu')
		main.iconphoto(False, tk.PhotoImage(file=self.icon))
		main.geometry(str(self.size[0])+'x'+str(self.size[1]))

			# window content
		# the .configure methods allow me to edit the size and font of the text
		title_label=Label(main, text="HERAKLES")
		title_label.config(font=('Courier', 50))
		title_label.grid(row=0, column=0, columnspan=3, padx=10, pady=10)
		
		u_name_label= Label(main, text='Username:')
		u_name_label.grid(row=1, column=0, pady=(10,0), padx=5)
		u_name = Entry(main, width=45)
		u_name.grid(row=1, column=1, padx=20, pady=(10,0))

		p_word_label= Label(main, text='Password:')
		p_word_label.grid(row=2, column=0, padx=5)
		p_word = Entry(main, width=45, show = '*')
		p_word.grid(row=2, column=1)

		check = Button(main, text='Show', 
			command=lambda: self.showPassword(p_word, check))
		check.grid(row=2, column=2, padx=5)

		confirm_button=Button(main, text='LOGIN', 
			command= lambda: self.login(u_name.get(), p_word.get(), root))
		confirm_button.config(font=('Courier', 50))
		confirm_button.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

		newacc_button=Button(main, text='Create Free Account', command=self.createScreen)
		newacc_button.config(font=('Courier', 20))
		newacc_button.grid(row=4, column=0, columnspan=3, padx=10, pady=10)

		# each row and column have same weight when resizing
		main.grid_columnconfigure(0,weight=1)
		main.grid_columnconfigure(1,weight=1)
		main.grid_columnconfigure(2,weight=1)
		main.grid_rowconfigure(0,weight=1)
		main.grid_rowconfigure(1,weight=1)
		main.grid_rowconfigure(2,weight=1)
		main.grid_rowconfigure(3,weight=1)
		main.grid_rowconfigure(4,weight=1)

		# if user is exitting game
		main.protocol("WM_DELETE_WINDOW", self.onClosing)
		
		# creates a loop for events
		main.mainloop()

	# create an account menu
	def createScreen(self):
		# hides the login menu
		self.main.withdraw()

		# creates a new window for creating a new account
		top = Toplevel()
		self.top = top

		# window set up
		top.title('Create An Account Menu')
		top.iconphoto(False, tk.PhotoImage(file=self.icon))
		top.geometry(str(self.size[0])+'x'+str(self.size[1]))

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

		check = Button(top, text='Show', 
			command=lambda: self.showPasswords(p_word, confirm, check))
		check.grid(row=2, column=2, padx=5)

		create_button=Button(top, text='Create Account', 
			command=lambda: self.createAccount(u_name.get(), p_word.get(), confirm.get()))
		create_button.config(font=('Courier', 50))
		create_button.grid(row=4, column=0, columnspan=3, padx=10, pady=10)

		close_button=Button(top, text='Close', command=self.close)
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
		top.protocol("WM_DELETE_WINDOW", self.onClosing)
