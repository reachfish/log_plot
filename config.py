#!/usr/bin/python
#coding:utf-8

patterns = (
	"[audioJitter] %d $_id$ normal in past %d ms in: range $audio_in_range$ .*, distrb $audio_recv$ out: range $audio_out_range$ total %d %d, distrb $audio_pending$",
	"read video sync state.($_id$ decodeDelta $video_decode_delta$ totalRtt:$video_rtt$ playDelay:$video_play_delay$ totalDelay:$video_total_delay$ overJitter:$video_over_jitter$",
	"read audio sync state.($_id$ decodeDelta $audio_decode_delta$ totalRtt:$audio_rtt$ playDelay:$audio_play_delay$ totalDelay:$audio_total_delay$ overJitter:$audio_over_jitter$",
	"$audio_status:1$ create audio receiver $_id$",
	"$audio_status:0$ $_id$ delete outdate audio receiver",
)

exc_0_fields = (
	"video_decode_delta",
)

stamp_type_fields = (
	"video_decode_delta",
)

keep_last_fields = (
	"audio_status",
)

cases = {
	1: ("video_rtt",  "video_decode_delta", "video_total_delay", "video_over_jitter"),
}
