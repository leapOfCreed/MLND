
def read_text():

	with open('movie_quotes.txt') as file:
		content = file.read()
		print (content)


class Test(object):
	"""docstring for Test"""
	def __init__(self, name):
		self.name = name


if __name__ == '__main__':
	read_text()