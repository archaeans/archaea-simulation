comfort_cal_sch = "!-   ===========  OUTPUT SCHEDULE ===========" + "\n\n" + \
                      "Schedule:Compact," + "\n" + \
                      "comfort_cal_sch,  !- Name" + "\n" + \
                      "Fractional,                !- Schedule Type Limits Name" + "\n" + \
                      "Through: 01/19,          !- Field 1" + "\n" + \
                      "For:AllDays,             !- Field 2" + "\n" + \
                      "Until: 24:00,            !- Field 3" + "\n" + \
                      "0,                      !- Field 4" + "\n" + \
                      "Through: 01/22,          !- Field 5" + "\n" + \
                      "For:AllDays,             !- Field 6" + "\n" + \
                      "Until: 24:00,            !- Field 7" + "\n" + \
                      "1,                      !- Field 8" + "\n" + \
                      "Through: 07/19,          !- Field 9" + "\n" + \
                      "For:AllDays,             !- Field 10" + "\n" + \
                      "Until: 24:00,            !- Field 11" + "\n" + \
                      "0,                      !- Field 12" + "\n" + \
                      "Through: 07/22,          !- Field 13" + "\n" + \
                      "For:AllDays,             !- Field 14" + "\n" + \
                      "Until: 24:00,            !- Field 15" + "\n" + \
                      "1,                      !- Field 16" + "\n" + \
                      "Through: 12/31,          !- Field 17" + "\n" + \
                      "For:AllDays,             !- Field 18" + "\n" + \
                      "Until: 24:00,            !- Field 19" + "\n" + \
                      "0,                      !- Field 20" + "\n" + \
                      "For: Allotherdays,       !- Field 21" + "\n" + \
                      "Until: 24:00,            !- Field 22" + "\n" + \
                      "0;                      !- Field 23" + "\n\n\n"

solar_radiation_sch = "!-   ===========  OUTPUT SCHEDULE ===========" + "\n\n" + \
                      "Schedule:Compact," + "\n" + \
                      "solar_radiation_sch,  !- Name" + "\n" + \
                      "Fractional,                !- Schedule Type Limits Name" + "\n" + \
                      "Through: 01/19,          !- Field 1" + "\n" + \
                      "For:AllDays,             !- Field 2" + "\n" + \
                      "Until: 24:00,            !- Field 3" + "\n" + \
                      "0,                      !- Field 4" + "\n" + \
                      "Through: 01/22,          !- Field 5" + "\n" + \
                      "For:AllDays,             !- Field 6" + "\n" + \
                      "Until: 24:00,            !- Field 7" + "\n" + \
                      "1,                      !- Field 8" + "\n" + \
                      "Through: 07/19,          !- Field 9" + "\n" + \
                      "For:AllDays,             !- Field 10" + "\n" + \
                      "Until: 24:00,            !- Field 11" + "\n" + \
                      "0,                      !- Field 12" + "\n" + \
                      "Through: 07/22,          !- Field 13" + "\n" + \
                      "For:AllDays,             !- Field 14" + "\n" + \
                      "Until: 24:00,            !- Field 15" + "\n" + \
                      "1,                      !- Field 16" + "\n" + \
                      "Through: 12/31,          !- Field 17" + "\n" + \
                      "For:AllDays,             !- Field 18" + "\n" + \
                      "Until: 24:00,            !- Field 19" + "\n" + \
                      "0,                      !- Field 20" + "\n" + \
                      "For: Allotherdays,       !- Field 21" + "\n" + \
                      "Until: 24:00,            !- Field 22" + "\n" + \
                      "0;                      !- Field 23" + "\n\n\n"

output_string_for_pmv_ppd = "!-   ===========  ALL OBJECTS IN CLASS: OUTPUT:VARIABLE ===========" + "\n\n" + \
                    "Output:Variable," + "\n" + \
                    "*,                       !- Key Value" + "\n" + \
                    "Zone Thermal Comfort Fanger Model PMV,  !- Variable Name" + "\n" + \
                    "Hourly,                  !- Reporting Frequency" + "\n" + \
                    "comfort_cal_sch;  !- Schedule Name" + "\n\n" + \
                    "Output:Variable," + "\n" + \
                    "*,                       !- Key Value" + "\n" + \
                    "Zone Thermal Comfort Fanger Model PPD,  !- Variable Name" + "\n" + \
                    "Hourly,                  !- Reporting Frequency" + "\n" + \
                    "comfort_cal_sch;  !- Schedule Name" + "\n\n\n"

output_string_for_solar_radiation = "!-   ===========  ALL OBJECTS IN CLASS: OUTPUT:VARIABLE ===========" + "\n\n" + \
                                    "Output:Variable," + "\n" + \
                                        "*,                       !- Key Value" + "\n" + \
                                        "Site Outdoor Air Drybulb Temperature,  !- Variable Name" + "\n" + \
                                        "Hourly,                  !- Reporting Frequency" + "\n" + \
                                        "solar_radiation_sch;        !- Schedule Name" + "\n\n" + \
                                    "Output:Variable," + "\n" + \
                                        "*,                       !- Key Value" + "\n" + \
                                        "Zone Air Temperature,    !- Variable Name" + "\n" + \
                                        "Hourly,                  !- Reporting Frequency" + "\n" + \
                                        "solar_radiation_sch;        !- Schedule Name" + "\n\n" + \
                                    "Output:Variable," + "\n" + \
                                        "*,                       !- Key Value" + "\n" + \
                                        "Zone Operative Temperature,  !- Variable Name" + "\n" + \
                                        "Hourly,                  !- Reporting Frequency" + "\n" + \
                                        "solar_radiation_sch;        !- Schedule Name" + "\n\n" + \
                                    "Output:Variable," + "\n" + \
                                        "*,                       !- Key Value" + "\n" + \
                                        "Zone Air Relative Humidity,  !- Variable Name" + "\n" + \
                                        "Hourly,                  !- Reporting Frequency" + "\n" + \
                                        "solar_radiation_sch;        !- Schedule Name" + "\n\n" + \
                                    "Output:Variable," + "\n" + \
                                        "*,                       !- Key Value" + "\n" + \
                                        "Zone Windows Total Transmitted Solar Radiation Energy,  !- Variable Name" + "\n" + \
                                        "Hourly,                  !- Reporting Frequency" + "\n" + \
                                        "solar_radiation_sch;        !- Schedule Name" + "\n\n" + \
                                    "Output:Variable," + "\n" + \
                                        "*,                       !- Key Value" + "\n" + \
                                        "Zone Mean Radiant Temperature,  !- Variable Name" + "\n" + \
                                        "Hourly,                  !- Reporting Frequency" + "\n" + \
                                        "solar_radiation_sch;        !- Schedule Name" + "\n\n\n"

version_string = "!-   ===========  ALL OBJECTS IN CLASS: VERSION ===========" + "\n" + "Version," + "\n" \
                     + "    9.5;                     !- Version Identifier\n\n\n"

surface_convection_algorithm_inside = "!-   ===========  ALL OBJECTS IN CLASS: SURFACECONVECTIONALGORITHM:INSIDE ===========\n" \
                                          + "SurfaceConvectionAlgorithm:Inside,\n" \
                                          + "TARP;                    !- Algorithm\n\n\n"

surface_convection_algorithm_outside = "!-   ===========  ALL OBJECTS IN CLASS: SURFACECONVECTIONALGORITHM:OUTSIDE ===========\n" \
                                           + "SurfaceConvectionAlgorithm:Outside,\n" \
                                           + "DOE-2;                   !- Algorithm\n\n\n"

unit_transition = "OutputControl:Table:Style,\n" + \
    "HTML,                    !- Column Separator\n" + \
    "JtoKWH;                  !- Unit Conversion\n\n\n"

output_summary_string = "AllSummary,               !- report 0\n" + \
    " EnvelopeSummary,               !- report 1\n" + \
    " ZoneCoolingSummaryMonthly,               !- report 2\n" + \
    " ZoneHeatingSummaryMonthly,               !- report 3\n" + \
    " ZoneElectricSummaryMonthly;               !- report 4\n"
