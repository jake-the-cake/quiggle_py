import json

def is_object(obj) -> bool:
	if isinstance(obj, str) or isinstance(obj, int) or isinstance(obj, bool) or not obj:
		return False
	return True

class Json:
	def __init__(self, value: any = None) -> dict:
		self.obj = {}
		self.value = value

	def to_json(self):
		if not is_object(self.value):
			self.obj['value'] = self.value
		else:
			# obj = vars(self.value).items()
			if hasattr(self.value, '__dict__'):
				for attr, val in vars(self.value).items():
					self.obj[attr] = str(to_json(val))
					# print(attr, val, 'ok')
			else:
				for attr in dir(self.value):
					self.obj[attr] = Json(attr).to_json()
					# print(attr, 'not ok')
			# if not obj: obj = vars(self.value).__dict__.items()
			# for attr, val in vars(self.value).items():
				# print(attr, val)
				# if not is_object(val):
				# if isinstance(val, str or int or bool) or not val:
					# print(attr)
					# self.obj[attr] = str(val)
				# else:
					# self.obj[attr] = Json(self.obj[attr]).to_json()
					# self.obj[attr] = to_json({ attr: val })
				# else:
					# self.obj[attr] = Json(obj or {self.obj[attr]: val}).to_json()
		return json.dumps(obj = self.obj, indent = 2)

def to_json(obj: any):
	return Json(obj).to_json()