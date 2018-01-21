#!/usr/bin/python
#coding:utf-8

import base
import pattern
import plot
import unittest

class TestTime(unittest.TestCase):
	def test_time(self):
		self.assertTrue(base.Time("2018-01-12 16:00:09") == base.Time("2018-01-12 16:00:09"))
		self.assertTrue(base.Time("2018-01-12 16:00:09") < base.Time("2018-01-12 16:00:10"))

		t = base.Time("2018-01-12 16:00:09") 
		self.assertEqual("2018-01-12 16:01:09", (t + 60).get_str())
		self.assertTrue(t == base.Time(t.get_stamp()))
		self.assertTrue(t == base.Time(t.get_str()))
		self.assertTrue(t == base.Time(t.get_datetime()))

		self.assertEqual("2018-01-12 16:00:09", base.Time.parse_time("1000:2018-01-12 16:00:09 ").get_str())

class TestPattern(unittest.TestCase):

	def test_parse_raw_pattern(self):

		def test(raw, replace):
			self.assertEqual(replace, pattern.Pattern("").parse_raw_pattern(raw))

		test("[hello],(world)!Are You Ok?\\\\", "\\[hello\\],\\(world\\)!Are You Ok\\?\\\\\\\\")
		test("streamId $_id$, video_rtt $video_rtt$ %d", "streamId {0}, video_rtt {0} {1}".format(pattern.val_regex, pattern.num_regex))
		test("in $recv$, .* out $pending$", "in {0}, .* out {0}".format(pattern.val_regex))

		#self.assertEqual({"_id":1, "video_rtt":2}, pattern.Pattern("streamId $_id$, video_rtt $video_rtt$ ").get_fields())

	def test_match(self):
		p = pattern.Pattern("range $in_range$ total $in_total$ $in_range_count$, distrb $in_dist$ out: range $out_range$")
		s = "range [232757, 233056] total 299 300, distrb [4, 15, 17] out: range [232774, 232994]"
		result, _id = p.match(s, ["in_range"])
		self.assertEqual({"in_range":[232757, 233056]}, result)
		result, _id = p.match(s, ["in_total"])
		self.assertEqual({"in_total":299}, result)
		result, _id = p.match(s, ["out_range"])
		self.assertEqual({"out_range":[232774, 232994]}, result)
		s = " create audio receiver 12345"
		p = pattern.Pattern("$audio_status:1$ create audio receiver $_id$")
		result, _id = p.match(s, ["audio_status"])
		self.assertEqual({"audio_status":1}, result)

class TestPatternManager(unittest.TestCase):

	def test_match(self):
		patterns = (
			"[videoJitter] %d $_id$ normal in past %d ms in: range $in_range$ .*, distrb $in_dist$ out: range $out_range$ total %d %d, distrb $out_dist$ END",
		) 

		fields = ("in_dist", "out_dist")
		file_names = "test.log"
		mgr = pattern.PatternManager()
		mgr.load_patterns(patterns)
		self.assertTrue(mgr.match(fields, file_names))
		self.assertFalse(mgr.match(fields, file_names, begin_time="2019-01-01 00:00:00"))
		self.assertFalse(mgr.match(fields, file_names, end_time="2018-01-01 00:00:00"))
		self.assertTrue(mgr.match(fields, file_names, incl=".* normal"))
		self.assertFalse(mgr.match(fields, file_names, incl="not exits"))

class TestPlot(unittest.TestCase):

	def test_plot(self):
		patterns = (
			"[audioJitter] %d $_id$ normal in past %d ms in: range $in_range$ .*, distrb $in_dist$ out: range $out_range$ total %d %d, distrb $out_dist$",
		) 

		fields = ("in_dist", "out_dist")
		file_names = "test.log"
		mgr = pattern.PatternManager()
		mgr.load_patterns(patterns)
		plot.show_plot(fields, file_names, "test")


if __name__ == "__main__":
	unittest.main()

