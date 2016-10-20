from Tkinter import *
from tkFileDialog import askopenfilename

class Application(Frame):

    def set_rules(self):
        self.rules = askopenfilename()
        print self.rules

    def set_initial(self):
    	self.initial = askopenfilename()
    	print self.initial

    def click(self, param):
    	print list(self.listbox.curselection())

    def set_vertices(self):
    	self.vertices = askopenfilename()
    	print self.vertices

    def set_edges(self):
    	self.edges = askopenfilename()
    	print self.edges

    def set_parallel(self):
    	self.parallel = not self.parallel
    	print self.parallel

    def set_memo(self):
    	self.memoization = not self.memoization
    	print self.memoization

    def createWidgets(self):

		self.mes = Message(text='Set input files.', width=300, font="bold", borderwidth=8, relief= RIDGE)
		self.mes.pack(fill=X)

		#self.text_rules = Text()
		#self.text_rules.pack(side=RIGHT, anchor=N, fill=X)

		self.button_rules = Button(root,text="Rules",command=self.set_rules)
		self.button_rules.pack(fill=X)

		#self.text_initial = Text()
		#self.text_initial.pack(side=RIGHT, anchor=N, fill=X)

		self.button_init = Button(root,text="Initial state",command=self.set_initial)
		self.button_init.pack(fill=X)

		self.mes = Message(text='Choose techniques to apply.', width=300, font="bold", borderwidth=8, relief= RIDGE)
		self.mes.pack(fill=X)

		self.c1 = Checkbutton(text="    Parallel    ", command=self.set_parallel)
		self.c1.pack()

		self.c2 = Checkbutton(text="Memoization", command=self.set_memo) 
		self.c2.pack()

		self.mes = Message(text='Set output files.', width=300, font="bold", borderwidth=8, relief= RIDGE)
		self.mes.pack(fill=X)

		self.button_vert = Button(root,text="Vertices",command=self.set_vertices)
		self.button_vert.pack(fill=X)

		self.button_edg = Button(root,text="Edges",command=self.set_edges)
		self.button_edg.pack(fill=X)


    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.rules = None
        self.initial = None
        self.vertices = None
        self.edges = None
        self.parallel = False
        self.memoization = False
        self.pack()
        self.createWidgets()

root = Tk()
root.title("BCSgen state space generating")
app = Application(master=root)
app.mainloop()