import appscript

def rprint(items,tabs = 0):
	for item in items:
		print '\t'*tabs,item
		if isinstance(item,List):
			rprint(item.tasks(),(tabs+1))
		if isinstance(item,Folder):
			rprint(item.groups(),(tabs+1))

class Application(object):
	def __init__(self):
		self.thl = appscript.app('The Hit List')
	def inbox(self):
		return List(self.thl.inbox)
	def today(self):
		return List(self.thl.today_list)
	def upcoming(self):
		return List(self.thl.upcoming_list)
	def folders(self):
		return Folder(self.thl.folders_group)
	def tags(self):
		tags = []
		for tag in self.thl.tags_group.tags():
			tags.append(Tag(tag))
		return tags
	def help(self):
		return self.thl.help()
			
	def find_list(self,name):
		return self.folders().find_list(name)
	def find_folder(self,name):
		return self.folders().find_folder(name)
	def find_task(self,name):
		return self.folders().find_task(name)
	
class Task(object):
	def __init__(self,obj=None):
		self._raw = obj
		self._properties = [
			'id','title','notes',
			'start_date','due_date',
			'estimated_time','actual_time',
			'archived_date','canceled_date',
			'modified_date','priority',
			'archived','canceled','completed',
			'url','completed_date','repeating'
			]
		if obj:
			for prop in self._properties:
				func = getattr(obj,prop)
				self.__setattr__(prop,func())
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
			obj[appscript.k.title] = self.title
		if self.__dict__.get('notes',None):
			obj[appscript.k.notes] = self.notes
		return obj
	def __repr__(self):
		return '<%s:%s:%s>'%(self.__class__,self.id,self.title)
	
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
				if isinstance(group,Folder):
					if group.name == name: return group
					result = _find_folder(name,group.groups())
					if result is not None: return result
			return None
		return _find_folder(name,self.groups())

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
				continue
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
	pass
class Tag(Group):
	pass
