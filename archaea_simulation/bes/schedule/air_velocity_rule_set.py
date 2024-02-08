from honeybee_energy.schedule.day import ScheduleDay
from honeybee_energy.schedule.rule import ScheduleRule
from honeybee_energy.schedule.ruleset import ScheduleRuleset
from honeybee_energy.schedule.typelimit import ScheduleTypeLimit
from ladybug.dt import Date, Time

###############################
### 1ST PERIOD (1.1 - 4.15) ###
###############################

air_velocity_1st_period: ScheduleDay = ScheduleDay(
    "air_velocity_1st_period",
    [0.16],
    [Time(0, 0)])


air_velocity_1st_period_rule: ScheduleRule = ScheduleRule(air_velocity_1st_period,
                                                                       apply_monday=True,
                                                                       apply_tuesday=True,
                                                                       apply_wednesday=True,
                                                                       apply_thursday=True,
                                                                       apply_friday=True,
                                                                       apply_saturday=True,
                                                                       apply_sunday=True,
                                                                       start_date=Date(1, 1),
                                                                       end_date=Date(4, 15))

###############################
### 2ND PERIOD (4.15 - 1o.15) ###
###############################

# Weekday
air_velocity_2nd_period: ScheduleDay = ScheduleDay(
    "air_velocity_2nd_period",
    [0.19],
    [Time(0, 0)])

air_velocity_2nd_period_rule: ScheduleRule = ScheduleRule(air_velocity_2nd_period,
                                                                       apply_monday=True,
                                                                       apply_tuesday=True,
                                                                       apply_wednesday=True,
                                                                       apply_thursday=True,
                                                                       apply_friday=True,
                                                                       apply_saturday=True,
                                                                       apply_sunday=True,
                                                                       start_date=Date(4, 16),
                                                                       end_date=Date(10, 15))

###############################
### 3RD PERIOD (10.15 - 7.31) ###
###############################

# Weekday
air_velocity_3rd_period: ScheduleDay = ScheduleDay(
    "air_velocity_3rd_period",
    [0.16],
    [Time(0, 0)])

air_velocity_3rd_period_rule: ScheduleRule = ScheduleRule(air_velocity_3rd_period,
                                                                       apply_monday=True,
                                                                       apply_tuesday=True,
                                                                       apply_wednesday=True,
                                                                       apply_thursday=True,
                                                                       apply_friday=True,
                                                                       apply_saturday=True,
                                                                       apply_sunday=True,
                                                                       start_date=Date(10, 16),
                                                                       end_date=Date(12, 31))

air_velocity_schedule_type_limit: ScheduleTypeLimit = ScheduleTypeLimit("air_velocity",
                                                                      unit_type='Velocity')

air_velocity_rule_set = ScheduleRuleset("air_velocity_rule_set",
                                    air_velocity_1st_period,
                                    schedule_rules=[air_velocity_1st_period_rule,
                                                    air_velocity_2nd_period_rule,
                                                    air_velocity_3rd_period_rule],
                                    schedule_type_limit=air_velocity_schedule_type_limit,
                                    holiday_schedule=air_velocity_1st_period)
