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

def get_pattern(file_name, pattern, begin_time, end_time):
	pattern_obj = re.compile(pattern) 

	result = []
	times = []
	begin_time_stamp = str2stamp(begin_time) if begin_time else None
	end_time_stamp = str2stamp(end_time) if end_time else None
	with open(file_name) as f:
		for line in f:
			time = get_time(line)
			time_stamp = str2stamp(time)
			if begin_time_stamp and time_stamp < begin_time_stamp:
				continue
			if end_time_stamp and time_stamp > end_time_stamp:
				break

			m = pattern_obj.search(line)
			if m:
				times.append(time)
				result.append([eval(v) for v in m.groups()])
				# for value in m.groups():
					# if value.find(",") == -1:
						# times.append(time)
						# result.append(int(value))
					# else:
						# values = [ int(v) for v in value.split(",") ]
						# times.append([ stamp2str(time_stamp - i + 1) for i in range(len(values), 0, -1) ])
						# result.append(values)

	return result, times

def plot(save_name, data, inches=None): 
	inches = inches or (18.5, 10.5)

	fig = plt.figure(save_name)
	fig.set_size_inches(*inches)
	fig.autofmt_xdate()
	plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
	#plt.legend(loc='best')
	plt.plot(*data)
	plt.savefig(save_name + ".png")
	plt.show()

def subplots(save_name, datas, titles=None, inches=None):
	empty = True
	for data in datas:
		if data:
			empty = False
			break
	if empty:
		return

	inches = inches or (18.5, 10.5)

	plot_num = len(datas)
	fig, axes = plt.subplots(plot_num, sharex=True)
	fig.autofmt_xdate()
	fig.set_size_inches(*inches)
	plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))

	for ax, data, title in zip(axes, datas, titles or ['P' + str(i+1) for i in range(plot_num)]):
		if not data:
			continue

		ax.set_title(title)
		ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
		for d in data:
			ax.plot(d[0], d[1],  label=str(d[2]))

	plt.savefig(save_name + ".png")
	plt.show()

def get_pattern_data(file_names, pattern_config, begin_time, end_time):
	pattern, fields, uid_index = pattern_config
	contents = []
	times = []
	for file_name in file_names:
		contents_, times_ = get_pattern(file_name, pattern, begin_time, end_time)
		contents.extend(contents_)
		times.extend(times_)

	ways = {}
	for content, time in zip(contents, times):
		uid = content[uid_index] if uid_index != -1 else 0
		if not ways.get(uid, None):
			ways[uid] = [[[], []] for i in range(len(fields))]

		time_stamp = str2stamp(time)
		time_dtime = str2datetime(time)
		for i, field in enumerate(fields):
			index = field[1]
			inc0 = True if len(fields) >= 3 and fields[2] else False
			value = content[index]
			if type(value) == list:
				ways[uid][i][0].extend([ datetime.datetime.fromtimestamp(time_stamp - j + 1) for j in range(len(value), 0, -1)])
				ways[uid][i][1].extend(value)
			elif inc0 or value != 0:
				ways[uid][i][0].append(time_dtime)
				ways[uid][i][1].append(value)

	names = [ field[0] for field in fields ]
	datas = []
	for i in range(len(fields)):
		data = []
		for uid, way in ways.iteritems():
			# data.append(way[i][0]) #time list
			# data.append(way[i][1]) #value list
			data.append([way[i][0], way[i][1], uid])
		datas.append(data)

	return datas, names

def show_pattern_plot(log_names, save_name, patterns, begin_time=None, end_time=None, inches=None):
	all_datas = []
	all_names = []

	log_files = log_names.split(",")
	for pattern_config in patterns:
		datas, names =  get_pattern_data(log_files, pattern_config, begin_time, end_time)
		all_datas.extend(datas)
		all_names.extend(names)

	for i, name in enumerate(all_names):
		if name.find("decode_delta") != -1:
			data = all_datas[i]
			for j in range(len(data)):
				d = data[j][1]
				data[j][1] = [ v - min(d) + 1000 for v in d]
		# for i in range(1, len(data), 2):
			# d = data[i]
			# data[i] = [ v - min(d) + 1000 for v in d ]

	subplots(save_name, all_datas, all_names)

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

