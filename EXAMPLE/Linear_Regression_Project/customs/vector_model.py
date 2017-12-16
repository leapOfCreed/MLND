
import numpy as np
import math


class Vector(object):
    """docstring for Vector"""

    def __init__(self, coordinates):

        try:
            if not coordinates:
                raise ValueError

            self.coordinates = np.array(coordinates)
            self.dimension = len(coordinates)

        except ValueError:
            raise ValueError('coordinates must be nonempty')
        except TypeError:
            raise TypeError('coordinates must be an iterable')
    # print format

    def __str__(self):
        return 'Vector: {}'.format(self.coordinates)
    # equal result

    def __eq__(self, v):
        return self.coordinates == v

    # vectors plus
    # v1(x1, y1, ..), v2(x2, y2, ..) v1+v2=(x1+x2, y1+y2, ..)
    def plus(self, v):
    	if type(v) == type(self):
    		content = list(self.coordinates + v.coordinates)
    		return Vector(content)
        return Vector(list(self.coordinates + v))

    # vectors mins
    # v1(x1, y1, ..), v2(x2, y2, ..) v1-v2=(x1-x2, y1-y2, ..)
    def mins(self, v):
    	if type(v) == type(self):
    		content = list(self.coordinates - v.coordinates)
    		return Vector(content)
        return Vector(list(self.coordinates - v))

    # vector scalar
    # v(x, y, ..), n v*n=(x*n, y*n, ..)
    def scalar(self, n):
    	content = list(self.coordinates * n)
    	return Vector(content)

    # vector magnitude
    # v(x, y, ..)  ||v|| = sqrt(x^2 + y^2, ..)
    def magnitude(self):
        # l = [i**2 for i in self.coordinates]
        # return math.sqrt(sum(l))
        return math.sqrt(sum(self.coordinates * self.coordinates))

    # vector direction
    # v(x, y, ..)  ||v|| = sqrt(x^2 + y^2, ..)  (1 / ||v||) * v
    def direction(self):
        try:
            return Vector([i / self.magnitude() for i in self.coordinates])
            # return self.coordinates / self.magnitude()
        except ZeroDivisionError:
            raise ZeroDivisionError('Cannot be the zero vector')

        # # another way
        # try:
        # 	return self.scalar(1. / self.magnitude())
        # except ZeroDivisionError:
        # 	raise ZeroDivisionError('Cannot be the zero vector')

    # vector dot product
    def dot_product(self, v):
        return sum(self.coordinates * v.coordinates)

    # vectors angle
    # return degrees and rad
    def angle(self, v):
        rad = math.acos(round(self.direction().dot_product(
            v.direction()), 9))
        # return 'Degree: %f, Rad: %f' % (rad * 180 / math.pi, rad)
        return rad * 180 / math.pi, rad

    def is_zero(self):
        return round(self.magnitude(), 9) == 0

    # Judge the Parallel
    def isParallel(self, v):
        return (
            self.is_zero() or v.is_zero() or self.angle(
                v)[0] == 0 or self.angle(v)[1] == math.pi
        )

    # Judge the Orthogonality
    def isOrthog(self, v):
        if abs(round(self.dot_product(v), 9)) == 0:
            return True, self.dot_product(v)
        return False, self.dot_product(v)

    # get ||V|| value by v and b
    def get_Parallel_Vector_Value(self, b_vector):
        return self.dot_product(b_vector.direction())

    # get parallel v (projecting v in b)
    def get_Parallel_Vector(self, b_vector):
        return b_vector.direction().scalar(self.get_Parallel_Vector_Value(b_vector))

    # get orthog vector
    def get_Orthog_Vector(self, b_vector):
        return self.mins(self.get_Parallel_Vector(b_vector))

    # vectors times
    def vectors_Times(self, v):
        return Vector([
        	self.coordinates[1] * v.coordinates[2] - self.coordinates[2] * v.coordinates[1], 
        	v.coordinates[0] * self.coordinates[2] - self.coordinates[0] * v.coordinates[2], 
        	self.coordinates[0] * v.coordinates[1] - self.coordinates[1] * v.coordinates[0]
        	])

    # area of parallelogram
    def area_Parallelogram(self, v):
    	return self.vectors_Times(v).magnitude()

    # area of triangle
    def area_Triangle(self, v):
    	return self.area_Parallelogram(v) / 2

if __name__ == '__main__':

    # vector1 = Vector([8.462, 7.893, -8.187])
    # w_vector1 = Vector([6.984, -5.975, 4.778])
    # print vector1.vectors_Times(w_vector1)

    # vector2 = Vector([-8.987, -9.838, 5.031])
    # w_vector2 = Vector([-4.268, -1.861, -8.866])
    # print vector2.area_Parallelogram(w_vector2)

    # vector3 = Vector([1.5, 9.547, 3.691])
    # w_vector3 = Vector([-6.007, 0.124, 5.772])
    # print vector3.area_Triangle(w_vector3)

    # vector1 = Vector([1.182, 5.562])
    # b_vector1 = Vector([1.773, 8.343])
    # print vector1.get_Parallel_Vector(b_vector1)
    # print vector1.isParallel(b_vector1)

    # vector2 = Vector([-9.88, -3.264, -8.159])
    # b_vector2 = Vector([-2.155, -9.353, -9.473])
    # print vector2.get_Orthog_Vector(b_vector2)

    # vector3 = Vector([3.009, -6.172, 3.692, -2.51])
    # b_vector3 = Vector([6.404, -9.144, 2.759, 8.718])
    # print vector3.get_Parallel_Vector(b_vector3)
    # print vector3.get_Orthog_Vector(b_vector3)

    vector1 = Vector([-2.328, -7.284, -1.214])
    vector2 = Vector([-1.821, 1.072, -2.94])
    print vector1.isParallel(vector2)

    
    print type(vector1.scalar(3))
    print vector1.plus(vector2)
    print type(vector1)



	# v1 = Vector([1.182, 5.562])
	# v2 = Vector([1.773, 8.343])

	# print v1.isParallel(v2)

    # vector7 = Vector([-7.579, -7.88])
    # vector8 = Vector([22.737, 23.64])
    # vector5 = Vector([-2.029, 9.97, 4.172])
    # vector6 = Vector([-9.231, -6.639, -7.245])

    # print vector5.angle(vector6)
    # print vector5.isParallel(vector6)
    # print vector1.isParallel(vector2)
    # print vector7.isParallel(vector8)

    # print vector1.isOrthog(vector2)
    # print vector7.isOrthog(vector8)
    # print vector5.isOrthog(vector6)


