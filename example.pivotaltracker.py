#!/usr/bin/env python
import sys

try:
	from pytracker import Tracker
	from pytracker import Story
	from pytracker import HostedTrackerAuth
except ImportError:
	exit('Fatal Error: Requires pytracker module. http://code.google.com/p/pytracker/')

import TheHitList

try:
	tracker_name = sys.argv[1]
	tracker_pass = sys.argv[2]
	tracker_proj = int(sys.argv[3])
	tracker_query = sys.argv[4]
	thl_target = sys.argv[5]
except IndexError:
	exit('Usage: '+sys.argv[0]+' <tracker_name> <tracker_pass> <tracker_proj_id> <tracker_query> <thl_target>')

def add_story(story,list):
	'''
	Add a PT Story to a THL List
	@param story: PT Story
	@param list: THL List
	'''
	for task in list.tasks():
		if task.title.startswith('(%s)'%story.story_id):
			print 'found', task.title
			return
	print 'adding', story.name
	newtask = TheHitList.Task()
	newtask.title = ('(%s) %s'%(story.story_id,story.name)).encode('utf8')
	newtask.notes = story.description.encode('utf8')
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
