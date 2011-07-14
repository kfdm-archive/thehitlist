#!/usr/bin/env python
# Example script for pulling in tasks from GitHub into TheHitList
import commands
import TheHitList
try:
	from github2.client import Github
except ImportError:
	exit('Fatal Error: Requires github module. http://github.com/ask/python-github2')

# Read in configuration information from git's configuration files
# To set, from the shell you can use
# git config <key name> <value>
# git config thl.list tasks
gh_name = commands.getoutput('/usr/local/bin/git config --get github.user')
gh_token = commands.getoutput('/usr/local/bin/git config --get github.token')
thl_list = commands.getoutput('/usr/local/bin/git config --get thl.list')

def add_issue(repo,issue,list):
	'''
	Add an issue from GitHub into THL
	@param repo: GitHub repo
	@param issue: GitHub issue
	@param list: THL List
	'''
	# This is part of our identifier for checking duplicates
	hash = '[%s#%s]'%( repo.name, issue.number)
	title = '%s %s /GitHub'%(issue.title,hash)
	
	# Loop through all the tasks
	for task in list.tasks():
		# and if we find our hash in the title
		if hash in task.title:
			# skip it
			print 'found', title
			return
	print 'adding', title
	newtask = TheHitList.Task()
	newtask.title = title.encode('utf8')
	list.add_task(newtask)

# Initialize the GitHub API
github = Github(gh_name,gh_token)
# Initialize the THL connection
thl = TheHitList.Application()
# Search for our list in THL
list =  thl.find_list(thl_list)

# Loop through all our GitHub repos
for repo in github.repos.list(gh_name):
	# If the repo has open issues
	if repo.open_issues > 0:
		# Get all the issues from the repo
		for issue in github.issues.list('%s/%s'%(repo.owner,repo.name),state='open'):
			# and add them into THL
			add_issue(repo,issue,list)
