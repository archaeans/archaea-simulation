from honeybee.room import Room as HB_Room
from honeybee.face import Face as HB_Face

from archaea_simulation.bes.schedule.program_types import conditioned_program
from archaea_simulation.bes.material.construction_set import construction_set
from honeybee_energy.lib.programtypes import office_program


class ThermalZone:
    identifier: str
    faces: "list[HB_Face]"
    room: HB_Room
    is_conditioned: bool
    zone_program: int

    
    def __init__(self, 
                 identifier: str, 
                 faces: "list[HB_Face]", 
                 is_conditioned: bool = True):
        self.identifier = identifier
        self.faces = faces
        self.room = HB_Room(identifier, faces)
        self.room.properties.energy.program_type = conditioned_program
        self.room.properties.energy.add_default_ideal_air()
        self.room.properties.energy.construction_set = construction_set