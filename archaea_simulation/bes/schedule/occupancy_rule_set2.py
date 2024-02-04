from honeybee_energy.schedule.day import ScheduleDay
from honeybee_energy.schedule.rule import ScheduleRule
from honeybee_energy.schedule.ruleset import ScheduleRuleset
from honeybee_energy.schedule.typelimit import ScheduleTypeLimit
from ladybug.dt import Time

# Weekday
always_off_occupancy_weekday2: ScheduleDay = ScheduleDay(
    "occupancy_weekday2",
    [0],
    [Time(0, 0)])

# Weekday
occupancy_weekday2: ScheduleDay = ScheduleDay(
    "occupancy_weekday2",
    [1],
    [Time(0, 0)])

# Weekend
occupancy_weekend2: ScheduleDay = ScheduleDay(
    "occupancy_weekend2",
    [1, 0.5],
    [Time(0, 0), Time(12, 0)])

occupancy_schedule_weekday_rule2: ScheduleRule = ScheduleRule(occupancy_weekday2,
                                                             apply_monday=True,
                                                             apply_tuesday=True,
                                                             apply_wednesday=True,
                                                             apply_thursday=True,
                                                             apply_friday=True)

occupancy_schedule_weekend_rule2: ScheduleRule = ScheduleRule(occupancy_weekend2,
                                                             apply_saturday=True,
                                                             apply_sunday=True)

occupancy_schedule_type_limit2: ScheduleTypeLimit = ScheduleTypeLimit("occupancy2",
                                                                      lower_limit=0,
                                                                      upper_limit=1,
                                                                      unit_type='Dimensionless')

occupancy_rule_set2 = ScheduleRuleset("occupancy_rule_set2",
                                     occupancy_weekday2,
                                     schedule_rules=[occupancy_schedule_weekday_rule2, occupancy_schedule_weekend_rule2],
                                     schedule_type_limit=occupancy_schedule_type_limit2,
                                     holiday_schedule=occupancy_weekend2)

always_off_occupancy_rule_set2 = ScheduleRuleset("Always Off2",
                                                always_off_occupancy_weekday2,
                                                schedule_type_limit=occupancy_schedule_type_limit2)
