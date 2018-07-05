#!/usr/bin/python
#coding:utf-8

#配置config.py时， 先阅读 readme.txt

use_time = True
patterns = (
	#观众音频
	("$audio_status:2$ create audio receiver $_id$", "音频状态"),
	("$audio_status:1$ $_id$ delete outdate audio receiver", "音频状态"),
	("$audio_status:0$ $_id$ delete audio receiver", "音频状态"),
	("read audio sync state.($_id$ decodeDelta $audio_decode_delta$ totalRtt:$audio_rtt$ playDelay:$audio_play_delay$ totalDelay:$audio_total_delay$ overJitter:$audio_over_jitter$", "音频decodedelta状态"),
	("[audioJitter] %d $_id$ normal in past %d ms in: range $audio_in_range$ .*, distrb $audio_recv$ out: range $audio_out_range$ total %d %d, distrb $audio_pending$", "音频收包个数"),

	#观众视频
	("[videoJitter] %d $_id$ normal in past %d ms in: range $video_in_range$ .*, distrb $video_recv$ out: range $video_out_range$ total %d %d, distrb $video_pending$", "视频收包个数"),
	("read video sync state.($_id$ decodeDelta $video_decode_delta$ totalRtt:$video_rtt$ playDelay:$video_play_delay$ totalDelay:$video_total_delay$ overJitter:$video_over_jitter$", "视频decodedelta状态"),
	("discard video cnt:$discard_video$", "观众视频"),

	#主播音频
	("checkIamSpeaking canspeak:.*,voicepacketnum:$spk_voice_pkt_num$", "主播开麦10s音频包数"),

	#主播视频

	#线程
	("transport thread .* wakeup $transport_wakeup$ times", ""),
	("video decode thread .* wakeup $video_decode_wakeup$ times", ""),
	("thread .* wakeup $wakeup$ times", ""),

	("succ now.*ssrc $ssrc$, waittime $waittime$, rc $rc$, nc $nc$, decodeDelta $delta$", ""),
	("$_id$ Generate target decode delta.*targetjitter $targetjitter$", ""),
	("$_id$ update max play jitter frameId %d jitter %d $maxrc$", ""),

	("send audio upload report.*uid $_id$.*pub $apub$=%d+%d send $asend$.*rtoresend $resend$ resendrate $resendrate$", ""),
	("uid:$_id$ uplink $uplink$ upvoice $upvoice$", ""),
	("audio download report.*speaker $_id$.*jitterrange[%d,$jitterrange$]", ""),

	("[yjtest] [audioJitter], uid.*nc $anc$, decodeDelta $adelta$.*ssrc $assrc$", ""),

	("process_packets: $process_packets$. ut_foss:$ut_foss$", ""),

	("$r1:1$0x1cb2830", ""),
	("$r2:2$0x1cb4b10", ""),
	("$r3:3$0x1cb1cb0", ""),

	("Ping$ping:idx$.*this=$_id$", ""),
	("this=$_id$.*empty$src_empty:idx$", ""),
	("this=$_id$.*got$src_not_empty:idx$", "")
)

exc_0_fields = (
	# "video_decode_delta",
)

stamp_type_fields = (
	"video_decode_delta",
	"audio_decode_delta",
	#"decode_time",
)

# keep_last_fields = (
#     "audio_status",
# )

wrap_type_fields = (
	"rc",
)

cases = {
	1: ("video_rtt",  "video_decode_delta", "video_total_delay", "video_over_jitter"),
	2: ("audio_status", "audio_recv", "audio_rtt",  "audio_decode_delta", "audio_total_delay", "audio_over_jitter"),
	3: ("ssrc","waittime","rc","nc","delta"),
	4: ("jitterrange","targetjitter"),
	5: ("anc", "adelta", "assrc"),
	6: ("process_packets", "ut_foss"),
	#7: ("r1", "r2", "r3"),
	7: ("ping", "src_empty", "src_not_empty"),
}

