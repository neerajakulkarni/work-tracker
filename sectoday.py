def Convert(t):
	hour = t // 3600
	t %= 3600
	minutes = t // 60
	t %= 60
	seconds = t
	if hour == 0 and minutes == 0:
		return(seconds, "seconds")
	elif hour == 0:
		return(minutes, "minutes", seconds, "seconds")
	else:
		return(hour, "hours", minutes, "minutes", seconds, "seconds")
