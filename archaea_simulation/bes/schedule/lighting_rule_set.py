from honeybee_energy.schedule.day import ScheduleDay
from honeybee_energy.schedule.rule import ScheduleRule
from honeybee_energy.schedule.ruleset import ScheduleRuleset
from honeybee_energy.schedule.typelimit import ScheduleTypeLimit
from ladybug.dt import Time, Date

###############################
### 1ST PERIOD (1.1 - 2.28) ###
###############################

# Weekday
lighting_weekday_1st_period: ScheduleDay = ScheduleDay(
    "lighting_weekday_1st_period",
    [0.05, 0.5, 0, 0.5],
    [Time(0, 0), Time(6, 0), Time(7, 0), Time(19, 0)])

# Weekend
lighting_weekend_1st_period: ScheduleDay = ScheduleDay(
    "lighting_weekend_1st_period",
    [0.05, 0.5],
    [Time(0, 0), Time(18, 0)])


lighting_schedule_weekday_rule_1st_period: ScheduleRule = ScheduleRule(lighting_weekday_1st_period,
                                                                       apply_monday=True,
                                                                       apply_tuesday=True,
                                                                       apply_wednesday=True,
                                                                       apply_thursday=True,
                                                                       apply_friday=True,
                                                                       start_date=Date(1, 1),
                                                                       end_date=Date(2, 28))

lighting_schedule_weekend_rule_1st_period: ScheduleRule = ScheduleRule(lighting_weekend_1st_period,
                                                                       apply_saturday=True,
                                                                       apply_sunday=True,
                                                                       start_date=Date(1, 1),
                                                                       end_date=Date(2, 28))

###############################
### 2ND PERIOD (3.1 - 4.30) ###
###############################

# Weekday
lighting_weekday_2nd_period: ScheduleDay = ScheduleDay(
    "lighting_weekday_2nd_period",
    [0.05, 0.5, 0, 0.5],
    [Time(0, 0), Time(6, 0), Time(7, 0), Time(19, 0)])

# Weekend
lighting_weekend_2nd_period: ScheduleDay = ScheduleDay(
    "lighting_weekend_2nd_period",
    [0.05, 0.5],
    [Time(0, 0), Time(19, 0)])

lighting_schedule_weekday_rule_2nd_period: ScheduleRule = ScheduleRule(lighting_weekday_2nd_period,
                                                                       apply_monday=True,
                                                                       apply_tuesday=True,
                                                                       apply_wednesday=True,
                                                                       apply_thursday=True,
                                                                       apply_friday=True,
                                                                       start_date=Date(3, 1),
                                                                       end_date=Date(4, 30))

lighting_schedule_weekend_rule_2nd_period: ScheduleRule = ScheduleRule(lighting_weekend_2nd_period,
                                                                       apply_saturday=True,
                                                                       apply_sunday=True,
                                                                       start_date=Date(3, 1),
                                                                       end_date=Date(4, 30))

###############################
### 3RD PERIOD (5.1 - 7.31) ###
###############################

# Weekday
lighting_weekday_3rd_period: ScheduleDay = ScheduleDay(
    "lighting_weekday_3rd_period",
    [0.05, 0, 0.5],
    [Time(0, 0), Time(7, 0), Time(20, 30)])

# Weekend
lighting_weekend_3rd_period: ScheduleDay = ScheduleDay(
    "lighting_weekend_3rd_period",
    [0.05, 0.5],
    [Time(0, 0), Time(20, 30)])

lighting_schedule_weekday_rule_3rd_period: ScheduleRule = ScheduleRule(lighting_weekday_3rd_period,
                                                                       apply_monday=True,
                                                                       apply_tuesday=True,
                                                                       apply_wednesday=True,
                                                                       apply_thursday=True,
                                                                       apply_friday=True,
                                                                       start_date=Date(5, 1),
                                                                       end_date=Date(7, 31))

lighting_schedule_weekend_rule_3rd_period: ScheduleRule = ScheduleRule(lighting_weekend_3rd_period,
                                                                       apply_saturday=True,
                                                                       apply_sunday=True,
                                                                       start_date=Date(5, 1),
                                                                       end_date=Date(7, 31))

###############################
### 4TH PERIOD (8.1 - 9.30) ###
###############################

# Weekday
lighting_weekday_4th_period: ScheduleDay = ScheduleDay(
    "lighting_weekday_4th_period",
    [0.05, 0.5, 0, 0.5],
    [Time(0, 0), Time(6, 0), Time(7, 0), Time(19, 0)])

# Weekend
lighting_weekend_4th_period: ScheduleDay = ScheduleDay(
    "lighting_weekend_4th_period",
    [0.05, 0.5],
    [Time(0, 0), Time(19, 0)])

lighting_schedule_weekday_rule_4th_period: ScheduleRule = ScheduleRule(lighting_weekday_4th_period,
                                                                       apply_monday=True,
                                                                       apply_tuesday=True,
                                                                       apply_wednesday=True,
                                                                       apply_thursday=True,
                                                                       apply_friday=True,
                                                                       start_date=Date(8, 1),
                                                                       end_date=Date(9, 30))

lighting_schedule_weekend_rule_4th_period: ScheduleRule = ScheduleRule(lighting_weekend_4th_period,
                                                                       apply_saturday=True,
                                                                       apply_sunday=True,
                                                                       start_date=Date(8, 1),
                                                                       end_date=Date(9, 30))

###############################
### 5TH PERIOD (10.1 - 12.31) ###
###############################

# Weekday
lighting_weekday_5th_period: ScheduleDay = ScheduleDay(
    "lighting_weekday_5th_period",
    [0.05, 0.5, 0, 0.5],
    [Time(0, 0), Time(6, 0), Time(7, 0), Time(19, 0)])

# Weekend
lighting_weekend_5th_period: ScheduleDay = ScheduleDay(
    "lighting_weekend_5th_period",
    [0.05, 0.5],
    [Time(0, 0), Time(18, 0)])

lighting_schedule_weekday_rule_5th_period: ScheduleRule = ScheduleRule(lighting_weekday_5th_period,
                                                                       apply_monday=True,
                                                                       apply_tuesday=True,
                                                                       apply_wednesday=True,
                                                                       apply_thursday=True,
                                                                       apply_friday=True,
                                                                       start_date=Date(10, 1),
                                                                       end_date=Date(12, 31))

lighting_schedule_weekend_rule_5th_period: ScheduleRule = ScheduleRule(lighting_weekend_5th_period,
                                                                       apply_saturday=True,
                                                                       apply_sunday=True,
                                                                       start_date=Date(10, 1),
                                                                       end_date=Date(12, 31))

lighting_schedule_type_limit: ScheduleTypeLimit = ScheduleTypeLimit("ligthing",
                                                                      lower_limit=0,
                                                                      upper_limit=1,
                                                                      unit_type='Dimensionless')

lighting_rule_set = ScheduleRuleset("lighting_rule_set",
                                    lighting_weekday_1st_period,
                                    schedule_rules=[lighting_schedule_weekday_rule_1st_period,
                                                    lighting_schedule_weekend_rule_1st_period,
                                                    lighting_schedule_weekday_rule_2nd_period,
                                                    lighting_schedule_weekend_rule_2nd_period,
                                                    lighting_schedule_weekday_rule_3rd_period,
                                                    lighting_schedule_weekend_rule_3rd_period,
                                                    lighting_schedule_weekday_rule_4th_period,
                                                    lighting_schedule_weekend_rule_4th_period,
                                                    lighting_schedule_weekday_rule_5th_period,
                                                    lighting_schedule_weekend_rule_5th_period],
                                    schedule_type_limit=lighting_schedule_type_limit,
                                    holiday_schedule=lighting_weekend_1st_period)

unconditioned_lighting_alldays: ScheduleDay = ScheduleDay(
    "unconditioned_lighting_alldays",
    [0.05, 0.1, 0.2, 0.4, 0.5, 0.35, 0.15, 0.35, 0.5, 0.4, 0.3, 0.2, 0.1],
    [Time(0, 0), Time(4, 0), Time(5, 0), Time(6, 0), Time(7, 0), Time(9, 0), Time(10, 0), Time(16, 0), Time(17, 0), Time(19, 0), Time(21, 0), Time(22, 0), Time(23, 0)])

unconditioned_summer_design_day_lighting: ScheduleDay = ScheduleDay(
    "unconditioned_winter_design_day_lighting",
    [0.5],
    [Time(0, 0)]
)

unconditioned_winter_design_day_lighting: ScheduleDay = ScheduleDay(
    "unconditioned_winter_design_day_lighting",
    [0.05],
    [Time(0, 0)]
)

unconditioned_lighting_rule_set = ScheduleRuleset("unconditioned_lighting_rule_set",
                                                  unconditioned_lighting_alldays,
                                                  schedule_type_limit=lighting_schedule_type_limit,
                                                  summer_designday_schedule=unconditioned_summer_design_day_lighting,
                                                  winter_designday_schedule=unconditioned_winter_design_day_lighting
                                                  )