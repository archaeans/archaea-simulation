import unittest

from archaea_simulation.cfd.utils.initialConditions import calculate_u_inlet

class TestInitialConditions(unittest.TestCase):
    def test_calculate_u_inlet_0(self):
          # Act
          u_x, u_y = calculate_u_inlet(0, 1)

          # Assert
          self.assertAlmostEqual(u_x, 0)
          self.assertAlmostEqual(u_y, -1)
    
    def test_calculate_u_inlet_90(self):
          # Act
          u_x, u_y = calculate_u_inlet(90, 1)

          # Assert
          self.assertAlmostEqual(u_x, -1)
          self.assertAlmostEqual(u_y, 0)
    
    def test_calculate_u_inlet_180(self):
          # Act
          u_x, u_y = calculate_u_inlet(180, 1)

          # Assert
          self.assertAlmostEqual(u_x, 0)
          self.assertAlmostEqual(u_y, 1)

    def test_calculate_u_inlet_270(self):
          # Act
          u_x, u_y = calculate_u_inlet(270, 1)

          # Assert
          self.assertAlmostEqual(u_x, 1)
          self.assertAlmostEqual(u_y, 0)