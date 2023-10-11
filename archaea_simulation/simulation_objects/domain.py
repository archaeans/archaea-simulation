import fileinput
import itertools
import os
import shutil
from distutils.dir_util import copy_tree as copytree
from pathlib import Path

from archaea.geometry.bounding_box import BoundingBox
from archaea.geometry.face import Face
from archaea.geometry.loop import Loop
from archaea.geometry.mesh import Mesh
from archaea.geometry.point3d import Point3d
from archaea.geometry.vector3d import Vector3d

from archaea_simulation.simulation_objects.wall import Wall
from archaea_simulation.simulation_objects.zone import Zone


class Domain(Zone):
    center: Point3d
    ground: Face
    x: float
    y: float
    z: float
    zones: "list[Zone]"
    context: "list[Wall]"
    context_mesh: "list[Mesh]"
    openings: "list[Wall]"
    MIN_DOMAIN_SIZE = 10

    def __init__(self,
                 center: Point3d,
                 x: float,
                 y: float,
                 z: float,
                 zones=None,
                 context=None):
        if context is None:
            context = []
        if zones is None:
            zones = []
        self.center = center
        self.x = x
        self.y = y
        self.z = z
        self.zones = zones
        self.context = context
        ground = self.init_ground()
        super().__init__(ground, self.z, wall_default_thickness=0)
        self.ground = self.floor

    @classmethod
    def from_meshes(cls, meshes: "list[Mesh]"):
        mesh_vertices = [mesh.vertices for mesh in meshes]
        vertices = list(itertools.chain.from_iterable(mesh_vertices))
        bbox = BoundingBox.from_points(vertices)
        x_dist = abs(bbox.max.x - bbox.min.x)
        y_dist = abs(bbox.max.y - bbox.min.y)
        z_dist = abs(bbox.max.z - bbox.min.z)
        domain = cls(Point3d(bbox.center.x, bbox.center.y, bbox.min.z), x_dist * 5, y_dist * 5, z_dist * 3)
        domain.context_mesh = meshes
        return domain

    def init_ground(self) -> Face:
        c = self.center
        ground_outer_loop = Loop([
            c.move(Vector3d(self.x / 2 * -1, self.y / 2 * -1, 0)),  # left-bottom
            c.move(Vector3d(self.x / 2 * -1, self.y / 2, 0)),  # left-top
            c.move(Vector3d(self.x / 2, self.y / 2, 0)),  # right-top
            c.move(Vector3d(self.x / 2, self.y / 2 * -1, 0)),  # right-bottom
        ])
        ground_inner_loops = [zone.floor.wall_border for zone in self.zones if zone.floor.wall_border.normal.z == 0]
        ground = Face(ground_outer_loop, ground_inner_loops)
        return ground

    def add_zone(self, zone: Zone):
        self.zones.append(zone)
        if zone.floor.wall_border.point_at_start.z == 0:
            self.floor.add_opening(zone.floor.wall_border.reverse())

    def create_solid_faces(self):
        return self.domain_faces() + self.domain_zone_faces()

    def domain_zone_faces(self):
        faces = []
        for zone in self.zones:
            faces += zone.create_solid_faces()

        return faces

    def domain_faces(self):
        faces = [self.floor.reverse(), self.ceiling.reverse()]
        faces += self.walls
        return faces

    def create_context_faces(self):
        faces = []
        for zone in self.zones:
            faces += zone.create_solid_faces()

        return faces

    def create_case(self, case_folder_path):
        if os.path.exists(case_folder_path):
            # Remove folder and files if any
            shutil.rmtree(case_folder_path)
        # Create file from scratch
        os.mkdir(case_folder_path)
        # Copy boilerplate case
        boilerplate_case = os.path.join(Path(__file__).resolve().parents[1], 'cfd/case')
        copytree(boilerplate_case, case_folder_path)
        # Create path to create stl files
        trisurface_path = os.path.join(case_folder_path, "constant", "triSurface")
        self.update_block_mesh_dict(case_folder_path)

        self.export_domain_to_stl(trisurface_path)

    def update_block_mesh_dict(self, case_folder_path):
        block_mesh_dict_path = os.path.join(case_folder_path, "system", "blockMeshDict")

        cells = 'x\t{x};\n    y\t{y};\n    z\t{z};'.format(x=int(self.x), y=int(self.y), z=int(self.z))
        vertices = '({x0}\t{y0}\t{z0})\n    ' \
                   '({x1}\t{y1}\t{z1})\n    ' \
                   '({x2}\t{y2}\t{z2})\n    ' \
                   '({x3}\t{y3}\t{z3})\n    ' \
                   '({x4}\t{y4}\t{z4})\n    ' \
                   '({x5}\t{y5}\t{z5})\n    ' \
                   '({x6}\t{y6}\t{z6})\n    ' \
                   '({x7}\t{y7}\t{z7})\n    '.format(x0=-self.x/2, y0=-self.y/2, z0=0,
                                                     x1=self.x/2, y1=-self.y/2, z1=0,
                                                     x2=self.x/2, y2=self.y/2, z2=0,
                                                     x3=-self.x/2, y3=self.y/2, z3=0,
                                                     x4=-self.x/2, y4=-self.y/2, z4=self.z,
                                                     x5=self.x/2, y5=-self.y/2, z5=self.z,
                                                     x6=self.x/2, y6=self.y/2, z6=self.z,
                                                     x7=-self.x/2, y7=self.y/2, z7=self.z,
                                                     )

        with fileinput.FileInput(block_mesh_dict_path, inplace=True) as file:
            for line in file:
                print(line.replace('// cells to replace', cells), end='')
        with fileinput.FileInput(block_mesh_dict_path, inplace=True) as file:
            for line in file:
                print(line.replace('// vertices to replace', vertices), end='')

    def export_domain_to_stl(self, path):
        if not os.path.exists(path):
            os.makedirs(path)
        self.export_context_to_stl(path)
        self.export_inlet_to_stl(path)
        self.export_outlet_to_stl(path)
        self.export_sides_to_stl(path)
        self.export_all_to_single_stl(path)

    def export_domain_to_single_mesh(self):
        mesh = Mesh()
        walls = self.domain_faces()
        mesh.add_from_faces(walls)
        return mesh

    def export_domain_ground_single_mesh(self):
        mesh = Mesh()
        mesh.add_from_faces([self.floor.reverse()])
        return mesh

    def export_zones_to_single_mesh(self):
        mesh = Mesh()
        walls = self.domain_zone_faces()
        mesh.add_from_faces(walls, False)
        return mesh

    def export_all_to_single_mesh(self):
        mesh = Mesh()
        walls = self.create_solid_faces()
        mesh.add_from_faces(walls)
        return mesh

    def export_all_to_single_stl(self, path):
        mesh = Mesh()
        walls = self.create_solid_faces()
        mesh.add_from_faces(walls)
        mesh.to_stl(path, "combined")

    def export_context_to_stl(self, path):
        mesh = Mesh()
        walls = self.create_context_faces()
        mesh.add_from_faces(walls)
        mesh.to_stl(path, "context")

    def export_context_meshes_to_stl(self, path):
        mesh = Mesh()
        for context_m in self.context_mesh:
            for polygon in context_m.polygons:
                vertices = []
                for index in polygon:
                    vertices.append(context_m.vertices[index])
                mesh.add_polygon(vertices)
        mesh.to_stl(path, "context_meshes")

    def export_inlet_to_stl(self, path):
        mesh = Mesh()
        mesh.add_from_faces([self.walls[3]])
        mesh.to_stl(path, "inlet")

    def export_outlet_to_stl(self, path):
        mesh = Mesh()
        mesh.add_from_faces([self.walls[1]])
        mesh.to_stl(path, "outlet")

    def export_sides_to_stl(self, path):
        mesh = Mesh()
        mesh.add_from_faces([self.walls[0], self.walls[2], self.floor.reverse(), self.ceiling.reverse()])
        mesh.to_stl(path, "sides")

