#!/usr/bin/python
# -*-coding:utf-8 -*
from matplotlib.pyplot import figure, show
import matplotlib.pyplot as plt
import sys
import os

def help():
	print "Plots histogram of population. Must be in ***.csv."
	print "\tData formatting\n\t============="
	print "\t\tData must be gathered, column by column."
	print """\t\tFor e.g., 
			x1;y1;z1
			x2;y2;z2
			x3;y3;z3"""
	print "\tOutput\n\t============="
	print "\t\tOne file will be created for each column."
	print """\t\tFor e.g., 
			x1;y1;z1
			x2;y2;z2
			x3;y3;z3
		will create three graphs, one for (x1,x2,x3), one for (y1,y2,y3) and one for (z1,z2,z3).
		The file will be created using the filename and removing the extension.
		For e.g., 
			in/data/file_example.csv => in/data/file_example_{1,2,3}.jpg
			example.data.csv => example.data_{1,2,3}.jpg
			/path/to/file.csv => /path/to/file_{1,2,3}.jpg"""

if len(sys.argv[1:]) > 0:
	if sys.argv[1] == "--help" or sys.argv[1] == "-h":
		print "Displaying help..."
		help()
	else:
		for filename in sys.argv[1:]:
			realname = "".join(filename.split(".")[:-1])
			if os.path.isfile(filename):
				with open(sys.argv[1], 'r') as file:
					lines = file.readlines()
					data = []
					for line in lines:
						d = line.split(";")
						if len(data) == 0:
							data = [[] for i in range(len(d))]
						for i,elt in enumerate(d):
							data[i].append(float(d[i]))
				for i,l in enumerate(data):
					fig=figure()
					ax = fig.add_subplot(111)
					plt.yscale('log')
					ax.hist(data[i], 50,bottom=1)
					fig.savefig(realname + "_" + str(i) + ".jpg")
					print "Created " + realname + "_" + str(i) + ".jpg"
			else:
				print "[FAILED] File " + filename + " doesn't exist here!"
				help()
else:
	print "[FAILED] No file given!"
	help()