from wx import NewId

class AutoId:
	def __getattr__(self, attr):
		if not hasattr(self, attr):
			id = NewId()
			setattr(self, attr, id)
			return id
		else:
			return self.__dict__[attr]
