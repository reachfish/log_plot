#!/usr/bin/python
#coding:utf-8

import base
import pattern
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
		test("streamId $_id$, video_rtt $video_rtt$ ", "streamId (\d+), video_rtt (\d+) ")
		test("in $[recv]$, .* out $[pending]$", "in (\[[^\]]+\]), .* out (\[[^\]]+\])")

		self.assertEqual({"_id":1, "video_rtt":2}, pattern.Pattern("streamId $_id$, video_rtt $video_rtt$ ").get_fields())

	def test_match(self):
		p = pattern.Pattern("range $[in_range]$ total $in_total$ $in_range_count$, distrb $[in_dist]$ out: range $[out_range]$")
		s = "range [232757, 233056] total 299 300, distrb [4, 15, 17] out: range [232774, 232994]"
		self.assertEqual({"in_range":"[232757, 233056]"}, p.match(s, ["in_range"]))
		self.assertEqual({"in_total":"299"}, p.match(s, ["in_total"]))
		self.assertEqual({"out_range":"[232774, 232994]"}, p.match(s, ["out_range"]))


if __name__ == "__main__":
	unittest.main()

