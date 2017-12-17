from Crypto.Hash import SHA256

class user:
	@staticmethod
	def crypto(password):
		return SHA256.new(password.encode ()).hexdigest()

	def __init__(self, name, username, email, password):
		self.name = name
		self.username = username
		self.email = email
		self.password = self.crypto(password)

	def to_object (self):
		return {
			'name': self.name,
			'username': self.username,
			'email': self.email,
			'password': self.password,
		}
