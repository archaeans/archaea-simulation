from archaea.geometry.point3d import Point3d
from archaea.geometry.loop import Loop
from archaea.geometry.face import Face
from archaea.geometry.vector3d import Vector3d
from archaea_simulation.simulation_objects.zone import Zone
from archaea_simulation.simulation_objects.wall import Wall
from archaea_simulation.simulation_objects.wall_type import WallType


class CourtyardBuilding:
    zones: "list[Zone]"


    def __init__(self,
                 center: Point3d,
                 number_of_storeys: int,
                 number_of_rooms: int,
                 courtyard_width: float,
                 room_width: float,
                 room_depth: float,
                 room_height: float,
                 room_wall_thickness: float,
                 room_window_existence: bool,
                 room_window_width: float,
                 room_window_height: float,
                 room_door_existence: bool,
                 room_door_width: float,
                 room_door_height: float,
                 ):
        self.center = center
        self.number_of_storeys = number_of_storeys
        self.number_of_rooms = number_of_rooms
        self.courtyard_width = courtyard_width
        self.room_width = room_width
        self.room_depth = room_depth
        self.room_height = room_height
        self.room_wall_thickness = room_wall_thickness
        self.room_window_existence = room_window_existence
        self.room_window_width = room_window_width
        self.room_window_height = room_window_height
        self.room_door_existence = room_door_existence
        self.room_door_width = room_door_width
        self.room_door_height = room_door_height
        self.create_zones()

    def create_zones(self):
        c = self.center
        building_block_width = self.number_of_rooms * self.room_width
        x_center_distance_first_room = building_block_width / 2
        y_shift = self.courtyard_width / 2

        zones = []
        self.create_block_zones(x_center_distance_first_room, y_shift, zones)
        self.create_block_zones(x_center_distance_first_room, -y_shift - self.room_depth, zones)
        self.zones = zones

    def create_block_zones(self, x_center_distance_first_room, y_shift, zones):
        for i in range(self.number_of_rooms):
            x_shift = x_center_distance_first_room - (i * self.room_width)
            zone = self.create_zone(x_shift, y_shift, i == 0, i == self.number_of_rooms - 1)
            zones.append(zone)

    def create_zone(self, x_shift, y_shift, is_start, is_end):
        c = self.center
        p0 = Point3d(c.x + x_shift, c.y + y_shift, c.z)
        p1 = Point3d(c.x + x_shift, c.y + y_shift + self.room_depth, c.z)
        p2 = Point3d(c.x + x_shift - self.room_width, c.y + y_shift + self.room_depth, c.z)
        p3 = Point3d(c.x + x_shift - self.room_width, c.y + y_shift, c.z)
        ground_loop_1 = Loop([p0, p3, p2, p1])
        ground_face_1 = Face(ground_loop_1)
        ground_wall = Wall(ground_loop_1, [], wall_type=WallType.INNER)
        ceiling_wall = Wall(ground_loop_1.move(Vector3d(0, 0, self.room_height)).reverse(), [], wall_type=WallType.OUTER)

        # zone = Zone(ground_face_1, self.room_height, walls=[ground_wall, ceiling_wall], wall_default_thickness=self.room_wall_thickness)
        zone = Zone(ground_face_1, self.room_height, wall_default_thickness=self.room_wall_thickness)
        return zone

    def create_window_wall(self, p_start: Point3d, p_end: Point3d):
        window_sill_height = 0.9
        wall_width = p_start.distance_to(p_end)
        width_ratio = (self.room_width - self.room_window_width) / self.room_window_width
        p_end_top = p_end.move(Vector3d(0, 0, self.room_height))
        p_start_top = p_start.move(Vector3d(0, 0, self.room_height))
        wall_outer_loop = Loop([p_start, p_end, p_end_top, p_start_top])

