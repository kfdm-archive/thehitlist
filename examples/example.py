#!/usr/bin/env python
import TheHitList
from clint.textui import puts, colored

thl = TheHitList.Application()

puts(colored.yellow('Print Today List'))
thl.today().rprint()

puts(colored.yellow('Print Recursive folders list'))
thl.folders().rprint()

puts(colored.yellow('Create new task in inbox'))
thl.new_task('Creating a new task')

puts(colored.yellow('Find named list or create a new one if it does not exist'))
list = thl.find_list('TheHitList.py')
if not list:
	list = thl.new_list('TheHitList.py')

if list:
	puts(colored.yellow('Create a new task in our list'))
	task = TheHitList.Task()
	task.title = "Testing TheHitList.py"
	task.notes = "Some notes can go here"
	task.print_obj()
	list.add_task(task)
