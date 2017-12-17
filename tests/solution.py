import datetime

class solution:
	def __init__ (self, contest, task, user, code, lang):
		self.contest_id = str(contest)
		self.task_id = str(task)
		self.user_id = str(user)
		self.code = str(code)
		self.time = datetime.datetime.utcnow()
		self.lang = str(lang)
		self.points = float('nan')
		self.label = ''

	def to_object (self):
		return {
			'contest_id': self.contest_id,
			'task_id': self.task_id,
			'user_id': self.user_id,
			'code': self.code,
			'lang': self.lang,
			'time': self.time,
			'points': self.points,
			'label': self.label,
		}
