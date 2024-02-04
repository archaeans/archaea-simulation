from honeybee_energy.schedule.day import ScheduleDay
from honeybee_energy.schedule.rule import ScheduleRule
from honeybee_energy.schedule.ruleset import ScheduleRuleset
from honeybee_energy.schedule.typelimit import ScheduleTypeLimit
from ladybug.dt import Time

# 1st
comfort_calculations_schedule_day_1: ScheduleDay = ScheduleDay(
    "comfort_calculations_schedule_day_1",
    [0],
    [Time(0, 0)])

# 2nd
comfort_calculations_schedule_day_2: ScheduleDay = ScheduleDay(
    "comfort_calculations_schedule_day_2",
    [1],
    [Time(0, 0)])

# 3rd
comfort_calculations_schedule_day_3: ScheduleDay = ScheduleDay(
    "comfort_calculations_schedule_day_3",
    [0],
    [Time(0, 0)])

# 4th
comfort_calculations_schedule_day_4: ScheduleDay = ScheduleDay(
    "comfort_calculations_schedule_day_4",
    [1],
    [Time(0, 0)])

# 5th
comfort_calculations_schedule_day_5: ScheduleDay = ScheduleDay(
    "comfort_calculations_schedule_day_5",
    [0],
    [Time(0, 0)])

# All other days
comfort_calculations_schedule_day_all_others: ScheduleDay = ScheduleDay(
    "comfort_calculations_schedule_day_all_others",
    [0],
    [Time(0, 0)])

comfort_calculations_schedule_type_limit: ScheduleTypeLimit = ScheduleTypeLimit("comfort_calculations",
                                                                                lower_limit=0,
                                                                                upper_limit=1,
                                                                                unit_type='Dimensionless')

comfort_calculations_rule_set = ScheduleRuleset("comfort_calculations_rule_set",
                                                comfort_calculations_schedule_day_all_others,
                                                schedule_rules=[comfort_calculations_schedule_day_1,
                                                                comfort_calculations_schedule_day_2,
                                                                comfort_calculations_schedule_day_3,
                                                                comfort_calculations_schedule_day_4,
                                                                comfort_calculations_schedule_day_5],
                                                schedule_type_limit=comfort_calculations_schedule_type_limit)

