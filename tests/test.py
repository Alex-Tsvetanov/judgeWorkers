class test:
	def __init__ (self, input_, output):
		self.input = input_
		self.output = output
	
	def to_object (self):
		return {
			'input': self.input,
			'output': self.output,
		}

