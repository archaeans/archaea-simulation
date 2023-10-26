def snappy_hex_mesh_geometry(geometry_name: str, file_name: str) -> str:
    return '{0}\n' \
           '    {{\n' \
           '\ttype triSurfaceMesh;\n' \
           '\tfile "{1}.stl";\n' \
           '    }}\n'.format(geometry_name, file_name)  # noqa: UP030


def snappy_hex_mesh_features(eMesh_name: str, level: int) -> str:
    return '{{\n' \
           '\tfile "{0}.eMesh";\n' \
           '\tlevel {1};\n' \
           '    }}\n'.format(eMesh_name, level)  # noqa: UP030

def snappy_hex_mesh_refinementSurfaces(geometry_name: str, level_1: str, level_2: str) -> str:
    return '{0}\n' \
           '    {{\n' \
           '\tlevel ({1} {2});\n' \
           '\tpatchInfo {{ type wall; }}\n' \
           '    }}\n'.format(geometry_name, level_1, level_2)  # noqa: F524, UP030

def snappy_hex_mesh_refinementRegions(geometry_name: str, level_1: str) -> str:
    return '{0}\n' \
           '    {{\n' \
           '\tmode  inside;\n' \
           '\tlevel {1};\n' \
           '    }}\n'.format(geometry_name, level_1)  # noqa: F524, UP030