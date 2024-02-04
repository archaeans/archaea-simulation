from honeybee_energy.schedule.day import ScheduleDay
from honeybee_energy.schedule.rule import ScheduleRule
from honeybee_energy.schedule.ruleset import ScheduleRuleset
from ladybug.dt import Time

from archaea_simulation.bes.schedule.type_limits import fraction

clothing_insulation: ScheduleDay = ScheduleDay(
    "clothing_insulation",
    [0.8],
    [Time(0, 0)])

clothing_insulation_rule: ScheduleRule = ScheduleRule(clothing_insulation,
                                                      apply_monday=True,
                                                      apply_tuesday=True,
                                                      apply_wednesday=True,
                                                      apply_thursday=True,
                                                      apply_friday=True,
                                                      apply_saturday=True,
                                                      apply_sunday=True)


clothing_insulation_rule_set = ScheduleRuleset("clothing_insulation_rule_set",
                                               clothing_insulation,
                                               schedule_type_limit=fraction)
