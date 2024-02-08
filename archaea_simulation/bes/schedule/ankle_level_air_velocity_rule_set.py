from honeybee_energy.schedule.day import ScheduleDay
from honeybee_energy.schedule.rule import ScheduleRule
from honeybee_energy.schedule.ruleset import ScheduleRuleset
from ladybug.dt import Time

from archaea_simulation.bes.schedule.type_limits import fraction

ank_level_air_velocity: ScheduleDay = ScheduleDay(
    "ank_level_air_velocity",
    [0.3],
    [Time(0, 0)])

ank_level_air_velocity_rule: ScheduleRule = ScheduleRule(ank_level_air_velocity,
                                                         apply_monday=True,
                                                         apply_tuesday=True,
                                                         apply_wednesday=True,
                                                         apply_thursday=True,
                                                         apply_friday=True,
                                                         apply_saturday=True,
                                                         apply_sunday=True)

ank_level_air_velocity_rule_set = ScheduleRuleset("ank_level_air_velocity_rule_set",
                                                  ank_level_air_velocity,
                                                  schedule_type_limit=fraction)
