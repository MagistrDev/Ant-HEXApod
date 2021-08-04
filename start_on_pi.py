from platform import platform


def IsRunningOnPi():
	return "arm" in platform()