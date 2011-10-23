#!/usr/bin/env python
import datetime
import TheHitList
from extra.Terminal import TerminalController

SPACER_STR		= '${BOLD}${BLUE}%s${NORMAL}'

TITLE_STR		= '${BOLD}${WHITE}%s${NORMAL}'
COMPLETE_STR	= '${BOLD}${CYAN}%s${NORMAL}'
CANCELED_STR	= '${BOLD}${BLACK}%s${NORMAL}'

DATE_STR		= '${YELLOW}%s${NORMAL}'
OVERDUE_STR		= '${RED}%s${NORMAL}'

thl = TheHitList.Application()
term = TerminalController()
spacer = term.render(SPACER_STR%'-'*50)

print 'Today\'s Tasks'
print spacer
for task in thl.today().tasks():
	if task.completed:
		print term.render(COMPLETE_STR % task.title)
	elif task.canceled:
		print term.render(CANCELED_STR % task.title)
	else:
		print term.render(TITLE_STR % task.title)
	
	if( task.start_date is not None ):
		buffer = 'Start: %s'%task.start_date.date()
		buffer += ' '*( 20 - len(buffer))
		buffer = term.render(DATE_STR % buffer)
	else:
		buffer = ' '*20
	
	if( task.due_date is not None ):
		str = 'Due: %s'%task.due_date.date()
		if (task.due_date < datetime.datetime.today() ):
			buffer += term.render(OVERDUE_STR % str)
		else:
			buffer += term.render(DATE_STR % str)
	print buffer
	
	if( task.notes != '' ): print 'Notes: %s'%task.notes
	
	print spacer
