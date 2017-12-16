from decimal import *
from copy import deepcopy

from vector_model import Vector
from linear_model import Line_Plane

getcontext().prec = 30

class LinearSystem(object):

    getcontext().prec = 30

    ALL_PLANES_MUST_BE_IN_SAME_DIM_MSG = 'All planes in the system should live in the same dimension'
    NO_SOLUTIONS_MSG = 'No solutions'
    INF_SOLUTIONS_MSG = 'Infinitely many solutions'

    def __init__(self, planes):
        try:
            d = planes[0].dimension
            for p in planes:
                assert p.dimension == d

            self.planes = planes
            self.dimension = d

        except AssertionError:
            raise Exception(self.ALL_PLANES_MUST_BE_IN_SAME_DIM_MSG)


#----------------------------------------------
    # exchange position between row1 and row2
    def swap_rows(self, row1, row2):
        if row1 > len(self.planes) - 1 or row2 > len(self.planes) - 1 or row1 < 0 or row2 < 0:
            raise Exception(self.ALL_PLANES_MUST_BE_IN_SAME_DIM_MSG)
        self.planes[row1], self.planes[row2] = self.planes[row2], self.planes[row1]
        
    # multiply coefficient and row items
    def multiply_coefficient_and_row(self, coefficient, row):
        self.planes[row].constant_term *= coefficient
        self.planes[row].normal_vector = self.planes[row].normal_vector.scalar(coefficient)
        
    # 
    def add_multiple_times_row_to_row(self, coefficient, row_to_add, row_to_be_added_to): 
        self.planes[row_to_be_added_to].normal_vector = self.planes[row_to_be_added_to].normal_vector.plus(self.planes[row_to_add].normal_vector.scalar(coefficient))
        self.planes[row_to_be_added_to].constant_term += self.planes[row_to_add].constant_term * coefficient
    
#----------------------------------------

    # triangular form 
    def compute_triangular_form(self):
        system = deepcopy(self)

        num_variables = self.dimension
        j = 0

        for i in range(len(self)):
            while j < num_variables:
                c = MyDecimal(system.planes[i].normal_vector.coordinates[j])
                if c.is_near_zero():
                    swap_produce = system.swap_with_row_below_for_nonzero_coefficient_if_able(i, j)
                    if not swap_produce:
                        j += 1
                        continue

                system.clear_coefficient_below(i, j)
                j += 1
                break
            
        return system

    # when first item of first row is zero
    def swap_with_row_below_for_nonzero_coefficient_if_able(self, row, col):
        for i in range(row + 1, len(self)):
            coefficient = MyDecimal(self.planes[i].normal_vector.coordinates[col])
            if not coefficient.is_near_zero():
                self.swap_rows(row, i)
                return True
        return False

    # make coefficient to be 1
    def clear_coefficient_below(self, row, col):
        beta = self.planes[row].normal_vector.coordinates[col]

        for i in range(row + 1, len(self)):
            n = self.planes[i].normal_vector.coordinates
            gamma = n[col]
            alpha = -gamma / beta
            self.add_multiple_times_row_to_row(alpha, row, i)

# optimize triangle form
# -------------------------------------------------------------

    def compute_rref(self):
        tf = self.compute_triangular_form()

        pivot_indices = tf.indices_of_first_nonzero_terms_in_each_row()

        for i in range(len(tf))[::-1]:
            j = pivot_indices[i]
            if j < 0:
                continue
            tf.scale_row_to_make_coefficient_equal_one(i, j)
            tf.clear_coefficient_above(i, j)

        return tf

    def scale_row_to_make_coefficient_equal_one(self, row, col):
        n = self.planes[row].normal_vector.coordinates
        beta = 1. / n[col]
        self.multiply_coefficient_and_row(beta, row)

    def clear_coefficient_above(self, row, col):
        for k in range(row)[::-1]:
            n = self.planes[k].normal_vector.coordinates
            alpha = -(n[col])
            self.add_multiple_times_row_to_row(alpha, row, k)

# -------------------------------------------------------------

# -------------------------------------------------------------
    
    def compute_solution(self):
        try:
            return self.do_gaussian_elimination_and_parametrize_solution()
        except Exception as e:
            if str(e) == self.NO_SOLUTIONS_MSG:
                return str(e)
            else:
                raise e


    def do_gaussian_elimination_and_parametrize_solution(self):
        rref = self.compute_rref()

        rref.raise_exception_if_contradictory_equation()
        direction_vectors = rref.extract_direction_vectors_for_parametrization()
        basepoint = rref.extract_basepoint_for_parametrization()

        return Parametrization(basepoint, direction_vectors)


    def raise_exception_if_contradictory_equation(self):
        for p in self.planes:
            try:
                p.first_nonzero_index(p.normal_vector.coordinates)
            except Exception as e:
                if str(e) == 'No nonzero elements found':

                    constant_term = MyDecimal(p.constant_term)
                    if not constant_term.is_near_zero():
                        raise Exception(self.NO_SOLUTIONS_MSG)
                else:
                    raise e


    def extract_direction_vectors_for_parametrization(self):
        num_variables = self.dimension
        pivot_indices = self.indices_of_first_nonzero_terms_in_each_row()
        free_variable_indices = set(range(num_variables)) - set(pivot_indices)

        direction_vectors = []

        for free_var in free_variable_indices:
            vector_coords = [0] * num_variables
            vector_coords[free_var] = 1
            for i,p in enumerate(self.planes):
                pivot_var = pivot_indices[i]
                if pivot_var < 0:
                    break
                vector_coords[pivot_var] = -p.normal_vector.coordinates[free_var]
            direction_vectors.append(Vector(vector_coords))

        return direction_vectors


    def extract_basepoint_for_parametrization(self):
        num_variables = self.dimension
        pivot_indices = self.indices_of_first_nonzero_terms_in_each_row()

        basepoint_coords = [0] * num_variables

        for i,p in enumerate(self.planes):
            pivot_var = pivot_indices[i]
            if pivot_var < 0:
                break
            basepoint_coords[pivot_var] = p.constant_term

        return Vector(basepoint_coords)

# -------------------------------------------------------------
    def compare_for_triangular_form(self):
        pass


    def indices_of_first_nonzero_terms_in_each_row(self):
        num_equations = len(self)
        num_variables = self.dimension

        indices = [-1] * num_equations

        for i, p in enumerate(self.planes):
            try:
                # print p.normal_vector
                indices[i] = p.first_nonzero_index(p.normal_vector.coordinates)
            except Exception as e:
                if str(e) == Line_Plane.NO_NONZERO_ELTS_FOUND_MSG:
                    continue
                else:
                    raise e

        return indices

    def __len__(self):
        return len(self.planes)

    def __getitem__(self, i):
        return self.planes[i]

    def __setitem__(self, i, x):
        try:
            assert x.dimension == self.dimension
            self.planes[i] = x

        except AssertionError:
            raise Exception(self.ALL_PLANES_MUST_BE_IN_SAME_DIM_MSG)

    def __str__(self):
        ret = 'Linear System:\n'
        temp = ['Equation {}: {}, constant_term: {}'.format(i+1, p.normal_vector, p.constant_term)
                for i, p in enumerate(self.planes)]
        ret += '\n'.join(temp)
        return ret


class MyDecimal(Decimal):

    def is_near_zero(self, eps=1e-10):
        return abs(self) < eps


class Parametrization(object):
    """docstring for Parametrization"""

    BASEPT_AND_DIR_VECTORS_MUST_BE_IN_SAME_DIM_MSG = ('The basepoint and direction vectors should all live in the same dimension')

    def __init__(self, basepoint, direction_vectors):
        
        self.basepoint = basepoint
        self.direction_vectors = direction_vectors
        self.dimension = self.basepoint.dimension

        try:
            for v in direction_vectors:
                assert v.dimension == self.dimension
        except AssertionError:
            raise Exception(BASEPT_AND_DIR_VECTORS_MUST_BE_IN_SAME_DIM_MSG)

    def __str__(self):
        output = 'Parametrization:\nbasepoint:\n'
        direction_vec = [list(i.coordinates) for i in self.direction_vectors]
        result = []
        for i in range(self.dimension):
            item = []
            item.append(self.basepoint.coordinates[i])
            for j in range(len(direction_vec)):
                item.append(direction_vec[j][i])
            result.append(item)

        return output + str(result)

        

if __name__ == '__main__':

    # print s.indices_of_first_nonzero_terms_in_each_row()

    p1 = Line_Plane(normal_vector=[7, 5, 3, -5], constant_term=1)
    p2 = Line_Plane(normal_vector=[-4, 6, 2, -2], constant_term=1)
    p3 = Line_Plane(normal_vector=[-9, 4, -5, 9], constant_term=1)
    p4 = Line_Plane(normal_vector=[-9, -10, 5, -4], constant_term=1)
    s = LinearSystem([p1, p2, p3, p4])
    r = s.compute_rref()
    print r




# Parametrization
# testing
# ---------------------------------------------------------
    # p1 = Line_Plane(normal_vector=[0.786, 0.786, 0.588], constant_term=-0.714)
    # p2 = Line_Plane(normal_vector=[-0.138, -0.138, 0.244], constant_term=0.319)
    # s = LinearSystem([p1, p2])
    # r = s.compute_rref()
    # print r
    # c = s.compute_solution()
    # print c
    # print

    # p1 = Line_Plane(normal_vector=[8.631, 5.112, -1.816], constant_term=-5.113)
    # p2 = Line_Plane(normal_vector=[4.315, 11.132, -5.27], constant_term=-6.775)
    # p3 = Line_Plane(normal_vector=[-2.158, 3.01, -1.727], constant_term=-0.831)
    # s = LinearSystem([p1, p2, p3])
    # r = s.compute_rref()
    # print r
    # c = s.compute_solution()
    # print c
    # print

    # p1 = Line_Plane(normal_vector=[0.935, 1.76, -9.365], constant_term=-9.955)
    # p2 = Line_Plane(normal_vector=[0.187, 0.352, -1.873], constant_term=-1.991)
    # p3 = Line_Plane(normal_vector=[0.374, 0.704, -3.746], constant_term=-3.982)
    # p4 = Line_Plane(normal_vector=[-0.561, -1.056, 5.619], constant_term=5.973)
    # s = LinearSystem([p1, p2, p3, p4])
    # r = s.compute_rref()
    # print r
    # c = s.compute_solution()
    # print c
    # print p3



# Gaussian Elimination Solution
# testing
# ---------------------------------------------------------
    # print 'example 1'
    # p1 = Line_Plane(normal_vector=[5.862, 1.178, -10.366], constant_term=-8.15)
    # p2 = Line_Plane(normal_vector=[-2.931, -0.589, 5.183], constant_term=-4.075)
    # s = LinearSystem([p1, p2])
    # r = s.compute_rref()
    # print r
    # c = s.compute_solution()
    # print c

    # print '\nexample 2'
    # p1 = Line_Plane(normal_vector=[8.631, 5.112, -1.816], constant_term=-5.113)
    # p2 = Line_Plane(normal_vector=[4.315, 11.132, -5.27], constant_term=-6.775)
    # p3 = Line_Plane(normal_vector=[-2.158, 3.01, -1.727], constant_term=-0.831)
    # s = LinearSystem([p1, p2, p3])
    # r = s.compute_rref()
    # print r
    # c = s.compute_solution()
    # print c


    # print '\nexample 3'
    # p1 = Line_Plane(normal_vector=[5.262, 2.739, -9.878], constant_term=-3.441)
    # p2 = Line_Plane(normal_vector=[5.111, 6.358, 7.638], constant_term=-2.152)
    # p3 = Line_Plane(normal_vector=[2.016, -9.924, -1.367], constant_term=-9.278)
    # p4 = Line_Plane(normal_vector=[2.167, -13.543, -18.883], constant_term=-10.567)
    # s = LinearSystem([p1, p2, p3, p4])
    # r = s.compute_rref()
    # print r
    # c = s.compute_solution()
    # print c



# compute_rref(self)
# testing
# ---------------------------------------------------------
    # p1 = Line_Plane(normal_vector=[1,1,1], constant_term=1)
    # p2 = Line_Plane(normal_vector=[0,1,1], constant_term=2)
    # s = LinearSystem([p1,p2])
    # r = s.compute_rref()
    # print r

    # p1 = Line_Plane(normal_vector=[1,1,1], constant_term=1)
    # p2 = Line_Plane(normal_vector=[1,1,1], constant_term=2)
    # s = LinearSystem([p1,p2])
    # r = s.compute_rref()
    # print r

    # p1 = Line_Plane(normal_vector=[1,1,1], constant_term=1)
    # p2 = Line_Plane(normal_vector=[0,1,0], constant_term=2)
    # p3 = Line_Plane(normal_vector=[1,1,-1], constant_term=3)
    # p4 = Line_Plane(normal_vector=[1,0,-2], constant_term=2)
    # s = LinearSystem([p1,p2,p3,p4])
    # r = s.compute_rref()
    # print r

    # p1 = Line_Plane(normal_vector=[0,1,1], constant_term=1)
    # p2 = Line_Plane(normal_vector=[1,-1,1], constant_term=2)
    # p3 = Line_Plane(normal_vector=[1,2,-5], constant_term=3)
    # s = LinearSystem([p1,p2,p3])
    # r = s.compute_rref()
    # print r

# compute_triangular_form(self)
# testing 
# ---------------------------------------------------------
    # p1 = Line_Plane(normal_vector=[0,1,1], constant_term=1)
    # p2 = Line_Plane(normal_vector=[1,1,1], constant_term=2)
    # s = LinearSystem([p1,p2])
    # t = s.compute_triangular_form()
    # if not (t[0].is_equal(p1) and t[1].is_equal(p2)):
    #     print 'test case 1 failed'
    # print t

    # p1 = Line_Plane(normal_vector=[1,1,1], constant_term=1)
    # p2 = Line_Plane(normal_vector=[1,1,1], constant_term=2)
    # s = LinearSystem([p1,p2])
    # t = s.compute_triangular_form()
    # print t

    # p1 = Line_Plane(normal_vector=[1,1,1], constant_term=1)
    # p2 = Line_Plane(normal_vector=[0,1,0], constant_term=2)
    # p3 = Line_Plane(normal_vector=[1,1,-1], constant_term=3)
    # p4 = Line_Plane(normal_vector=[1,0,-2], constant_term=2)
    # s = LinearSystem([p1,p2,p3,p4])
    # t = s.compute_triangular_form()
    # print t

    # p1 = Line_Plane(normal_vector=[0,1,1], constant_term=1)
    # p2 = Line_Plane(normal_vector=[1,-1,1], constant_term=2)
    # p3 = Line_Plane(normal_vector=[1,2,-5], constant_term=3)
    # s = LinearSystem([p1,p2,p3])
    # t = s.compute_triangular_form()
    # print t

# swap_rows(self, row1, row2)
# multiply_coefficient_and_row(self, coefficient, row)
# add_multiple_times_row_to_row(self, coefficient, row_to_add, row_to_be_added_to)
# testing
# ---------------------------------------------------------

    # p0 = Line_Plane(normal_vector=[1, 1, 1], constant_term=1)
    # p1 = Line_Plane(normal_vector=[0, 1, 0], constant_term=2)
    # p2 = Line_Plane(normal_vector=[1,1, -1], constant_term=3)
    # p3 = Line_Plane(normal_vector=[1, 0, -2], constant_term=2)

    # s = LinearSystem([p0, p1, p2, p3])

    # s.swap_rows(0,1)
    # if not (s[0] == p1 and s[1] == p0 and s[2] == p2 and s[3] == p3):
    #     print 'test case 1 failed'

    # s.swap_rows(1,3)
    # if not (s[0] == p1 and s[1] == p3 and s[2] == p2 and s[3] == p0):
    #     print 'test case 2 failed'

    # s.swap_rows(3,1)
    # if not (s[0] == p1 and s[1] == p0 and s[2] == p2 and s[3] == p3):
    #     print 'test case 3 failed'


    # s.multiply_coefficient_and_row(1,0)
    # if not (s[0] == p1 and s[1] == p0 and s[2] == p2 and s[3] == p3):
    #     print 'test case 4 failed'

    # s.multiply_coefficient_and_row(-1,2)
    # if not (s[0] == p1 and
    #         s[1] == p0 and
    #         s[2] == Line_Plane(normal_vector = [-1,-1,1], constant_term = -3) and
    #         s[3] == p3):
    #     print 'test case 5 failed'
    #     print s

    # s.multiply_coefficient_and_row(10,1)
    # if not (s[0] == p1 and
    #         s[1] == Line_Plane(normal_vector = [10,10,10], constant_term = 10) and
    #         s[2] == Line_Plane(normal_vector = [-1,-1,1], constant_term = -3) and
    #         s[3] == p3):
    #     print 'test case 6 failed'
    #     print s

    # s.add_multiple_times_row_to_row(0,0,1)
    # if not (s[0] == p1 and
    #         s[1] == Line_Plane(normal_vector = [10,10,10], constant_term = 10) and
    #         s[2] == Line_Plane(normal_vector = [-1,-1,1], constant_term = -3) and
    #         s[3] == p3):
    #     print 'test case 7 failed'
    #     print s

    # s.add_multiple_times_row_to_row(1,0,1)
    # if not (s[0] == p1 and
    #         s[1] == Line_Plane(normal_vector = [10,11,10], constant_term = 12) and
    #         s[2] == Line_Plane(normal_vector = [-1,-1,1], constant_term = -3) and
    #         s[3] == p3):
    #     print 'test case 8 failed'
    #     print s

    # s.add_multiple_times_row_to_row(-1,1,0)
    # if not (s[0] == Line_Plane(normal_vector = [-10,-10,-10], constant_term = -10) and
    #         s[1] == Line_Plane(normal_vector = [10,11,10], constant_term = 12) and
    #         s[2] == Line_Plane(normal_vector = [-1,-1,1], constant_term = -3) and
    #         s[3] == p3):
    #     print 'test case 9 failed'
    #     print s


    # print '{},{},{},{}'.format(s[0], s[1], s[2], s[3])
    # print len(s)
    # print s

    # s[0] = p1
    # print s

    # print MyDecimal('1e-9').is_near_zero()
    # print MyDecimal('1e-11').is_near_zero()
