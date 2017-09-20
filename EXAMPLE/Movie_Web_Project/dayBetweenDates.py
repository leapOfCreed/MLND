# Judge the year werther is leap year

def isLeapYear(year):

	if year % 4 == 0 and year % 100 != 0 or year % 400 == 0:
		return True
	return False

# Get the special days in the special month
def dayInMonth(year, month):
	if isLeapYear(year):
		days = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
		return days[month-1]
	else:
		days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
		return days[month-1]

def dateIsBefore(y1, m1, d1, y2, m2, d2):
	if y1 < y2:
		return True
	if y1 == y2:
		if m1 < m2:
			return True
		if m1 == m2:
			return d1 < d2
	return False


# The next day
def nextDay(year, month, day):
	days = dayInMonth(year, month)
	if month == 12 and day == days:
		return year + 1, 1, 1
	if day == days:
		return year, month + 1, 1
	return year, month, day + 1

# The days between two dates
def daysBetweenDates(y1, m1, d1, y2, m2, d2):
	days = 0
	while dateIsBefore(y1, m1, d1, y2, m2, d2):
		y1, m1, d1 = nextDay(y1, m1, d1)
		days += 1
	return days



if __name__ == '__main__':
	print nextDay(2017, 2, 28)

	print daysBetweenDates(2017, 4, 27, 2017, 10, 1)