#!/usr/bin/env python
import TheHitList
from extra.Terminal import TerminalController
HILIGHT = '${BOLD}${YELLOW}%s${NORMAL}'
term = TerminalController()
def tprint(string): print term.render(HILIGHT % string)

thl = TheHitList.Application()

tprint('Print Today List')
thl.today().rprint()

tprint('Print Recursive folders list')
thl.folders().rprint()

tprint('Create new task in inbox')
thl.new_task('Creating a new task')

tprint('Find named list or create a new one if it does not exist')
list =  thl.find_list('TheHitList.py')
if not list:
	list = thl.new_list('TheHitList.py')

if list:
	tprint('Create a new task in our list')
	task = TheHitList.Task()
	task.title = "Testing TheHitList.py"
	task.notes = "Some notes can go here"
	task.print_obj()
	list.add_task(task)