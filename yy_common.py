#!/usr/bin/python
#coding:utf-8

import sys
import os
import re
import time as TIME

def get_time(log):
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

def stamp2str(time):
	return TIME.strftime("%Y-%m-%d %H:%M:%S", TIME.localtime(time))

def time_str_diff(time1, time2):
	return str2stamp(time1) - str2stamp(time2)

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
		cmd = sys.argv[1]
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

