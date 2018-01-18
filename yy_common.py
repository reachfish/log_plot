#!/usr/bin/python

import sys
import os

def common_main(cmds, help_doc, min_arg_num):
	def help():
		print help_doc

	if len(sys.argv) < min_arg_num:
		help()
	else:
		cmd = cmds.get(sys.argv[1], None)
		if cmd:
			cmd(*sys.argv[2:])
		else:
			help()

if __name__ == "__main__":
	for file_name in os.listdir("/home/yujun/workspace/yycmd"):
		if file_name.endswith(".py") and file_name != "yy_common.py":
			print file_name

