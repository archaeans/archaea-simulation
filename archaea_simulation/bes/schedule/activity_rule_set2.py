from honeybee_energy.schedule.day import ScheduleDay
from honeybee_energy.schedule.rule import ScheduleRule
from honeybee_energy.schedule.ruleset import ScheduleRuleset
from honeybee_energy.schedule.typelimit import ScheduleTypeLimit
from ladybug.dt import Time

# Weekday
activity_weekday2: ScheduleDay = ScheduleDay(
    "activity_weekday2",
    [72, 126, 117, 108],
    [Time(0, 0), Time(8, 0), Time(9, 0), Time(18, 0)])

# Weekend
activity_weekend2: ScheduleDay = ScheduleDay(
    "activity_weekend2",
    [72, 144, 117],
    [Time(0, 0), Time(9, 30), Time(12, 0)])

activity_schedule_weekday_rule2: ScheduleRule = ScheduleRule(activity_weekday2,
                                                             apply_monday=True,
                                                             apply_tuesday=True,
                                                             apply_wednesday=True,
                                                             apply_thursday=True,
                                                             apply_friday=True)

activity_schedule_weekend_rule2: ScheduleRule = ScheduleRule(activity_weekend2,
                                                             apply_saturday=True,
                                                             apply_sunday=True)

activity_schedule_type_limit2: ScheduleTypeLimit = ScheduleTypeLimit("activity2",
                                                                      lower_limit=0,
                                                                      upper_limit=1000,
                                                                      unit_type='ActivityLevel')

activity_rule_set2 = ScheduleRuleset("activity_rule_set2",
                                    activity_weekday2,
                                    schedule_rules=[activity_schedule_weekday_rule2, activity_schedule_weekend_rule2],
                                    schedule_type_limit=activity_schedule_type_limit2,
                                    holiday_schedule=activity_weekend2)