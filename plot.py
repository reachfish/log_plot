import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import pattern

def show_plot(fields, log_files, save_name, begin_time="", end_time=""):
	manager = pattern.PatternManager()
	results = manager.match(fields, log_files, begin_time, end_time)
	datas = [ (field, data) for (field, data) in results if data ]
	if not datas:
		print "No Find"
		return

	inches = (18.5, 10.5)
	plot_num = len(datas)
	fig, axes = plt.subplots(plot_num, sharex=True)
	fig.autofmt_xdate()
	fig.set_size_inches(*inches)
	#plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))

	for ax, (field, data) in zip(axes, datas)
		ax.set_title(field)
		ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
		for _id, (x, y) in data.iteritems():
			ax.plot(x, y  label=str(_id))

	plt.savefig(save_name + ".png")
	plt.show()


