# LOGIN MENU

# importing libraries 
import sys
import tkinter as tk
from tkinter import *
from tkinter import messagebox

def loginScreen(size, icon, root):
	
	# button function
	def checkCredentials():
		# login criteria
		if len(u_name.get()) <=0:
			error=messagebox.showerror('Incorrect Input','You must have a username')
			return
	    
		if len(p_word.get()) < 6:
			u_name.delete(0,END)
			p_word.delete(0,END)
			error=messagebox.showerror('Incorrect Input','Password must be at least 6 characters')
			return

		box=messagebox.showinfo('Success', 'Password Accepted')

	# reveals window and sets up the name, size and icon 
	root.deiconify()
	root.title('Login Menu')
	root.iconphoto(False, tk.PhotoImage(file=icon))
	root.geometry(str(size[0])+'x'+str(size[1]))

	# window content
	welcome_label=Label(root, text="HERAKLES")
	welcome_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

	u_name_label= Label(root, text='Username:')
	u_name_label.grid(row=1, column=0, pady=(10,0))
	u_name = Entry(root, width=15)
	u_name.grid(row=1, column=1, padx=20, pady=(10,0))

	p_word_label= Label(root, text='Password:')
	p_word_label.grid(row=2, column=0)
	p_word = Entry(root, width=15)
	p_word.grid(row=2, column=1)

	confirm_button=Button(root, text='LOGIN', command=checkCredentials)
	confirm_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

	root.mainloop()