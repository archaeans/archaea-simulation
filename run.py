import argparse
import sys
import os
import getopt
import subprocess
from archaea.geometry.point3d import Point3d

from specklepy.api import operations
from specklepy.transports.server import ServerTransport
from specklepy.objects.geometry import Mesh, Base

from archaea_simulation.speckle.account import get_auth_speckle_client
from archaea_simulation.speckle.vtk_to_speckle import vtk_to_speckle
from archaea_simulation.simulation_objects.domain import Domain
from archaea_simulation.cfd.utils.path import get_cfd_export_path, get_bes_export_path
from archaea_simulation.simulation_objects.courtyard_building import CourtyardBuilding


def run(argv):
    parser = argparse.ArgumentParser(description="Welcome to Archaea Simulation CLI program for CFD and BES calculations!")

    # Define arguments
    parser.add_argument("-n", "--name", default="test", help="Project name (default: test)")
    parser.add_argument("-x", "--exec", action="store_true", help="Execute simulations (default: False)")
    parser.add_argument("-ws", "--wind-speed", default=10.0, type=float, help="Wind speed (default: 10)")
    parser.add_argument("-wd", "--wind-direction", default=0, type=float, help="Wind direction (default: 0)")
    parser.add_argument("-dw", "--domain-width", default=25.0, type=float, help="Domain width (default: 25.0)")
    parser.add_argument("-dd", "--domain-depth", default=25.0, type=float, help="Domain depth (default: 25.0)")
    parser.add_argument("-dh", "--domain-height", default=10.0, type=float, help="Domain height (default: 10.0)")
    parser.add_argument("-nos", "--number-of-storeys", default=1, type=int, help="Number of storeys (default: 1)")
    parser.add_argument("-nor", "--number-of-rooms", default=3, type=int, help="Number of rooms (default: 3)")
    parser.add_argument("-cw", "--courtyard-width", default=10.0, type=float, help="Courtyard width (default: 10.0)")
    parser.add_argument("-rw", "--room-width", default=4.0, type=float, help="Room width (default: 4.0)")
    parser.add_argument("-rd", "--room-depth", default=4.0, type=float, help="Room depth (default: 4.0)")
    parser.add_argument("-rh", "--room-height", default=3.0, type=float, help="Room height (default: 3.0)")
    parser.add_argument("-rwt", "--room-wall-thickness", default=0.1, type=float, help="Room wall thickness (default: 0.1)")
    parser.add_argument("-rwe", "--room-window-existence", default=1, type=int, help="Room window existence (default: 1)")
    parser.add_argument("-rww", "--room-window-width", default=0.6, type=float, help="Room window width (default: 0.6)")
    parser.add_argument("-rwh", "--room-window-height", default=1.2, type=float, help="Room window height (default: 1.2)")
    parser.add_argument("-rde", "--room-door-existence", default=1, type=int, help="Room door existence (default: 1)")
    parser.add_argument("-rdw", "--room-door-width", default=0.8, type=float, help="Room door width (default: 0.8)")
    parser.add_argument("-rdh", "--room-door-height", default=2.0, type=float, help="Room door height (default: 2.0)")
    parser.add_argument("-ddy", "--design-day-year-file", required=True, type=str, help=".ddy file for EnergyPlus simulation")
    parser.add_argument("-epw", "--energy-plus-weather-file", required=True, type=str, help=".epw file for EnergyPlus simulation")

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    
    # Parse arguments
    args = parser.parse_args()

    # Use parsed arguments
    arg_name = args.name
    arg_exec = args.exec
    arg_wind_speed = args.wind_speed
    arg_wind_direction = args.wind_direction
    arg_domain_width = args.domain_width
    arg_domain_depth = args.domain_depth
    arg_domain_height = args.domain_height
    arg_number_of_storeys = args.number_of_storeys
    arg_number_of_rooms = args.number_of_rooms
    arg_courtyard_width = args.courtyard_width
    arg_room_width = args.room_width
    arg_room_depth = args.room_depth
    arg_room_height = args.room_height
    arg_room_wall_thickness = args.room_wall_thickness
    arg_room_window_existence = args.room_window_existence
    arg_room_window_width = args.room_window_width
    arg_room_window_height = args.room_window_height
    arg_room_door_existence = args.room_door_existence
    arg_room_door_width = args.room_door_width
    arg_room_door_height = args.room_door_height
    arg_ddy_path = args.design_day_year_file
    arg_epw_path = args.energy_plus_weather_file

    center = Point3d(0, 0, 0)
    courtyard_building = CourtyardBuilding(
        center,
        arg_number_of_storeys,
        arg_number_of_rooms,
        arg_courtyard_width,
        arg_room_width,
        arg_room_depth,
        arg_room_height,
        arg_room_wall_thickness,
        bool(arg_room_window_existence),
        arg_room_window_width,
        arg_room_window_height,
        bool(arg_room_door_existence),
        arg_room_door_width,
        arg_room_door_height
    )



    # Get authorized speckle client
    client = get_auth_speckle_client()

    results = client.stream.search("Archaea Tests")
    if not results:
        new_stream_id = client.stream.create(name="Archaea Tests")

    results = client.stream.search("Archaea Tests")
    stream = results[0]

    transport = ServerTransport(stream_id=stream.id, client=client)

    branches = client.branch.list(stream.id)
    is_openfoam_branch_exist = any(branch.name == "OpenFOAM" for branch in branches)

    if not is_openfoam_branch_exist:
        branch_id = client.branch.create(stream.id, "OpenFOAM", "Created by Archaea.")

    branch = client.branch.get(stream.id, "OpenFOAM")
    domain = Domain(center,
                    float(arg_domain_width),       # x
                    float(arg_domain_depth),       # y
                    float(arg_domain_height),      # z
                    context_meshes = courtyard_building.context,
                    wind_direction = float(arg_wind_direction),
                    wind_speed = float(arg_wind_speed) 
                    )

    for zone in courtyard_building.zones:
        domain.add_zone(zone)

    base = Base(detachable={'Domain', 'Buildings', 'Results'})
    
    domain_ground_mesh = Mesh()
    domain_ground_mesh.units = 'm'
    domain_ground_mesh.name = 'Ground'
    archaea_domain_mesh = domain.export_domain_ground_single_mesh()
    domain_ground_mesh.vertices = [item for sublist in archaea_domain_mesh.vertices for item in sublist]
    domain_ground_mesh.faces = [item for sublist in archaea_domain_mesh.polygons for item in [len(sublist)] + sublist]

    zones_mesh = Mesh()
    zones_mesh.units = 'm'
    zones_mesh.name = 'Buildings'
    archaea_zone_mesh = domain.export_zones_to_single_mesh()
    zones_mesh.vertices = [item for sublist in archaea_zone_mesh.vertices for item in sublist]
    zones_mesh.faces = [item for sublist in archaea_zone_mesh.polygons for item in [len(sublist)] + sublist]

    context_mesh = Mesh()
    context_mesh.units = 'm'
    context_mesh.name = 'Context'
    archaea_context_mesh = domain.export_context_to_single_mesh()
    context_mesh.vertices = [item for sublist in archaea_context_mesh.vertices for item in sublist]
    context_mesh.faces = [item for sublist in archaea_context_mesh.polygons for item in [len(sublist)] + sublist]

    base.Domain = [domain_ground_mesh]
    base.Buildings = [zones_mesh]
    base.Context = [context_mesh]

    cfd_case_folder = get_cfd_export_path(arg_name)
    bes_case_folder = get_bes_export_path(arg_name)
    if not os.path.exists(cfd_case_folder):
        os.makedirs(cfd_case_folder)

    domain.create_cfd_case(cfd_case_folder)
    idf_file_path = domain.create_bes_case(bes_case_folder, arg_name, arg_ddy_path)

    if arg_exec:
        print("##################################")
        print("### BUILDING ENERGY SIMULATION ###")
        print("##################################\n")

        cmd_bes = [
            "/usr/local/EnergyPlus-23-2-0/energyplus", 
            "-w", arg_epw_path,
            "-d", bes_case_folder,
            idf_file_path
        ]

        completed_process_bes = subprocess.run(cmd_bes, shell=False)
        print(completed_process_bes.stdout)

        return

        print("\n####################################")
        print("### COMPUTATIONAL FLUID DYNAMICS ###")
        print("####################################\n")
        cmd_cfd = os.path.join(cfd_case_folder, './Allrun')
        completed_process_cfd = subprocess.run(cmd_cfd, shell=False)
        print(completed_process_cfd.stdout)

        vtk_file = os.path.join(cfd_case_folder, 'postProcessing', 'cutPlaneSurface', '400', 'U_cutPlane.vtk')

        legend_point = Point3d(domain.center.x + (domain.x / 2) + 5, domain.center.y - (domain.y / 2), 0)
        result_meshes = vtk_to_speckle(vtk_file, legend_point)
        base.Results = result_meshes

        obj_id = operations.send(base, [transport])

        # now create a commit on that branch with your updated data!
        commit_id = client.commit.create(
            stream.id,
            obj_id,
            branch.name,
            message="Sent from Archaea.",
            source_application='Archaea'
        )

if __name__ == "__main__":
    run(sys.argv)
