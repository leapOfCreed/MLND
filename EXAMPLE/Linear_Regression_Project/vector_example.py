from math import sqrt, pi, acos
from decimal import Decimal, getcontext

getcontext().prec = 30

class Vector(object):

	CANNOT_NORMALIZED_ZERO_VECTOR_MSG = 'Cannot normalized the zero vector'
	NO_UNIQUE_PARALLEL_COMPONENT_MSG = ''
	NO_UNIQUE_ORTHOGONAL_COMPONENT_MSG = ''
	ONLY_DEFINED_IN_TWO_THREE_DIMS_MSG = ''

	"""docstring for Vector"""
	def __init__(self, coordinates):
		try:
			if not coordinates:
				raise ValueError
			self.coordinates = tuple([Decimal(x) for x in coordinates])
			self.dimension = len(coordinates)

		except ValueError:
			raise ValueError('The coordinates must be nonempty')

		except TypeError:
			raise TypeError('The coordinates must be an iterable')


	def __str__(self):
		return 'Vector: {}'.format(self.coordinates)


	def __eq__(self, v):
		return self.coordinates == v.coordinates


	def plus(self, v):
		plus_coordinates = [x + y for x, y in zip(self.coordinates, v.coordinates)]
		return Vector(plus_coordinates)


	def minus(self, v):
		minus_coordinates = [x - y for x, y in zip(self.coordinates, v.coordinates)]
		return Vector(minus_coordinates)


	def scalar(self, count):
		scalar_coordinates = [x * Decimal(count) for x in self.coordinates]
		return Vector(scalar_coordinates)


	def magnitude(self):
		mag_coordinates = [x ** 2 for x in self.coordinates]
		return sqrt(sum(mag_coordinates))


	def normalized(self):
		try:
			magnitude = self.magnitude()
			return self.scalar(1./magnitude)

		except ZeroDivisionError:
			raise Exception('Cannot normalized the zero vector')


	def dot(self, v):
		return sum([x * y for x, y in zip(self.coordinates, v.coordinates)])


	def angle(self, v, in_degrees = False):
		try:
			u1 = self.normalized()
			u2 = v.normalized()
			angle = acos(u1.dot(u2))

			if in_degrees:
				degress_per_radians = 180. / pi
				return angle * degress_per_radians
			else:
				return angle

		except Exception as e:
			if str(e) == self.CANNOT_NORMALIZED_ZERO_VECTOR_MSG:
				return Exception('Cannot compute an angle with the zero vector')
			else:
				raise e


	def is_Parallel(self, v):
		return (self.is_zero() or v.is_zero() or self.angle(v) == 0 or self.angle(v) == pi)


	def is_Orthogonal(self, v, tolerance = 1e-10):
		return self.dot(v) < tolerance


	def is_zero(self, tolerance = 1e-10):
		return self.magnitude() < tolerance


	def component_orthogonal_to(self, basic):
		try:
			projection = self.component_parallel_to(basic)
			return self.minus(projection)

		except Exception as e:
			if str(e) == self.NO_UNIQUE_PARALLEL_COMPONENT_MSG:
				raise Exception(self.NO_UNIQUE_ORTHOGONAL_COMPONENT_MSG)
			else:
				raise e


	def component_parallel_to(self, basic):
		try:
			u = basic.normalized()
			weight = self.dot(u)
			return u.scalar(weight)

		except Exception as e:
			if str(e) == self.CANNOT_NORMALIZED_ZERO_VECTOR_MSG:
				raise Exception(self.NO_UNIQUE_PARALLEL_COMPONENT_MSG)
			else:
				raise e


	def cross(self, v):
		try:
			x_1, y_1, z_1 = self.coordinates
			x_2, y_2, z_2 = v.coordinates
			cross_coordinates = [y_1*z_2 - y_2*z_1, -(x_1*z_2 - x_2*z_1), x_1*y_2 - x_2*y_1]
			return Vector(cross_coordinates)

		except ValueError as e:
			msg = str(e)
			if msg == 'need more than 2 values to unpack':
				self_embedded_in_R3 = Vector(self.coordinates + ('0',))
				v_embedded_in_R3 = Vector(v.coordinates + ('0',))
				return self_embedded_in_R3.cross(v_embedded_in_R3)
			elif (msg == 'too many values to unpack' or msg == 'need more than 1 value to unpack'):
				raise Exception(self.ONLY_DEFINED_IN_TWO_THREE_DIMS_MSG)
			else:
				raise e


	def area_parallel_with(self, v):
		cross_product = self.cross(v)
		return cross_product.magnitude()


	def area_triangle_with(self, v):
		return self.area_parallel_with(v) / 2.0


if __name__ == '__main__':

	vector3 = Vector([1.5, 9.547, 3.691])
	w_vector3 = Vector([-6.007, 0.124, 5.772])
	print vector3.area_triangle_with(w_vector3)

	v = Vector([-7.578, -7.88])
	w = Vector([22.737, 23.64])
	print v.is_Orthogonal(w)
	print v.is_Parallel(w)

	v1 = Vector([1,2,4])
	v2 = Vector([5,7,9])
	v = v1.plus(v2)
	print v

	v = v1.minus(v2)
	print v

	v = v1.scalar(5)
	print v

	v = v1.magnitude()
	print v

	v = v1.dot(v2)
	print v