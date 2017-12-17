class checker:
	def __init__ (self, name, command):
		self.name = name
		self.command = command
	
	def get_command (self, in1, out1, out2):
		return self.command.replace ('(in1)', in1).replace ('(out1)', out1).replace ('(out2)', out2)
	
	def to_object (self):
		return {
			'name': self.name,
			'command': self.command,
		}
