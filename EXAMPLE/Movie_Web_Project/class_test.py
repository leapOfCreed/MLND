
class Test(object):
	"""docstring for Test"""
	def __init__(self, name):
		self.name = name


class Test_plus(Test):
	"""docstring for Test_plus"""
	def __init__(self, name, times):
		# Init parent class
		super(Test_plus, self).__init__(name) # same as Test.__init__(self, name)
		self.times = times
		

if __name__ == '__main__':
	
	test = Test('test')
	print(test.__module__)
	print(test.__doc__)
	print(test.name)

	test1 = Test_plus('test1', 79)
	print(test1.name)

	# test2 = Test_plus(test, 37)
	# print(test2.name)
	# print(test2.times)
		