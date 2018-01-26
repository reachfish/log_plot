# 功能

根据log搜索字段，并画出时序图

# 安装要求

python + matplotlib

1. 安装python 2.7
2. 安装pip
3. 安装matplotlib，命令:  pip install matplotlib
	如果安装过程报错"UnicodeEncodeError: ‘ascii’ codec can’t encode character",可以参考 http://blog.csdn.net/a542551042/article/details/48676031

# 执行命令

python plot.py -f log_file_names  [-o out_pic_name]  -a  fields   [-i  include]   [-b  begin_time]  [-e  end_time]

	log_file_names: 搜索日志名，可以多个，中间用","分开

	out_pic_name: 输出图片名，默认为out

	fields: 字段名，可以多个，中间用","分开，包含两种
		1. 字段名， 如： video_rtt
		2. 字段的快捷编号，在config.py中的cases中定义， 
		   如cases中定义了 1: ("video_rtt",  "video_decode_delta",
		   "video_total_delay", "video_over_jitter"),
		   则1表示video_rtt,video_decode_delta,video_total_delay,video_over_jitter这几个字段

	include: 搜索结果中包含的关键字，是正则表达式，如 "123456|abcdef" 表示只搜索出现关键字 123456 或 abcdef 的日志行

	begin_time: 开始时间，格式为 "2000-01-01 00:00:00" 这样的，注意不要漏了双引号，不然命令行会错误解析成"2000-01-01"了
	end_time: 结束时间，格式和begin_time一样

例子:
	python  plot.py -f test.log  -a   video_rtt
	python plot.py -f test.log  -a 1,audio_rtt  -b "2018-01-20 10:00:00"

# 模式配置库

配置config.py文件

patterns: 模式串
	1感兴趣的字段
	  1)日志里真实出现的字段，使用"$name$"来表示。如：
		日志 "read audio sync state.(1235891575 decodeDelta 889 totalRtt:69"，
	    假如只对里面的uid和totoalRtt感兴趣，可以增加一个pattern: "read audio sync state.($_id$ decodeDelta %d totalRtt:$video_rtt$"
	    这里，$_id$ 和 $video_rtt$ 就是真实字段。
	  2)日志里没出现的字段，使用"$name:value$"来替代，这里的作用是相当于给这条log打一个变量标志。如：
	     日志："create audio receiver 1439543540"、"1439543540 delete outdate audio receiver"、"1439543540 delete audio receiver"
		 想用一个字段audio_status来分别表示这三种情况，并且create是2，delete outdate是1，delete是0，那么这三条log对应的pattern就可以分别记为 
		"$audio_status:2$ create audio receiver $_id$"
		"$audio_status:1$ $_id$ delete outdate audio receiver"
		"$audio_status:0$ $_id$ delete audio receiver"
	2 不感兴趣的字段，不需要使用字段名，用 "%d"来代替好了，如对1)中的decodeDelta不感兴趣，就不需要给它起名了，直接用 "%d"代替就行了
	3.对于list类型(如[1,2,3,4])的变量会把它的每个值拆分到前面的时间里，如：
	  对于pattern为"videoRecv $video_recv$"的模式在匹配"2018-01-01 01:00:10 videoRecv [1,2,3,4]"后得到的实际结果为:
	  "2018-01-01 01:00:07", video_recv = 1
	  "2018-01-01 01:00:08", video_recv = 2
	  "2018-01-01 01:00:09", video_recv = 3
	  "2018-01-01 01:00:10", video_recv = 4
	4. 特殊字段： $_id$
	  _id表示区分同一个pattern下的不同用户，在画一个字段的图时，不同的_id是对应不同的曲线的。这里，常见的就是对应流的uid。
	5. pattern 里支持 ".*" 来表示任何长度的匹配，如：
		"read audio sync .* totalRtt:$video_rtt$" 是可以匹配上 "read audio sync state.(1235891575 decodeDelta 889 totalRtt:69"的。

stamp_type_fields:时间戳类型的变量
	不同的媒体流比较它们的时间戳大小没意义，放在同一个图会有问题，所以对时间戳类型的变量作了处理，对每个流各自的原始时间戳d，分别做个归一化的处理：d' = d - min{d} + 1000，于是每个流的时间戳，最小值都是1000，这样把它们放在同一个图中才会比较直观

cases: 字段名的快捷编号
	如，里面配置了 1: ("video_rtt",  "video_decode_delta", "video_total_delay", "video_over_jitter"),
	那么编号1,就代表了"video_rtt,video_decode_delta,video_total_delay,video_over_jitter"
	命令行里输入1就简单方便了

