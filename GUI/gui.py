from time import time
import sys
import os.path
sys.path.append(os.path.abspath('../'))
import Import as Import
import Explicit_state_space_generator as Gen

from Tkinter import *
from tkFileDialog import askopenfilename

"""
Application is main framework for the GUI
"""
class Application(Frame):
    """
    Checks if all fields are filled
    """
    def get_ready(self, *args):
        if self.rules and self.initial and self.vertices and self.edges and self.bound.get() != "":
           self.compute.config(state=NORMAL)

    """
    Computes the state space above set parameters
    """
    def compute(self):
        self.compute.config(state=DISABLED)
        self.compute.config(text="Computing...")

        rules, state = Import.import_rules(self.rules, self.initial)
        states = {state}
        bound = int(self.bound.get())
        done = Gen.work_manager(states, rules, self.vertices, self.edges, bound, self.parallel, self.memoization)

        self.compute.config(state=NORMAL)
        self.compute.config(text="Finish")
        self.compute.config(command=root.destroy)

    """
    Sets path to file with rules
    """
    def set_rules(self):
        self.rules = askopenfilename()
        self.text_rules.config(state=NORMAL)
        self.text_rules.delete(0, END)
        self.text_rules.insert(END, self.rules.__str__())
        self.text_rules.config(state="readonly")

    """
    Sets path to file with initial conditions
    """
    def set_initial(self):
        self.initial = askopenfilename()
        self.text_initial.config(state=NORMAL)
        self.text_initial.delete(0, END)
        self.text_initial.insert(END, self.initial.__str__())
        self.text_initial.config(state="readonly")

    """
    Sets path to output vertices file 
    """
    def set_vertices(self):
        self.vertices = askopenfilename()
        self.text_vert.config(state=NORMAL)
        self.text_vert.delete(0, END)
        self.text_vert.insert(END, self.vertices.__str__())
        self.text_vert.config(state="readonly")

    """
    Sets path to output edges file 
    """
    def set_edges(self):
        self.edges = askopenfilename()
        self.text_edg.config(state=NORMAL)
        self.text_edg.delete(0, END)
        self.text_edg.insert(END, self.edges.__str__())
        self.text_edg.config(state="readonly")

    """
    Sets variable parallel in order to (not) apply paralle computing
    """
    def set_parallel(self):
        self.parallel = not self.parallel

    """
    Sets variable memoization in order to (not) apply memoization
    """
    def set_memo(self):
        self.memoization = not self.memoization

    """
    This is where visual behaviour is maintained
    """
    def createWidgets(self):
        self.mes = Message(root,text='Input', width=300, font="bold", borderwidth=8, relief= RIDGE)
        self.mes.grid(row=0, column=0, columnspan=2, ipadx=205)

        self.text_rules = Entry(root,width=30, state="readonly", readonlybackground='white', textvariable=self.rulesVar)
        self.text_rules.grid(row=1, column=1)

        self.button_rules = Button(root,text="Rules",command=self.set_rules, width=25)
        self.button_rules.grid(row=1, column=0)

        self.text_initial = Entry(root,width=30, state="readonly", readonlybackground='white', textvariable=self.initVar)
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

        self.text_vert = Entry(root,width=30, state="readonly", readonlybackground='white', textvariable=self.vertVar)
        self.text_vert.grid(row=7, column=1)

        self.button_vert = Button(root,text="Vertices",command=self.set_vertices, width=25)
        self.button_vert.grid(row=7, column=0)

        self.text_edg = Entry(root,width=30, state="readonly", readonlybackground='white', textvariable=self.edgVar)
        self.text_edg.grid(row=8, column=1)

        self.button_edg = Button(root,text="Edges",command=self.set_edges, width=25)
        self.button_edg.grid(row=8, column=0)

        self.compute = Button(root,text="Compute",command=self.compute, width=25, state=DISABLED)
        self.compute.grid(row=9, column=1)

        self.exit = Button(root,text="Cancel",command=root.destroy, width=25)
        self.exit.grid(row=9, column=0)

        self.vertVar.trace("w", self.get_ready)
        self.edgVar.trace("w", self.get_ready)
        self.initVar.trace("w", self.get_ready)
        self.rulesVar.trace("w", self.get_ready)
        self.bound.trace("w", self.get_ready)


    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.rules = None
        self.initial = None
        self.vertices = None
        self.edges = None
        self.parallel = False
        self.memoization = False
        self.vertVar = StringVar()
        self.edgVar = StringVar()
        self.initVar = StringVar()
        self.rulesVar = StringVar()
        self.bound = StringVar(value="")
        self.grid()
        self.createWidgets()

root = Tk()
root.title("BCSgen state space generating")
app = Application(master=root)
app.mainloop()