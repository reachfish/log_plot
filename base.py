#!/usr/bin/python
#coding:utf-8

import time
import re
from datetime import datetime

time_fmt = r"(\d+)\-(\d+)\-(\d+) (\d+):(\d+):(\d+)" 

class Time(object):

	def __init__(self, t):
		if type(t) == float:
			self._t = t
		elif type(t) == str:
			m = re.match(time_fmt, t)
			if m:
				tup = [ int(v) for v in m.groups() ]
				tup.extend([0, 0, 0])
				self._t = time.mktime(tup)
			else:
				self._t = 0
		elif type(t) == datetime:
			self._t = time.mktime(t.timetuple())
		else:
			raise TypeError

	@classmethod
	def parse_time(cls, string):
		m = re.search(time_fmt, string)
		if not m:
			return Time(0)

		return Time(time_fmt.replace("(\d+)", "%d").format(*m.groups())

	def get_stamp(self):
		return self._t

	def get_str(self):
		return time.strftime("%Y-%m-%d %H:%M:%S", TIME.localtime(self._t))

	def get_datetime(self):
		return datetime.fromtimestamp(self._t)

	def __lt__(self, other):
		return self._t < other._t

	def ___le__(self, other):
		return self._t <= other._t

	def __eq__(self, other):
		return self._t == other._t

	def __ne__(self, other):
		return self._t != other._t

	def __gt__(self, other):
		return self._t > other._t

	def __ge__(self, other):
		return self._t >= other._t

	def __add__(self, sec):
		return Time(self._t + sec)

	def __sub__(self, sec):
		return Time(self._t - sec)

class Singleton(type):
	def __init__(self, name, bases, class_dict):
		super(Singleton, self).__init__(name, bases, class_dict)
		self._instance = None

	def __call__(self, *args, **kwargs):
		if self._instance is None:
			self._instance = super(Singleton, self).__call__(*args, **kwargs)

		return self._instance

