#!/usr/bin/python
#coding:utf-8

import re
import base

class PreFilter(object):
	def __init__(self, fields):
		self._fields = fields

	def filter(self, field, value):
		pass

class Inc0Filter(PreFilter):
	def filter(self, field, value):
		return value != 0 or field not in self._fields

class PostProcesser(object):
	def __init__(self, fields):
		self._fields = fields

	def process(self, field, data):
		pass

class StampPostProcesser(PostProcesser):
	def process(self, field, data):
		if field not in fields:
			return

		for _id in data.keys():
			d = data[_id]
			data[_id] = [ v - min(d) + 1000 for v in d ]


class Pattern(object):
	def __init__(self, pattern):
		self._parse_raw_pattern(pattern)

	def _parse_raw_pattern(self, pattern):
		self._fields = {}
		word_regex = r"\$[\w\d_]+\$"
		m = re.match(word_regex, pattern)
		if not m:
			return

		for i, v in enumerate(m.groups(), 1):
			self._fields[v] = i

		for c in "\\()[]{}+*?.":
			pattern = pattern.replace(c, "\\" + c)

		self._pattern = re.subn(word_regex, "(\d+)", pattern)

	def get_fields(self):
		return self._fields

	def match(content, fields):
		m = self._pattern.search(content)
		if not m:
			return

		result = {}
		for field in fields:
			index = self._fields.get(field, None)
			if index != None:
				result[field] = m.group(index)

		return result

class PatternManager(object):
	__metaclass__ = base.Singleton 

	def __init__(self):
		self._patterns = []
		self._fields = {}
		self._filters = []
		self._processers = []

	def load_patterns(self, patterns):
		index = len(self._patterns)
		for patt in patterns:
			pattern = Pattern(patt)
			self._patterns.append(pattern)
			for field in patt.get_fields().keys():
				if not self._fields.get(field, None):
					self._fields[field] = []
				self._fields[field].append(index)
			index += 1

	def add_value_filter(self, filter):
		self._filters.append(filter)

	def add_post_processer(self, processer):
		self._processers.append(processer)

	def match(self, fields, file_names, begin_time, end_time):
		patterns = self._find_patterns(fields)
		results = [{} for i in range(len(fields))]
		for file_name in file_names:
			self._match_patterns(file_name, fields, patterns, begin_time, end_time, results)

		for processer in self.processer:
			for field, data in results.iteritems():
				processer.process(field, data)

		return results

	def _match_patterns(self, file_name, fields, patterns, begin_time, end_time, results):
		t1 = base.Time(begin_time) if begin_time else None
		t2 = base.Time(end_time) if end_time else None
		with open(file_name) as f:
			for line in f:
				t = base.Time.parse_time(line)
				if t1 and t < t1:
					continue
				if t2 and t > t2:
					break
				for pattern in patterns:
					result = pattern.match(line, fields)
					if not result:
						continue

					_id = result.get("_id", "_id_") 
					for field, value in result.iteritems():
						self._put_field(field, _id, t, value, results[field])

	def _put_field(self, field, _id, t, value, data):
		if not data.get(_id, None):
			data[_id] = ([],[],_id)
		value = eval(value)
		if type(value) == list:
			data[_id][0].extend([(t - i + 1).get_datetime() for i in range(len(value), 0, -1)])
			data[_id][1].extend(value)
		else:
			for flt in self._filters:
				if flt.filter(field, value):
					return
			data[_id][0].append(t.get_datetime())
			data[_id][1].append(value)


