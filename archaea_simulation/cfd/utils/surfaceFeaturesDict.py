def surface_features_entry(name: str) -> str:
    return f"{name}\n" \
           "{\n" \
           f'\tsurfaces\n\t(\n\t\t"{name}.stl"\n\t);\n' \
           "\tincludedAngle\t180;\n" \
           "\twriteObj\tyes;\n" \
           "}"