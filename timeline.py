#! /bin/env python
# SC 20160328 Plot detection timeline
# CJL 20161117 Update for VLA FRB 121102 paper

from numpy import *
from matplotlib.pyplot import *
import datetime
from pylab import date2num
from astropy import time

# parse obs data
(obs, t1, t2, tel, burst) = loadtxt('obs_data.txt', dtype=str, unpack=True)
for i in range(len(obs)):
	if obs[i] == 'mjd':
		t1c = time.Time(float(t1[i]), format='mjd').iso
		t2c = time.Time(float(t2[i]), format='mjd').iso
		obs[i], t1[i] = t1c.split()
		_, t2[i] = t2c.split()
obsdate = array(map(lambda od: datetime.datetime.strptime(od, "%Y-%m-%d"), obs))

# Define an offset and symbol type for each telescope
telescopes = ['AO', 'VLA', 'Effelsberg', 'AMI']
offs = [3, 2, 1, 0]
offset = dict(zip(telescopes, offs))
psyms = ['+', 'v', 'x', '.']
psym = dict(zip(telescopes, psyms))
pcols = ['g','r','b','y']
pcol = dict(zip(telescopes, pcols))

# set font properties
rc('font', family='sans-serif')
rc('font', serif='Times New Roman')
rc('font', size=16)

def putdot(ax, i):
	pltx = obsdate[i]
	plty = offset[tel[i]]
	if int(burst[i]):
		ax.scatter(pltx, plty, marker='o', s=300, linewidth=2, facecolor='none', edgecolor='k')
		if int(burst[i]) > 1:
			ax.scatter(pltx, plty, marker='o', s=600, linewidth=2, facecolor='none', edgecolor='k')

	ax.scatter(pltx, plty, marker=psym[tel[i]], s=100, linewidth=3, facecolor=pcol[tel[i]], edgecolor='none')

def d2n(yyyy, mm, dd):
	return( date2num(datetime.date(yyyy, mm, dd)) )

# Paint on all dots, then fiddle

def labeltelleft(ax, num):
	for teln in telescopes:
		yval = offset[teln]
		xval = xl - 0.5
		ax.text(xval, yval, teln, horizontalalignment='right', verticalalignment='center')

def labeltelright(ax, num):
	for teln in telescopes:
		yval = offset[teln]
		xval = xr + 0.5
		ax.text(xval, yval, teln, horizontalalignment='left', verticalalignment='center')

xl = d2n(2016, 8, 19)
xr = d2n(2016, 9, 23)
fig, ax = subplots(1, 1, figsize=(15, 4))
for i in range(len(obsdate)):
	putdot(ax, i)
ax.set_xlim( (xl, xr) )
ax.set_ylim( (-0.4, 3.4) )
ax.tick_params(labelright='off', labelleft='off')

# boxes for simultaneous coverage of VLA bursts
axhspan(-0.2, 3.2, 0.67, 0.701, fill=False, linestyle='dashed') # 57643
axhspan(-0.2, 3.2, 0.726, 0.757, fill=False, linestyle='dashed') # 57645
axhspan(-0.2, 3.2, 0.812, 0.873, fill=False, linestyle='dashed') # 57648 57649

ax.set_yticks( [0, 1, 2, 3] )
#ax0.spines['left'].set_visible(True)
labeltelleft(ax, 0)
labeltelright(ax, 0)

#show()
savefig('timeline.png')