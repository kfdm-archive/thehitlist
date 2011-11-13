#!/usr/bin/env python
# Example for importing PivotalTracker stories into THL

import commands
import TheHitList
from clint.textui import puts, colored
try:
	from pytracker import Tracker
	from pytracker import Story
	from pytracker import HostedTrackerAuth
except ImportError:
	exit('Fatal Error: Requires pytracker module. http://code.google.com/p/pytracker/')

# Read in configuration information from git's configuration files
# To set, from the shell you can use
# git config <key name> <value>
# git config thl.list tasks
PT_LOGIN = commands.getoutput('/usr/local/bin/git config --get pivotal.login')
PT_PASS = commands.getoutput('/usr/local/bin/git config --get pivotal.password')
PT_PROJECT_ID = commands.getoutput('/usr/local/bin/git config --get pivotal.projectid')
PT_QUERY = commands.getoutput('/usr/local/bin/git config --get pivotal.query')
THL_LIST = commands.getoutput('/usr/local/bin/git config --get thl.list')


def add_story(story, list):
	'''
	Add a PT Story to a THL List
	@param story: PT Story
	@param list: THL List
	'''
	for task in list.tasks():
		if task.notes == story.url:
			puts(colored.red(task.title))
			return
	puts(colored.yellow(story.name))
	newtask = TheHitList.Task()
	newtask.title = ('%s /Pivotal' % (story.name)).encode('utf8')
	newtask.notes = story.url.encode('utf8')
	list.add_task(newtask)

#Talk to Tracker
auth = HostedTrackerAuth(PT_LOGIN, PT_PASS)
tracker = Tracker(int(PT_PROJECT_ID), auth)
stories = tracker.GetStories(PT_QUERY)

#Talk to THL
thl = TheHitList.Application()
list = thl.find_list(THL_LIST)
print ''  # Line spacer
if list:
	for story in stories:
		add_story(story, list)
