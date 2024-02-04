from honeybee_energy.schedule.day import ScheduleDay
from honeybee_energy.schedule.rule import ScheduleRule
from honeybee_energy.schedule.ruleset import ScheduleRuleset
from honeybee_energy.schedule.typelimit import ScheduleTypeLimit
from ladybug.dt import Time

# Weekday
always_off_occupancy_weekday: ScheduleDay = ScheduleDay(
    "occupancy_weekday",
    [0],
    [Time(0, 0)])

# Weekday
occupancy_weekday: ScheduleDay = ScheduleDay(
    "occupancy_weekday",
    [1, 0, 1],
    [Time(0, 0), Time(7, 30), Time(19, 0)])

# Weekend
occupancy_weekend: ScheduleDay = ScheduleDay(
    "occupancy_weekend",
    [1, 0.5],
    [Time(0, 0), Time(12, 0)])

occupancy_schedule_weekday_rule: ScheduleRule = ScheduleRule(occupancy_weekday,
                                                             apply_monday=True,
                                                             apply_tuesday=True,
                                                             apply_wednesday=True,
                                                             apply_thursday=True,
                                                             apply_friday=True)

occupancy_schedule_weekend_rule: ScheduleRule = ScheduleRule(occupancy_weekend,
                                                             apply_saturday=True,
                                                             apply_sunday=True)

occupancy_schedule_type_limit: ScheduleTypeLimit = ScheduleTypeLimit("occupancy",
                                                                      lower_limit=0,
                                                                      upper_limit=1,
                                                                      unit_type='Dimensionless')

occupancy_rule_set = ScheduleRuleset("occupancy_rule_set",
                                     occupancy_weekday,
                                     schedule_rules=[occupancy_schedule_weekday_rule, occupancy_schedule_weekend_rule],
                                     schedule_type_limit=occupancy_schedule_type_limit,
                                     holiday_schedule=occupancy_weekend)

always_off_occupancy_rule_set = ScheduleRuleset("Always Off",
                                                always_off_occupancy_weekday,
                                                schedule_type_limit=occupancy_schedule_type_limit)
