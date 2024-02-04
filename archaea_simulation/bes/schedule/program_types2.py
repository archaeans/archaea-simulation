from __future__ import annotations

from honeybee_energy.load.infiltration import Infiltration
from honeybee_energy.load.people import People
from honeybee_energy.load.equipment import ElectricEquipment
from honeybee_energy.load.lighting import Lighting
from honeybee_energy.load.ventilation import Ventilation
from honeybee_energy.programtype import ProgramType

from archaea_simulation.bes.schedule.lighting_rule_set2 import lighting_rule_set2, unconditioned_lighting_rule_set2
from archaea_simulation.bes.schedule.occupancy_rule_set2 import occupancy_rule_set2, always_off_occupancy_rule_set2
from archaea_simulation.bes.schedule.infiltration_rule_set import conditioned_infiltration_rule_set
from archaea_simulation.bes.schedule.occupancy_rule_set import occupancy_rule_set, always_off_occupancy_rule_set
from archaea_simulation.bes.schedule.air_velocity_rule_set import air_velocity_rule_set
from archaea_simulation.bes.schedule.activity_rule_set2 import activity_rule_set2
from archaea_simulation.bes.schedule.clothing_insulation_rule_set import clothing_insulation_rule_set
from archaea_simulation.bes.schedule.ankle_level_air_velocity_rule_set import ank_level_air_velocity_rule_set
from archaea_simulation.bes.schedule.equipment_rule_set import equipment_rule_set, unconditioned_equipment_rule_set
from archaea_simulation.bes.schedule.equipment_rule_set2 import equipment_rule_set2, unconditioned_equipment_rule_set2
from archaea_simulation.bes.schedule.lighting_rule_set import lighting_rule_set, unconditioned_lighting_rule_set
from archaea_simulation.bes.schedule.hvac_rule_set import setpoint

conditioned_program2: ProgramType = ProgramType("conditioned_program2")
unconditioned_program2: ProgramType = ProgramType("unconditioned_program2")

conditioned_program2.setpoint = setpoint

conditioned_program2.people = People("people_schedule2",
                                            0.033,
                                            occupancy_rule_set2,
                                            air_velocity_rule_set,
                                            clothing_insulation_rule_set,
                                            ank_level_air_velocity_rule_set,
                                            activity_schedule=activity_rule_set2)

unconditioned_program2.people = People("always_off_people_schedule2",
                                              0,
                                              always_off_occupancy_rule_set,
                                              air_velocity_rule_set,
                                              clothing_insulation_rule_set,
                                              ank_level_air_velocity_rule_set)

# W/m2 value comes from below link that need to be validated.
# https://knowledge.autodesk.com/support/revit/getting-started/caas/simplecontent/content/equipment-and-lighting-loads.html
conditioned_program2.electric_equipment = ElectricEquipment("equipment_schedule2",
                                                                   9.17,
                                                                   equipment_rule_set2,
                                                                   radiant_fraction=0.3)

unconditioned_program2.electric_equipment = ElectricEquipment("unconditioned_equipment_schedule2",
                                                                     9.17,
                                                                     unconditioned_equipment_rule_set2,
                                                                     radiant_fraction=0.3)

conditioned_program2.lighting = Lighting("lighting_schedule2",
                                                4.5,
                                                lighting_rule_set2)

unconditioned_program2.lighting = Lighting("lighting_schedule2",
                                                  4.5,
                                                  unconditioned_lighting_rule_set2)

conditioned_program2.infiltration = Infiltration("conditioned_infiltration_schedule2",
                                                        0,
                                                        conditioned_infiltration_rule_set)

unconditioned_program2.infiltration = Infiltration("unconditioned_infiltration_schedule2",
                                                          0,
                                                          conditioned_infiltration_rule_set,
                                                          constant_coefficient=0,
                                                          temperature_coefficient=0,
                                                          velocity_coefficient=0.2240)
