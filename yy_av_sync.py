#!/usr/bin/python
#coding:utf-8

import yy_common as COMMON

def multi_video_sync(file_name):
	print file_name
	print "###################"

	contents, times = COMMON.get_pattern(file_name, r"(\d+) multi video sync state \((\d+)\-\>(\d+) = (\d+)")
	ways = {}

	for content, time in zip(contents, times):
		uid = content[0]
		v1 = int(content[1])
		v2 = int(content[2])
		delta = int(content[3])
		if not ways.get(uid, None):
			ways[uid] = ([], [], [])
		ways[uid][0].append(COMMON.str2datetime(time))
		ways[uid][1].append(v1)
		ways[uid][2].append(v2)

	data = []
	colors = ['r', 'b', 'g', 'k', 'm', 'y']
	for uid, way in ways.iteritems():
		color = colors[0]
		colors.pop(0)
		data.append(way[0])
		data.append(way[1])
		data.append(color + "-")
		data.append(way[0])
		data.append(way[2])
		data.append(color + "+")

	COMMON.plot("video_sync", data)


def video_rtt(file_name, pic_name):
	print file_name
	print "###################"

	patterns = (
		# (r"read video sync state\.\((\d+) decodeDelta (\d+) totalRtt:(\d+) playDelay:\d+ totalDelay:(\d+)", 
			# (("video_decode_delta", 1, False), ("video_rtt", 2, False),("video_total_delay", 3, False)), 0),

		(r"read audio sync state\.\((\d+) decodeDelta (\d+) totalRtt:(\d+) playDelay:\d+ totalDelay:(\d+)", 
			(("audio_decode_delta", 1, False), ("audio_rtt", 2, False),("audio_total_delay", 3, False)), 0),

		# (r"read video sync state\.\((\d+) decodeDelta (\d+) totalRtt:(\d+) playDelay:\d+ totalDelay:(\d+)", 
			# (("decode_delta", 1, False), ("rtt", 2, False),("total_delay", 3, False)), 0),
		# (r"\[videoJitter\] \d+ (\d+) normal.*bufPlayTime (\d+)",
			# (("buffPlay", 1, False),), 0,
			# ),
		# (r"\[videoJitter\] \d+ (\d+) normal in past.*total (\d+) \d+, distrb (\[[^\]]*\]) out: range.* total (\d+) \d+, distrb (\[[^\]]*\])",
			# (("recv", 2, True),("pending", 4, True)), 0,
			# ),
		(r"\[audioJitter\] \d+ (\d+) normal in past.*total (\d+) \d+, distrb (\[[^\]]*\]) out: range.* total (\d+) \d+, distrb (\[[^\]]*\])",
			(("recv", 2, True),("pending", 4, True)), 0,
			),

		# (r"myUid (\d+),.*rttAvg (\d+), rttMin (\d+), rttMax (\d+)",
			# (("rttAvg", 1, True),("rttMin", 2, True),("rttMax", 3, True)), 0,
			# ),
	)

	begin_time = "2018-01-12 16:26:20"
	end_time = "2018-01-12 16:35:00"
	COMMON.show_pattern_plot(file_name, pic_name, patterns, begin_time, end_time)

cmds = {
	"-multi_sync": multi_video_sync,
	"-video_rtt": video_rtt,
}

help_doc = """
usage:

-multi_sync file_name
	多路视频同步修改

-video_rtt: log_name pic_name
	视频rtt

"""

if __name__ == "__main__":
	COMMON.common_main(cmds, help_doc)
