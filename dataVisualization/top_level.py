#top-level class for hackcmu2015
from Tkinter import *
from ttk import Button,Scrollbar
from svgToTkinter import SVG
from parsecsv import *
import pytrends
import requests

import random

class Display(object):
	def __init__(self,image):
		self.map = SVG(image)
		self.width = self.map.width
		self.height = self.map.height
		self.font = "helvetica 16"
		self.col_bg = "#FFFFFE"
		self.col_text = "#CCCCCF"
		self.col_min = (255,14,47)
		self.col_max = (111,130,158)
		self.states = ['WA', 'DE', 'DC', 'WI', 'WV', 'HI', 'FL', 'WY', 'NH', 'NJ', 'NM', 'TX', 'LA', 'NC', 'ND', 'NE', 'TN', 'NY', 'PA', 'MT', 'RI', 'NV', 'VA', 'CO', 'AK', 'AL', 'AR', 'VT', 'GA', 'IN', 'IA', 'MA', 'AZ', 'CA', 'ID', 'CT', 'ME', 'MD', 'OH', 'UT', 'MO', 'MN', 'MI', 'KS', 'OK', 'MS', 'SC', 'KY', 'SD', 'OR', 'IL']
		self.colorDict = {key:"azure" for key in self.states}
		
	
	
	def init_interface(self,root):
		#widget declarations
		self.searchbar = Entry(root,font=self.font,bg=self.col_bg,foreground=self.col_text)
		self.execute = Button(root,text="Get Trends",command=self.query)
		self.scrolltime = Scrollbar(root,orient=HORIZONTAL,command=self.temp)
		#self.scrolltime.config(command=self.output.yview)
		
		#gridding of widgets
		self.space = Canvas(root,width=self.width,height=self.height,bg=self.col_bg)
		self.space.grid(row=2,column=2,rowspan=4,columnspan=4,sticky=W+E+N+S)
		self.searchbar.grid(row=1,column=2,columnspan=3,sticky=W+E+N+S,padx=20,pady=20)
		self.execute.grid(row=1,column=5,sticky=W)#,sticky=W+E+N+S)
		self.scrolltime.grid(row=6,column=2,columnspan=4,sticky=W+E+N+S)
		self.draw_map()
		
	def draw_map(self):
		self.space.delete(ALL)
		self.map.draw(self.space,self.colorDict)
		
	def temp(self,x,y):
		print "%s,%s"%(x,y)
		
	def convert(self,data):
		print data
		results = {}
		for pair in data:
			(state,factor) = (pair[0], pair[1])
			print (state, factor)
			(r,g,b) = tuple(map(lambda x, y: int((float(factor)/100)*x + (1 - float(factor)/100)*y), self.col_min, self.col_max))
			print (r,g,b)
			results[state] = "#%02x%02x%02x"%(r,g,b)
		return results
		
	def query(self):
		term = self.searchbar.get()
		if term !="":
			self.searchbar.delete(0,'end')
			colors = Data(term)
			if colors != []:
				self.colorDict = self.convert(colors.getData())
				self.draw_map()
		
		
	def run(self):
		root = Tk()
		self.init_interface(root)
		root.mainloop()
		
whale = Display("Blank_US_Map.svg")
whale.run()		