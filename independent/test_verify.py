"""Focused exact identities, input guards and counterexamples to wrong formulas."""
from fractions import Fraction as Q
from itertools import product
import sys
import unittest

import verify as v


class InputGuards(unittest.TestCase):
    def test_nonsquare_matrix(self):
        with self.assertRaises(v.VerificationError):
            v.matrix([[1, 0], [0]])

    def test_empty_matrix(self):
        with self.assertRaises(v.VerificationError):
            v.matrix([])

    def test_float_entries(self):
        with self.assertRaises(v.VerificationError):
            v.matrix([[0.5, 0.5], [0.5, 0.5]])

    def test_boolean_entries(self):
        with self.assertRaises(v.VerificationError):
            v.matrix([[True, False], [False, True]])

    def test_zero_denominator(self):
        with self.assertRaises(v.VerificationError):
            v.matrix([["1/0"]])

    def test_nan_rational(self):
        with self.assertRaises(v.VerificationError):
            v.matrix([["NaN"]])

    def test_signed_row_and_column_stochastic(self):
        with self.assertRaises(v.VerificationError):
            v.stochastic(v.matrix([[2, -1], [-1, 2]]))

    def test_row_stochastic_only(self):
        with self.assertRaises(v.VerificationError):
            v.stochastic(v.matrix([[1, 0], [1, 0]]))

    def test_wrong_row_sums(self):
        with self.assertRaises(v.VerificationError):
            v.stochastic(v.matrix([[1, 1], [0, 0]]))

    def test_duplicate_partition_label(self):
        with self.assertRaises(v.VerificationError):
            v.exceptional(3, ((0, 1), (1,)), (0, 1))

    def test_missing_partition_label(self):
        with self.assertRaises(v.VerificationError):
            v.exceptional(3, ((0,), (2,)), (0, 1))

    def test_empty_partition_class(self):
        with self.assertRaises(v.VerificationError):
            v.exceptional(2, ((0, 1), ()), (0, 1))

    def test_boolean_partition_label(self):
        with self.assertRaises(v.VerificationError):
            v.exceptional(2, ((False,), (1,)), (0, 1))

    def test_out_of_range_class_image(self):
        with self.assertRaises(v.VerificationError):
            v.exceptional(2, ((0,), (1,)), (0, 99))

    def test_duplicate_class_image(self):
        with self.assertRaises(v.VerificationError):
            v.exceptional(2, ((0,), (1,)), (0, 0))

    def test_unequal_class_interchange(self):
        with self.assertRaises(v.VerificationError):
            v.exceptional(3, ((0,), (1, 2)), (1, 0))

    def test_negative_power(self):
        with self.assertRaises(v.VerificationError):
            v.power(v.identity(2), -1)

    def test_noninteger_power(self):
        for exponent in (True, 2.0, Q(2)):
            with self.subTest(exponent=exponent), self.assertRaises(v.VerificationError):
                v.power(v.identity(2), exponent)

    def test_wrong_occupancy_normalization(self):
        F, E, p = v.exceptional(3, ((0, 1), (2,)), (0, 1))
        M = v.multiply(E, v.fixture_target(3))
        with self.assertRaises(v.VerificationError):
            v.validate_occupancy(M, E, ((0, 1), (2,)), 2 * p)

    def test_nonaveraged_occupancy_input(self):
        _, E, p = v.exceptional(3, ((0, 1), (2,)), (0, 1))
        with self.assertRaises(v.VerificationError):
            v.validate_occupancy(v.identity(3), E, ((0, 1), (2,)), p)

    def test_local_radius_guard(self):
        with self.assertRaises(v.VerificationError):
            v.audit_local(3, ((0, 1), (2,)), (0, 1), eta=Q(1, 4))

    def test_invalid_mixing_parameter(self):
        for eta in (Q(-1), Q(2)):
            with self.subTest(eta=eta), self.assertRaises(v.VerificationError):
                v.audit_fixture(2, ((0,), (1,)), (0, 1), eta=eta)


class ExactIdentities(unittest.TestCase):
    def test_three_permanent_algorithms_on_all_binary_three_by_three_matrices(self):
        for entries in product(range(2), repeat=9):
            A = v.matrix([entries[0:3], entries[3:6], entries[6:9]])
            values = (v.permanent_dp(A), v.permanent_permutations(A), v.permanent_ryser(A))
            self.assertEqual(len(set(values)), 1)

    def test_empty_permanent_convention(self):
        self.assertEqual(v.checked_permanent(()), 1)

    def test_exceptional_enumeration(self):
        for n, expected in ((2, 3), (3, 10), (4, 47)):
            parameters = list(v.exceptional_parameters(n))
            self.assertEqual(len(parameters), expected)
            self.assertEqual(len({v.exceptional(n, C, pi)[0] for C, pi in parameters}), expected)

    def test_period_two_exception_is_not_idempotent(self):
        F, E, p = v.exceptional(4, ((0, 1), (2, 3)), (1, 0))
        self.assertNotEqual(F, E)
        self.assertEqual(v.power(F, 2), E)
        self.assertEqual(v.power(F, 3), F)
        self.assertEqual(v.checked_permanent(F), p)

    def test_noncommuting_power_derivatives(self):
        A = v.fixture_target(3)
        X = v.matrix([[1, -1, 0], [0, 1, -1], [-1, 0, 1]])
        # Add an asymmetric zero-row/column-sum direction to avoid a circulant test.
        X = v.add(X, v.matrix([[1, -1, 0], [-1, 1, 0], [0, 0, 0]]))
        self.assertNotEqual(v.multiply(A, X), v.multiply(X, A))
        for k in (0, 1, 2, 3, 5, 8):
            binary = v.power_derivative_binary(A, X, k)
            self.assertEqual(binary, v.power_derivative_sequential(A, X, k))
            self.assertEqual(binary[0], v.power(A, k))
        _, D2 = v.power_derivative_binary(A, X, 2)
        self.assertNotEqual(D2, v.scale(Q(2), v.multiply(A, X)))

    def test_tangent_hessian_uses_factor_two(self):
        F = v.uniform(2)
        Y = v.matrix([[1, -1], [-1, 1]])
        coefficients = v.permanent_coefficients(F, Y)
        self.assertEqual(coefficients, (Q(1, 2), Q(0), Q(2)))
        self.assertEqual(v.permanent_hessian(F, Y), 4)

    def test_fixture_noncommuting_projection(self):
        result = v.audit_fixture(3, ((0, 1), (2,)), (0, 1))
        self.assertTrue(result["noncommutes_with_E"])
        self.assertGreater(result["delta"], 0)

    def test_delta_zero_tangent_endpoint(self):
        result = v.audit_fixture(3, ((0, 1, 2),), (0,))
        self.assertEqual(result["delta"], 0)
        self.assertGreater(result["tangent_squared"], 0)
        self.assertEqual(result["leakage_component_squared"], 0)

    def test_permutation_endpoint_no_tangent(self):
        result = v.audit_fixture(3, ((0,), (1,), (2,)), (1, 2, 0))
        self.assertEqual(result["tangent_squared"], 0)
        self.assertGreater(result["delta"], 0)

    def test_attributed_counterexample(self):
        result = v.known_counterexample()
        self.assertEqual(result["increase"], Q(1, 64))
        self.assertGreater(result["permanent_of_square"], result["permanent"])

    def test_dimension_two_sharp_constant(self):
        result = v.dimension_two_stability()
        self.assertEqual(result["stability_constant"], Q(3, 8))
        sharp = [r for r in result["records"] if r["t"] == Q(1, 2) and r["k"] == 2][0]
        self.assertEqual(sharp["gap"], Q(3, 32))
        self.assertEqual(sharp["distance_squared"], Q(1, 4))

    def test_stress_fixture_period_and_noncommutation(self):
        A = v.stress_matrix()
        F, E, _ = v.exceptional(4, ((0, 1), (2, 3)), (1, 0))
        self.assertNotEqual(v.multiply(F, A), v.multiply(A, F))
        self.assertNotEqual(v.multiply(E, A), v.multiply(A, E))
        self.assertLess(v.norm_squared(v.subtract(A, F)), Q(1, 32768) ** 2)

    def test_exact_large_rational_serialization_restores_process_limit(self):
        old = sys.get_int_max_str_digits() if hasattr(sys, "get_int_max_str_digits") else None
        text = v.serialize_report({"value": Q(10 ** 5000 + 1, 3)})
        self.assertIn("/3", text)
        if old is not None:
            self.assertEqual(sys.get_int_max_str_digits(), old)


if __name__ == "__main__":
    unittest.main()
