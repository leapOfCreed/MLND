
from random import randint


print 'number ' + '|' + ' occurrence'
for i in range(10):
	print '     ' + str(i) + ' | ' + '*' * randint(1, 3)

