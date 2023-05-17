from archaea.geometry.point3d import Point3d
from archaea.geometry.loop import Loop
from archaea.geometry.line_segment import LineSegment
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
        # self.create_block_zones(x_center_distance_first_room, y_shift, zones)
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

        # NOTE: If we want to open ground of storey 1, we should change wall_type to wall_type=WallType.INNER
        ground_wall = Wall(ground_loop_1, [], wall_type=WallType.OUTER)
        ceiling_wall = Wall(ground_loop_1.move(Vector3d(0, 0, self.room_height)).reverse(), [], wall_type=WallType.OUTER)

        window_wall = self.create_window_wall(p0, p3)

        door_wall = self.create_door_wall(p2, p1)

        side_wall_1_type = WallType.OUTER
        if is_start and not is_end:
            side_wall_1_type = WallType.INNER

        side_wall_2_type = WallType.OUTER
        if is_end and not is_start:
            side_wall_2_type = WallType.INNER

        if not is_start and not is_end:
            side_wall_1_type = WallType.INNER
            side_wall_2_type = WallType.INNER

        side_wall_line_1 = LineSegment(p3, p2)
        side_wall_loop_1 = side_wall_line_1.extrude(Vector3d(0, 0, self.room_height))
        side_wall_1 = Wall(side_wall_loop_1.outer_loop, [], wall_type=side_wall_1_type)

        side_wall_line_2 = LineSegment(p1, p0)
        side_wall_loop_2 = side_wall_line_2.extrude(Vector3d(0, 0, self.room_height))
        side_wall_2 = Wall(side_wall_loop_2.outer_loop, [], wall_type=side_wall_2_type)

        zone = Zone(
            ground_face_1,
            self.room_height,
            walls=[window_wall, door_wall, side_wall_1, side_wall_2],
            wall_default_thickness=self.room_wall_thickness
        )
        # zone = Zone(ground_face_1, self.room_height, wall_default_thickness=self.room_wall_thickness)
        return zone

    def create_window_wall(self, p_start: Point3d, p_end: Point3d):
        window_sill_height = 0.9

        window_wall_line = LineSegment(p_start, p_end)

        moved_wall_line = window_wall_line.move(Vector3d(0, 0, window_sill_height))
        window_start_point = moved_wall_line.point_at(0.4)
        window_end_point = moved_wall_line.point_at(0.6)
        window_line = LineSegment(window_start_point, window_end_point)
        window_loop = window_line.extrude(Vector3d(0, 0, self.room_window_height))

        wall_width = window_wall_line.length
        width_ratio = (self.room_width - self.room_window_width) / self.room_window_width

        window_wall_loop = window_wall_line.extrude(Vector3d(0, 0, self.room_height))
        window_wall = Wall(window_wall_loop.outer_loop, [window_loop.outer_loop], wall_type=WallType.OUTER)

        return window_wall

    def create_door_wall(self, p_start: Point3d, p_end: Point3d):
        door_sill_height = 0.2

        door_wall_line = LineSegment(p_start, p_end)

        moved_wall_line = door_wall_line.move(Vector3d(0, 0, door_sill_height))
        door_start_point = moved_wall_line.point_at(0.1)
        door_end_point = moved_wall_line.point_at(0.32)
        door_line = LineSegment(door_start_point, door_end_point)
        door_loop = door_line.extrude(Vector3d(0, 0, self.room_door_height))

        wall_width = door_wall_line.length
        width_ratio = (self.room_width - self.room_window_width) / self.room_window_width

        door_wall_loop = door_wall_line.extrude(Vector3d(0, 0, self.room_height))
        door_wall = Wall(door_wall_loop.outer_loop, [door_loop.outer_loop], wall_type=WallType.OUTER)

        return door_wall

