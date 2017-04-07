#! /bin/env python
# SC 20160328 Plot detection timeline
# CJL 20161117 Update for VLA FRB 121102 paper

from numpy import *
from matplotlib.pyplot import *
from matplotlib.dates import DateFormatter
import datetime
from pylab import date2num
from astropy import time

# parse obs data
(obs, t1, t2, tel, burst, band) = loadtxt(sys.argv[1], dtype=str, unpack=True)
ymds = []
for i in range(len(obs)):
    if obs[i] == 'mjd':
        t1c = time.Time(float(t1[i]), format='mjd').iso
	ymd = t1c.split()[0]
	ymds.append(ymd)
    else:
        ymds.append(obs[i])
obsdate = list(map(lambda od: datetime.datetime.strptime(od, "%Y-%m-%d"), ymds))

# Define an offset and symbol type for each telescope
telescopes = ['Arecibo', 'VLA', 'Effelsberg', 'AMI-LA']
offs = [3, 2, 1, 0]
offset = dict(zip(telescopes, offs))
psyms = ['+', 'v', 'x', '.']
psym = dict(zip(telescopes, psyms))
pcols = ['g','r','b','y']
pcol = dict(zip(telescopes, pcols))

if obsdate[0].year == 2015:
    telescopes = telescopes[:-1]

# set font properties
rc('font', family='sans-serif')
rc('font', serif='Times New Roman')
rc('font', size=16)

def putdot(ax, i):
	pltx = obsdate[i]
	plty = offset[tel[i]]
	if int(burst[i]):
		ax.scatter(pltx, plty, marker='o', s=400, linewidth=2, facecolor='none', edgecolor='k')
		if int(burst[i]) > 1:
			ax.scatter(pltx, plty, marker='o', s=800, linewidth=2, facecolor='none', edgecolor='k')
			if int(burst[i]) > 2:
				ax.scatter(pltx, plty, marker='o', s=1200, linewidth=2, facecolor='none', edgecolor='k')
	if tel[i] == 'AMI':
		s = 250
	else:
		s = 80
#	ax.plot_date(pltx, plty)#, s=band[i], verticalalignment='center', horizontalalignment='center')
	ax.text(pltx, plty, s=band[i], verticalalignment='center', horizontalalignment='center')
#	ax.scatter(pltx, plty, marker=psym[tel[i]], s=s, linewidth=3, facecolor=pcol[tel[i]], edgecolor='none')

def d2n(yyyy, mm, dd):
	return( date2num(datetime.date(yyyy, mm, dd)) )

# Paint on all dots, then fiddle

def labeltelleft(ax, num):
	for teln in telescopes:
		yval = offset[teln]
		xval = xl[num] - 0.5
   		ax.text(xval, yval, teln, horizontalalignment='right', verticalalignment='center')

def labeltelright(ax, num):
	for teln in telescopes:
		yval = offset[teln]
		xval = xr[num] + 0.5
   		ax.text(xval, yval, teln, horizontalalignment='left', verticalalignment='center')

if obsdate[0].year == 2016:
    xl = [d2n(2016, 8, 22)]
    xr = [d2n(2016, 9, 23)]
else:
    xl = [d2n(2015, 11, 22), d2n(2016, 4, 23)]
    xr = [d2n(2015, 12, 21), d2n(2016, 5, 29)]

if obsdate[0].year == 2016:
    fig, ax = subplots(1, 1, figsize=(15, 4.5))
    for i in range(len(obsdate)):
	putdot(ax, i)
    axs = [ax]
else:
    fig, ax = subplots(1, 1, figsize=(15, 4.5))
    gs = GridSpec(1, 2, width_ratios=[1,1.2])
    axs = [subplot(gs[0]), subplot(gs[1])]
    for i in range(len(obsdate)):
        if obsdate[i].year == 2015:        
            ax = axs[0]
        else:
            ax = axs[1]
        putdot(ax, i)

for ax in axs:
    ax.tick_params(labelright='off', labelleft='off')
    ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
    ax.fmt_xdata = DateFormatter('%Y-%m-%d %H:%M:%S')

    if obsdate[0].year == 2016:
        ax.set_ylim( (-0.4, 3.4) )
        ax.set_xlim( (xl[0], xr[0]) )
    else:
        ax.set_ylim( (0.6, 3.4) )
        i = axs.index(ax)
        ax.set_xlim( (xl[i], xr[i]) )

# boxes for simultaneous coverage of VLA bursts
for ax in axs:
    if obsdate[0].year == 2016:
        axhspan(0.1, 1.8, 0.657, 0.657, fill=False, linestyle='dashed') # 57643
        axhspan(0.1, 2.9, 0.718, 0.718, fill=False, linestyle='dashed') # 57645
        axhspan(0.1, 2.9, 0.813, 0.813, fill=False, linestyle='dashed') # 57648 57649
        axhspan(2.1, 2.9, 0.813, 0.813, fill=False, lw=3, linestyle='solid') # 57648 57649
        axhspan(0.1, 2.9, 0.844, 0.844, fill=False, linestyle='dashed') # 57648 57649
        ax.set_yticks( [0, 1, 2, 3] )
    else:
#    	axhspan(1.1, 2.9, 0.657, 0.657, fill=False, linestyle='dashed') # 57643
#	    axhspan(1.1, 2.9, 0.718, 0.718, fill=False, linestyle='dashed') # 57645
        ax.set_yticks( [1, 2, 3] )


for ax in axs:
    ax.tick_params(labelright='off', labelleft='off', width=0)
    i = axs.index(ax)
    if obsdate[0].year == 2016:
        labeltelleft(ax, i)
        labeltelright(ax, i)
    else:
        if i == 0:
            labeltelleft(ax, i)
            ax.spines['right'].set_visible(False)
        elif i == 1:
            labeltelright(ax, i)
            ax.spines['left'].set_visible(False)

fig.autofmt_xdate()

#show()
pngsuff = '0' if '0' in sys.argv[1] else ''
savefig('timeline{0}.png'.format(pngsuff))
