#!/usr/bin/python
#coding:utf-8

import yy_common as COMMON

def multi_video_sync(file_name):
	print file_name
	print "###################"

	contents, times = COMMON.get_pattern(file_name, r"(\d+) multi video sync state \((\d+)\-\>(\d+) = (\d+)")
	ways = {}

	counter = COMMON.index_counter()
	for content, time in zip(contents, times):
		uid = content[0]
		v1 = int(content[1])
		v2 = int(content[2])
		delta = int(content[3])
		if not ways.get(uid, None):
			ways[uid] = ([], [], [])
		# ways[uid][0].append(counter.get_index(time))
		ways[uid][0].append(COMMON.str2datetime(time))
		ways[uid][1].append(v1)
		ways[uid][2].append(v2)

	data = []
	colors = ['r', 'g', 'b']
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

cmds = {
	"-multi_sync": multi_video_sync,
}

help_doc = """
usage:

-multi_sync file_name
	多路视频同步修改

"""

if __name__ == "__main__":
	COMMON.common_main(cmds, help_doc)
