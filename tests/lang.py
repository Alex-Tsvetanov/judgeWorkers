class lang:
	def __init__ (self, name, ext, mode, commandCompile, commandExecute):
		self.name = str(name)
		self.ext = str(ext)
		self.mode = str(mode)
		self.commandCompile = str(commandCompile)
		self.commandExecute = str(commandExecute)

	def to_object (self):
		return {
			'name': self.name,
			'ext': self.ext,
			'mode': self.mode,
			'compile': self.commandCompile,
			'execute': self.commandExecute ,
		}
	
	@staticmethod
	def from_cursor (cursor):
		cursor.pop('_id', None)
		return cursor 
	
	@staticmethod
	def from_cursor_to_string (cursor):
		cursor.pop('_id', None)
		
		return {
			'name': cursor['name'],
			'ext': cursor['ext'],
			'mode': cursor['mode'],
			'compile': cursor['compile'].format ('(your source file)','(output file)'),
			'execute': cursor['execute'].format ('(output file)'),
		}
		 
