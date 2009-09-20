import TheHitList

thl = TheHitList.Application()

print 'Today'
for task in thl.today().tasks():
	print task
print

for item in thl.folders().groups():
	print item
	if isinstance(item, TheHitList.Folder):
		print item.groups()
	elif isinstance(item, TheHitList.List):
		print item.tasks()
	else:
		print 'Error',type(item)
	print

list =  thl.find_list('TheHitList.py')
if list:
	task = TheHitList.Task()
	task.title = "Testing TheHitList.py"
	task.notes = "Some notes can go here"
	task.print_obj()
	list.add_task(task)
