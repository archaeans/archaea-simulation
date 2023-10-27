from typing import Optional, List

import vtk
from specklepy.objects.geometry import Mesh, Plane, Point, Vector, Base
from specklepy.objects.other import DisplayStyle
from archaea.geometry.point3d import Point3d
from archaea.geometry.vector3d import Vector3d
from archaea.geometry.mesh import Mesh as ArchaeaMesh
import numpy as np
import matplotlib
import matplotlib.cm as cm


class Text(Base, speckle_type="Objects.Other.Text"):
    plane: Plane
    value: str
    height: float = 1
    rotation: float = 0

def average(lst):
    return sum(lst) / len(lst)


def to_int(rgba):
    return int(rgba[3] << 24 | rgba[0] << 16 | rgba[1] << 8 | rgba[2])


def vtk_to_speckle(path: str, legend_point: Point3d):
    # Load the .vtk file
    reader = vtk.vtkPolyDataReader()
    reader.SetFileName(path)
    reader.Update()

    vtk_data = reader.GetOutput()

    # Extract point coordinates
    vtk_points = vtk_data.GetPoints().GetData()
    numpy_point_array = np.array(vtk_points)
    numpy_point_array_with_values = [[p, []] for p in numpy_point_array]
    flat_point_array = [float(num) for sublist in numpy_point_array for num in sublist]

    # Extract U vectors
    cell_data = vtk_data.GetCellData()
    u_vectors = cell_data.GetArray('U')
    u_array = np.array(u_vectors)
    u_magnitudes = [(u[0] ** 2 + u[1] ** 2 + u[2] ** 2) ** 0.5 for u in u_array]
    u_min = 0
    u_max = max(u_magnitudes)

    norm = matplotlib.colors.Normalize(vmin=u_min, vmax=u_max, clip=True)
    mapper = cm.ScalarMappable(norm=norm, cmap=cm.jet)

    # Extract polygon information
    vtk_polygons = vtk_data.GetPolys().GetData()
    polygon_array = np.array(vtk_polygons).tolist()
    polygon_indices = []
    polygons = []
    current_index = 0
    while True:
        if current_index >= len(polygon_array):
            break
        ngon = polygon_array[current_index]
        polygon_indices.append(ngon)
        polygons.append(polygon_array[current_index:current_index+ngon+1])
        current_index += ngon + 1

    for i, polygon in enumerate(polygons):
        ngon = polygon[0]
        vertices = polygon[1:]
        for vertex_index in vertices:
            numpy_point_with_values = numpy_point_array_with_values[vertex_index]
            numpy_point_with_values[1].append(u_magnitudes[i])

    point_magnitudes = [average(p[1]) for p in numpy_point_array_with_values]

    colors = [to_int(list(mapper.to_rgba(value, bytes=True))) for value in point_magnitudes]
    legend_values = np.linspace(u_min, u_max, 10)
    legend_colors = [to_int(list(mapper.to_rgba(value, bytes=True))) for value in legend_values]

    mesh = Mesh()
    mesh.units = 'm'
    mesh.name = 'Section 1.5m'
    mesh.vertices = flat_point_array
    mesh.faces = polygon_array
    mesh.colors = colors

    legend_mesh_and_texts = create_legend_from_vtk(legend_values, legend_colors, legend_point)

    return [mesh] + legend_mesh_and_texts

def create_legend_from_vtk(legend_values: list[float], legend_colors: list[int], legend_point: Point3d):
    legend_mesh = Mesh()
    legend_texts = []
    legend_mesh.units = 'm'
    legend_mesh.name = 'Legend'

    display_style = DisplayStyle()
    display_style.color = -16777216
    display_style.linetype = "Continuous"
    display_style.units = "m"
    display_style.lineweight = 0

    start_p = legend_point
    archaea_mesh = ArchaeaMesh()
    legend_mesh_colors = []
    for index, legend_color in enumerate(legend_colors):
        v = [start_p, start_p.move(Vector3d(2, 0, 0)), start_p.move(Vector3d(2, 2, 0)), start_p.move(Vector3d(0, 2, 0))]
        archaea_mesh.add_polygon(v, share_vertices=False)
        legend_mesh_colors += [legend_color, legend_color, legend_color, legend_color]
        
        text_v = Point3d(start_p.x + 2.5, start_p.y + 1, 0)
        start_p = start_p.move(Vector3d(0, 2, 0))
        plane = Plane.from_list([text_v.x, text_v.y, text_v.z,
                                0, 0, 1,
                                1, 0, 0,
                                0, 1, 0,
                                3])
        text = Text()
        text.height = 1
        text.value = str(round(legend_values[index], 1))
        text.plane = plane
        text.units = "m"
        text.displayStyle = display_style
        legend_texts.append(text)

    legend_unit_text_p = Point3d(legend_point.x, legend_point.y - 1.5 + 1, 0)
    legend_unit_plane = Plane.from_list([legend_unit_text_p.x, legend_unit_text_p.y, legend_unit_text_p.z,
                                        0, 0, 1,
                                        1, 0, 0,
                                        0, 1, 0,
                                        3])
    
    text = Text()
    text.height = 1
    text.value = "m/s"
    text.plane = legend_unit_plane
    text.units = "m"
    text.displayStyle = display_style
    legend_texts.append(text)
    
    legend_mesh.vertices = [item for sublist in archaea_mesh.vertices for item in sublist]
    legend_mesh.faces = [item for sublist in archaea_mesh.polygons for item in [len(sublist)] + sublist]
    legend_mesh.colors = legend_mesh_colors

    return [legend_mesh] + legend_texts

