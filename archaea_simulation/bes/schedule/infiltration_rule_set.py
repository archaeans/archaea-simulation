from honeybee_energy.schedule.day import ScheduleDay
from honeybee_energy.schedule.ruleset import ScheduleRuleset
from ladybug.dt import Time

from archaea_simulation.bes.schedule.type_limits import fraction

# Weekday

infiltration_design_day: ScheduleDay = ScheduleDay(
    "infiltration_design_day",
    [1],
    [Time(0, 0)])

conditioned_infiltration_rule_set = ScheduleRuleset("conditioned_infiltration_schedule",
                                                    infiltration_design_day,
                                                    schedule_type_limit=fraction)
