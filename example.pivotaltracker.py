#!/usr/bin/env python
#import getpass

#defaults write com.pivotaltracker name <name>
#defaults write com.pivotaltracker pass <pass>
#defaults write com.pivotaltracker project <project_id>
#defaults write com.pivotaltracker query <query>
#defaults write com.pivotaltracker thl_list <The Hit List list name>

try:
	from pytracker import Tracker
	from pytracker import Story
	from pytracker import HostedTrackerAuth
except ImportError:
	exit('Fatal Error: Requires pytracker module. http://code.google.com/p/pytracker/')

try:
	import pydefaults
except ImportError:
	exit('Fatal Error: Requires pydefaults module. https://github.com/kfdm/pydefaults/')

settings = pydefaults.database('com.pivotaltracker')


import TheHitList
from extra.Terminal import TerminalController
term = TerminalController()
def found(string): print term.render('${BOLD}${RED}Found${NORMAL} %s'%string)
def adding(string): print term.render('${BOLD}${YELLOW}Adding${NORMAL} %s'%string)

def add_story(story,list):
	'''
	Add a PT Story to a THL List
	@param story: PT Story
	@param list: THL List
	'''
	for task in list.tasks():
		if task.notes == story.url:	
			found(task.title)
			return
	adding(story.name)
	newtask = TheHitList.Task()
	newtask.title = ('%s /Pivotal'%(story.name)).encode('utf8')
	newtask.notes = story.url.encode('utf8')
	list.add_task(newtask)

#Talk to Tracker
auth = HostedTrackerAuth(settings['login'], settings['pass'])
tracker = Tracker(int(settings['project_id']), auth)
stories = tracker.GetStories(settings['query'])

#Talk to THL
thl = TheHitList.Application()
list =  thl.find_list(settings['thl_list'].encode('utf-8'))
print '' #Line spacer
if list:
	for story in stories:
		add_story(story,list)
