#!/usr/bin/python

import sys
from validator import Validator
if __name__ == "__main__":
	if len(sys.argv) == 1:
		print("Syntax: {} [-a <org>/<basepath>] [-f <file>] [-u <url>] [-e <kafka>/<space>/<series>]".format(sys.argv[0]), file=sys.stderr)
		print(" -a: autosearch; find appropriate compose files on GitHub")
		print(" -f: filebased; load docker-compose from a docker-compose file")
		print(" -fl: filebased list; load paths or URLs as lines from a text file")
		print(" -u: urlbased; direct URL or path specification")
		print(" -e: eventing; send results to Kafka endpoint with space and series selection")
		print("Example: {} -a elastest/deploy -e kafka.cloudlab.zhaw.ch/user-1-docker_label_consistency/nightly".format(sys.argv[0]))
		sys.exit(1)

	autosearch = None
	filebasedlist = None
	filebased = None
	urlbased = None
	eventing = None

	i = 1
	while i < len(sys.argv):
		if sys.argv[i] == "-a":
			autosearch = sys.argv[i + 1]
		elif sys.argv[i] == "-fl":
			filebasedlist = sys.argv[i + 1]	
		elif sys.argv[i] == "-f":
			filebased = sys.argv[i + 1]	
		elif sys.argv[i] == "-u":
			urlbased = sys.argv[i + 1]
		elif sys.argv[i] == "-e":
			eventing = sys.argv[i + 1]
			if not "kafka" in dir():
				print("warning: eventing disabled")
				eventing = None
		
		i += 1

	my_validator = Validator()
	my_validator.validator(autosearch, filebasedlist, urlbased, eventing, filebased)