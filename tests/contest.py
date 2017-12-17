class contest:
	def __init__ (self, name, langs, start, end, tasks):
		self.name = str(name)
		self.langs = langs
		self.start = start
		self.end = end
		self.tasks = tasks

	def to_object (self):
		return {
			'name': self.name,
			'langs': self.langs,
			'start': self.start,
			'end': self.end,
			'tasks': self.tasks,
		}

