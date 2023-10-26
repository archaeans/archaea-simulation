from archaea.geometry.bounding_box import BoundingBox
from archaea.geometry.loop import Loop
from archaea.geometry.face import Face
from archaea.geometry.mesh import Mesh
from archaea.geometry.point3d import Point3d
from archaea.geometry.vector3d import Vector3d
from archaea.geometry.plane import Plane

from archaea_simulation.simulation_objects.zone import Zone


def create_refinement_box_mesh(bbox: BoundingBox, scale: float):
    scaled_height = bbox.z_dist * scale
    scaled_u_min = bbox.min.x - (bbox.x_dist / 2 * scale) + bbox.x_dist / 2
    scaled_v_min = bbox.min.y - (bbox.y_dist / 2 * scale) + bbox.y_dist / 2

    scaled_u_max = bbox.max.x + (bbox.x_dist / 2 * scale) - bbox.x_dist / 2
    scaled_v_max = bbox.max.y + (bbox.y_dist / 2 * scale) - bbox.y_dist / 2

    scaled_u_corner_1 = scaled_u_max
    scaled_v_corner_1 = scaled_v_min

    scaled_u_corner_2 = scaled_u_min
    scaled_v_corner_2 = scaled_v_max

    global_scaled_min = bbox.plane.point_at(scaled_u_min, scaled_v_min)
    global_scaled_corner_1 = bbox.plane.point_at(scaled_u_corner_1, scaled_v_corner_1)
    global_scaled_max = bbox.plane.point_at(scaled_u_max, scaled_v_max)
    global_scaled_corner_2 = bbox.plane.point_at(scaled_u_corner_2, scaled_v_corner_2)

    p0 = Point3d(global_scaled_min.x, global_scaled_min.y, global_scaled_min.z)
    p1 = Point3d(global_scaled_corner_1.x, global_scaled_corner_1.y, global_scaled_min.z)
    p2 = Point3d(global_scaled_max.x, global_scaled_max.y, global_scaled_min.z)
    p3 = Point3d(global_scaled_corner_2.x, global_scaled_corner_2.y, global_scaled_min.z)

    ground_loop_1 = Loop([p0, p3, p2, p1])
    ground_face_1 = Face(ground_loop_1)
    zone_without_hole = Zone(ground_face_1, scaled_height)
    mesh = Mesh()
    faces = zone_without_hole.create_solid_faces()
    mesh.add_from_faces(faces)

    return mesh
