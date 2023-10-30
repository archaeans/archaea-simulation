import unittest
import os

from archaea.geometry.point3d import Point3d
from archaea_simulation.speckle.vtk_to_speckle import vtk_to_speckle


class Setup(unittest.TestLoader):
    path = os.path.join(os.getcwd(), 'test', 'speckle', 'U_cutPlane.vtk')

class TestDomain(unittest.TestCase):
    def test_vtk_to_speckle(self):
        # Arrange
        print(Setup.path)

        # Act
        vtk_to_speckle(Setup.path, Point3d.origin())
        