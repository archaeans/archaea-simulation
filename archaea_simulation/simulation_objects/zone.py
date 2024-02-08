from archaea.geometry.face import Face
from archaea.geometry.vector3d import Vector3d
from archaea_simulation.simulation_objects.wall import Wall
from archaea_simulation.simulation_objects.wall_type import WallType
from archaea_simulation.simulation_objects.thermal_zone import ThermalZone

from honeybee.facetype import Wall as HB_WallType
from honeybee.facetype import Floor as HB_FloorType
from honeybee.facetype import RoofCeiling as HB_RoofCeilingType
from honeybee.boundarycondition import Outdoors as HB_OutdoorsCondition
from honeybee.boundarycondition import Ground as HB_GroundCondition
from honeybee.room import Room as HB_Room
from honeybee.aperture import Aperture as HB_Aperture
from honeybee.face import Face as HB_Face
from honeybee.face import Face3D as HB_Face3D
from honeybee.face import Plane as HB_Plane

from ladybug_geometry.geometry3d.pointvector import Point3D as LB_Point3D


class Zone:
    floor: Wall
    ceiling: Wall
    walls: "list[Wall]"
    height: float
    volume: float
    wall_default_thickness: float
    openings: "list[Face]"

    def __init__(self, floor: Face, height, walls=None, wall_default_thickness=0.1):
        self.floor = Wall(floor.outer_loop, floor.inner_loops)
        self.floor.update_wall_type(WallType.OUTER)
        self.height = height
        self.wall_default_thickness = wall_default_thickness
        self.volume = self.floor.area * height
        move_vector = Vector3d(0, 0, self.height)
        self.ceiling = self.floor.move(move_vector).reverse() 
        if walls is None:
            self.create_walls(move_vector)
        else:
            self.walls = walls

    def create_walls(self, move_vector):
        wall_lines = self.floor.outer_loop.segments
        walls = []
        for line in wall_lines:
            border: Face = line.extrude(move_vector)
            wall = Wall(border.outer_loop, border.inner_loops)
            walls.append(wall)
        self.walls = walls

    def all_surfaces(self):
        all_surfaces = self.walls.copy()
        all_surfaces.append(self.floor.reverse())
        all_surfaces.append(self.ceiling.reverse())
        return all_surfaces
    
    def has_opening(self):
        return True in [any(wall.openings) for wall in self.walls]

    def create_solid_faces(self) -> "list[Face]":
        faces = []
        for wall in self.all_surfaces():
            faces += wall.create_solid_faces(self.has_opening())
        return faces
    
    def rotate(self, axis, angle, origin=None):
        rotated_floor = self.floor.rotate(axis, angle, origin)
        rotated_walls = [wall.rotate(axis, angle, origin) for wall in self.walls]
        return Zone(rotated_floor, self.height, rotated_walls, self.wall_default_thickness)

    def convert_to_thermal_zone(self, identifier: str):
        HB_faces = []
        HB_floor3d = HB_Face3D([LB_Point3D(p.x, p.y, p.z) for p in self.floor.outer_loop.points])
        HB_floor = HB_Face("{id}_{face_name}".format(id=identifier, face_name="floor"), HB_floor3d, HB_FloorType(), HB_GroundCondition())
        HB_faces.append(HB_floor)
        HB_ceiling3d = HB_Face3D([LB_Point3D(p.x, p.y, p.z) for p in self.ceiling.outer_loop.points])
        HB_ceiling = HB_Face("{id}_{face_name}".format(id=identifier, face_name="ceiling"), HB_ceiling3d, HB_RoofCeilingType(), HB_OutdoorsCondition())
        HB_faces.append(HB_ceiling)
        for i, wall in enumerate(self.walls):
            HB_wall3d = HB_Face3D([LB_Point3D(p.x, p.y, p.z) for p in wall.outer_loop.points])
            wall_id = "{id}_{face_name}_{wall_id}".format(id=identifier, face_name="wall", wall_id=i)
            HB_wall = HB_Face(wall_id, HB_wall3d, HB_WallType(), HB_OutdoorsCondition())
            if wall.has_opening:
                for j, opening in enumerate(wall.openings):
                    HB_opening3d = HB_Face3D([LB_Point3D(p.x, p.y, p.z) for p in opening.points])
                    HB_opening = HB_Aperture("{wall_id}_{opening_id}".format(wall_id=wall_id, opening_id=j), HB_opening3d, HB_OutdoorsCondition())
                    HB_wall.add_aperture(HB_opening)
            HB_faces.append(HB_wall)
        return ThermalZone(identifier, HB_faces)