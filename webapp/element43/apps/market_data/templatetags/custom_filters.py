from django import template

register = template.Library()

def sec0to1(val):
	"""
	Converts the system security values into values between 0 and 1
	"""
	retval = 0.0
	
	if val < 0:
		retval = 0.0
	elif val > 1:
		retval = 1.0
	else:
		retval = round(val, 1)
	
	return retval

register.filter('sec0to1', sec0to1)

def sec0to10(val):
	"""
	Converts the system security values into values between 0 and 10
	"""
	retval = val * 10
	
	if retval < 0:
		retval = 0
	elif retval > 10:
		retval = 10
	else:
		retval = int(round(retval))
	
	return retval

register.filter('sec0to10', sec0to10)