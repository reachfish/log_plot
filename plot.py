#!/usr/bin/python
#coding:utf-8

import os
import matplotlib
if not os.getenv("DISPLAY", None):
	matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pattern
import numpy

def show_plot(fields, log_files, save_name, incl=None, begin_time=None, end_time=None):
	mgr = pattern.PatternManager()
	results = mgr.match(fields, log_files, incl, begin_time, end_time)
	if not results:
		print "Not Find"
		return

	inches = (18.5, 10.5)
	plot_num = len(results)
	fig, axes = plt.subplots(plot_num, sharex=True)
	fig.autofmt_xdate()
	fig.set_size_inches(*inches)

	if type(axes) != numpy.ndarray:
		axes = (axes,)
	for ax, (field, data) in zip(axes, results.items()):
		ax.set_title(field)
		ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
		for _id, (x, y) in data.iteritems():
			ax.plot(x, y, label=str(_id))

	plt.savefig(save_name + ".png")
	plt.show()

if __name__ == "__main__":
	import sys
	import config
	mgr = pattern.PatternManager()
	mgr.load_patterns(config.patterns)
	mgr.add_value_filter(pattern.Excl0Filter(config.exc_0_fields))
	mgr.add_post_processer(pattern.StampPostProcesser(config.stamp_type_fields))

	
	def help():
		print """
usage:

log_file_name     out_pic_name     fields
	查看指标图

support fields:

"""
		print "  ".join(mgr.get_fields())
		print ""
		print "常用用法"
		for i, fields in config.cases.iteritems():
			print i, "  ".join(fields)

	if len(sys.argv) < 4:
		help()
		exit()

	log_file_names = sys.argv[1]
	save_name = sys.argv[2]
	fields = sys.argv[3:]
	index = sys.argv[3]
	if index.isdigit():
		fields = config.cases.get(int(index), None)
		if not fields:
			help()
			exit()

	show_plot(fields, log_file_names, save_name)


