from honeybee_energy.schedule.day import ScheduleDay
from honeybee_energy.schedule.ruleset import ScheduleRuleset
from honeybee_energy.schedule.typelimit import ScheduleTypeLimit
from honeybee_energy.load.setpoint import Setpoint
from ladybug.dt import Time

# Heating
default_heating_day_schedule: ScheduleDay = ScheduleDay(
    "winter_design_day",
    [0, 18, 0],
    [Time(0, 0), Time(8, 0), Time(17, 0)])

winter_heating_design_day: ScheduleDay = ScheduleDay(
    "winter_heating_design_day",
    [0, 18, 0],
    [Time(0, 0), Time(9, 0), Time(17, 0)])

summer_heating_design_day: ScheduleDay = ScheduleDay(
    "summer_heating_design_day",
    [0, 0, 0],
    [Time(0, 0), Time(8, 0), Time(16, 0)])

# Cooling
default_cooling_day_schedule: ScheduleDay = ScheduleDay(
    "winter_design_day",
    [23, 23, 23],
    [Time(0, 0), Time(8, 0), Time(17, 0)])

winter_cooling_design_day: ScheduleDay = ScheduleDay(
    "winter_cooling_design_day",
    [23, 23, 23],
    [Time(0, 0), Time(9, 0), Time(17, 0)])

summer_cooling_design_day: ScheduleDay = ScheduleDay(
    "summer_cooling_design_day",
    [23, 23, 23],
    [Time(0, 0), Time(8, 0), Time(16, 0)])







# Heating
default_heating_day_schedule2: ScheduleDay = ScheduleDay(
    "winter_design_day",
    [20],
    [Time(0, 0)])

winter_heating_design_day2: ScheduleDay = ScheduleDay(
    "winter_heating_design_day",
    [20],
    [Time(0, 0)])

summer_heating_design_day2: ScheduleDay = ScheduleDay(
    "summer_heating_design_day",
    [20],
    [Time(0, 0)])

# Cooling
default_cooling_day_schedule2: ScheduleDay = ScheduleDay(
    "summer_design_day",
    [26],
    [Time(0, 0)])

winter_cooling_design_day2: ScheduleDay = ScheduleDay(
    "winter_cooling_design_day",
    [26],
    [Time(0, 0)])

summer_cooling_design_day2: ScheduleDay = ScheduleDay(
    "summer_cooling_design_day",
    [26],
    [Time(0, 0)])

temperature_schedule_type_limit: ScheduleTypeLimit = ScheduleTypeLimit("hvac",
                                                                       unit_type='Temperature')

heating_rule_set = ScheduleRuleset("heating_rule_set",
                                   default_heating_day_schedule2,
                                   summer_designday_schedule=summer_heating_design_day2,
                                   winter_designday_schedule=winter_heating_design_day2,
                                   schedule_type_limit=temperature_schedule_type_limit)

cooling_rule_set = ScheduleRuleset("cooling_rule_set",
                                   default_cooling_day_schedule2,
                                   summer_designday_schedule=summer_cooling_design_day2,
                                   winter_designday_schedule=winter_cooling_design_day2,
                                   schedule_type_limit=temperature_schedule_type_limit)

setpoint: Setpoint = Setpoint("setpoint",
                              heating_rule_set,
                              cooling_rule_set)

# TODO: Check correctness later
