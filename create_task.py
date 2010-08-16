#!/usr/bin/env python
import TheHitList
from optparse import OptionParser

if __name__ == '__main__':
	parser = OptionParser()
	parser.add_option("--show", dest="show", help="Show tasks in a list", default=None)
	parser.add_option("--list", dest="list", help="Add task to a specific list", default=None)
	(opts,args) = parser.parse_args()
	
	thl = TheHitList.Application()
	
	if(opts.show):
		if opts.show == 'inbox':
			list = thl.inbox()
		else:
			list = thl.find_list(opts.show)
		for task in list.tasks():
			print task.title
		exit()
	
	if(len(args)==0): parser.error('Missing Task')
	
	newtask = TheHitList.Task()
	newtask.title = ' '.join(args)
	if opts.list is None:
		list = thl.inbox()
	else:
		list = thl.find_list(opts.list)
	list.add_task(newtask)
	print 'Task (%s) has been added'%newtask.title
		