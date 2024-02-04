from honeybee_energy.schedule.typelimit import ScheduleTypeLimit

fraction: ScheduleTypeLimit = ScheduleTypeLimit("Fractional",
                                                lower_limit=0,
                                                upper_limit=1,
                                                unit_type='Dimensionless')
