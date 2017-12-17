class task:
	def __init__ (self, name, description, tests, checker, visible):
		self.name = str(name)
		self.description = description
		self.tests = tests
		self.checker = checker
		self.visible = visible

	def to_object (self):
		return {
			'name': self.name,
			'description': self.description,
			'tests': self.tests,
			'checker': self.checker,
			'visible': self.visible
		}


