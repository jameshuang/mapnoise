import os
import sys
import signal
import getopt
import time
import FileDialog

import matplotlib as mpl
mpl.rcParams['examples.directory'] = './'

import matplotlib.pyplot as plt
import matplotlib.cbook as cbook
#import numpy as np
from PIL import Image
import csv

def within(p, lrbt):
	return p[1] >= lrbt[0] and p[1] <= lrbt[1] and p[0] >= lrbt[2] and p[0] <= lrbt[3]

'''
def getPointsFromFileByAlt(file, lrbt, alt):
	p1 = []		# The first point where the flight hit the altitude
	with open(file, 'rb') as csvfile:
		csvDoc = csv.DictReader(csvfile, delimiter = ',', quotechar='"')
		for row in csvDoc:
			altTmp = float(row['Altitude'])
			if altTmp < alt - 50 or altTmp > alt + 50:
				continue
			pTmp = row['Position'].split(',')
			p = [ float(pTmp[0]), float(pTmp[1]) ]
			if within(p, lrbt): 
				p1 = p
	csvfile.close()
	return p1
'''

def getPointsFromFile(file, lrbt, alt):
	points = []
	with open(file, 'rb') as csvfile:
		csvDoc = csv.DictReader(csvfile, delimiter = ',', quotechar='"')
		for row in csvDoc:
			altTmp = float(row['Altitude'])
			if alt > 0:
				if altTmp < alt - 50 or altTmp > alt + 50:
					continue
			pTmp = row['Position'].split(',')
			p = [ float(pTmp[0]), float(pTmp[1]), altTmp ]
			if within(p, lrbt): 
				points.append(p)
	csvfile.close()
	return points
			
def getPoints(lrbt, dir, mon, alt):
	points = []		# Sample: [ [37.3296,-121.979] ]
	misses = 0
	datadir = os.path.join(dir, mon)
	for f in os.listdir(datadir):
		'''
		#p = getPoint(lrbt, alt, 'data/AS200_a5e3115.csv')
		p = getPoint(lrbt, alt, os.path.join(datadir, f))
		if p:
			points.append(p)
		else:
			misses += 1
		'''
		tmp = getPointsFromFile(os.path.join(datadir, f), lrbt, alt)
		if tmp:
			points += tmp
		else:
			misses += 1
	return points, misses

def getXYC(points, lrbt, w, h):
	wtmp = w / (lrbt[1] - lrbt[0])
	htmp = h / (lrbt[3] - lrbt[2])
	x = []
	y = []
	c = []
	for p in points:
		if p[1] >= lrbt[0] and p[1] <= lrbt[1] and p[0] >= lrbt[2] and p[0] <= lrbt[3]:
			x.append((p[1] - lrbt[0]) * wtmp)
			y.append((p[0] - lrbt[2]) * htmp)
			if p[2] > 6000:
				c.append('blue')
			elif p[2] > 5000:
				c.append('royalblue')
			elif p[2] > 4000:
				c.append('mediumpurple')
			elif p[2] > 3000:
				c.append('violet')
			elif p[2] > 2000:
				c.append('magenta')
			elif p[2] > 1000:
				c.append('deeppink')
			else:
				c.append('crimson')
	return x,y,c

def usage():
	print 'Usage: '
	print '    mapnoise.py -d <DataDir> -m <YYYY-MM> -a <Altitude>'
	print '    <Altitude>:  0: all altitudes'
	print '                >0: the specified altitude'

def main(argv):
	DIR = 'data'
	MON = "2016-05"
	ALT = 0
	try:
		opts, args = getopt.getopt(argv,"ha:d:m:")
	except getopt.GetoptError:
		usage()
		sys.exit(1)
	for opt, arg in opts:
		if opt == '-h':
			usage()
			sys.exit(0)
		elif opt in ("-d"):
			DIR = arg
		elif opt in ("-m"):
			MON = arg
		elif opt in ("-a"):
			ALT = int(arg)
		else:
			usage()
			sys.exit(1)
			
	mapImg = os.path.join(os.path.dirname(os.path.realpath(sys.argv[0])), 'images/map.png')
	#mapImgGpsFile = 'images/map.gps'
	mapGps = [-122.178994, -121.767252, 37.224073, 37.486435]

	img = Image.open(mapImg)
	W,H = img.size
	img.close()


	imgfile = cbook.get_sample_data(mapImg)
	imgdata = plt.imread(imgfile)
	ax = plt.gca()
	plt.text(0.5, 0.01, 'MapNoise (c) 2016', ha='center', va='center', transform=ax.transAxes)
	plt.axis('off')
	plt.imshow(imgdata, zorder=0, extent=[0, W, 0, H])
	
	# Load GPS points
	points,misses = getPoints(mapGps, DIR, MON, ALT)
	# Convert to x,y coordinates
	x,y,c = getXYC(points, mapGps, W, H)
	plt.scatter(x,y,color=c,zorder=1)
	plt.title("Month: " + MON + ", Altitude: " + str(ALT) + ', Misses: ' + str(misses))
	plt.show()

if __name__ == "__main__":
	signal.signal(signal.SIGINT, signal.SIG_DFL)
	main(sys.argv[1:])
