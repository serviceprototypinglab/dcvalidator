# Checks for inconsistencies in docker-compose labels
# Dependencies: sudo apt-get install python3-kafka

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
import Levenshtein
import typoMistake
from collections import Counter
try:
	import kafka
except:
	print("Warning: no kafka support")

RATIO = 0.6

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
		if m:
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

	def __duplicate_tag_founder__(self, itterable, counter):
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
			counter += 1
			if type(key)==type(tuple()) or type(key)==type(list()):
				if key[0] in visited:
				    self.__log_writer__("="*(27) + " ERROR " + "="*(27))
				    self.__log_writer__('Line {}, this {} key is duplicate'.format(counter, key[0]))
				    self.__log_writer__("="*(61) + '\n')
				    break
				else:
				    visited.append(key[0])
		return counter

	def __itterator__(self, itterable, counter=0):
		if type(itterable) == type(dict()):
			for key in itterable:
				counter += 1
				if type(itterable[key])==type(list()):
#  		   	   	   	  __duplicate_tag_founder__(itterable[key])
					counter = self.__duplicate_tag_founder__(itterable[key], counter)
#  		   	   	   	  itterator(itterable[key])
				else:
					self.__itterator__(itterable[key], counter=counter)
		elif (type(itterable)==type(tuple()) or type(itterable)==type(list())):
#  		   	  __duplicate_tag_founder__(itterable)
			counter = self.__duplicate_tag_founder__(itterable, counter)
			for item in itterable:
				counter += 1
				self.__itterator__(item, counter=counter)
				
	def __top_level_property_checker__(self, itterable):
		priority = {
			'version': 4,
			'services': 3,
			'networks': 2,
			'volumes': 2
		}

		if type(itterable) == type(dict()):
			temp_itterable = list(itterable)
			for index in range(1,len(temp_itterable)-1):
				if priority[temp_itterable[index]] < priority[temp_itterable[index + 1]]:
					self.__log_writer__('Top level property warning:'+ str(temp_itterable[index])+ 'better not be before'+ str(temp_itterable[index + 1]))
				if priority[temp_itterable[index - 1]] < priority[temp_itterable[index]]:
					self.__log_writer__('Top level property warning:'+ str(temp_itterable[index])+ 'better not be after'+ str(temp_itterable[index - 1]))
		if type(itterable) == type(list()):
			for index in range(1,len(itterable)-1):
				if priority[itterable[index][0]] < priority[itterable[index + 1][0]]:
					self.__log_writer__('Top level property warning:'+ str(itterable[index][0])+ 'better not be before'+ str(itterable[index + 1][0]))
				if priority[itterable[index - 1][0]] < priority[itterable[index][0]]:
					self.__log_writer__('Top level property warning:'+ str(itterable[index][0])+ 'better not be after'+ str(itterable[index - 1][0]))
	
	def __log_writer__(self, text):
		print(text)
		f = open("logs.txt", "a+")
		f.writelines(text + '\n')
		f.close()

	def __typomistake__(self, parsed, targetTag):
		tag_list_similarity = {}
		# err_message = ""
		for generalTag in parsed:
			tmp = []
			for tag in typoMistake.tags[targetTag]:
				ratio = Levenshtein.ratio(generalTag, tag)
				if ratio == 1:
					break
				elif 1 > ratio >= RATIO:
				    if [ratio,tag] not in tmp:
				        tmp.append([ratio,tag])
			if len(tmp) > 0:
			    tmp.sort(key=lambda tmp: tmp[0], reverse=True)
			    tag_list_similarity[generalTag] = tmp
		for eachTag in tag_list_similarity:
			pair = 0
			while pair < len(tag_list_similarity[eachTag]):
				if tag_list_similarity[eachTag][pair][0] < 0.8:
					tag_list_similarity[eachTag].remove(tag_list_similarity[eachTag][pair])
				pair += 1
		return tag_list_similarity
		# if len(tag_list_similarity) > 0:
		#     for tag in tag_list_similarity:
		#         err_message += "I can not find "+str(tag)+", but there is my suggestion: \n"
		#         for item in tag_list_similarity[tag]:
		#             for match in item:
		#                 err_message += str(match[1])
		# if len(err_message) > 0:
		#     self.__log_writer__(err_message)

	def __consistencycheck__(self, contents, labelArray):
		print("checking consistency...")

		numservices = 0
		alltags = {}
		faulty = {}
		errors = Counter()
		warnings = Counter()

		for content in contents:
			parsed = yamlreader.reader(contents[content])
			# if 'Top level property' in labelArray:
			# 	self.__top_level_property_checker__(parsed)
			self.__itterator__(parsed)
				
				
			if "https://github.com/" in content:
				contentname = "faulty:" + content.split("/")[4]
			else:
				contentname = "faulty:None"
			faulty[contentname] = 0.0


			c = yaml.load(contents[content], Loader=yaml.FullLoader)

			if 'Typing mistakes' in labelArray:
				err_message = ""
				tag_list_similarity = self.__typomistake__(c, 'general')
				if len(tag_list_similarity) > 0:
					for tag in tag_list_similarity:
						if len(tag_list_similarity[tag]) > 0:
							err_message += "I can not find '"+str(tag)+"' tag. Maybe you can use: \n"
							for item in tag_list_similarity[tag]:
							    err_message += str(item[1]) + '\n'
				if len(err_message) > 0:
					self.__log_writer__("=================== ERROR ===================")
					self.__log_writer__(err_message)
					self.__log_writer__("=============================================")

			
			if "volumes" in c:
				cachevolumes = []
				for volume in c["volumes"]:
					cachevolumes.append(volume)
			if 'configs' in c:
				cacheconfigs = []
				for configname in c['configs']:
					cacheconfigs.append(configname)
					if 'file' in c['configs'][configname]:
						if not os.path.exists(c['configs'][configname]['file']):
							self.__log_writer__("=================== ERROR ===================")
							self.__log_writer__("Under config {}".format(c['configs'][configname]))
							self.__log_writer__("Check the file {}".format(c['configs'][configname]['file']))
							self.__log_writer__("=============================================")

			if "services" in c:
				cacheService = []
				cacheports = []
				cachecontainername = []
				self.__log_writer__("= type: docker-compose")
				for service in c["services"]:
					cacheService.append(service)

				for service in c["services"]:
					cachedns = []
					cacheexpose = []
					self.__log_writer__("- service:"+ service)
					numservices += 1
					if 'Container name' in labelArray:
						if not "container_name" in c["services"][service]:
							self.__log_writer__("**Warning**  no container name found")
							warnings['container_name_missing'] += 1
						elif c["services"][service]["container_name"] in cachecontainername:
							self.__log_writer__("Duplicate container name: "+ c["services"][service]["container_name"])
							# raise Exception ('Duplicate container name')
							warnings['container_name_duplicate'] += 1
						else:
							cachecontainername.append(c["services"][service]["container_name"])
					if "volumes" in c["services"][service]:
						if type(c["services"][service]["volumes"]) == type(list()):
							for volume in c["services"][service]["volumes"]:
								if type(volume) == type(""):
									if ':' in volume:
										temp_dir = volume.split(':')
										onhostvolume = temp_dir[0]
										if not os.path.exists(onhostvolume):
											if onhostvolume not in cachevolumes:
												self.__log_writer__("=================== ERROR ===================")
												self.__log_writer__("Under service: {}".format(service))
												self.__log_writer__("Check volume "+ str(volume))
												self.__log_writer__("=============================================")
								elif type(volume) == type(dict()):
									if 'Typing mistakes' in labelArray:
										err_message = ""
										tag_list_similarity = self.__typomistake__(volume, 'volumes')
										if len(tag_list_similarity) > 0:
											for tag in tag_list_similarity:
												if len(tag_list_similarity[tag]) > 0:
													err_message += "I can not find '"+str(tag)+"' tag under '"+service+"' service. Maybe you can use: \n"
													for item in tag_list_similarity[tag]:
													    err_message += str(item[1]) + '\n'
										if len(err_message) > 0:
											self.__log_writer__("=================== ERROR ===================")
											self.__log_writer__(err_message)
											self.__log_writer__("=============================================")
									if 'type' in volume:
										if volume['type'] not in 'volume bind tmpfs npipe':
											self.__log_writer__("=================== ERROR ===================")
											self.__log_writer__("Under service: {}".format(service))
											self.__log_writer__("Wrong type {} for volume \nVolume types are: volume, bind, tmpfs, npipe".format(volume['type']))
											self.__log_writer__("=============================================")
											errors['volume_type'] =+ 1
											faulty[contentname] = faulty.get(contentname, 0) + 1
									if 'source' in volume:
										if not os.path.exists(volume['source']):
											if volume['source'] not in cachevolumes:
												self.__log_writer__("=================== ERROR ===================")
												self.__log_writer__("Under service: {}".format(service))
												self.__log_writer__("Wrong type {} for volume \nVolume types are: volume, bind, tmpfs, npipe".format(volume['type']))
												self.__log_writer__("=============================================")
									

					if "ports" in c["services"][service] and 'Duplicate ports' in labelArray:
						for port in c["services"][service]["ports"]:
							if type(port) == type(""):
								try:
									port_temp = port.split(':')
								except:
									self.__log_writer__("Tip: It's better to use the HOST:CONTAINER structure")
								else:
									port_host = port_temp[0]
									if port_host in cacheports:
										self.__log_writer__("Duplicate ports in service "+service+ " port "+ str(port_host))
										# raise Exception ('Duplicate ports')
										warnings['duplicate_ports'] += 1
									else:
										cacheports.append(port_host)
							if type(port) == type(int()):
								cacheports.append(port)
					if 'Labels' in labelArray:
						if not "labels" in c["services"][service]:
							self.__log_writer__("  ! no labels found")
							faulty[contentname] = faulty.get(contentname, 0) + 1
							continue 
						else:
							for labelpair in c["services"][service]["labels"]:
								self.__log_writer__("  - label:"+ str(labelpair))
								label, value = labelpair.split("=")
								alltags[label] = alltags.get(label, 0) + 1

					if 'DNS' in labelArray:
						if "dns" in c["services"][service]:
							dns = c["services"][service]["dns"]
							if type(dns) == type(list()):
								for ip in dns:
									try:
										splitedIp = ip.split('.')
										for section in splitedIp:
											if len(section) > 3 or len(section) < 1:
												self.__log_writer__("=================== ERROR ===================")
												self.__log_writer__("Under service: {}".format(service))
												self.__log_writer__("The DNS is not appropriate!")
												self.__log_writer__("=============================================")
												errors['dns_malformed'] += 1
												faulty[contentname] = faulty.get(contentname, 0) + 1
										if ip not in cachedns:
											cachedns.append(ip)
										else:
											self.__log_writer__("=================== ERROR ===================")
											self.__log_writer__("Under service: {}".format(service))
											self.__log_writer__("Duplicate DNS!")
											self.__log_writer__("=============================================")
											errors['dns_duplicate'] += 1
											faulty[contentname] = faulty.get(contentname, 0) + 1
									except:
										self.__log_writer__("=================== ERROR ===================")
										self.__log_writer__("Under service: {}".format(service))
										self.__log_writer__("The DNS is not appropriate!")
										self.__log_writer__("=============================================")
										errors['dns_malformed'] += 1
										faulty[contentname] = faulty.get(contentname, 0) + 1
										continue
									
							elif  type(dns) == type(str()):
								try:
									splitedIp = dns.split('.')
									if len(splitedIp) > 3 or len(splitedIp) < 1:
										self.__log_writer__("=================== ERROR ===================")
										self.__log_writer__("Under service: {}".format(service))
										self.__log_writer__("The DNS is not appropriate!")
										self.__log_writer__("=============================================")
										errors['dns_malformed'] += 1
										faulty[contentname] = faulty.get(contentname, 0) + 1
								except:
									self.__log_writer__("=================== ERROR ===================")
									self.__log_writer__("Under service: {}".format(service))
									self.__log_writer__("The DNS is not appropriate!")
									self.__log_writer__("=============================================")
									errors['dns_malformed'] += 1
									faulty[contentname] = faulty.get(contentname, 0) + 1
							
							else:
								self.__log_writer__("=================== ERROR ===================")
								self.__log_writer__("Under service: {}".format(service))
								self.__log_writer__("The DNS can be a single value or a list!")
								self.__log_writer__("=============================================")

					if 'Typing mistakes' in labelArray:
						err_message = ""
						tag_list_similarity = self.__typomistake__(c["services"][service], 'service')
						if len(tag_list_similarity) > 0:
							for tag in tag_list_similarity:
								if len(tag_list_similarity[tag]) > 0:
									err_message += "I can not find '"+str(tag)+"' tag under '"+service+"' service. Maybe you can use: \n"
									for item in tag_list_similarity[tag]:
									    err_message += str(item[1]) + '\n'
						if len(err_message) > 0:
							self.__log_writer__("=================== ERROR ===================")
							self.__log_writer__(err_message)
							self.__log_writer__("=============================================")
					
					if 'Duplicate expose' in labelArray:
						if 'expose' in c["services"][service]:
							expose = c["services"][service]['expose']
							if type(expose) == type(list()):
								for port in expose:
									port = int(port)
									if 1 < port < 65536:
										if port not in cacheexpose:
											cacheexpose.append(port)
										else:
											self.__log_writer__("=================== ERROR ===================")
											self.__log_writer__("Under service: {}".format(service))
											self.__log_writer__("Duplicate port {} exposed!".format(port))
											self.__log_writer__("=============================================")
											errors['expose_port_duplicate'] += 1
											faulty[contentname] = faulty.get(contentname, 0) + 1
									else:
										self.__log_writer__("=================== ERROR ===================")
										self.__log_writer__("Under service: {}".format(service))
										self.__log_writer__("The port {} that exposed is not appropriate!".format(port))
										self.__log_writer__("=============================================")
										errors['expose_port_malformed'] += 1
										faulty[contentname] = faulty.get(contentname, 0) + 1
							else:
								self.__log_writer__("=================== ERROR ===================")
								self.__log_writer__("Under service: {}".format(service))
								self.__log_writer__("Value of expose can be a list!")
								self.__log_writer__("=============================================")
								errors['expose_syntax'] += 1
								faulty[contentname] = faulty.get(contentname, 0) + 1

					if 'depends_on' in c["services"][service]:
						for denpendecy in c["services"][service]['depends_on']:
							if denpendecy not in cacheService:
								self.__log_writer__("=================== ERROR ===================")
								self.__log_writer__("Under service: {}".format(service))
								self.__log_writer__("Wrong dependency! There is no such service with name of {}".format(denpendecy))
								self.__log_writer__("=============================================")
								errors['dependency_missing'] += 1
								faulty[contentname] = faulty.get(contentname, 0) + 1
					if 'build' in c["services"][service]:
						build = c["services"][service]['build']
						if type(build) == type(""):
							if not os.path.exists(build):
								self.__log_writer__("=================== ERROR ===================")
								self.__log_writer__("Under service: {}".format(service))
								self.__log_writer__("Check build directory "+ str(build))
								self.__log_writer__("=============================================")
						elif type(build) == type(dict()):
							build_path = ""
							if 'Typing mistakes' in labelArray:
								err_message = ""
								tag_list_similarity = self.__typomistake__(build, 'build')
								if len(tag_list_similarity) > 0:
									for tag in tag_list_similarity:
										if len(tag_list_similarity[tag]) > 0:
											err_message += "I can not find '"+str(tag)+"' tag under '"+service+"' service. Maybe you can use: \n"
											for item in tag_list_similarity[tag]:
											    err_message += str(item[1]) + '\n'
								if len(err_message) > 0:
									self.__log_writer__("=================== ERROR ===================")
									self.__log_writer__(err_message)
									self.__log_writer__("=============================================")
							if 'context' in build:
								if os.path.exists(build['context']):
									build_path = os.path.join(build_path,build['context'])
								else:
									self.__log_writer__("=================== ERROR ===================")
									self.__log_writer__("Under service: {}".format(service))
									self.__log_writer__("Check build context directory "+ str(build['context']))
									self.__log_writer__("=============================================")
							if 'dockerfile' in build:
								dockerfilepath = os.path.join(build_path,build['dockerfile'])
								if not os.path.exists(dockerfilepath):
									self.__log_writer__("=================== ERROR ===================")
									self.__log_writer__("Under service: {}".format(service))
									self.__log_writer__("Check build dockerfile "+ str(dockerfilepath))
									self.__log_writer__("=============================================")
					if 'configs' in c["services"][service]:
						configs = c["services"][service]['configs']
						if type(configs) == type(list()):
							if type(configs[0]) == type(""):
								for config in configs:
									if config not in cacheconfigs:
										self.__log_writer__("=================== ERROR ===================")
										self.__log_writer__("Under service: {}".format(service))
										self.__log_writer__("I can not find config "+ str(config))
										self.__log_writer__("=============================================")
							elif type(configs[0]) == type(dict()):
								for config in configs:
									if 'Typing mistakes' in labelArray:
										err_message = ""
										tag_list_similarity = self.__typomistake__(configs, 'configs')
										if len(tag_list_similarity) > 0:
											for tag in tag_list_similarity:
												if len(tag_list_similarity[tag]) > 0:
													err_message += "I can not find '"+str(tag)+"' tag under '"+service+"' service. Maybe you can use: \n"
													for item in tag_list_similarity[tag]:
													    err_message += str(item[1]) + '\n'
										if len(err_message) > 0:
											self.__log_writer__("=================== ERROR ===================")
											self.__log_writer__(err_message)
											self.__log_writer__("=============================================")
									if 'source' in config:
										if config['source'] not in cacheconfigs:
											self.__log_writer__("=================== ERROR ===================")
											self.__log_writer__("Under service: {}".format(service))
											self.__log_writer__("I can not find 'source' {} in config ".format(str(config)))
											self.__log_writer__("=============================================")
			elif "apiVersion" in c and "items" in c:
				self.__log_writer__("= type: kubernetes")
				for service in c["items"]:
					name = service["metadata"]["name"]
					self.__log_writer__("- service:"+ str(service["kind"])+ str(name))
					numservices += 1
					if not "labels" in service["metadata"]:
						self.__log_writer__("  ! no labels found")
						faulty[contentname] = faulty.get(contentname, 0) + 1
						continue
					for label in service["metadata"]["labels"]:
						value = service["metadata"]["labels"][label]
						self.__log_writer__("  - label:"+ str(label)+ "="+ str(value))
						alltags[label] = alltags.get(label, 0) + 1
			else:
				self.__log_writer__("! no docker-compose or kubernetes service entries found")
				faulty[contentname] = faulty.get(contentname, 0) + 1
				continue

		return numservices, alltags, faulty, errors, warnings

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
				self.__log_writer__("success")
				success = True
			except Exception as e:
				self.__log_writer__("error (sleep {})".format(t)+ str(e))
				time.sleep(t)
				t *= 2

	def validator(self, autosearch, filebasedlist, urlbased, eventing, filebased=None, labelArray=[], jsonpath= None):
		composefiles = []

		d_start = time.time()
		# TODO enable cache again
		# cachefiles = self.__loadcache__()
		cachefiles = []

		if filebasedlist:
			f = open(filebasedlist)
			composefiles += [line.strip() for line in f.readlines()]

		if urlbased:
			composefiles += [urlbased]
		if filebased:
			composefiles += [filebased]
		if autosearch:
			if not cachefiles:
				org, basepath = autosearch.split("/")
				composefiles += self.__autosearch_github__(org, basepath)
			else:
				composefiles += cachefiles
		
		contents = self.__loading__(cachefiles, composefiles)
		
		numservices, alltags, faulty, error_types, warnings = self.__consistencycheck__(contents, labelArray)
		d_end = time.time()

		self.__log_writer__("services: {}".format(numservices))
		self.__log_writer__("labels:")
		for label in alltags:
			self.__log_writer__("- {}: {} ({:.1f}% coverage)".format(label, alltags[label], 100 * alltags[label] / numservices))
		self.__log_writer__("time: {:.1f}s".format(d_end - d_start))

		d = {}
		d["agent"] = "sentinel-generic-agent"
		d["services"] = float(numservices)
		d["errors"] = error_types
		d["warnings"] = warnings
		for label in alltags:
			d[label] = float(alltags[label])
		d.update(faulty)
		if eventing:
			kafka, space, series = eventing.split("/")
			print("sending message... {}".format(d))
			self.__sendmessage__(kafka, space, series, json.dumps(d))
		elif jsonpath != None:
			with open(jsonpath, 'w') as outfile:
				json.dump(d, outfile)
		else:
			print("not sending message... {}".format(json.dumps(d)))
