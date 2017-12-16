from vector_model import Vector
from decimal import Decimal


class Line_Plane(object):
	"""docstring for Line"""
	NO_NONZERO_ELTS_FOUND_MSG = 'No nonzero elements found'

	def __init__(self, normal_vector=None, constant_term=None):

		self.dimension = 3

		if not normal_vector:
			all_zeros = [0]*self.dimension
			normal_vector = Vector(all_zeros)
		self.normal_vector = Vector(normal_vector)

		if not constant_term:
			constant_term = 0
		self.constant_term = constant_term
		self.dimension = len(normal_vector)

	def isParallelTo(self, ell):
		v_self = self.normal_vector
		v_ell = ell.normal_vector

		return v_self.isParallel(v_ell)

	def intersection(self, ell):

		if not self.isParallelTo(ell):
			A, B = self.normal_vector.coordinates
			C, D = ell.normal_vector.coordinates
			k1 = self.constant_term
			k2 = ell.constant_term

			x_numerator = D * k1 - B * k2
			y_numerator = A * k2 - C * k1
			denom = 1 / (A*D - B*C)

			return Vector([x_numerator, y_numerator]).scalar(denom)

		else:
			return 'They are paralleled'

	def is_equal(self, ell):

		if list(self.normal_vector.coordinates) == list(ell.normal_vector.coordinates) and self.constant_term == ell.constant_term:
			return True

		v1 = self.normal_vector.coordinates
		v2 = ell.normal_vector.coordinates
		v = set()
		if not 0 in v2:
			v = set(v1 / v2)
			if ell.constant_term != 0:
				v.add(self.constant_term / ell.constant_term)
			else:
				return self.constant_term == ell.constant_term

		return len(v) == 1

	def __str__(self):

		num_decimal_places = 3

		def write_coefficient(coefficient, is_initial_term=False):
			coefficient = round(coefficient, num_decimal_places)
			if coefficient % 1 == 0:
				coefficient = int(coefficient)

			output = ''

			if coefficient < 0:
				output += '-'
			if coefficient > 0 and not is_initial_term:
				output += '+'

			if not is_initial_term:
				output += ' '

			if abs(coefficient) != 1:
				output += '{}'.format(abs(coefficient))

			return output

		n = self.normal_vector.coordinates

		try:
			initial_index = Line_Plane.first_nonzero_index(n)
			terms = [write_coefficient(n[i], is_initial_term=(i == initial_index)) + 
					'x_{}'.format(i+1) for i in range(self.dimension) if round(n[i],
					num_decimal_places) != 0]
			output = ' '.join(terms)

		except Exception as e:
			if str(e) == self.NO_NONZERO_ELTS_FOUND_MSG:
				output = '0'
			else:
				raise e

		constant = round(self.constant_term, num_decimal_places)
		if constant % 1 == 0:
			constant = int(constant)
		output += ' = {}'.format(constant)

		return output

	@staticmethod
	def first_nonzero_index(iterable):
		for k, item in enumerate(iterable):
			if not MyDecimal(item).is_near_zero():
				return k
		raise Exception(Line_Plane.NO_NONZERO_ELTS_FOUND_MSG)


class MyDecimal(Decimal):

	def is_near_zero(self, eps=1e-10):
		return abs(self) < eps



if __name__ == '__main__':

	# Line example

	line1 = Line_Plane([4.046, 2.836], 1.21)
	line2 = Line_Plane([10.115, 7.09], 3.025)
	print 'group 1'
	print line1.intersection(line2)
	print line1.isParallelTo(line2)

	line3 = Line_Plane([7.204, 3.182], 8.68)
	line4 = Line_Plane([8.172, 4.114], 9.883)
	print 'group 2'
	print line3.intersection(line4)
	print line3.isParallelTo(line4)

	line5 = Line_Plane([1.182, 5.562], 6.744)
	line6 = Line_Plane([1.773, 8.343], 9.525)
	print 'group 3'
	print line5.intersection(line6)
	print line5.isParallelTo(line6)


	# Plane example
	print '------'

	plane1 = Line_Plane([-0.412, 3.806, 0.728], -3.46)
	plane2 = Line_Plane([1.03, -9.515, -1.82], 8.65)
	print plane1.is_equal(plane2)

	plane3 = Line_Plane([2.611, 5.528, 0.283], 4.6)
	plane4 = Line_Plane([7.715, 8.306, 5.342], 3.76)
	print plane3.isParallelTo(plane4)

	plane5 = Line_Plane([-7.926, 8.625, -7.212], -7.952)
	plane6 = Line_Plane([-2.642, 2.875, -2.404], -2.443)
	print plane5.isParallelTo(plane6)
	print plane5.is_equal(plane6)
