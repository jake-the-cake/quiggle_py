import json

class Response:
	def __init__(self, req) -> None:
		pass

	def html():
		return '''
		<!doctype html>
		<html lang="en">
			<head>
				<meta charset="utf-8">
				<title>Hello, HTML!</title>
			</head>
			<body>
				<h1>Hello, HTML!</h1>
			</body>
		</html>
		'''
	
	def json():
		return json.dumps({
			'data': 'In JSON format'
		})