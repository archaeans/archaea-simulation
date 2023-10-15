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
from archaea_simulation.cfd.utils.snappyHexMeshDict import snappy_hex_mesh_geometry, snappy_hex_mesh_refinementSurfaces, snappy_hex_mesh_features
from archaea_simulation.cfd.utils.surfaceFeaturesDict import surface_features_entry
from archaea_simulation.cfd.utils.initialConditions import calculate_u_inlet

class Domain(Zone):
    center: Point3d
    ground: Face
    x: float
    y: float
    z: float
    wind_direction: float
    wind_speed: float
    zones: "list[Zone]"
    context: "list[Wall]"
    context_meshes: "list[Mesh]"
    openings: "list[Wall]"
    MIN_DOMAIN_SIZE = 10

    def __init__(self,
                 center: Point3d,
                 x: float,
                 y: float,
                 z: float,
                 wind_speed: float = 10,
                 wind_direction: float = 0,
                 zones=None,
                 context=None,
                 context_meshes=None):
        if context is None:
            self.context = []
        else:
            self.context = context
        if context_meshes is None:
            self.context_meshes = []
        else:
            self.context_meshes = context_meshes
        if zones is None:
            self.zones = []
        else:
            self.zones = zones
        self.center = center
        self.x = x
        self.y = y
        self.z = z
        self.wind_speed = wind_speed
        self.wind_direction = wind_direction
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
        domain.context_meshes = meshes
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
        self.export_domain_to_stl(trisurface_path)
        self.update_block_mesh_dict(case_folder_path)
        self.update_snappy_hex_mesh_dict(case_folder_path)
        self.update_surface_features_dict(case_folder_path)
        self.update_initial_conditions(case_folder_path)

    def update_initial_conditions(self, case_folder_path):
        u_file = os.path.join(case_folder_path, "0", "U")
        u_inlet = calculate_u_inlet(self.wind_direction, self.wind_speed)
        with fileinput.FileInput(u_file, inplace=True) as file:
                for line in file:
                    print(line.replace('// Uinlet to replace', u_inlet), end='')

    def update_surface_features_dict(self, case_folder_path):
        surface_features_dict_path = os.path.join(case_folder_path, "system", "surfaceFeaturesDict")
        if any(self.zones):
            zones_entry = surface_features_entry("zones")
            with fileinput.FileInput(surface_features_dict_path, inplace=True) as file:
                for line in file:
                    print(line.replace('// zones to replace', zones_entry), end='')
        if any(self.context_meshes):
            context_meshes_entry = surface_features_entry("context_meshes")
            with fileinput.FileInput(surface_features_dict_path, inplace=True) as file:
                for line in file:
                    print(line.replace('// context meshes to replace', context_meshes_entry), end='')

    def update_snappy_hex_mesh_dict(self, case_folder_path):
        """Snappy hex mesh dict defines which meshes will be considered
        while volume meshes creating.

        Args:
            case_folder_path: where dict file will be searched.
        """  # noqa: D205
        snappy_hex_mesh_dict_path = os.path.join(case_folder_path, "system", "snappyHexMeshDict")
        if any(self.zones):
            zones_entry = snappy_hex_mesh_geometry("zones", "zones")
            zones_features_entry = snappy_hex_mesh_features("zones", 1)
            zones_refinement_entry = snappy_hex_mesh_refinementSurfaces("zones")
            with fileinput.FileInput(snappy_hex_mesh_dict_path, inplace=True) as file:
                for line in file:
                    print(line.replace('// zones to replace', zones_entry), end='')
            with fileinput.FileInput(snappy_hex_mesh_dict_path, inplace=True) as file:
                for line in file:
                    print(line.replace('// zones features to replace', zones_features_entry), end='')
            with fileinput.FileInput(snappy_hex_mesh_dict_path, inplace=True) as file:
                for line in file:
                    print(line.replace('// zones refinementSurfaces to replace', zones_refinement_entry), end='')
        if any(self.context_meshes):
            context_meshes_entry = snappy_hex_mesh_geometry("context_meshes", "context_meshes")
            context_meshes_features_entry = snappy_hex_mesh_features("context_meshes", 1)
            context_meshes_refinement_entry = snappy_hex_mesh_refinementSurfaces("context_meshes")
            with fileinput.FileInput(snappy_hex_mesh_dict_path, inplace=True) as file:
                for line in file:
                    print(line.replace('// context meshes to replace', context_meshes_entry), end='')
            with fileinput.FileInput(snappy_hex_mesh_dict_path, inplace=True) as file:
                for line in file:
                    print(line.replace('// context meshes features to replace', context_meshes_features_entry), end='')
            with fileinput.FileInput(snappy_hex_mesh_dict_path, inplace=True) as file:
                for line in file:
                    print(line.replace('// context meshes refinementSurfaces to replace', context_meshes_refinement_entry), end='')
        

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
                   '({x7}\t{y7}\t{z7})\n    '.format(x0=-self.x/2 + self.center.x, y0=-self.y/2 + self.center.y, z0=0,
                                                     x1=self.x/2 + self.center.x, y1=-self.y/2 + self.center.y, z1=0,
                                                     x2=self.x/2 + self.center.x, y2=self.y/2 + self.center.y, z2=0,
                                                     x3=-self.x/2 + self.center.x, y3=self.y/2 + self.center.y, z3=0,
                                                     x4=-self.x/2 + self.center.x, y4=-self.y/2 + self.center.y, z4=self.z,
                                                     x5=self.x/2 + self.center.x, y5=-self.y/2 + self.center.y, z5=self.z,
                                                     x6=self.x/2 + self.center.x, y6=self.y/2 + self.center.y, z6=self.z,
                                                     x7=-self.x/2 + self.center.x, y7=self.y/2 + self.center.y, z7=self.z,
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
        self.export_zones_to_stl(path)
        self.export_inlet_to_stl(path)
        self.export_outlet_to_stl(path)
        self.export_sides_to_stl(path)
        self.export_all_to_single_stl(path)
        self.export_context_meshes_to_stl(path)

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
    
    def export_context_to_single_mesh(self):
        mesh = Mesh()
        for m in self.context_meshes:
            for p in m.polygons:
                mesh.add_polygon([m.vertices[p_index] for p_index in p])
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
        if any(self.context_meshes):
            for context_m in self.context_meshes:
                for polygon in context_m.polygons:
                    vertices = []
                    for index in polygon:
                        vertices.append(context_m.vertices[index])
                    mesh.add_polygon(vertices)
        mesh.to_stl(path, "combined")

    def export_zones_to_stl(self, path):
        if any(self.zones):
            mesh = Mesh()
            walls = self.create_context_faces()
            mesh.add_from_faces(walls)
            mesh.to_stl(path, "zones")

    def export_context_meshes_to_stl(self, path):
        if any(self.context_meshes):
            mesh = Mesh()
            for context_m in self.context_meshes:
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
