''''Use this class for the retreival of data.'''
import pdb
import numpy as np
import pandas as pd
import random
import datetime as dt
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
pd.plotting.register_matplotlib_converters()  # Removes warning messages


## Randomize data for now
#   Initialize variables
atime = np.array([dt.datetime.now()])           # sample time array
ammr = np.array([random.uniform(0.0001,0.05)])    # mmr array
adewpt = np.array([random.uniform(0,90)])         # dew point array (degF)
arh = np.array([random.uniform(0,100)])           # relative humidity array

#	First Print Line
print('time\tmmr\tdewpt\trh')

# 	Function for help with plotting
style.use('fivethirtyeight')
fig = plt.figure()             # Initialize plot
ax = fig.add_subplot(111)      # Initialize axis

#	Start creating data
def data(i):

	#	Generate random data
	p_m = random.choice([-1,1])    		# randomly select +/-
	var = random.uniform(0.001,0.01)      # variance from last scan
	tm = dt.datetime.now()
	mmr = ammr[-1] * (1 + p_m*var)
	dewpt = adewpt[-1] * (1 + p_m*var)
	rh = arh[-1] * (1 + p_m*var)

	#	Append data to array
	atime = np.append(atime, tm)
	ammr = np.append(ammr, mmr)
	adewpt = np.append(adewpt, dewpt)
	arh = np.append(arh, rh)

	# 	Start by printing
	print('{}\t{:.4f}\t{:.2f}\t{:.2f}'.format(tm.strftime('%H%M%S'),mmr,dewpt,rh))

	# 	Create plot
	ax.clear()
	ax.plot(atime,adewpt)



# pdb.set_trace()
ani = animation.FuncAnimation(fig, data, frames=200, interval=1000)

plt.show()







## Retreive data from RS232


## Retreive data from Analog input
# COPY FROM dataq.py WHEN ABLE TO GET WORKING
