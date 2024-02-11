import os
import re
import sys
import json

from ladybug.futil import write_to_file
from ladybug.analysisperiod import AnalysisPeriod
from honeybee_energy.simulation.runperiod import RunPeriod
from honeybee_energy.simulation.shadowcalculation import ShadowCalculation
from honeybee.model import Model
from honeybee.room import Room
from honeybee_energy.simulation.parameter import SimulationParameter
from honeybee_energy.lib.programtypes import office_program
from honeybee_energy.hvac.idealair import IdealAirSystem
from honeybee_energy.run import to_openstudio_osw, run_osw, run_idf, output_energyplus_files

from archaea_simulation.bes.static_constants import output_summary_string, \
surface_convection_algorithm_inside, \
surface_convection_algorithm_outside, \
output_string_for_solar_radiation, \
version_string

from archaea_simulation.bes.schedule.generator import sequential_compact_schedule_generator
from ladybug.futil import preparedir, nukedir
from honeybee_energy.measure import Measure


def create_idf(thermal_rooms: "list[Room]", case_folder: str, case_name: str, ddy_file_path: str, epw_file_path: str):
    adj_info = Room.solve_adjacency(thermal_rooms)
    # Get input Model
    model: Model = Model('archeae_bes', thermal_rooms)
    model.tolerance = 0.0001
    model.units = 'Meters'

    # Get the input SimulationParameter
    sim_par = SimulationParameter()
    sim_par.output.add_zone_energy_use()
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
    idf_file_path = os.path.join(case_folder, "run", "in.idf")
    write_to_file(idf_file_path, idf_str, True)


    clean_name = re.sub(r'[^.A-Za-z0-9_-]', '_', model.display_name)
    model = model.duplicate()
    model.properties.energy.remove_hvac_from_no_setpoints()
    model_dict = model.to_dict(triangulate_sub_faces=True)
    
    model.properties.energy.add_autocal_properties_to_dict(model_dict)
    model_json = os.path.join(case_folder, '{}.hbjson'.format(clean_name))
    if (sys.version_info < (3, 0)):  # we need to manually encode it as UTF-8
        with open(model_json, 'wb') as fp:
            model_str = json.dumps(model_dict, ensure_ascii=False)
            fp.write(model_str.encode('utf-8'))
    else:
        with open(model_json, 'w', encoding='utf-8') as fp:
            model_str = json.dump(model_dict, fp, ensure_ascii=False)


    sim_par_dict = sim_par.to_dict()
    sim_par_json = os.path.join(case_folder, 'simulation_parameter.json')
    with open(sim_par_json, 'w') as fp:
        json.dump(sim_par_dict, fp)

    sch_directory = os.path.join(case_folder, 'schedules')

    measure = Measure("/home/koral/Documents/Git/Archaeans/archaea-simulation/archaea_simulation/bes/honeybee-openstudio-gem/lib/measures/from_honeybee_simulation_parameter")
    measure.arguments[0].value = sim_par_json
    osw = to_openstudio_osw(
        case_folder, 
        model_json, 
        sim_par_json, 
        additional_measures=[measure],
        epw_file=epw_file_path, 
        # schedule_directory=sch_directory
        )
    

    # osm, idf = run_osw(osw)


    return idf_file_path