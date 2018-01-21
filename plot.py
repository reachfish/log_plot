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
import getopt

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
		lines = []
		for _id, (x, y) in data.iteritems():
			line, = ax.plot(x, y, label=str(_id))
			lines.append(line)
		ax.legend(handles=lines)

	full_save_name = save_name + ".png"
	plt.savefig(full_save_name)
	plt.show()

	print 'save_file:',  full_save_name

if __name__ == "__main__":
	import sys
	import re
	import config
	mgr = pattern.PatternManager()
	mgr.load_patterns(config.patterns)
	mgr.add_value_filter(pattern.Excl0Filter(config.exc_0_fields))
	mgr.add_post_processer(pattern.StampPostProcesser(config.stamp_type_fields))
	# mgr.add_post_processer(pattern.KeepLastProcesser(config.keep_last_fields))

	
	def help():
		print """
usage:

-f log_file_names  [-o out_pic_name]  -a  fields   [-i  include]   [-b  begin_time]  [-e  end_time]
	查看指标图

	-f log_file_names  log文件名,可以多个，文件名间用逗号分开
	-o out_pic_name 输出图片名，默认为out
	-a 指标，指标间用逗号分开
	-i include    过滤包含关键字内容，可选
	-b begin_time 日志开始时间，格式为 2000-01-01 00:00:00 这样的，可选
	-e end_time   日志结束时间，可选

	python plot.py -f 1.log  -out video_rtt  -a   video_rtt
	python plot.py -f 1.log  -a video_rtt,video_decode  -b "2018-01-20 10:00:00"

support fields:

"""
		print "  ".join(mgr.get_fields())
		print ""
		print "常用用法"
		for i, fields in config.cases.iteritems():
			print i, "  ".join(fields)

	try: 
		opts,args = getopt.getopt(sys.argv[1:], "f:o:a:i:b:e", [])
	except getopt.GetoptError:
		help()
		exit()

	log_file_names = ""
	out_pic_name = "out"
	fields = []
	begin_time = ""
	end_time = ""
	include = ""

	p = re.compile(r"[;,\s]\s*")
	for o, a in opts:
		if not a: continue
		if o == "-f":
			log_file_names = p.split(a)
		elif o == "-o":
			out_pic_name = a
		elif o == "-i":
			include = a
		elif o == "-b":
			begin_time = a
		elif o == "-e":
			end_time = a
		elif o == "-a":
			for v in p.split(a):
				if v.isdigit():
					fields.extend(config.cases.get(int(v), []))
				else:
					fields.append(v)

	if not log_file_names:
		print "请输入文件名 -f"
		exit()

	if not fields:
		print "请输入查看指标 -a"
		exit()

	show_plot(fields, log_file_names, out_pic_name, include, begin_time, end_time)

