import unittest

from archaea_simulation.cfd.utils.decomposition import distribute_cores

class TestDecomposition(unittest.TestCase):
    def test_decomposition_14(self):
        # Act
        x, y, z = distribute_cores(14)

        # Assert
        self.assertEqual(x, 2)
        self.assertEqual(y, 1)
        self.assertEqual(z, 7)

    def test_decomposition_16(self):
        # Act
        x, y, z = distribute_cores(16)

        # Assert
        self.assertEqual(x, 4)
        self.assertEqual(y, 2)
        self.assertEqual(z, 2)

    def test_decomposition_17(self):
        # Act
        x, y, z = distribute_cores(17)

        # Assert
        self.assertEqual(x, 1)
        self.assertEqual(y, 1)
        self.assertEqual(z, 17)