from .material_set import *
from honeybee_energy.constructionset import ConstructionSet, WallConstructionSet, FloorConstructionSet, RoofCeilingConstructionSet, ApertureConstructionSet
from honeybee_energy.construction.opaque import OpaqueConstruction
from honeybee_energy.construction.window import WindowConstruction

exterior_glazing: WindowConstruction = WindowConstruction("Exterior Glazing", [GL01])
ground_floor: OpaqueConstruction = OpaqueConstruction("Ground Floor",
                                                      [gypsum_plastering_0_01,
                                                       xps_0_04,
                                                       cast_concrete_0_12,
                                                       cast_concrete_light_0_05,
                                                       floor_roof_screed_0_03,
                                                       timber_flooring_0_03])

exterior_wall: OpaqueConstruction = OpaqueConstruction("Exterior Wall",
                                                       [lime_mortar_0_02,
                                                        xps_0_04,
                                                        brickk_0_19,
                                                        lime_mortar_0_01,
                                                        gypsum_plastering_0_01])

roof: OpaqueConstruction = OpaqueConstruction("Roof",
                                              [miscel_mater_roof_0_08,
                                               floor_roof_screed_0_03,
                                               xps_0_08,
                                               cast_concrete_0_12,
                                               gypsum_plastering_0_01])

basement_floor: OpaqueConstruction = OpaqueConstruction("Basement Floor",
                                                        [temel_betonu,
                                                         tesviye_betonu,
                                                         floor_roof_screed_0_03,
                                                         epoksi])

inner_wall: OpaqueConstruction = OpaqueConstruction("Inner Wall",
                                                    [gypsum_plastering_0_01,
                                                     brick_0_09,
                                                     gypsum_plastering_0_01])


wall_construction_set: WallConstructionSet = WallConstructionSet(exterior_wall, inner_wall, ground_floor)
floor_construction_set: FloorConstructionSet = FloorConstructionSet(exterior_wall, inner_wall, ground_floor)
roof_construction_set: RoofCeilingConstructionSet = RoofCeilingConstructionSet(roof, inner_wall, ground_floor)
aperture_construction_set: ApertureConstructionSet = ApertureConstructionSet(exterior_glazing)
construction_set: ConstructionSet = ConstructionSet("construction_set",
                                                    wall_construction_set,
                                                    floor_construction_set,
                                                    roof_construction_set,
                                                    aperture_construction_set)
