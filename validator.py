# Checks for inconsistencies in docker-compose labels
# Dependencies: sudo apt-get install python3-kafka
# 				pip install ruamel.yaml

import urllib.request
import yaml
import time
import re
import os
import os.path
import hashlib
import json
import sys
import yamlreader
try:
	import kafka
except:
	print("Warning: no kafka support")




class Validator:

	def __autosearch_github__(self, project, path):
		print("https://api.github.com/search/code?q={}+in:path+org:{}&type=Code".format(path, project))
		f = urllib.request.urlopen("https://api.github.com/search/code?q={}+in:path+org:{}&type=Code".format(path, project))
		s = f.read().decode("utf-8")
		f.close()

		composefiles = []
		allresults = json.loads(s)
		results = allresults["items"]
		for result in results:
			if result["name"].endswith("docker-compose.yml") or (result["name"].endswith(".yml") and "docker-compose" in result["name"]):
				path = result["repository"]["html_url"] + "/blob/master/" + result["path"]
				composefiles.append(path)
		return composefiles

	def __normalise_githuburl__(self, url):
		m = re.match(r"^https://github.com/(.+)/blob/(.+)", url)
		if len(m.groups()) == 2:
			url = "https://raw.githubusercontent.com/{}/{}".format(m.groups()[0], m.groups()[1])
		return url

	def __loadcache__(self):
		cachefiles = {}
		if os.path.isdir("_cache"):
			st = os.stat("_cache/entries")
			cacheage = time.time() - st.st_mtime
			if cacheage < 0 or cacheage > 3600:
				print("discard cache...")
				return cachefiles
			print("loading cache...")
			f = open("_cache/entries")
			cachedfiles = f.readlines()
			f.close()
			for cachedfile in cachedfiles:
				cachedfile = cachedfile[:-1]
				unique = hashlib.md5(cachedfile.encode("utf-8")).hexdigest()
				cachefiles[cachedfile] = "_cache/{}.cache".format(unique)
		return cachefiles

	def __loading__(self, cachefiles, composefiles, localSearch=False):
		print("loading compose files...", end="", flush=True)
		contents = {}
		for composefile in composefiles:
			
			composefile_load = self.__normalise_githuburl__(composefile)
			if composefile in cachefiles:
				composefile_load = cachefiles[composefile]
			if composefile_load in cachefiles:
				composefile_load = cachefiles[composefile_load]
			if "http" in composefile_load:
				f = urllib.request.urlopen(composefile_load)
				s = f.read().decode("utf-8")
			else:
				f = open(composefile_load)
				s = f.read()
			contents[composefile] = s
			if not composefile in cachefiles:
				os.makedirs("_cache", exist_ok=True)
				f = open("_cache/entries", "a")
				print(composefile, file=f)
				f.close()
				unique = hashlib.md5(composefile.encode("utf-8")).hexdigest()
				f = open("_cache/{}.cache".format(unique), "w")
				f.write(s)
				f.close()
			print(".", end="", flush=True)
		print()
		return contents

	def __duplicate_tag_founder__(self, itterable):
		# tag_set = set()
		# for i in itterable:
		# 	if type(i) == type(tuple()):
		# 		if i[0] in tag_set:
		# 			err_message = '* Duplicate label {} in Docker-compose file.'.format(i[0])
		# 			print("="*(len(err_message)//2 - 3) + " ERROR " + "="*(len(err_message)//2 - 3))
		# 			print(err_message)
		# 			print("="*len(err_message))
		# 		else:
		# 			tag_set.add(i[0])
		# 		if type(i[1]) == type(list()):
		# 			self.__duplicate_tag_founder__(i[1])
		visited = []
		for key in itterable:
		    if type(key)==type(tuple()) or type(key)==type(list()):
		        if key[0] in visited:
		            print("="*(27) + " ERROR " + "="*(27))
		            print('This {} key is duplicate '.format(key[0]))
		            print("="*(61) + '\n')
		            break
		        else:
		            visited.append(key[0])

	def __itterator__(self, itterable):
		if type(itterable) == type(dict()):
		    for key in itterable:
		        if type(itterable[key])==type(list()):
#  		              __duplicate_tag_founder__(itterable[key])
		            self.__duplicate_tag_founder__(itterable[key])
#  		              itterator(itterable[key])
		        else:
		            self.__itterator__(itterable[key])
		elif (type(itterable)==type(tuple()) or type(itterable)==type(list())):
#  		      __duplicate_tag_founder__(itterable)
		    self.__duplicate_tag_founder__(itterable)
		    for item in itterable:
		        self.__itterator__(item)

	def __consistencycheck__(self, contents):
		print("checking consistency...")

		numservices = 0
		alltags = {}
		faulty = {}

		for content in contents:
			parsed = yamlreader.reader(contents[content])
			
			self.__itterator__(parsed)
				
				
				
				
			contentname = "faulty:" + content.split("/")[4]
			faulty[contentname] = 0.0

			c = yaml.load(contents[content])

			if "services" in c:
				cacheports = []
				cachecontainername = []
				print("= type: docker-compose")
				for service in c["services"]:
					print("- service:", service)
					numservices += 1
					if not "container_name" in c["services"][service]:
						print("**Warning**  no container name found")
					elif c["services"][service]["container_name"] in cachecontainername:
						print("Duplicate container name: ", c["services"][service]["container_name"])
						# raise Exception ('Duplicate container name')
					else:
						cachecontainername.append(c["services"][service]["container_name"])
					if "volumes" in c["services"][service]:
						for volume in c["services"][service]["volumes"]:
							temp_dir = volume.split(':')
							onhostdir = temp_dir[0]
							if not os.path.exists(onhostdir):
								print ("Check path ", onhostdir, " for volume on service", service)
								# raise Exception ('Path Error')
					if "ports" in c["services"][service]:
						for port in c["services"][service]["ports"]:
							port_temp = port.split(':')
							port_host = port_temp[0]
							if port_host in cacheports:
								print("Duplicate ports in service ",service, " port ", port_host)
								# raise Exception ('Duplicate ports')
							else:
								cacheports.append(port_host)
					if not "labels" in c["services"][service]:
						print("  ! no labels found")
						faulty[contentname] = faulty.get(contentname, 0) + 1
						continue 
					for labelpair in c["services"][service]["labels"]:
						print("  - label:", labelpair)
						label, value = labelpair.split("=")
						alltags[label] = alltags.get(label, 0) + 1
					

			elif "apiVersion" in c and "items" in c:
				print("= type: kubernetes")
				for service in c["items"]:
					name = service["metadata"]["name"]
					print("- service:", service["kind"], name)
					numservices += 1
					if not "labels" in service["metadata"]:
						print("  ! no labels found")
						faulty[contentname] = faulty.get(contentname, 0) + 1
						continue
					for label in service["metadata"]["labels"]:
						value = service["metadata"]["labels"][label]
						print("  - label:", label, "=", value)
						alltags[label] = alltags.get(label, 0) + 1
			else:
				print("! no docker-compose or kubernetes service entries found")
				faulty[contentname] = faulty.get(contentname, 0) + 1
				continue

		return numservices, alltags, faulty

	def __sendmessage__(self, host, label, series, message):
		if kafka.__version__.startswith("0"):
			c = kafka.client.KafkaClient(hosts=[host])
			if series:
				p = kafka.producer.keyed.KeyedProducer(c)
			else:
				p = kafka.producer.simple.SimpleProducer(c)
		else:
			p = kafka.KafkaProducer(bootstrap_servers=host)
		success = False
		t = 0.2
		while not success:
			try:
				if kafka.__version__.startswith("0"):
					if series:
						p.send_messages(label, series.encode("utf-8"), message.encode("utf-8"))
					else:
						p.send_messages(label, message.encode("utf-8"))
				else:
					p.send(label, key=series.encode("utf-8"), value=message.encode("utf-8"))
					p.close()
				print("success")
				success = True
			except Exception as e:
				print("error (sleep {})".format(t), e)
				time.sleep(t)
				t *= 2

	def validator(self, autosearch, filebased, urlbased, eventing, filebasedlist=None):
		composefiles = []

		d_start = time.time()
		cachefiles = self.__loadcache__()

		if filebased:
			f = open(filebased)
			composefiles += [line.strip() for line in f.readlines()]

		if urlbased:
			composefiles += [urlbased]

		if autosearch:
			if not cachefiles:
				org, basepath = autosearch.split("/")
				composefiles += self.__autosearch_github__(org, basepath)
			else:
				composefiles += cachefiles
		
		contents = self.__loading__(cachefiles, composefiles)
		
		numservices, alltags, faulty = self.__consistencycheck__(contents)
		d_end = time.time()

		print("services: {}".format(numservices))
		print("labels:")
		for label in alltags:
			print("- {}: {} ({:.1f}% coverage)".format(label, alltags[label], 100 * alltags[label] / numservices))
		print("time: {:.1f}s".format(d_end - d_start))

		d = {}
		d["agent"] = "sentinel-generic-agent"
		d["services"] = float(numservices)
		for label in alltags:
			d[label] = float(alltags[label])
		d.update(faulty)
		if eventing:
			kafka, space, series = eventing.split("/")
			print("sending message... {}".format(d))
			self.__sendmessage__(kafka, space, series, json.dumps(d))
		else:
			print("not sending message... {}".format(d))
