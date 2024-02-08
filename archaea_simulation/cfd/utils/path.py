import os

def get_archaea_sim_path():
    home = os.path.expanduser('~')
    return os.path.join(home, 'Documents', 'archaea-simulation')

def get_cfd_export_foam_path():
    foam_run = os.getenv('FOAM_RUN')
    if foam_run is None:
        home = os.path.expanduser('~')
        foam_run = os.path.join(home, 'Documents', 'archaea-simulation')
    return foam_run

def get_cfd_export_path(case_name: str):
    return os.path.join(get_archaea_sim_path(), case_name,  'cfd')

def get_bes_export_path(case_name: str):
    return os.path.join(get_archaea_sim_path(), case_name, 'bes')
