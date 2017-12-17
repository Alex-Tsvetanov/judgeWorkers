class homework:
	def __init__ (self, name, langs, start, end, evaling):
		self.name = str(name)
		self.langs = langs
		self.start = start
		self.end = end
		self.type = evaling;

	def to_object (self):
		return {
			'name': self.name,
			'langs': self.langs,
			'start': self.start,
			'end': self.end,
			'type': self.type
		}


