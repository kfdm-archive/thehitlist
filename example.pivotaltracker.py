#!/usr/bin/env python
#import getpass

try:
	from pytracker import Tracker
	from pytracker import Story
	from pytracker import HostedTrackerAuth
except ImportError:
	exit('Fatal Error: Requires pytracker module. http://code.google.com/p/pytracker/')

import TheHitList

tracker_name = raw_input('Tracker Username: ')
#tracker_pass = getpass.getpass('Tracker Password: ')
tracker_pass = raw_input('Tracker Password: ')
tracker_proj = int(raw_input('Tracker Project: '))
tracker_query = raw_input('Tracker Query: ')
thl_target = raw_input('Target List: ')

def add_story(story,list):
	'''
	Add a PT Story to a THL List
	@param story: PT Story
	@param list: THL List
	'''
	for task in list.tasks():
		if task.notes == story.url:	
			print 'found', task.title
			return
	print 'adding', story.name
	newtask = TheHitList.Task()
	newtask.title = ('%s /Pivotal'%(story.name)).encode('utf8')
	newtask.notes = story.url.encode('utf8')
	list.add_task(newtask)

#Talk to Tracker
auth = HostedTrackerAuth(tracker_name, tracker_pass)
tracker = Tracker(tracker_proj, auth)
stories = tracker.GetStories(tracker_query)

#Talk to THL
thl = TheHitList.Application()
list =  thl.find_list(thl_target)

if list:
	for story in stories:
		add_story(story,list)
