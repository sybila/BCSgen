from Tkinter import *
from tkFileDialog import askopenfilename

class Application(Frame):
	def ready(self):
		if self.rules and self.initial and self.vertices and self.edges:
			return True
		else:
			return False

	def compute(self):
		return

	def set_rules(self):
		self.rules = askopenfilename()
		self.text_rules.config(state=NORMAL)
		self.text_rules.delete(0, END)
		self.text_rules.insert(END, self.rules.__str__())
		self.text_rules.config(state="readonly")
		print self.rules

	def set_initial(self):
		self.initial = askopenfilename()
		self.text_initial.config(state=NORMAL)
		self.text_initial.delete(0, END)
		self.text_initial.insert(END, self.initial.__str__())
		self.text_initial.config(state="readonly")
		print self.initial

	def set_vertices(self):
		self.vertices = askopenfilename()
		self.text_vert.config(state=NORMAL)
		self.text_vert.delete(0, END)
		self.text_vert.insert(END, self.vertices.__str__())
		self.text_vert.config(state="readonly")
		print self.vertices

	def set_edges(self):
		self.edges = askopenfilename()
		self.text_edg.config(state=NORMAL)
		self.text_edg.delete(0, END)
		self.text_edg.insert(END, self.edges.__str__())
		self.text_edg.config(state="readonly")
		print self.edges

	def set_parallel(self):
		self.parallel = not self.parallel
		print self.parallel

	def set_memo(self):
		self.memoization = not self.memoization
		print self.memoization

	def print_all(self):
		print "rules: ", self.rules
		print "initial: ", self.initial
		print "vertices: ", self.vertices
		print "edges: ", self.edges
		print "parallel: ", self.parallel
		print "memoization: ", self.memoization
		print "bound: |", int(self.bound.get()), "|"

	def createWidgets(self):
		self.mes = Message(root,text='Input', width=300, font="bold", borderwidth=8, relief= RIDGE)
		self.mes.grid(row=0, column=0, columnspan=2, ipadx=205)

		self.text_rules = Entry(root,width=30, state="readonly", readonlybackground='white')
		self.text_rules.grid(row=1, column=1)

		self.button_rules = Button(root,text="Rules",command=self.set_rules, width=25)
		self.button_rules.grid(row=1, column=0)

		self.text_initial = Entry(root,width=30, state="readonly", readonlybackground='white')
		self.text_initial.grid(row=2, column=1)

		self.button_init = Button(root,text="Initial state",command=self.set_initial,  width=25)
		self.button_init.grid(row=2, column=0)

		self.bound_name = Label(root,text="Bound:",  width=25).grid(row=3, column=0)
		self.bound_wid = Entry(root,textvariable=self.bound, width=30)
		self.bound_wid.grid(row=3, column=1)

		self.mes = Message(root,text='Choose techniques to apply', width=300, font="bold", borderwidth=8, relief= RIDGE)
		self.mes.grid(row=4, column=0, columnspan=2, ipadx=115)

		self.c1 = Checkbutton(root,text="Parallel", command=self.set_parallel)
		self.c1.grid(row=5, column=0)

		self.c2 = Checkbutton(root,text="Memoization", command=self.set_memo) 
		self.c2.grid(row=5, column=1)

		self.mes = Message(root,text='Output', width=300, font="bold", borderwidth=8, relief= RIDGE)
		self.mes.grid(row=6, column=0, columnspan=2, ipadx=200)

		self.text_vert = Entry(root,width=30, state="readonly", readonlybackground='white')
		self.text_vert.grid(row=7, column=1)

		self.button_vert = Button(root,text="Vertices",command=self.set_vertices, width=25)
		self.button_vert.grid(row=7, column=0)

		self.text_edg = Entry(root,width=30, state="readonly", readonlybackground='white')
		self.text_edg.grid(row=8, column=1)

		self.button_edg = Button(root,text="Edges",command=self.set_edges, width=25)
		self.button_edg.grid(row=8, column=0)

		self.compute = Button(root,text="Compute",command=self.compute, width=25, state=DISABLED)
		self.compute.grid(row=9, column=1)

		if self.ready():
			print 'yes'
			self.compute.config(state=NORMAL)


	def __init__(self, master=None):
		Frame.__init__(self, master)
		self.rules = None
		self.initial = None
		self.vertices = None
		self.edges = None
		self.parallel = False
		self.memoization = False
		self.bound = StringVar()
		self.grid()
		self.createWidgets()

root = Tk()
root.title("BCSgen state space generating")
app = Application(master=root)
app.mainloop()

app.print_all()