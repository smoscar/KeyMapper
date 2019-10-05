from KeyMapper import *
from KeyTrigger import *
import sys

if __name__ == "__main__":
	if len(sys.argv) > 1 and (sys.argv[1] == '-c' or sys.argv[1] == '--config'):
		km = KeyMapper()
	else:
		kt = KeyTrigger()
