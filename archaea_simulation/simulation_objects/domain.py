import fileinput
import itertools
import os
import shutil
import math
from distutils.dir_util import copy_tree as copytree
from pathlib import Path

from archaea.geometry.bounding_box import BoundingBox
from archaea.geometry.face import Face
from archaea.geometry.loop import Loop
from archaea.geometry.mesh import Mesh
from archaea.geometry.point3d import Point3d
from archaea.geometry.vector3d import Vector3d
from archaea.geometry.plane import Plane

from archaea_simulation.simulation_objects.wall import Wall
from archaea_simulation.simulation_objects.zone import Zone
from archaea_simulation.cfd.utils.snappyHexMeshDict import snappy_hex_mesh_geometry, snappy_hex_mesh_refinementSurfaces, snappy_hex_mesh_features, snappy_hex_mesh_refinementRegions
from archaea_simulation.cfd.utils.surfaceFeaturesDict import surface_features_entry
from archaea_simulation.cfd.utils.initialConditions import calculate_u_inlet
from archaea_simulation.cfd.utils.refinementBox import create_refinement_box_mesh
from archaea_simulation.cfd.utils.decomposition import hiearchical_coeffs 

class Domain(Zone):
    bbox: BoundingBox
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
    # refinement_meshes: "list[Mesh]"
    refinement_mesh: Mesh
    openings: "list[Wall]"
    MIN_DOMAIN_SIZE = 10
    x_scale: float
    y_scale: float
    z_scale: float

    def __init__(self,
                 center: Point3d,
                 x: float,
                 y: float,
                 z: float,
                 x_scale: float = 5,
                 y_scale: float = 5,
                 z_scale: float = 3,
                 wind_speed: float = 10,
                 wind_direction: float = 0,
                 zones=None,
                 context=None,
                 context_meshes=None,
                 refinement_mesh=None):
        self.refinement_meshes = []
        self.refinement_mesh = refinement_mesh
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
        self.x = x * x_scale
        self.y = y * y_scale
        self.z = z * z_scale
        self.x_scale = x_scale
        self.y_scale = y_scale
        self.z_scale = z_scale
        self.wind_speed = wind_speed
        self.wind_direction = wind_direction
        self.init_corners()
        ground = self.init_ground()
        super().__init__(ground, self.z, wall_default_thickness=0)
        self.ground = self.floor

    @classmethod
    def from_meshes(
        cls, 
        meshes: "list[Mesh]", 
        x_scale: float = 5, 
        y_scale: float = 5, 
        z_scale: float = 3, 
        wind_speed: float = 10,
        wind_direction: float = 15
        ):
        mesh_vertices = [mesh.vertices for mesh in meshes]
        vertices = list(itertools.chain.from_iterable(mesh_vertices))

        # Calculate the radians based on the given degree, we use different rotation for angles.
        radians = math.radians(-wind_direction)

        # Calculate the u and v vectors using trigonometry
        u_axis = Vector3d(math.cos(radians), math.sin(radians), 0)
        v_axis = Vector3d(-math.sin(radians), math.cos(radians), 0)

        plane = Plane(Point3d.origin(), u_axis, v_axis)
        bbox = BoundingBox.from_points_in_plane(vertices, plane)
        center = plane.point_at(bbox.center.x, bbox.center.y)
        refinement_mesh_level_1 = create_refinement_box_mesh(bbox, 1.5)
        x_dist = abs(bbox.max.x - bbox.min.x)
        y_dist = abs(bbox.max.y - bbox.min.y)
        z_dist = abs(bbox.max.z - bbox.min.z)
        domain = cls(
            Point3d(center.x, center.y, bbox.min.z),
            x_dist,
            y_dist,
            z_dist,
            x_scale=x_scale,
            y_scale=y_scale,
            z_scale=z_scale,
            wind_direction=wind_direction,
            wind_speed=wind_speed
            )
        domain.context_meshes = meshes
        domain.refinement_mesh = refinement_mesh_level_1
        return domain
    
    def init_corners(self):
        c = self.center
        v = Vector3d(0,0,1)
        self.p0 = c.move(Vector3d(self.x / 2 * -1, self.y / 2 * -1, 0)).rotate(v, self.wind_direction, c)  # left-bottom-floor
        self.p1 = c.move(Vector3d(self.x / 2, self.y / 2 * -1, 0)).rotate(v, self.wind_direction, c)  # right-bottom-floor
        self.p2 = c.move(Vector3d(self.x / 2, self.y / 2, 0)).rotate(v, self.wind_direction, c) # right-top-floor
        self.p3 = c.move(Vector3d(self.x / 2 * -1, self.y / 2, 0)).rotate(v, self.wind_direction, c)  # left-top-floor
        self.p4 = self.p0.move(Vector3d(0, 0, self.z))
        self.p5 = self.p1.move(Vector3d(0, 0, self.z))
        self.p6 = self.p2.move(Vector3d(0, 0, self.z))
        self.p7 = self.p3.move(Vector3d(0, 0, self.z))

    def init_ground(self) -> Face:
        ground_outer_loop = Loop([self.p0, self.p3, self.p2, self.p1])
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

    def create_case(self, case_folder_path, number_of_cores: int = 6):
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
        self.update_decompose_par_dict(case_folder_path, number_of_cores)
        self.update_block_mesh_dict(case_folder_path)
        self.update_snappy_hex_mesh_dict(case_folder_path)
        self.update_surface_features_dict(case_folder_path)
        self.update_initial_conditions(case_folder_path)
        self.update_cut_plane_surface(case_folder_path)

    def update_decompose_par_dict(self, case_folder_path, number_of_cores):
        decompose_par_dict_path = os.path.join(case_folder_path, "system", "decomposeParDict")
        hiearchical_coeffs_str = hiearchical_coeffs(number_of_cores)
        with fileinput.FileInput(decompose_par_dict_path, inplace=True) as file:
            for line in file:
                print(line.replace('// number of subdomains to replace', f'numberOfSubdomains {number_of_cores};'), end='')
        with fileinput.FileInput(decompose_par_dict_path, inplace=True) as file:
            for line in file:
                print(line.replace('// hierarchicalCoeffs to replace', hiearchical_coeffs_str), end='')

    def update_cut_plane_surface(self, case_folder_path):
        cut_plane_surface_dict_path = os.path.join(case_folder_path, "system", "cutPlaneSurface")
        cut_plane_surface_point = f'point       ({self.center.x} {self.center.y} 1.5);'
        with fileinput.FileInput(cut_plane_surface_dict_path, inplace=True) as file:
                for line in file:
                    print(line.replace('// point to replace', cut_plane_surface_point), end='')

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
        if self.refinement_mesh is not None:
            refinement_mesh_entry = surface_features_entry("refinement_mesh")
            with fileinput.FileInput(surface_features_dict_path, inplace=True) as file:
                for line in file:
                    print(line.replace('// refinement mesh to replace', refinement_mesh_entry), end='')

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
            zones_refinement_entry = snappy_hex_mesh_refinementSurfaces("zones", 3, 3)
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
            context_meshes_refinement_entry = snappy_hex_mesh_refinementSurfaces("context_meshes", 3, 3)
            with fileinput.FileInput(snappy_hex_mesh_dict_path, inplace=True) as file:
                for line in file:
                    print(line.replace('// context meshes to replace', context_meshes_entry), end='')
            with fileinput.FileInput(snappy_hex_mesh_dict_path, inplace=True) as file:
                for line in file:
                    print(line.replace('// context meshes features to replace', context_meshes_features_entry), end='')
            with fileinput.FileInput(snappy_hex_mesh_dict_path, inplace=True) as file:
                for line in file:
                    print(line.replace('// context meshes refinementSurfaces to replace', context_meshes_refinement_entry), end='')

        if self.refinement_mesh is not None:
            refinement_mesh_entry = snappy_hex_mesh_geometry("refinement_mesh", "refinement_mesh")
            refinement_mesh_features_entry = snappy_hex_mesh_features("refinement_mesh", 1)
            refinement_mesh_refinement_entry = snappy_hex_mesh_refinementRegions("refinement_mesh", 2)
            with fileinput.FileInput(snappy_hex_mesh_dict_path, inplace=True) as file:
                for line in file:
                    print(line.replace('// refinement mesh to replace', refinement_mesh_entry), end='')
            with fileinput.FileInput(snappy_hex_mesh_dict_path, inplace=True) as file:
                for line in file:
                    print(line.replace('// refinement mesh features to replace', refinement_mesh_features_entry), end='')
            with fileinput.FileInput(snappy_hex_mesh_dict_path, inplace=True) as file:
                for line in file:
                    print(line.replace('// refinement mesh refinementRegions to replace', refinement_mesh_refinement_entry), end='')

        in_mesh_point = self.p0.move(self.p0.vector_to(self.center).normalized())
        location_in_mesh = f'locationInMesh ({in_mesh_point.x} {in_mesh_point.y} {self.center.z + 1});'
        with fileinput.FileInput(snappy_hex_mesh_dict_path, inplace=True) as file:
            for line in file:
                print(line.replace('// location in mesh to replace', location_in_mesh), end='')

    def update_block_mesh_dict(self, case_folder_path):
        block_mesh_dict_path = os.path.join(case_folder_path, "system", "blockMeshDict")

        cells = 'x\t{x};\n    y\t{y};\n    z\t{z};'.format(x=int(self.x / 2), y=int(self.y / 2), z=int(self.z / 2))
        vertices = '({x0}\t{y0}\t{z0})\n    ' \
                   '({x1}\t{y1}\t{z1})\n    ' \
                   '({x2}\t{y2}\t{z2})\n    ' \
                   '({x3}\t{y3}\t{z3})\n    ' \
                   '({x4}\t{y4}\t{z4})\n    ' \
                   '({x5}\t{y5}\t{z5})\n    ' \
                   '({x6}\t{y6}\t{z6})\n    ' \
                   '({x7}\t{y7}\t{z7})\n    '.format(x0=self.p0.x, y0=self.p0.y, z0=self.p0.z,
                                                     x1=self.p1.x, y1=self.p1.y, z1=self.p1.z,
                                                     x2=self.p2.x, y2=self.p2.y, z2=self.p2.z,
                                                     x3=self.p3.x, y3=self.p3.y, z3=self.p3.z,
                                                     x4=self.p4.x, y4=self.p4.y, z4=self.p4.z,
                                                     x5=self.p5.x, y5=self.p5.y, z5=self.p5.z,
                                                     x6=self.p6.x, y6=self.p6.y, z6=self.p6.z,
                                                     x7=self.p7.x, y7=self.p7.y, z7=self.p7.z
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
        self.export_refinement_meshes_to_stl(path)

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
    
    def export_refinement_meshes_to_stl(self, path):
        # TODO: When we have multiple refinement box
        # if any(self.refinement_meshes):
        #     for refinement_m in self.refinement_meshes:
        #         refinement_m.to_stl(path, "refinement")
        if self.refinement_mesh is not None:
            self.refinement_mesh.to_stl(path, "refinement_mesh")

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
