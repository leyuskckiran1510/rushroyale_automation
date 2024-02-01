

class Event:
	_initiated = None
	def __new__(cls,*args,**kwargs) -> "Event":
		return super().__new__(cls,*args,**kwargs)

	def __init__(self) -> None:
		...	