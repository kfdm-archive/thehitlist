#!/usr/bin/env python
import datetime
import TheHitList
from clint.textui import puts, colored

thl = TheHitList.Application()
spacer = colored.blue('-'*50)

print 'Today\'s Tasks'
print spacer
for task in thl.today().tasks():
	if task.completed:
		puts(colored.cyan(task.title))
	elif task.canceled:
		puts(colored.black(task.title))
	else:
		puts(colored.white(task.title))

	if(task.start_date is not None):
		buffer = 'Start: %s'%task.start_date.date()
		buffer += ' '*(20 - len(buffer))
		buffer = colored.yellow(buffer)
	else:
		buffer = ' '*20

	if(task.due_date is not None):
		str = 'Due: %s'%task.due_date.date()
		if(task.due_date < datetime.datetime.today()):
			buffer += colored.red(str)
		else:
			buffer += colored.yellow(str)
	puts(buffer)

	if(task.notes != ''):
		print 'Notes: %s' % task.notes

	print spacer
