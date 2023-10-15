import os


def get_cfd_export_path():
    foam_run = os.getenv('FOAM_RUN')
    if foam_run is None:
        home = os.path.expanduser('~')
        foam_run = os.path.join(home, 'Documents')

    return os.path.join(foam_run, 'archaea-simulation', 'cfd')
