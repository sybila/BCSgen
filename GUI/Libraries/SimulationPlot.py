from PyQt4 import QtGui, QtCore
import math
import matplotlib.pyplot as plt
import numpy as np

class SimulationPlot(QtGui.QWidget):
	def __init__(self, data, times, translations, screenWidth, screenHeight, parent= None):
		super(SimulationPlot, self).__init__()

		self.setWindowModality(QtCore.Qt.ApplicationModal)
		plt.rcParams["figure.figsize"] = (int(math.floor(screenWidth/80.)) - 4, int(math.floor(screenHeight/80.)) - 3)

		self.fig, self.ax = plt.subplots()
		self.fig.canvas.set_window_title('Simulation results')

		size = len(data[0])

		for i in range(size):
			self.ax.plot(times, self.column(data, i), label=translations[i])

		self.ax.legend(loc='upper center', bbox_to_anchor=(0.5,-0.1), ncol=4)

		numOfLines = int(len(translations)/4.0)/2 + 1.2

		self.fig.subplots_adjust(bottom=0.15*numOfLines)
		self.ax.grid('on')

		self.interactive_legend().show()

	def interactive_legend(self):
		if self.ax is None:
			self.ax = plt.gca()
		if self.ax.legend_ is None:
			self.ax.legend()

		return InteractiveLegend(self.ax.legend_)

	def column(self, matrix, i):
 		return [row[i] for row in matrix]

class InteractiveLegend(object):
	def __init__(self, legend):
		self.legend = legend
		self.fig = legend.axes.figure

		self.lookup_artist, self.lookup_handle = self._build_lookups(legend)
		self._setup_connections()

		self.onpick_count = 0

		self.update()

	def _setup_connections(self):
		for artist in self.legend.texts + self.legend.legendHandles:
			artist.set_picker(8) # 8 points tolerance

		self.fig.canvas.mpl_connect('pick_event', self.on_pick)
		self.fig.canvas.mpl_connect('button_press_event', self.on_click)

	def _build_lookups(self, legend):
		labels = [t.get_text() for t in legend.texts]
		handles = legend.legendHandles
		label2handle = dict(zip(labels, handles))
		handle2text = dict(zip(handles, legend.texts))

		lookup_artist = {}
		lookup_handle = {}
		for artist in legend.axes.get_children():
			if artist.get_label() in labels:
				handle = label2handle[artist.get_label()]
				lookup_handle[artist] = handle
				lookup_artist[handle] = artist
				lookup_artist[handle2text[handle]] = artist

		lookup_handle.update(zip(handles, handles))
		lookup_handle.update(zip(legend.texts, handles))

		return lookup_artist, lookup_handle

	def on_pick(self, event):
		if self.onpick_count % 2 == 0:  # this is problem !
			handle = event.artist
			if handle in self.lookup_artist:
				artist = self.lookup_artist[handle]
				artist.set_visible(not artist.get_visible())
				self.update()
		self.onpick_count += 1

	def on_click(self, event):
		if event.button == 3:
			visible = False
		elif event.button == 2:
			visible = True
		else:
			return

		for artist in self.lookup_artist.values():
			artist.set_visible(visible)
		self.update()

	def update(self):
		for artist in self.lookup_artist.values():
			handle = self.lookup_handle[artist]
			if artist.get_visible():
				handle.set_visible(True)
			else:
				handle.set_visible(False)
		self.fig.canvas.draw()

	def show(self):
		plt.show()

