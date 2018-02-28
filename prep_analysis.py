from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
try:
	import _pickle as pickle
except:
	import pickle
import csv
from random import shuffle
import sys
import time
import numpy as np
import multiprocessing as mp
import threading
import math
import datetime



csv_file = 'scraping_metadata.csv'
pickle_file = 'scraping_metadata.pickle'

data = (pickle.load(open(pickle_file, 'rb')))['data']


data_set = []

counter = 1
session_dict = {}
session_list = sorted(list(data.keys()))


for session in session_list:

	#to figure out how many threads -- accidentally forogt to include
	num_threads = max(list(data[session].keys()))


	#to figure out when the first scrape in the session started
	date_time_array = []
	scrape_time_dict = {}
	for threadID in data[session]:
		data_points = data[session][threadID]
		for elem in data_points:
			date_time_array.append(elem['date_time'])
			scrape_time_dict.update( { elem['date_time']:elem['scrape_time'] } )
	if len(date_time_array) == 0:
		continue
	start = min(date_time_array)
	end = max(date_time_array) + datetime.timedelta(seconds=scrape_time_dict[max(date_time_array)]) #end inclusive

	#session dictionary
	session_dict.update( { counter:(start, end, num_threads) } )

	#to get the data
	for threadID in data[session]:
		data_points = data[session][threadID]
		for elem in data_points:
			data_row = [counter, num_threads, (elem['date_time']-start+datetime.timedelta(seconds=elem['scrape_time'])).total_seconds(), elem['scrape_time']]
			data_set.append(data_row)

	counter += 1

session_array = []
for row in data_set:

	session_num = row[0]
	session_array.append(session_num)

	if session_num == 1:
		continue

	if row[1] != session_dict[session_num-1][2]:
		continue

	# to correctly add on the relative time
	row[2] = row[2] + (session_dict[session_num-1][1]-session_dict[session_num-1][0]).total_seconds()

with open(csv_file, 'w', encoding = 'utf-8') as f:
	writer = csv.writer(f)
	header = [["index", "numthread", "rtime", "stime"]]
	writer.writerows(header + data_set)







