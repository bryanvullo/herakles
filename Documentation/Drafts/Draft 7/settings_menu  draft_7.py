# SETTINGS MENU

# importing libraries
import tkinter as tk
from tkinter import *
from tkinter import messagebox

# importing my own libraries
import database
import credentials

class settings_menu:
	def __init__(self, size, icon, current_settings):
		self.size=size
		self.icon=icon

		# adjusts font for the screen
		if size[0] == 600:
			size[1] +=100
			self.title_font=25
			self.main_font=15
			self.font=10
		elif size[0] == 900:
			self.title_font=50
			self.main_font=30
			self.font=20
		else:
			self.title_font=70
			self.main_font=40
			self.font=25

		# creates a list of all the current settings
		settings = list(current_settings.split(','))

		# settings layout " windowsize, difficulty, volume, music, sfx "
		# creates variables so to change in the menu
		self.window_size = settings[0]
		self.difficulty = settings[1]
		self.volume = settings[2]
		self.music = settings[3]
		self.sfx = settings[4]

	def save(self, volume, music, sfx):
		self.volume=volume
		self.music=music
		self.sfx=sfx
		# saves new settings to database
		settings = self.window_size+','+self.difficulty+','+str(volume)+','+str(music)+','+str(sfx)
		database.save_settings(settings)

		# now store variables in credentials to be retrieved by main script
		sizes = self.window_size.split('x')
		sizes[0] = int(sizes[0])
		sizes[1] = int(sizes[1])

		credentials.window_size = sizes
		credentials.difficulty = self.difficulty
		credentials.volume = self.volume
		credentials.music = self.music
		credentials.sfx = self.sfx

	def set_size(self, size):
		self.window_size = size

	def set_difficulty(self, difficulty):
		self.difficulty = difficulty

	def mute_volume(self, volume, slider):
		self.volume = volume
		slider.set(volume)

	def mute_music(self, music, slider):
		self.music = music
		slider.set(music)

	def mute_sfx(self, sfx, slider):
		self.sfx = sfx
		slider.set(sfx)

	def onClosing(self, root):
		if messagebox.askyesno("Quit", "Would you like to leave. Any unsaved changed will be lost")==1:
			root.destroy()

	def menu(self):
		# initialise tkinter and hides root window
		root = Tk()
		root.withdraw()
		main = Toplevel()

		# window set up
		main.title('Options Menu')
		main.iconphoto(False, tk.PhotoImage(file=self.icon))
		main.geometry(str(self.size[0])+'x'+str(self.size[1]))

		# window content
		title_label=Label(main, text="HERAKLES")
		title_label.config(font=('Courier', self.title_font))
		title_label.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

		option_label=Label(main, text="Options")
		option_label.config(font=('Courier', self.main_font))
		option_label.grid(row=1, column=0, columnspan=4, padx=10, pady=10)

		# size
		size_option_label=Label(main, text="Window Size")
		size_option_label.config(font=('Courier', self.font))
		size_option_label.grid(row=2, column=0, padx=10, pady=10)

		size1_button=Button(main, text='600x400', 
			command=lambda: self.set_size('600x400'))
		size1_button.config(font=('Courier', self.font))
		size1_button.grid(row=2, column=1, padx=10, pady=10)

		size2_button=Button(main, text='900x600', 
			command=lambda: self.set_size('900x600'))
		size2_button.config(font=('Courier', self.font))
		size2_button.grid(row=2, column=2, padx=10, pady=10)

		size3_button=Button(main, text='1050x700', 
			command=lambda: self.set_size('1050x700'))
		size3_button.config(font=('Courier', self.font))
		size3_button.grid(row=2, column=3, padx=10, pady=10)

		# difficulty
		difficulty_option_label=Label(main, text="Difficulty")
		difficulty_option_label.config(font=('Courier', self.font))
		difficulty_option_label.grid(row=3, column=0, padx=10, pady=10)

		difficulty1_button=Button(main, text='Hero', 
			command=lambda: self.set_difficulty('hero'))
		difficulty1_button.config(font=('Courier', self.font))
		difficulty1_button.grid(row=3, column=1, padx=10, pady=10)

		difficulty2_button=Button(main, text='Demigod', 
			command=lambda: self.set_difficulty('demigod'))
		difficulty2_button.config(font=('Courier', self.font))
		difficulty2_button.grid(row=3, column=2, padx=10, pady=10)

		difficulty3_button=Button(main, text='Godly', 
			command=lambda: self.set_difficulty('godly'))
		difficulty3_button.config(font=('Courier', self.font))
		difficulty3_button.grid(row=3, column=3, padx=10, pady=10)

		# volume
		volume_option_label=Label(main, text="Volume")
		volume_option_label.config(font=('Courier', self.font))
		volume_option_label.grid(row=4, column=0, padx=10, pady=10)

		volume_slider = Scale(main, from_=0, to=100, resolution=1, length=150, orient=HORIZONTAL)
		volume_slider.set(int(self.volume))
		volume_slider.grid(row=4, column=1, columnspan=2, padx=10, pady=10)

		mute_volume = Button(main, text='Mute', 
			command=lambda: self.mute_volume(0, volume_slider))
		mute_volume.config(font=('Courier', self.font))
		mute_volume.grid(row=4, column=3, padx=10, pady=10)

		# music
		music_option_label=Label(main, text="Music")
		music_option_label.config(font=('Courier', self.font))
		music_option_label.grid(row=5, column=0, padx=10, pady=10)

		music_slider = Scale(main, from_=0, to=100, resolution=1, length=150, orient=HORIZONTAL)
		music_slider.set(int(self.music))
		music_slider.grid(row=5, column=1, columnspan=2, padx=10, pady=10)

		mute_music = Button(main, text='Mute', 
			command=lambda: self.mute_music(0, music_slider))
		mute_music.config(font=('Courier', self.font))
		mute_music.grid(row=5, column=3, padx=10, pady=10)

		# sfx
		sfx_option_label=Label(main, text="SFX")
		sfx_option_label.config(font=('Courier', self.font))
		sfx_option_label.grid(row=6, column=0, padx=10, pady=10)

		sfx_slider = Scale(main, from_=0, to=100, resolution=1, length=150, orient=HORIZONTAL)
		sfx_slider.set(int(self.sfx))
		sfx_slider.grid(row=6, column=1, columnspan=2, padx=10, pady=10)

		mute_sfx = Button(main, text='Mute', 
			command=lambda: self.mute_sfx(0, sfx_slider))
		mute_sfx.config(font=('Courier', self.font))
		mute_sfx.grid(row=6, column=3, padx=10, pady=10)

		# keys labels
		keys_label=Label(main, text="Key Layout")
		keys_label.config(font=('Courier', self.font))
		keys_label.grid(row=7, column=0, padx=10, pady=10)

		keys2_label=Label(main, text="W\nA\nS\nD\nQ\nE\nSPACE\nSHIFT\nMOUSE")
		keys2_label.config(font=('Courier', self.font))
		keys2_label.grid(row=7, column=1, padx=10, pady=10)

		keys3_label=Label(main, text="Move Up\nMove Left\nMove Down\nMove Right\nSwitch Weapons\nAttack\nJump\nAlternate(Sprint/Special Attack)\nAim/Cursor")
		keys3_label.config(font=('Courier', self.font))
		keys3_label.grid(row=7, column=2, padx=10, pady=10)

		# save button
		save_button=Button(main, text='Save', 
			command=lambda: self.save(volume_slider.get(),music_slider.get(),sfx_slider.get()))
		save_button.config(font=('Courier', self.font))
		save_button.grid(row=8, column=0, columnspan=4, padx=10, pady=10)

		# each row and column have same weight when resizing
		main.grid_columnconfigure(0,weight=1)
		main.grid_columnconfigure(1,weight=1)
		main.grid_columnconfigure(2,weight=1)
		main.grid_columnconfigure(3,weight=1)
		main.grid_rowconfigure(0,weight=1)
		main.grid_rowconfigure(1,weight=1)
		main.grid_rowconfigure(2,weight=1)
		main.grid_rowconfigure(3,weight=1)
		main.grid_rowconfigure(4,weight=1)
		main.grid_rowconfigure(5,weight=1)
		main.grid_rowconfigure(6,weight=1)
		main.grid_rowconfigure(7,weight=1)
		main.grid_rowconfigure(8,weight=1)

		# if user is exitting game
		main.protocol("WM_DELETE_WINDOW", lambda:self.onClosing(root))
		
		# creates a loop for events
		main.mainloop()
