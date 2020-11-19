''''Use this class for the setup of the running plot in the humidity_cart GUI.'''


from matplotlib.backends.backend_qt5agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
import pandas as pd


class Canvas(FigureCanvas):
	def __init__(self, parent=None, width=10, height=6, dpi=100):
		fig = Figure(figsize=(width,height), dpi=dpi)
		self.axes = fig.add_subplot(111)
		
		FigureCanvas.__init__(self, fig)
		self.setParent(parent)
	
	
	def plot(self):
		# Pull in relevent data

