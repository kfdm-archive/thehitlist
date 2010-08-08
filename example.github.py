#!/usr/bin/env python

import commands
import TheHitList
try:
	from github2.client import Github
except ImportError:
	exit('Fatal Error: Requires github module. http://github.com/ask/python-github2')

def add_issue(repo,story,list):
	'''
	Add a PT Story to a THL List
	@param story: PT Story
	@param list: THL List
	'''
	hash = '[%s#%s]'%( repo.name, issue.number)
	title = '%s %s /gh-%s'%( issue.title, hash, repo.name )
	
	for task in list.tasks():
		if hash in task.title:
		#if task.title.startswith('(%s)'%story.story_id):
			print 'found', title
			return
	print 'adding', title
	newtask = TheHitList.Task()
	newtask.title = title.encode('utf8')
	list.add_task(newtask)

gh_name = commands.getoutput('/usr/local/bin/git config --global --get github.user')
gh_token = commands.getoutput('/usr/local/bin/git config --global --get github.token')
thl_list = commands.getoutput('/usr/local/bin/git config --global --get thl.list')

github = Github(gh_name,gh_token)
thl = TheHitList.Application()
list =  thl.find_list(thl_list)

for repo in github.repos.list(gh_name):
	if repo.open_issues > 0:
		for issue in github.issues.list('%s/%s'%(repo.owner,repo.name),state='open'):
			add_issue(repo,issue,list)