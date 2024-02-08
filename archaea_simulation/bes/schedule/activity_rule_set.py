from honeybee_energy.schedule.day import ScheduleDay
from honeybee_energy.schedule.rule import ScheduleRule
from honeybee_energy.schedule.ruleset import ScheduleRuleset
from honeybee_energy.schedule.typelimit import ScheduleTypeLimit
from ladybug.dt import Time

# Weekday
activity_weekday: ScheduleDay = ScheduleDay(
    "activity_weekday",
    [72, 70, 108],
    [Time(0, 0), Time(7, 30), Time(19, 0)])

# Weekend
activity_weekend: ScheduleDay = ScheduleDay(
    "activity_weekend",
    [72, 144, 180, 108],
    [Time(0, 0), Time(9, 30), Time(12, 0), Time(18, 0)])

activity_schedule_weekday_rule: ScheduleRule = ScheduleRule(activity_weekday,
                                                             apply_monday=True,
                                                             apply_tuesday=True,
                                                             apply_wednesday=True,
                                                             apply_thursday=True,
                                                             apply_friday=True)

activity_schedule_weekend_rule: ScheduleRule = ScheduleRule(activity_weekend,
                                                             apply_saturday=True,
                                                             apply_sunday=True)

activity_schedule_type_limit: ScheduleTypeLimit = ScheduleTypeLimit("activity",
                                                                    lower_limit=0,
                                                                    upper_limit=1000,
                                                                    unit_type='ActivityLevel')

activity_rule_set = ScheduleRuleset("activity_rule_set",
                                    activity_weekday,
                                    schedule_rules=[activity_schedule_weekday_rule, activity_schedule_weekend_rule],
                                    schedule_type_limit=activity_schedule_type_limit,
                                    holiday_schedule=activity_weekend)