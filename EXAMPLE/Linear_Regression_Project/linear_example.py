from decimal import Decimal, getcontext

from vector_model import Vector

getcontext().prec = 30


class Line(object):

    NO_NONZERO_ELTS_FOUND_MSG = 'No nonzero elements found'

    def __init__(self, normal_vector=None, constant_term=None):
        self.dimension = 2

        if not normal_vector:
            all_zeros = ['0']*self.dimension
            normal_vector = Vector(all_zeros)
        self.normal_vector = normal_vector

        if not constant_term:
            constant_term = Decimal('0')
        self.constant_term = Decimal(constant_term)

        self.set_basepoint()

    def __eq__(self, ell):
        if Vector(self.normal_vector).is_zero():
            if not Vector(ell.normal_vector).is_zero():
                return False
            else:
                diff = self.constant_term - ell.constant_term
                return MyDecimal(diff).is_near_zero()
        elif Vector(ell.normal_vector).is_zero():
            return False

        if not Vector(self.normal_vector).isParallel(Vector(ell.normal_vector)):
            return False

        x0 = self.basepoint
        y0 = ell.basepoint
        basepoint_difference = x0.mins(y0)

        v = self.normal_vector
        return basepoint_difference.isOrthog(v)

    def is_parallel_to(self, ell):
        v1 = self.normal_vector
        v2 = ell.normal_vector

        return v1.isParallel(v2)

    def set_basepoint(self):
        # try:
        n = self.normal_vector
        c = self.constant_term
        basepoint_coords = ['0']*self.dimension

        initial_index = Line.first_nonzero_index(n)
        initial_coefficient = n[initial_index]

        basepoint_coords[initial_index] = c/initial_coefficient
        self.basepoint = Vector(basepoint_coords)

        # except Exception as e:
        #     if str(e) == Line.NO_NONZERO_ELTS_FOUND_MSG:
        #         self.basepoint = None
        #     else:
        #         raise e

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

        n = self.normal_vector

        try:
            initial_index = Line.first_nonzero_index(n)
            terms = [write_coefficient(n[i], is_initial_term=(i == initial_index)) + 'x_{}'.format(i+1)
                     for i in range(self.dimension) if round(n[i], num_decimal_places) != 0]
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
        raise Exception(Line.NO_NONZERO_ELTS_FOUND_MSG)

    def intersection(self, ell):
        try:
            A, B = Vector(self.normal_vector).coordinates
            C, D = Vector(ell.normal_vector).coordinates
            k1 = self.constant_term
            k2 = ell.constant_term

            x_numerator = D * k1 - B * k2
            y_numerator = A * k2 - C * k1
            one_over_denom = Decimal('1')/(A * D - B * C)

            return Vector([x_numerator, y_numerator]).scalar(one_over_denom)

        except ZeroDivisionError:
            if self == ell:
                return self
            else:
                return None

        # # vector1 = Line(vector1)
        # denominator = self.normal_vector[
        #     0] * vector1.normal_vector[1] - self.normal_vector[1] * vector1.normal_vector[0]
        # if denominator == 0:
        #     return 'Parallel lines have no intersection'
        # return (vector1.normal_vector[1] * self.constant_term - \
        #         self.normal_vector[1] * vector1.constant_term) / denominator, \
        #        (self.normal_vector[0] * vector1.constant_term - \
        #         vector1.normal_vector[0] * self.constant_term)


class MyDecimal(Decimal):

    def is_near_zero(self, eps=1e-10):
        return abs(self) < eps



if __name__ == '__main__':

    line1 = Line([4.046, 2.836], 1.21)
    line2 = Line([10.115, 7.09], 3.025)
    print 'group 1'
    print line1.intersection(line2)

    # line3 = Line([7.204, 3.182], 8.68)
    # line4 = Line([8.172, 4.114], 9.883)
    # print 'group 2'
    # print line3.intersection(line4)

    # line5 = Line([1.182, 5.562], 6.744)
    # line6 = Line([1.773, 8.343], 9.525)
    # print 'group 3'
    # print line5.intersection(line6)

    # line1 = Line([2, 4], 8)
    # line2 = Line([5, 10], 12)

    # print line1.normal_vector
    # print line1.intersection(line2)