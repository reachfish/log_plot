#!/usr/bin/python
#coding:utf-8

import re
import base

num_regex = "-?\d+"
val_regex = "(%s|\[[^\]]+\])"%(num_regex,)

class PreFilter(object):
	def __init__(self, fields):
		self._fields = fields

	def filter(self, field, value):
		pass

class Excl0Filter(PreFilter):
	def filter(self, field, value):
		return value == 0 and field in self._fields

class PostProcesser(object):
	def __init__(self, fields):
		self._fields = fields

	def process(self, results):
		pass

class StampPostProcesser(PostProcesser):
	def process(self, results):
		for field, datas in results.iteritems():
			if field not in self._fields:
				continue

			for d in datas.itervalues():
				d[1] = [ v - min(d[1]) + 1000 for v in d[1] ]

class Pattern(object):
	def __init__(self, pattern):
		self._fields = {}
		lst = re.findall(r"\$\[?([\w\d_]+)\]?\$", pattern)
		if lst:
			self._fields = dict([ (v, i) for i, v in enumerate(lst, 1) ])
		elif pattern:
			print "Pattern No Field", pattern

		pattern = self.parse_raw_pattern(pattern)
		self._pattern = re.compile(pattern)


	def parse_raw_pattern(self, pattern):
		for c in "\\()[]{}+?":
			pattern = pattern.replace(c, "\\" + c)

		pattern = re.sub("\$[\w\d_]+\$", val_regex, pattern)
		pattern = re.sub("\$[\w\d_]+:\d+\$", "", pattern)
		pattern = re.sub(r"%d|%u|%hhu", num_regex, pattern)
		#pattern = re.sub(r"%f", "-?\d+.\d+", pattern)

		for c in "$":
			pattern = pattern.replace(c, "\\" + c)

		return pattern

	def get_fields(self):
		return self._fields

	def match(self, content, fields):
		m = self._pattern.search(content)
		if not m:
			return None, None

		result = {}
		for field in fields:
			index = self._fields.get(field, None)
			if index != None:
				result[field] = m.group(index)

		_id_idx = self._fields.get("_id", None)
		_id = m.group(_id_idx) if _id_idx else None

		return result, _id

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
			for field in pattern.get_fields().keys():
				if not self._fields.get(field, None):
					self._fields[field] = []
				self._fields[field].append(index)
			index += 1

	def get_fields(self):
		return self._fields.keys()

	def add_value_filter(self, filter):
		self._filters.append(filter)

	def add_post_processer(self, processer):
		self._processers.append(processer)

	def match(self, fields, file_names, incl=None, begin_time=None, end_time=None):
		if type(file_names) == str:
			file_names = (file_names,)
		patterns = self._find_patterns(fields)
		results = {}
		for file_name in file_names:
			self._match_patterns(file_name, fields, patterns, incl, begin_time, end_time, results)

		for processer in self._processers:
			processer.process(results)

		return results

	def _find_patterns(self, fields):
		exclude = []
		patterns = []
		for field in fields:
			if not self._fields.get(field, None):
				exclude.append(field)
				continue
			for pattern in self._fields[field]:
				if not pattern in patterns:
					patterns.append(pattern)

		if exclude:
			print '[Warning] No Field Pattern:', exclude

		return [self._patterns[i] for i in patterns]

	def _match_patterns(self, file_name, fields, patterns, incl, begin_time, end_time, results):
		t1 = base.Time(begin_time) if begin_time else None
		t2 = base.Time(end_time) if end_time else None
		pat = re.compile(incl) if incl else None
		with open(file_name) as f:
			for line in f:
				t = base.Time.parse_time(line)
				if t1 and t < t1:
					continue
				if t2 and t > t2:
					break
				if pat and not pat.search(line):
					continue
				for pattern in patterns:
					result, _id = pattern.match(line, fields)
					if not result:
						continue

					if _id is None:
						_id = "$_id"
					for field, value in result.iteritems():
						self._put_field(field, _id, t, value, results)

	def _put_field(self, field, _id, t, value, results):
		if not results.get(field):
			results[field] = {}
		data = results[field]
		if not data.get(_id, None):
			data[_id] = [[],[]]
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

