#!/usr/bin/env python
import TheHitList
from optparse import OptionParser

if __name__ == '__main__':
	parser = OptionParser()
	parser.add_option("--list", dest="list", help="List tasks in Inbox", default=False,action="store_true")
	(opts,args) = parser.parse_args()
	
	thl = TheHitList.Application()
	
	if(opts.list):
		for task in thl.inbox().tasks():
			print task.title
		exit()
	
	if(len(args)==0): parser.error('Missing Task')
	
	newtask = TheHitList.Task()
	newtask.title = ' '.join(args)
	thl.inbox().add_task(newtask)
	print 'Task (%s) has been added'%newtask.title
		