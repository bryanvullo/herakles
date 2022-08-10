# PROGRESS MENU

# importing libraries
import tkinter as tk
from tkinter import *
from tkinter import messagebox

# importing my own libraries
import database
import credentials

class progress():
	def __init__(self, size, icon):
		self.size = size
		self.icon = icon

		self.display = 'character'

	def onClosing(self):
		if messagebox.askyesno("Quit", "Would you like to leave. Any unsaved changed will be lost")==1:
			self.root.destroy()

	def change_menu(self, change):
		self.display = change

		self.root.destroy()
		self.menu()

	def menu(self):
		self.items = credentials.items
		self.bosses = credentials.bosses
		self.map = credentials.map_discovered

		# initialise tkinter and hides root window
		root = Tk()
		root.withdraw()
		main = Toplevel()
		self.root = root

		# window set up
		main.title('Progress Menu')
		main.iconphoto(False, tk.PhotoImage(file=self.icon))
		main.geometry(str(self.size[0])+'x'+str(self.size[1]))

		# window content
		title_label=Label(main, text="HERAKLES")
		title_label.config(font=('Courier', 50))
		title_label.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

		map_button=Button(main, text='Map', 
			command=lambda: self.change_menu('map'))
		map_button.config(font=('Courier', 20))
		map_button.grid(row=1, column=0, padx=10, pady=10)

		char_button=Button(main, text='Character', 
			command=lambda: self.change_menu('character'))
		char_button.config(font=('Courier', 20))
		char_button.grid(row=1, column=1, padx=10, pady=10)

		progress_button=Button(main, text='Progress', 
			command=lambda: self.change_menu('progress'))
		progress_button.config(font=('Courier', 20))
		progress_button.grid(row=1, column=2, padx=10, pady=10)

		frame = LabelFrame(main)
		frame.grid(row=2, column=0, columnspan=4, padx=10, pady=10)

		if self.display == 'character':
			char_button.config(relief=SUNKEN)
			label=Label(frame, text= 'character')
			label.config(font=('Courier', 50))
			label.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

		elif self.display == 'map':
			map_button.config(relief=SUNKEN)
			label=Label(frame, text= 'map')
			label.config(font=('Courier', 50))
			label.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

		elif self.display == 'progress':
			progress_button.config(relief=SUNKEN)
			label=Label(frame, text= 'progress')
			label.config(font=('Courier', 50))
			label.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

		# each row and column have same weight when resizing
		main.grid_columnconfigure(0,weight=1)
		main.grid_columnconfigure(1,weight=1)
		main.grid_columnconfigure(2,weight=1)
		main.grid_columnconfigure(3,weight=1)
		main.grid_rowconfigure(0,weight=1)
		main.grid_rowconfigure(1,weight=1)
		main.grid_rowconfigure(2,weight=1)

		# if user is exitting game
		main.protocol("WM_DELETE_WINDOW", self.onClosing)

		# creates a loop for events
		main.mainloop()

# Menu = progress((900,600), 'Sprites/Images/icon.png')
# Menu.menu()

