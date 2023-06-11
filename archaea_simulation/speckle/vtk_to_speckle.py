from typing import Optional, List

import vtk
from specklepy.objects.geometry import Mesh
import numpy as np
import matplotlib
import matplotlib.cm as cm


def average(lst):
    return sum(lst) / len(lst)


def to_int(rgba):
    return int(rgba[3] << 24 | rgba[0] << 16 | rgba[1] << 8 | rgba[2])


def vtk_to_speckle(path: str):
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

    mesh = Mesh()
    mesh.units = 'm'
    mesh.name = 'Section 1.5m'
    mesh.vertices = flat_point_array
    mesh.faces = polygon_array
    mesh.colors = colors

    return mesh


vtk_to_speckle('/home/koral/OpenFOAM/koral-9/run/archaea-simulation/cfd/test-for-speckle-vtk/postProcessing'
               '/cutPlaneSurface/400/U_cutPlane.vtk')
