# displaying save files for user to choose
import sys
import tkinter as tk
from tkinter import *
from tkinter import messagebox

# my own libraries
import credentials
import database

def select(choice, root):
		confirm = messagebox.askyesno('Confirmation', 'Would you like to load this save file?')
		if confirm == 1:
			credentials.savefile = choice
			root.destroy()

def onClosing():
	if messagebox.askyesno("Quit", "Would you like to quit game?") == 1:
		sys.exit()

def delete(ID, size, icon, root):
	if messagebox.askyesno("Delete", "Are you sure you would like to delete this savefile? This action is irreversible.") == 1:
		database.deleteSaveFile(ID)

	# updates temporary file
	credentials.savefiles[ID][0] = 'Empty'
	credentials.savefiles[ID][1] = 0

	# detroys main window then calls again so that savefiles are updated
	root.destroy()
	displaySaveFiles(size, icon)

def rename(ID, newFilename, window, root, size, icon):
	# updates database
	database.renameSaveFile(ID, newFilename)

	# detroys the renameWindow
	window.destroy()

	# updates the temporary file
	credentials.savefiles[ID][0] = newFilename

	# detroys main window then calls again so that file names are updated
	root.destroy()
	displaySaveFiles(size, icon)

def cancelRename(window, root):
	# destroys the renameWindow
	window.destroy()

	# shows the main window
	root.deiconify()

def renameWindow(ID, size, icon, root):
	# hides main window
	root.withdraw()

	# creates a new window to fetch new savefile name
	renameWindow = Toplevel()
	renameWindow.iconphoto(False, tk.PhotoImage(file=icon))
	renameWindow.geometry(str(size[0])+'x'+str(size[1]))

	# displays window text
	title_label=Label(renameWindow, text="Rename Savefile")
	title_label.config(font=('Courier', 30))
	title_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

	# description for entry widget
	label=Label(renameWindow, text='New Savefile Name: ')
	label.grid(row=1, column=0, padx=10, pady=10)

	# entry widget so user can input the new savefile name
	entry = Entry(renameWindow, width=40)
	entry.grid(row=1, column=1)

	# button to confirm new name
	confirmbutton = Button(renameWindow, text='Confirm New Savefile Name', command= lambda: rename(ID, entry.get(), renameWindow, root, size, icon))
	confirmbutton.grid(row=2, column=1)

	returnbutton = Button(renameWindow, text='Cancel', command= lambda: cancelRename(renameWindow, root))
	returnbutton.grid(row=2, column=0)

	# makes everything spread out on the window evenly 
	renameWindow.grid_columnconfigure(0,weight=1)
	renameWindow.grid_columnconfigure(1,weight=1)
	renameWindow.grid_rowconfigure(0,weight=1)
	renameWindow.grid_rowconfigure(1,weight=1)
	renameWindow.grid_rowconfigure(2,weight=1)

	# if user is exitting game
	renameWindow.protocol("WM_DELETE_WINDOW", onClosing)

	renameWindow.mainloop()

def displaySaveFiles(size, icon):
	# loads savefiles info
	savefiles = credentials.savefiles

	# initialises tkinter window
	root = Tk()
	root.title('Save Files Selection')
	root.iconphoto(False, tk.PhotoImage(file=icon))
	root.geometry(str(size[0])+'x'+str(size[1]))

	# title at the top
	title_label=Label(root, text="HERAKLES")
	title_label.config(font=('Courier', 50))
	title_label.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

	# extra message for user
	welcome_message = 'Welcome back '+credentials.username+'!'
	welcome_label = Label(root, text=welcome_message)
	welcome_label.config(font=('Courier', 30))
	welcome_label.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

	# selection of savefiles
	text1 = savefiles[0][0] +' -  Progress: '+ str(savefiles[0][1]/10*100) +'%'
	sf1 = Button(root, text=text1, command=lambda: select(0, root))
	sf1.grid(row=2, column=0, padx=5)

	renameButton1 = Button(root, text='Rename', command= lambda: renameWindow(0, size, icon, root))
	renameButton1.grid(row=2, column=1, padx=5)

	deleteButton1 = Button(root, text='Delete', command= lambda: delete(0, size, icon, root))
	deleteButton1.grid(row=2, column=2, padx=5)

	text2 = savefiles[1][0] +' -  Progress: '+ str(savefiles[1][1]/10*100) +'%'
	sf2 = Button(root, text=text2, command=lambda: select(1, root))
	sf2.grid(row=3, column=0, padx=5)

	renameButton2 = Button(root, text='Rename', command= lambda: renameWindow(1, size, icon, root))
	renameButton2.grid(row=3, column=1, padx=5)

	deleteButton2 = Button(root, text='Delete', command= lambda: delete(1, size, icon, root))
	deleteButton2.grid(row=3, column=2, padx=5)

	text3 = savefiles[2][0] +' -  Progress: '+ str(savefiles[2][1]/10*100) +'%'
	sf3 = Button(root, text=text3, command=lambda: select(2, root))
	sf3.grid(row=4, column=0, padx=5)

	renameButton3 = Button(root, text='Rename', command= lambda: renameWindow(2, size, icon, root))
	renameButton3.grid(row=4, column=1, padx=5)

	deleteButton3 = Button(root, text='Delete', command= lambda: delete(2, size, icon, root))
	deleteButton3.grid(row=4, column=2, padx=5)

	# makes everything spread out on the window evenly
	root.grid_columnconfigure(0,weight=1)
	root.grid_rowconfigure(0,weight=1)
	root.grid_rowconfigure(1,weight=1)
	root.grid_rowconfigure(2,weight=1)
	root.grid_rowconfigure(3,weight=1)
	root.grid_rowconfigure(4,weight=1)

	# if user is exitting game
	root.protocol("WM_DELETE_WINDOW", onClosing)

	# creates a loop for events
	root.mainloop()