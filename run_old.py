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


def run_cfd(argv):
    # Default values
    arg_name = "test"
    arg_exec = False
    arg_domain_width = 25.0
    arg_domain_depth = 25.0
    arg_domain_height = 10.0
    arg_number_of_storeys = 1
    arg_number_of_rooms = 3
    arg_courtyard_width = 10.0
    arg_room_width = 4.0
    arg_room_depth = 4.0
    arg_room_height = 3.0
    arg_room_wall_thickness = 0.1
    arg_room_window_existence = 1
    arg_room_window_width = 0.6
    arg_room_window_height = 1.2
    arg_room_door_existence = 1
    arg_room_door_width = 0.8
    arg_room_door_height = 2.0
    arg_wind_direction = 0
    arg_wind_speed = 10.0

    arg_help = "{0}\n\n" \
               "Welcome to stl exporter program for cfd calculations! \n" \
               "Use below flags to generate stl.\n" \
               " -n\t--name                        <name>                   default: test\n" \
               " -x\t--exec                        <exec>                   default: 0\n" \
               " -ws\t--wind-speed                 <wind_speed>              default: 10\n" \
               " -wd\t--wind-direction             <wind_direction>          default: 0\n" \
               " -dw\t--domain-width               <domain_width>            default: 100.0\n" \
               " -dd\t--domain-depth               <domain_depth>            default: 50.0\n" \
               " -dh\t--domain-height              <domain_height>           default: 50.0\n" \
               " -nos\t--number-of-storeys         <number_of_storeys>        default: 1\n" \
               " -nor\t--number-of-rooms           <number_of_rooms>          default: 3\n" \
               " -cw\t--courtyard-width            <courtyard_width>         default: 10.0\n" \
               " -rw\t--room-width                 <room_width>              default: 4.0\n" \
               " -rd\t--room-depth                 <room_depth>              default: 4.0\n" \
               " -rh\t--room-height                <room_height>             default: 3.0\n" \
               " -rwt\t--room-wall-thickness       <room_wall_thickness>      default: 0.1\n" \
               " -rwe\t--room-window-existence     <room_window_existence>    default: 1\n" \
               " -rww\t--room-window-width         <room_window_width>        default: 0.6\n" \
               " -rwh\t--room-window-height        <room_window_height>       default: 1.2\n" \
               " -rde\t--room-door-existence       <room_door_existence>      default: 1\n" \
               " -rdw\t--room-door-width           <room_door_width>          default: 0.8\n" \
               " -rdh\t--room-door-height          <room_door_height>         default: 2.0\n".format(argv[0])

    try:
        opts, args = getopt.getopt(argv[1:], "hxn:ws:wd:dw:dd:dh:nos:nor:cw:rw:rd:rh:rwt:rwe:rww:rwh:rde:rdw:rdh:",
                                   ["help",
                                    "exec",
                                    "name=",
                                    "wind-speed=",
                                    "wind-direction=",
                                    "domain-width=",
                                    "domain-depth=",
                                    "domain-height=",
                                    "number-of-storeys=",
                                    "number-of-rooms=",
                                    "courtyard-width=",
                                    "room-width=",
                                    "room-depth=",
                                    "room-height=",
                                    "room-wall-thickness=",
                                    "room-window-existence=",
                                    "room-wall-width=",
                                    "room-wall-height=",
                                    "room-door-existence=",
                                    "room-door-width=",
                                    "room-door-height="])
    except ValueError:
        print(arg_help)
        sys.exit(2)

    # if user does not provide any argument, print help message
    if len(opts) == 0:
        print(arg_help)  # print the help message
        print("NOTE: Stl generated with default parameters because no argument provided.\n")

    # Find the upcoming flag and set it to it's value
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(arg_help)  # print the help message
            sys.exit(2)
        elif opt in ("-x", "--exec"):
            arg_exec = True
        elif opt in ("-n", "--name"):
            arg_name = arg
        elif opt in ("-ws", "--wind-speed"):
            arg_wind_speed = arg
        elif opt in ("-wd", "--wind-direction"):
            arg_wind_direction = arg
        elif opt in ("-dw", "--domain-width"):
            arg_domain_width = arg
        elif opt in ("-dd", "--domain-depth"):
            arg_domain_depth = arg
        elif opt in ("-dh", "--domain-height"):
            arg_domain_height = arg
        elif opt in ("-nos", "--number-of-storeys"):
            arg_number_of_storeys = arg
        elif opt in ("-nor", "--number-of-rooms"):
            arg_number_of_rooms = arg
        elif opt in ("-cw", "--courtyard-width"):
            arg_courtyard_width = arg
        elif opt in ("-rw", "--room-width"):
            arg_room_width = arg
        elif opt in ("-rd", "--room-depth"):
            arg_room_depth = arg
        elif opt in ("-rh", "--room-height"):
            arg_room_height = arg
        elif opt in ("-rwt", "--room-wall-thickness"):
            arg_room_wall_thickness = arg
        elif opt in ("-rwe", "--room-window-existence"):
            arg_room_window_existence = arg
        elif opt in ("-rww", "--room-window-width"):
            arg_room_window_width = arg
        elif opt in ("-rwh", "--room-window-height"):
            arg_room_window_height = arg
        elif opt in ("-dwe", "--door-window-existence"):
            arg_room_door_existence = arg
        elif opt in ("-dww", "--door-window-width"):
            arg_room_door_width = arg
        elif opt in ("-dwh", "--door-window-height"):
            arg_room_door_height = arg

    center = Point3d(0,0,0)

    courtyard_building = CourtyardBuilding(
        center,
        int(arg_number_of_storeys),
        int(arg_number_of_rooms),
        float(arg_courtyard_width),
        float(arg_room_width),
        float(arg_room_depth),
        float(arg_room_height),
        float(arg_room_wall_thickness),
        bool(arg_room_window_existence),
        float(arg_room_window_width),
        float(arg_room_window_height),
        bool(arg_room_door_existence),
        float(arg_room_door_width),
        float(arg_room_door_height)
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
    domain.create_bes_case(bes_case_folder, arg_name, "ddy_file_path")

    if arg_exec:
        cmd = os.path.join(cfd_case_folder, './Allrun')
        completed_process = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print(completed_process.stdout)

        vtk_file = os.path.join(cfd_case_folder, 'postProcessing',
                            'cutPlaneSurface', '400', 'U_cutPlane.vtk')

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
    run_cfd(sys.argv)
