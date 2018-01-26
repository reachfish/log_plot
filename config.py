#!/usr/bin/python
#coding:utf-8

#配置config.py时， 先阅读 readme.txt

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

	#主播音频
	("checkIamSpeaking canspeak:.*,voicepacketnum:$spk_voice_pkt_num$", "主播开麦10s音频包数"),

	#主播视频

	#线程
	# ("transport thread .* wakeup $transport_wakeup$ times", ""),
	# ("video decode thread .* wakeup $video_decode_wakeup$ times", ""),
	("thread .* wakeup $wakeup$ times", ""),
)

exc_0_fields = (
	# "video_decode_delta",
)

stamp_type_fields = (
	"video_decode_delta",
	"audio_decode_delta",
)

# keep_last_fields = (
#     "audio_status",
# )

cases = {
	1: ("video_rtt",  "video_decode_delta", "video_total_delay", "video_over_jitter"),
	2: ("audio_status", "audio_recv", "audio_rtt",  "audio_decode_delta", "audio_total_delay", "audio_over_jitter"),
}
