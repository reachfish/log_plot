#!/usr/bin/python
#coding:utf-8

import re
import yy_common as COMMON

def count_thread_max(file_name):
	print file_name
	print "###############"
	pattern = re.compile(r'thread in past (\d+) ms, wakeup (\d+) times')
	lines = []
	limit = 100 
	with open(file_name) as f:
		for line in f:
			m = pattern.search(line)
			if not m:
				continue
			time, wakeup = m.groups()
			wakeup_per_sec = int(wakeup) * 1000 / int(time)
			if wakeup_per_sec >= limit:
				lines.append((wakeup_per_sec, line))
	list.sort(lines, key = lambda elem: -elem[0])
	for elem in lines:
		print elem

	print "\n\n"

def count_thread_win(file_name):
	print file_name
	print "###############"
	pattern = re.compile(r'\[thread\] (.+) thread in past (\d+) ms, wakeup (\d+) times')

	limit = 150 
	win_size = 300

	limit = 400 
	win_size = 100

	counter = {}
	with open(file_name) as f:
		for line in f:
			m = pattern.search(line)
			if not m:
				continue
			name = m.group(1)
			time_stamp = COMMON.str2stamp(COMMON.get_time(line))
			wakeup = int(m.group(3))
			if not counter.get(name, None):
				counter[name] = []

			find = False
			elem = (time_stamp, wakeup,)
			for one in counter[name]:
				t = one[len(one)-1]
				if abs(time_stamp - t[0] - 32) <= 1:
					find = True
					one.append(elem)
					break
				else:
					#print name , time_stamp - t[0], elem[2],  t[2]
					pass
			if not find:
				counter[name].append([elem])

	for name, paths in counter.iteritems():
		#print name, len(paths)
		for arr in paths:
			begin = 0
			end = 0

			total = 0
			time = 0
			window = []
			for (k, v) in arr:
				while window and k - window[0][0] > win_size:
					total -= window[0][1]
					window.pop(0)

				window.append((k,v))
				total += v
				time = k - window[0][0] + 32
				if total >= limit * time and time >= win_size:
					print int(total/time), name, COMMON.stamp2str(window[0][0]), ' ~ ', COMMON.stamp2str(k)
					if end > 0 and k - end > 35:
						#print total/time, name, COMMON.stamp2str(begin), ' ~ ', COMMON.stamp2str(end)
						begin = window[0][1]
					end = k

			#if total >= limit * time and time >= 300:
			#		print total/time, name, COMMON.stamp2str(window[0][0]), ' ~ ', COMMON.stamp2str(end)

cmds = {
	"-max": count_thread_max,
	"-win": count_thread_win,
}

help_doc = """
usage:

-max file_name
  查看线程唤醒最大次数

-win file_name
  查看线程在一段时间内被唤醒次数

"""

if __name__ == "__main__":
	COMMON.common_main(cmds, help_doc)

