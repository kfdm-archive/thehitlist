try:
	import appscript
except ImportError:
	import sys
	print >> sys.stderr,'Requires appscript module'
	print >> sys.stderr,'http://appscript.sourceforge.net/py-appscript/install.html'
	print >> sys.stderr,'"sudo easy_install appscript"'
	exit(1)

def rprint(item,tabs = 0):
	'''Recursively print Task, Folder, or Group objects'''
	if isinstance(item,Task):
		print '\t'*tabs,'<Task>',item.title
	if isinstance(item,List):
		print '\t'*tabs,'<List>',item.name
		for task in item.tasks():
			rprint(task,(tabs+1))
	if isinstance(item,Folder):
		print '\t'*tabs,'<Folder>',item.name
		for group in item.groups():
			rprint(group,(tabs+1))

class Application(object):
	def __init__(self):
		self.thl = appscript.app('The Hit List')
	def inbox(self):
		'''Return the inbox List'''
		return List(self.thl.inbox)
	def today(self):
		'''Return the today List'''
		return List(self.thl.today_list)
	def upcoming(self):
		'''Return the upcoming List'''
		return List(self.thl.upcoming_list)
	def folders(self):
		'''Return the root Folder'''
		return Folder(self.thl.folders_group)
	def tags(self):
		'''Return a list of Tag objects'''
		tags = []
		for tag in self.thl.tags_group.tags():
			tags.append(Tag(tag))
		return tags
			
	def find_list(self,name):
		if name.lower() in ['inbox', 'upcoming', 'today']:
			list = getattr(self,name.lower())
			return list()
		'''Recursivly find a List by name'''
		name = unicode(name,'utf-8')
		return self.folders().find_list(name)
	def find_folder(self,name):
		'''Recursivly find a Folder by name'''
		name = unicode(name,'utf-8')
		return self.folders().find_folder(name)
	def find_task(self,name):
		'''Recursivly find a Task by name'''
		name = unicode(name,'utf-8')
		return self.folders().find_task(name)
	
	def add_task(self,task):
		'''Add a Task to the inbox'''
		self.inbox().add_task(task)
	def add_list(self,list):
		'''Add a List to the root folder'''
		self.folders().add_list(list)
	def new_list(self,name):
		'''Add a list to the root folder with the specified name'''
		list = List()
		list.name = name
		self.add_list(list)
		return self.find_list(name)
	def new_task(self,title):
		'''Add a task to the inbox with the specified title'''
		task = Task()
		task.title = title
		self.inbox().add_task(task)
	
class Task(object):
	def __init__(self,obj=None):
		self._raw = obj
		self._properties = [
			'id','title','notes',
			'start_date','due_date',
			'estimated_time','actual_time',
			'canceled_date',
			'modified_date','priority',
			'archived','canceled','completed',
			'url','completed_date','repeating'
			]
		if obj:
			for prop in self._properties:
				func = getattr(obj,prop)
				value = func()
				if value == appscript.k.missing_value: value = None
				self.__setattr__(prop,value)
		else:
			self.id = None
			self.title = None
	def print_obj(self):
		for prop in self._properties:
			value = self.__dict__.get(prop,None)
			if value: print prop,':',value
	def format_obj(self):
		obj = {}
		if self.__dict__.get('title',None):
			obj[appscript.k.title] = unicode(self.title,'utf-8')
		if self.__dict__.get('notes',None):
			obj[appscript.k.notes] = unicode(self.notes,'utf-8')
		return obj
	def __repr__(self):
		return '<%s:%s:%s>'%(self.__class__,self.id,self.title)
	def rprint(self):
		rprint(self)
	
class Group(object):
	def __init__(self,obj=None):
		self._raw = obj
		self._properties = [
			'id','name',
			'modified_date',
			'created_date'
			]
		if obj:
			for prop in self._properties:
				func = getattr(obj,prop)
				self.__setattr__(prop,func())
	def print_obj(self):
		for prop in self._properties:
			print prop,self.__getattribute__(prop)
	def __repr__(self):
		return '<%s:%s:%s>'%(self.__class__,self.id,self.name)
	def find_list(self,name):
		def _find_list(name,groups):
			for group in groups:
				if isinstance(group,Folder):
					result = _find_list(name,group.groups())
					if result is not None: return result
				if group.name == name: return group
			return None
		return _find_list(name,self.groups())
	def find_folder(self,name):
		def _find_folder(name,groups):
			for group in groups:
				if isinstance(group,Smart_Folder):
					if group.name == name: return group
				if isinstance(group,Folder):
					if group.name == name: return group
					result = _find_folder(name,group.groups())
					if result is not None: return result
			return None
		return _find_folder(name,self.groups())
	def rprint(self):
		rprint(self)

class List(Group):
	def tasks(self):
		tasks = []
		for task in self._raw.tasks():
			tasks.append(Task(task))
		return tasks
	def add_task(self,task):
		self._raw().make(
			new=appscript.k.task,
			with_properties=task.format_obj()	
		)
	def format_obj(self):
		obj = {}
		if self.__dict__.get('name',None):
			obj[appscript.k.name] = self.name
		return obj
class Folder(Group):
	def groups(self):
		if not self._raw.groups: return []
		groups = []
		for group in self._raw.groups():
			tmpClass = group.class_()
			if tmpClass == appscript.k.folder:
				groups.append(Folder(group))
			elif tmpClass == appscript.k.smart_folder:
				groups.append(Smart_Folder(group))
			elif tmpClass == appscript.k.list_:
				groups.append(List(group))
			else:
				print 'Error:',tmpClass
		return groups
	def add_list(self,list):
		self._raw().make(
			new=appscript.k.list_,
			with_properties=list.format_obj()
		)
class Smart_Folder(Group):
	def tasks(self):
		tasks = []
		for task in self._raw.tasks():
			tasks.append(Task(task))
		return tasks
class Tag(Group):
	pass
