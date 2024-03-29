import functools
from archaea.geometry.face import Face
from archaea.geometry.loop import Loop
from archaea_simulation.simulation_objects.wall_type import WallType


class Wall(Face):
    wall_border: Loop
    openings: "list[Loop]"
    wall_type: WallType
    has_opening: bool
    thickness: float

    def __init__(self, border: Loop, openings: "list[Loop]", wall_type: WallType = WallType.OUTER, thickness=0.1):
        super().__init__(border, inner_loops=openings)
        self.wall_border = self.outer_loop
        self.openings = self.inner_loops
        self.wall_type = wall_type
        self.has_opening = len(self.openings) > 0
        self.thickness = thickness

    def create_solid_faces(self, include_inner_offset: bool):
        faces = []
        if self.wall_type == WallType.OUTER:
            faces.append(self)
            if not include_inner_offset:
                return faces
        inner_wall = self.offset(self.thickness).move(self.plane.normal.scale(self.thickness * -1))
        faces.append(inner_wall)
        for inner_loop in self.inner_loops:
            hole_depth_faces = inner_loop.extrude(self.thickness, True)
            faces += hole_depth_faces
        return faces

    def update_wall_type(self, wall_type: WallType):
        self.wall_type = wall_type

    def add_opening(self, opening: Loop):
        self.inner_loops.append(opening)

    def reverse(self):
        reversed_outer_loop = self.outer_loop.reverse()
        reversed_inner_loops = [loop.reverse() for loop in self.inner_loops]
        return Wall(reversed_outer_loop, reversed_inner_loops, self.wall_type, self.thickness)
    
    def rotate(self, axis, angle, origin=None):
        rotated_border_points = [p.rotate(axis, angle, origin) for p in self.wall_border.points]
        rotated_border_loop = Loop(rotated_border_points)

        rotated_opening_loops = []
        for opening_loop in self.openings:
            rotated_opening_points = [p.rotate(axis, angle, origin) for p in opening_loop.points]
            rotated_opening_loop = Loop(rotated_opening_points)
            rotated_opening_loops.append(rotated_opening_loop)

        return Wall(rotated_border_loop, rotated_opening_loops, self.wall_type, self.thickness)


    @functools.cached_property
    def gross_wall_area(self):
        return self.outer_loop.area

    @functools.cached_property
    def net_wall_area(self):
        return self.area

    @functools.cached_property
    def openings_area(self):
        return self.gross_wall_area - self.net_wall_area
