#top-level class for hackcmu2015
from Tkinter import *
from ttk import Button,Scrollbar


class Display(object):
	def __init__(self,width,height):
		self.width = width
		self.height = height
		self.font = "helvetica 16"
		self.col_bg = "#FFFFFE"
		self.col_text = "#CCCCCF"
		self.col_max = (255,14,47)
		self.col_min = (111,130,158)
	
	
	def init_interface(self,root):
		#widget declarations
		self.searchbar = Entry(root,font=self.font,bg=self.col_bg,foreground=self.col_text)
		self.execute = Button(root,text="Get Trends",command=self.query)
		self.scrolltime = Scrollbar(root,orient=HORIZONTAL,command=self.temp)
		#self.scrolltime.config(command=self.output.yview)
		
		#gridding of widgets
		self.map = Canvas(root,width=0.8*self.width,height=0.8*self.height,bg=self.col_bg)
		self.map.grid(row=2,column=2,rowspan=4,columnspan=4,sticky=W+E+N+S)
		self.searchbar.grid(row=1,column=2,columnspan=3,sticky=W+E+N+S,padx=20,pady=20)
		self.execute.grid(row=1,column=5,sticky=W)#,sticky=W+E+N+S)
		self.scrolltime.grid(row=6,column=2,columnspan=4,sticky=W+E+N+S)
		
	def temp(self,x,y):
		print "%s,%s"%(x,y)
		
	def convert(self,data):
		results = {}
		for pair in data:
			(state,factor) = pair
			(r,g,b) = tuple(map(lambda x, y: (factor/100)*x + (1 - factor/100)*y, self.col_min, self.col_max))
			results[state] = "%02x02x02x"%(r,g,b)
		return results
		
	def query(self):
		term = self.searchbar.get()
		self.searchbar.delete(0,'end')
		#call Anna's code
		data = []
		#amal's code on self.convert(data)
		
	def run(self):
		root = Tk()
		self.init_interface(root)
		root.mainloop()
		
whale = Display(700,500)
whale.run()		