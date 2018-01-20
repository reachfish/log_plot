#!/usr/bin/python
#coding:utf-8

patterns = (
	"[audioJitter] %d $_id$ normal in past %d ms in: range $[audio_in_range]$ .*, distrb $[audio_recv]$ out: range $[audio_out_range]$ total %d %d, distrb $[audio_pending]$",
	"read video sync state.($_id$ decodeDelta $video_decode_delta$ totalRtt:$video_rtt$ playDelay:$video_play_delay$ totalDelay:$video_total_delay$ overJitter:$video_over_jitter$",
)

exc_0_fields = (
	"video_decode_delta",
)

stamp_type_fields = (
	"video_decode_delta",
)
