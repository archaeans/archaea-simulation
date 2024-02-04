import os

from ladybug.futil import write_to_file
from ladybug.analysisperiod import AnalysisPeriod
from honeybee_energy.simulation.runperiod import RunPeriod
from honeybee_energy.simulation.shadowcalculation import ShadowCalculation
from honeybee.model import Model
from honeybee.room import Room
from honeybee_energy.simulation.parameter import SimulationParameter

from archaea_simulation.bes.static_constants import output_summary_string, \
surface_convection_algorithm_inside, \
surface_convection_algorithm_outside, \
output_string_for_solar_radiation, \
version_string

from archaea_simulation.bes.schedule.generator import sequential_compact_schedule_generator


def create_idf(thermal_rooms: "list[Room]", case_folder: str, case_name: str, ddy_file_path: str):
    adj_info = Room.solve_adjacency(thermal_rooms)
    # Get input Model
    model: Model = Model('archeae_bes', thermal_rooms)
    model.tolerance = 0.0001

    # Get the input SimulationParameter
    sim_par = SimulationParameter()
    sim_par.shadow_calculation = ShadowCalculation("FullExterior")
    sim_par.timestep = 20
    sim_par.run_period = RunPeriod.from_analysis_period(AnalysisPeriod())
    sim_par.sizing_parameter.add_from_ddy_990_010(ddy_file_path)

    solar_radiation_sch = sequential_compact_schedule_generator("solar_radiation_sch", "Fractional", [1, 11, 21], list(range(1, 13)))

    idf_str = \
        surface_convection_algorithm_inside + \
        surface_convection_algorithm_outside + \
        solar_radiation_sch + \
        output_string_for_solar_radiation + \
        '\n\n'.join((sim_par.to_idf()
                    .replace("None;                     !- unit conversion", "JtoKWH;                  !- unit conversion")
                    .replace("AllSummary;               !- report 0", output_summary_string), model.to.idf(model)))

    # idf_str = model.to.idf(model)
    # idf_str = sim_par.to_idf() \
    # .replace("None;                     !- unit conversion", "JtoKWH;                  !- unit conversion") \
    # .replace("AllSummary;               !- report 0", output_summary_string), model.to.idf(model)
    idf_file_path = os.path.join(case_folder, "{case_name}.idf".format(case_name=case_name))
    write_to_file(idf_file_path, idf_str, True)
    return idf_file_path