import unittest

from archaea.geometry.face import Face
from archaea.geometry.loop import Loop
from archaea.geometry.mesh import Mesh
from archaea.geometry.point3d import Point3d

from archaea_simulation.simulation_objects.domain import Domain
from archaea_simulation.simulation_objects.wall import Wall
from archaea_simulation.simulation_objects.wall_type import WallType
from archaea_simulation.simulation_objects.zone import Zone


class Setup(unittest.TestLoader):
    # ground loop1
    center = Point3d(0, 0, 0)
    # init domain
    domain = Domain(center, 50, 100, 50)

    # zone init
    p0 = Point3d(0, 0, 0)
    p1 = Point3d(4, 0, 0)
    p2 = Point3d(4, 4, 0)
    p3 = Point3d(0, 4, 0)

    ground_loop_1 = Loop([p0, p3, p2, p1])
    ground_face_1 = Face(ground_loop_1)
    ground_wall_1 = Wall(ground_face_1.outer_loop, ground_face_1.inner_loops, 
                         wall_type=WallType.INNER)

    zone_without_hole = Zone(ground_face_1, 3)
    zone = Zone(ground_face_1, 3)

    # outer wall
    p4 = Point3d(0, 0, 0)
    p5 = Point3d(4, 0, 0)
    p6 = Point3d(4, 0, 3)
    p7 = Point3d(0, 0, 3)

    # outer wall hole loop window
    p8 = Point3d(1, 0, 0.8)
    p9 = Point3d(3, 0, 0.8)
    p10 = Point3d(3, 0, 2.4)
    p11 = Point3d(1, 0, 2.4)

    # outer wall hole loop door
    p12 = Point3d(0.2, 4, 0.2)
    p13 = Point3d(1.2, 4, 0.2)
    p14 = Point3d(1.2, 4, 2.2)
    p15 = Point3d(0.2, 4, 2.2)

    outer_wall_hole_loop_window = Loop([p8, p11, p10, p9])
    outer_wall_hole_loop_door = Loop([p12, p13, p14, p15])
    outer_wall_loop = Loop([p4, p7, p6, p5])
    outer_wall_face = Face(outer_wall_loop, [outer_wall_hole_loop_window])

    outer_wall_with_opening = Wall(outer_wall_face.outer_loop, 
                                   outer_wall_face.inner_loops)

    zone.walls[3].add_opening(outer_wall_hole_loop_window)
    zone.walls[1].add_opening(outer_wall_hole_loop_door)


class TestDomain(unittest.TestCase):
    def test_domain_init(self):
        # Arrange
        mesh = Mesh()

        # Act
        Setup.domain.add_zone(Setup.zone)
        walls = Setup.domain.create_solid_faces()
        mesh.add_from_faces(walls)
        mesh.to_stl("", "test_domain_init")

    def test_domain_from_meshes(self):
        # Arrange
        mesh = Mesh()
        faces = Setup.zone_without_hole.create_solid_faces()
        for face in faces:
            mesh.add_polygon(face.outer_loop.points[:-1])

        # Act
        domain_mesh = Mesh()
        domain = Domain.from_meshes([mesh])
        # TODO: make sure exported correctly!
        # domain.export_context_meshes_to_stl("")
        walls = domain.create_solid_faces()
        domain_mesh.add_from_faces(walls)
        domain_mesh.to_stl("", "test_domain_from_meshes")

    def test_domain_from_meshes_with_bbox(self):
        # Arrange
        p0 = Point3d(2, 2, 0)
        p1 = Point3d(3, 1, 0)
        p2 = Point3d(6, 4, 0)
        p3 = Point3d(5, 5, 0)

        ground_loop_1 = Loop([p0, p3, p2, p1])
        ground_face_1 = Face(ground_loop_1)
        zone_without_hole = Zone(ground_face_1, 3)

        mesh = Mesh()
        faces = zone_without_hole.create_solid_faces()
        mesh.add_from_faces(faces)
        mesh.to_stl("", "test_domain_from_meshes_with_bbox_context")

        # Act
        domain_mesh = Mesh()
        domain = Domain.from_meshes([mesh])
        walls = domain.create_solid_faces()
        domain_mesh.add_from_faces(walls)
        domain_mesh.to_stl("", "test_domain_from_meshes_with_bbox")        
