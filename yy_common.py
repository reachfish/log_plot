#!/usr/bin/python
#coding:utf-8

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

import sys
import os
import re
import time as TIME
import datetime

class index_counter:
	def __init__(self, values=None):
		self.m = {}
		self.index = 1
		self.values = values

	def get_index(self, value):
		index = self.m.get(value, None)
		if index:
			return index

		if self.values is not None:
			index = self.values[0]
			self.values.pop(0)
		else:
			self.index += 1
			index = self.index 

		self.m[value] = index 

		return index

def get_time(log):
	m = re.search(r"(\d+)\-(\d+)\-(\d+) (\d+):(\d+):(\d+)", log)
	if m:
		return "{0}-{1}-{2} {3}:{4}:{5}".format(*(m.groups()))

	time_len = len("2018-01-16 10:25:11")
	return log[0:time_len]

def str2stamp(time):
	m = re.match(r'(\d+)-(\d+)-(\d+) (\d+):(\d+):(\d+)', time)
	if not m:
		return 0
	t = [ int(v) for v in m.groups() ]
	t.append(0)
	t.append(0)
	t.append(0)

	return TIME.mktime(t)

def str2datetime(time):
	return datetime.datetime.strptime(time, "%Y-%m-%d %H:%M:%S")

def stamp2str(time):
	return TIME.strftime("%Y-%m-%d %H:%M:%S", TIME.localtime(time))

def time_str_diff(time1, time2):
	return str2stamp(time1) - str2stamp(time2)

def get_pattern(file_name, pattern):
	pattern_obj = re.compile(pattern) 

	result = []
	times = []
	with open(file_name) as f:
		for line in f:
			m = pattern_obj.search(line)
			if m:
				result.append(m.groups())
				times.append(get_time(line))

	return result, times

def plot(save_name, data, inches=None): 
	inches = inches or (18.5, 10.5)

	fig = plt.figure(save_name)
	fig.set_size_inches(*inches)
	fig.autofmt_xdate()
	plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
	plt.plot(*data)
	plt.savefig(save_name + ".png")
	plt.show()



def common_main(cmds, help_doc):
	def help():
		print help_doc

	#解析命令行格式
	lines = help_doc.split("\n")
	fmt = {} 
	for line in lines:
		arr = re.split(r'[;,\s]\s*', line)
		if arr and arr[0] and arr[0][0] == "-":
			fmt[arr[0]] = arr[1:]

	#执行命令
	cmd = None
	func = None
	argv = []
	if type(cmds) == dict:
		cmd = sys.argv[1] if len(sys.argv) > 1 else None
		func = cmds.get(cmd, None)
		argv = sys.argv[2:]
	else:
		cmd = ""
		func = cmds
		argv = sys.argv[1:]

	if not func:
		print help_doc
		return

	if fmt.get(cmd, None) != None and len(argv) !=  len(fmt[cmd]):

		print ""
		print "argment err, usage:"
		print "\t", cmd, " ".join(fmt[cmd]) 
		return

	func(*argv)

if __name__ == "__main__":
	for file_name in os.listdir("/home/yujun/workspace/yycmd"):
		if file_name.endswith(".py") and file_name != "yy_common.py":
			print file_name

