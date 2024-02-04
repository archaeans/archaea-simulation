from honeybee_energy.schedule.day import ScheduleDay
from honeybee_energy.schedule.rule import ScheduleRule
from honeybee_energy.schedule.ruleset import ScheduleRuleset
from honeybee_energy.schedule.typelimit import ScheduleTypeLimit
from ladybug.dt import Time

# Weekday
equipment_weekday: ScheduleDay = ScheduleDay(
    "equipment_weekday",
    [0.029, 0.49, 0.029, 0.87, 0.029],
    [Time(0, 0), Time(7, 0), Time(7, 30), Time(19, 0), Time(22, 0)])

unconditioned_equipment_alldays: ScheduleDay = ScheduleDay(
    "unconditioned_equipment_alldays",
    [0.05, 0.1, 0.2, 0.4, 0.5, 0.35, 0.15, 0.35, 0.5, 0.4, 0.3, 0.2, 0.1],
    [Time(0, 0), Time(4, 0), Time(5, 0), Time(6, 0), Time(7, 0), Time(9, 0), Time(10, 0), Time(16, 0), Time(17, 0), Time(19, 0), Time(21, 0), Time(22, 0), Time(23, 0)])

# Weekend
equipment_weekend: ScheduleDay = ScheduleDay(
    "equipment_weekend",
    [0.029, 0.49, 0.67, 0.029, 0.49],
    [Time(0, 0), Time(9, 30), Time(10, 0), Time(12, 0), Time(18, 0)])

equipment_schedule_weekday_rule: ScheduleRule = ScheduleRule(equipment_weekday,
                                                             apply_monday=True,
                                                             apply_tuesday=True,
                                                             apply_wednesday=True,
                                                             apply_thursday=True,
                                                             apply_friday=True)

equipment_schedule_weekend_rule: ScheduleRule = ScheduleRule(equipment_weekend,
                                                             apply_saturday=True,
                                                             apply_sunday=True)

conditioned_summer_design_day_equipment: ScheduleDay = ScheduleDay(
    "conditioned_summer_design_day_equipment",
    [0.76],
    [Time(0, 0)]
)

conditioned_winter_design_day_equipment: ScheduleDay = ScheduleDay(
    "conditioned_winter_design_day_equipment",
    [0],
    [Time(0, 0)]
)

equipment_schedule_type_limit: ScheduleTypeLimit = ScheduleTypeLimit("equipment",
                                                                     lower_limit=0,
                                                                     upper_limit=1,
                                                                     unit_type='Dimensionless')

equipment_rule_set = ScheduleRuleset("equipment_rule_set",
                                     equipment_weekday,
                                     schedule_rules=[equipment_schedule_weekday_rule, equipment_schedule_weekend_rule],
                                     schedule_type_limit=equipment_schedule_type_limit,
                                     holiday_schedule=equipment_weekend,
                                     summer_designday_schedule=conditioned_summer_design_day_equipment,
                                     winter_designday_schedule=conditioned_winter_design_day_equipment)

unconditioned_summer_design_day_equipment: ScheduleDay = ScheduleDay(
    "unconditioned_summer_design_day_equipment",
    [0.5],
    [Time(0, 0)]
)

unconditioned_winter_design_day_equipment: ScheduleDay = ScheduleDay(
    "unconditioned_winter_design_day_equipment",
    [0.05],
    [Time(0, 0)]
)

unconditioned_equipment_rule_set = ScheduleRuleset("unconditioned_equipment_rule_set",
                                                   unconditioned_equipment_alldays,
                                                   schedule_type_limit=equipment_schedule_type_limit,
                                                   summer_designday_schedule=unconditioned_summer_design_day_equipment,
                                                   winter_designday_schedule=unconditioned_winter_design_day_equipment)
